"""Compile abstract URIs to concrete OS actions."""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from nlp2uri.models import HostPlatform, OSAction
from nlp2uri.platform_detect import detect_platform


def compile_uri_to_actions(
    uri: str,
    os: HostPlatform | None = None,
) -> list[OSAction]:
    host = os or detect_platform()
    parsed = urlparse(uri)
    scheme = parsed.scheme.lower()
    params = _query_params(parsed)

    if scheme in {"http", "https", "file", "cursor", "vscode", "vscode-insiders"}:
        return [_open_uri(host, uri)]

    if scheme in {"ms-settings", "x-apple-systempreferences"}:
        return [_open_uri(host, uri)]

    if scheme == "app":
        return _compile_app(host, parsed.netloc, parsed.path, params, uri)

    if scheme == "desktop-screenshot":
        return _compile_screenshot(host, parsed.netloc, params, uri)

    if scheme == "desktop-window":
        return _compile_window(host, parsed.netloc, params, uri)

    if scheme == "nlp2uri":
        return _compile_legacy_nlp2uri(host, uri)

    raise ValueError(f"unsupported uri scheme: {scheme}")


def _query_params(parsed) -> dict[str, str]:
    raw = parse_qs(parsed.query, keep_blank_values=False)
    return {k: unquote(v[0]) for k, v in raw.items() if v}


def _first_available(names: tuple[str, ...]) -> str | None:
    for name in names:
        if shutil.which(name):
            return name
    return None


def _open_uri(host: HostPlatform, uri: str) -> OSAction:
    if host == HostPlatform.LINUX:
        opener = _first_available(("xdg-open", "gio", "gnome-open")) or "xdg-open"
        return OSAction(host, opener, [uri])
    if host == HostPlatform.MACOS:
        return OSAction(host, "open", [uri])
    if host == HostPlatform.WINDOWS:
        return OSAction(host, "cmd", ["/c", "start", "", uri])
    return OSAction(host, "echo", [uri])


def _compile_app(
    host: HostPlatform,
    authority: str,
    path: str,
    params: dict[str, str],
    uri: str,
) -> list[OSAction]:
    app = authority.lower()
    action = path.strip("/") or "open"

    if app == "settings" and action == "open":
        return _compile_settings(host)

    if app == "file" and action == "open":
        native = params.get("path", "")
        if native:
            return [_open_uri(host, Path(native).expanduser().as_uri())]
        return [_open_uri(host, uri)]

    if action == "open" and params.get("path"):
        normalized = params["path"]
        native_scheme = {"cursor": "cursor", "vscode": "vscode", "code": "vscode"}.get(app, app)
        native_uri = f"{native_scheme}://file{Path(normalized).as_posix()}"
        if _first_available(("xdg-open", "open", "cmd")):
            return [_open_uri(host, native_uri)]
        return [OSAction(host, app, [normalized])]

    if action == "open":
        return _compile_launch_app(host, app)

    raise ValueError(f"unsupported app uri: {uri}")


def _compile_settings(host: HostPlatform) -> list[OSAction]:
    if host == HostPlatform.WINDOWS:
        return [_open_uri(host, "ms-settings:")]
    if host == HostPlatform.MACOS:
        return [_open_uri(host, "x-apple.systempreferences:")]
    for candidate in (
        "gnome-control-center",
        "systemsettings",
        "kcmshell5",
        "xfce4-settings-manager",
    ):
        if _first_available((candidate,)):
            return [OSAction(host, candidate, [])]
    return [_open_uri(host, "file:///usr/share/applications")]


def _compile_launch_app(host: HostPlatform, name: str) -> list[OSAction]:
    if host == HostPlatform.LINUX:
        gtk = _first_available(("gtk-launch",))
        desktop_id = _desktop_id_for_app(name)
        if gtk and desktop_id:
            return [OSAction(host, gtk, [desktop_id])]
        opener = _first_available(("xdg-open",)) or "xdg-open"
        return [OSAction(host, opener, [name])]
    if host == HostPlatform.MACOS:
        return [OSAction(host, "open", ["-a", name])]
    if host == HostPlatform.WINDOWS:
        return [OSAction(host, "cmd", ["/c", "start", "", name])]
    return [OSAction(host, "echo", [name])]


def _compile_screenshot(
    host: HostPlatform,
    authority: str,
    params: dict[str, str],
    uri: str,
) -> list[OSAction]:
    target = authority or "screen"
    out_dir = Path(os.environ.get("NLP2URI_CAPTURE_DIR", "/tmp/nlp2uri-captures"))
    outfile = str(out_dir / f"capture-{target}.png")

    if target == "screen":
        if host == HostPlatform.LINUX:
            if _first_available(("grim",)):
                return [OSAction(host, "grim", [outfile])]
            if _first_available(("scrot",)):
                return [OSAction(host, "scrot", [outfile])]
            if _first_available(("import",)):
                return [OSAction(host, "import", ["-window", "root", outfile])]
            return [OSAction(host, "bash", ["-lc", f"echo portal-screenshot > {outfile}"])]
        if host == HostPlatform.MACOS:
            return [OSAction(host, "screencapture", ["-x", outfile])]
        if host == HostPlatform.WINDOWS:
            ps = (
                "Add-Type -AssemblyName System.Windows.Forms; "
                "[System.Windows.Forms.Screen]::PrimaryScreen.Bounds"
            )
            return [OSAction(host, "powershell", ["-NoProfile", "-Command", ps])]

    title = params.get("title", "")
    mode = params.get("mode", "active")
    if host == HostPlatform.LINUX:
        if _first_available(("import",)) and title:
            return [OSAction(host, "import", ["-window", title, outfile])]
        if _first_available(("grim",)):
            return [OSAction(host, "grim", ["-g", "0,0 100x100", outfile])]
        return [OSAction(host, "bash", ["-lc", f"echo window-capture:{title}:{mode} > {outfile}"])]
    if host == HostPlatform.MACOS:
        if title:
            return [OSAction(host, "screencapture", ["-l", title, outfile])]
        return [OSAction(host, "screencapture", ["-w", outfile])]
    if host == HostPlatform.WINDOWS:
        if title:
            ps = f"Write-Output 'window:{title}' | Out-File -FilePath '{outfile}'"
            return [OSAction(host, "powershell", ["-NoProfile", "-Command", ps])]
        return [OSAction(host, "snippingtool", ["/clip"])]

    raise ValueError(f"unsupported screenshot uri: {uri}")


def _compile_window(
    host: HostPlatform,
    authority: str,
    params: dict[str, str],
    uri: str,
) -> list[OSAction]:
    action = authority or "focus"
    name = params.get("name") or params.get("title", "")
    if action != "focus":
        raise ValueError(f"unsupported desktop-window action: {uri}")

    if not name:
        raise ValueError("desktop-window focus requires name or title")

    if host == HostPlatform.LINUX:
        wmctrl = _first_available(("wmctrl",))
        if wmctrl:
            return [OSAction(host, wmctrl, ["-a", name])]
        xdotool = _first_available(("xdotool",))
        if xdotool:
            script = f"xdotool search --name {name} windowactivate"
            return [OSAction(host, "bash", ["-lc", script])]
        return _compile_launch_app(host, name)

    if host == HostPlatform.MACOS:
        script = f'tell application "{name}" to activate'
        return [OSAction(host, "osascript", ["-e", script])]

    if host == HostPlatform.WINDOWS:
        ps = (
            f"(Get-Process -Name '{name}' -ErrorAction SilentlyContinue | "
            f"Select-Object -First 1).MainWindowHandle"
        )
        return [OSAction(host, "powershell", ["-NoProfile", "-Command", ps])]

    return [OSAction(host, "echo", [name])]


def _compile_legacy_nlp2uri(host: HostPlatform, uri: str) -> list[OSAction]:
    parsed = urlparse(uri)
    segments = [parsed.netloc, parsed.path.lstrip("/")]
    path = "/".join(part for part in segments if part)
    params = _query_params(parsed)

    if path == "settings/linux":
        return _compile_settings(host)
    if path == "app/open":
        return _compile_launch_app(host, params.get("name", ""))
    if path == "app/focus":
        return _compile_window(host, "focus", params, uri)
    if path.startswith("capture/"):
        target = path.split("/", 1)[1]
        return _compile_screenshot(host, target, params, uri)

    raise ValueError(f"unsupported legacy nlp2uri path: {path}")


def _desktop_id_for_app(name: str) -> str | None:
    lowered = name.lower().removesuffix(".desktop")
    candidates = (
        f"{lowered}.desktop",
        f"org.{lowered}.desktop",
        f"{lowered}-desktop.desktop",
    )
    for desktop_dir in (
        "/usr/share/applications",
        "/var/lib/snapd/desktop/applications",
        "/usr/local/share/applications",
    ):
        base = Path(desktop_dir)
        if not base.is_dir():
            continue
        for candidate in candidates:
            if (base / candidate).is_file():
                return candidate
        for entry in base.glob("*.desktop"):
            if lowered in entry.name.lower():
                return entry.name
    return None
