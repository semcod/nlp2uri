"""Compile abstract URIs to concrete OS actions."""

from __future__ import annotations

import os
import shutil
from collections.abc import Callable
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from nlp2uri.desktop_apps import desktop_id_for_app as _desktop_id_for_app
from nlp2uri.models import HostPlatform, OSAction
from nlp2uri.platform_detect import detect_platform
from nlp2uri.host.endpoint import build_endpoint_actions, is_endpoint_uri
from nlp2uri.systemmap.compile import compile_system_map_uri, is_system_map_uri
from nlp2uri.systemmap.getv_uri import compile_getv_uri, is_getv_uri


_OPEN_URI_SCHEMES = frozenset(
    {"http", "https", "file", "cursor", "vscode", "vscode-insiders"}
)
_NATIVE_SETTINGS_SCHEMES = frozenset({"ms-settings", "x-apple.systempreferences"})


def compile_uri_to_actions(
    uri: str,
    os: HostPlatform | None = None,
) -> list[OSAction]:
    host = os or detect_platform()
    parsed = urlparse(uri)
    scheme = parsed.scheme.lower()
    params = _query_params(parsed)

    if scheme in _OPEN_URI_SCHEMES or scheme in _NATIVE_SETTINGS_SCHEMES:
        return [_open_uri(host, uri)]

    if scheme == "app":
        return _compile_app(host, parsed.netloc, parsed.path, params, uri)

    if scheme == "desktop-screenshot":
        return _compile_screenshot(host, parsed.netloc, params, uri)

    if scheme == "desktop-window":
        return _compile_window(host, parsed.netloc, params, uri)

    if scheme == "nlp2uri":
        return _compile_legacy_nlp2uri(host, uri)

    if is_getv_uri(uri):
        return compile_getv_uri(uri, host)

    if is_endpoint_uri(uri):
        return build_endpoint_actions(uri, host)

    if is_system_map_uri(uri):
        extra = {k: v for k, v in params.items()}
        return compile_system_map_uri(uri, host, config=extra or None)

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


def _compile_app_settings(
    host: HostPlatform,
    path: str,
    action: str,
) -> list[OSAction] | None:
    panel = path.strip("/")
    if panel and panel != "open":
        return _compile_settings_panel(host, panel)
    if action == "open" or panel == "open":
        return _compile_settings(host)
    return None


def _compile_app_file_open(
    host: HostPlatform,
    params: dict[str, str],
    uri: str,
) -> list[OSAction]:
    native = params.get("path", "")
    if native:
        return [_open_uri(host, Path(native).expanduser().as_uri())]
    return [_open_uri(host, uri)]


def _compile_app_open_with_path(
    host: HostPlatform,
    app: str,
    params: dict[str, str],
) -> list[OSAction]:
    normalized = params["path"]
    native_scheme = {"cursor": "cursor", "vscode": "vscode", "code": "vscode"}.get(app, app)
    native_uri = f"{native_scheme}://file{Path(normalized).as_posix()}"
    if _first_available(("xdg-open", "open", "cmd")):
        return [_open_uri(host, native_uri)]
    return [OSAction(host, app, [normalized])]


def _compile_app_named(
    host: HostPlatform,
    app: str,
    path: str,
    action: str,
    params: dict[str, str],
    uri: str,
) -> list[OSAction] | None:
    if app == "settings":
        return _compile_app_settings(host, path, action)
    if app == "terminal" and action == "open":
        return _compile_terminal(host, params)
    if app == "file" and action == "open":
        return _compile_app_file_open(host, params, uri)
    return None


def _compile_app_open(
    host: HostPlatform,
    app: str,
    action: str,
    params: dict[str, str],
) -> list[OSAction] | None:
    if action != "open":
        return None
    if params.get("path"):
        return _compile_app_open_with_path(host, app, params)
    return _compile_launch_app(host, app)


def _compile_app(
    host: HostPlatform,
    authority: str,
    path: str,
    params: dict[str, str],
    uri: str,
) -> list[OSAction]:
    app = authority.lower()
    action = path.strip("/") or "open"

    named = _compile_app_named(host, app, path, action, params, uri)
    if named is not None:
        return named

    opened = _compile_app_open(host, app, action, params)
    if opened is not None:
        return opened

    raise ValueError(f"unsupported app uri: {uri}")


_WINDOWS_SETTINGS_PANELS: dict[str, str] = {
    "network": "ms-settings:network",
    "wifi": "ms-settings:network-wifi",
    "bluetooth": "ms-settings:bluetooth",
    "display": "ms-settings:display",
    "sound": "ms-settings:sound",
    "privacy": "ms-settings:privacy",
}

_MACOS_SETTINGS_PANELS: dict[str, str] = {
    "network": "x-apple.systempreferences:com.apple.preference.network",
    "wifi": "x-apple.systempreferences:com.apple.preference.network",
    "bluetooth": "x-apple.systempreferences:com.apple.preference.security?Privacy_Bluetooth",
    "display": "x-apple.systempreferences:com.apple.preference.displays",
    "sound": "x-apple.systempreferences:com.apple.preference.sound",
    "privacy": "x-apple.systempreferences:com.apple.preference.security",
}


def _windows_settings_panel_uri(panel: str) -> str:
    return _WINDOWS_SETTINGS_PANELS.get(panel, f"ms-settings:{panel}")


def _macos_settings_panel_uri(panel: str) -> str:
    return _MACOS_SETTINGS_PANELS.get(panel, f"x-apple.systempreferences:{panel}")


def _linux_settings_panel_actions(host: HostPlatform, panel: str) -> list[OSAction]:
    for candidate, args in (
        ("gnome-control-center", [panel]),
        ("kcmshell5", [panel]),
        ("systemsettings", [panel]),
    ):
        if _first_available((candidate,)):
            return [OSAction(host, candidate, args)]
    return [_open_uri(host, f"app://settings/{panel}")]


def _compile_settings_panel(host: HostPlatform, panel: str) -> list[OSAction]:
    if host == HostPlatform.WINDOWS:
        return [_open_uri(host, _windows_settings_panel_uri(panel))]
    if host == HostPlatform.MACOS:
        return [_open_uri(host, _macos_settings_panel_uri(panel))]
    return _linux_settings_panel_actions(host, panel)


def _linux_terminal_actions(host: HostPlatform, path: str) -> list[OSAction]:
    for tool, args in (
        ("gnome-terminal", ["--working-directory", path] if path else []),
        ("konsole", ["--workdir", path] if path else []),
        ("alacritty", ["--working-directory", path] if path else []),
        ("xterm", ["-e", f"bash -lc 'cd {path} && exec $SHELL'"] if path else []),
    ):
        if _first_available((tool,)):
            return [OSAction(host, tool, args)]
    return [OSAction(host, "bash", ["-lc", f"echo terminal:{path or '.'}"])]


def _macos_terminal_actions(host: HostPlatform, path: str) -> list[OSAction]:
    if path:
        script = f'tell application "Terminal" to do script "cd {path}"'
        return [OSAction(host, "osascript", ["-e", script])]
    return [OSAction(host, "open", ["-a", "Terminal"])]


def _windows_terminal_actions(host: HostPlatform, path: str) -> list[OSAction]:
    if path and _first_available(("wt",)):
        return [OSAction(host, "wt", ["-d", path])]
    if path:
        return [OSAction(host, "cmd", ["/c", "start", "cmd", "/k", f"cd /d {path}"])]
    return [OSAction(host, "cmd", ["/c", "start", "cmd"])]


def _compile_terminal(host: HostPlatform, params: dict[str, str]) -> list[OSAction]:
    path = params.get("path", "")
    if host == HostPlatform.LINUX:
        return _linux_terminal_actions(host, path)
    if host == HostPlatform.MACOS:
        return _macos_terminal_actions(host, path)
    if host == HostPlatform.WINDOWS:
        return _windows_terminal_actions(host, path)
    return [OSAction(host, "echo", [path or "terminal"])]


_LINUX_SETTINGS_APPS: tuple[str, ...] = (
    "gnome-control-center",
    "systemsettings",
    "kcmshell5",
    "xfce4-settings-manager",
)


def _windows_settings_actions(host: HostPlatform) -> list[OSAction]:
    return [_open_uri(host, "ms-settings:")]


def _macos_settings_actions(host: HostPlatform) -> list[OSAction]:
    return [_open_uri(host, "x-apple.systempreferences:")]


def _linux_settings_actions(host: HostPlatform) -> list[OSAction]:
    for candidate in _LINUX_SETTINGS_APPS:
        if _first_available((candidate,)):
            return [OSAction(host, candidate, [])]
    return [_open_uri(host, "file:///usr/share/applications")]


def _compile_settings(host: HostPlatform) -> list[OSAction]:
    if host == HostPlatform.WINDOWS:
        return _windows_settings_actions(host)
    if host == HostPlatform.MACOS:
        return _macos_settings_actions(host)
    return _linux_settings_actions(host)


def _linux_launch_app_actions(host: HostPlatform, name: str) -> list[OSAction]:
    gtk = _first_available(("gtk-launch",))
    desktop_id = _desktop_id_for_app(name)
    if gtk and desktop_id:
        return [OSAction(host, gtk, [desktop_id])]
    opener = _first_available(("xdg-open",)) or "xdg-open"
    return [OSAction(host, opener, [name])]


def _macos_launch_app_actions(host: HostPlatform, name: str) -> list[OSAction]:
    return [OSAction(host, "open", ["-a", name])]


def _windows_launch_app_actions(host: HostPlatform, name: str) -> list[OSAction]:
    return [OSAction(host, "cmd", ["/c", "start", "", name])]


def _compile_launch_app(host: HostPlatform, name: str) -> list[OSAction]:
    if host == HostPlatform.LINUX:
        return _linux_launch_app_actions(host, name)
    if host == HostPlatform.MACOS:
        return _macos_launch_app_actions(host, name)
    if host == HostPlatform.WINDOWS:
        return _windows_launch_app_actions(host, name)
    return [OSAction(host, "echo", [name])]


def _capture_outfile(target: str) -> str:
    out_dir = Path(os.environ.get("NLP2URI_CAPTURE_DIR", "/tmp/nlp2uri-captures"))
    return str(out_dir / f"capture-{target}.png")


def _linux_screen_capture(host: HostPlatform, outfile: str) -> OSAction:
    for tool, args in (
        ("grim", [outfile]),
        ("scrot", [outfile]),
        ("import", ["-window", "root", outfile]),
    ):
        if _first_available((tool,)):
            return OSAction(host, tool, args)
    return OSAction(host, "bash", ["-lc", f"echo portal-screenshot > {outfile}"])


def _macos_screen_capture(host: HostPlatform, outfile: str) -> OSAction:
    return OSAction(host, "screencapture", ["-x", outfile])


def _windows_screen_capture(host: HostPlatform) -> OSAction:
    ps = (
        "Add-Type -AssemblyName System.Windows.Forms; "
        "[System.Windows.Forms.Screen]::PrimaryScreen.Bounds"
    )
    return OSAction(host, "powershell", ["-NoProfile", "-Command", ps])


def _compile_screen_capture(host: HostPlatform, outfile: str) -> OSAction:
    if host == HostPlatform.LINUX:
        return _linux_screen_capture(host, outfile)
    if host == HostPlatform.MACOS:
        return _macos_screen_capture(host, outfile)
    if host == HostPlatform.WINDOWS:
        return _windows_screen_capture(host)
    raise ValueError(f"unsupported screen capture host: {host.value}")


def _linux_window_capture(
    host: HostPlatform,
    outfile: str,
    *,
    title: str,
    mode: str,
) -> OSAction:
    if _first_available(("import",)) and title:
        return OSAction(host, "import", ["-window", title, outfile])
    if _first_available(("grim",)):
        return OSAction(host, "grim", ["-g", "0,0 100x100", outfile])
    return OSAction(host, "bash", ["-lc", f"echo window-capture:{title}:{mode} > {outfile}"])


def _macos_window_capture(host: HostPlatform, outfile: str, *, title: str) -> OSAction:
    if title:
        return OSAction(host, "screencapture", ["-l", title, outfile])
    return OSAction(host, "screencapture", ["-w", outfile])


def _windows_window_capture(host: HostPlatform, outfile: str, *, title: str) -> OSAction:
    if title:
        ps = f"Write-Output 'window:{title}' | Out-File -FilePath '{outfile}'"
        return OSAction(host, "powershell", ["-NoProfile", "-Command", ps])
    return OSAction(host, "snippingtool", ["/clip"])


def _compile_window_capture(
    host: HostPlatform,
    outfile: str,
    params: dict[str, str],
) -> OSAction:
    title = params.get("title", "")
    mode = params.get("mode", "active")
    if host == HostPlatform.LINUX:
        return _linux_window_capture(host, outfile, title=title, mode=mode)
    if host == HostPlatform.MACOS:
        return _macos_window_capture(host, outfile, title=title)
    if host == HostPlatform.WINDOWS:
        return _windows_window_capture(host, outfile, title=title)
    raise ValueError(f"unsupported window capture host: {host.value}")


def _compile_screenshot(
    host: HostPlatform,
    authority: str,
    params: dict[str, str],
    uri: str,
) -> list[OSAction]:
    target = authority or "screen"
    outfile = _capture_outfile(target)
    if target == "screen":
        return [_compile_screen_capture(host, outfile)]
    if target == "window":
        return [_compile_window_capture(host, outfile, params)]
    raise ValueError(f"unsupported screenshot uri: {uri}")


def _linux_window_move_actions(
    host: HostPlatform,
    *,
    title: str,
    screen: str,
) -> list[OSAction]:
    xdotool = _first_available(("xdotool",))
    if xdotool:
        script = (
            f"WID=$(xdotool search --name '{title}' | head -n1); "
            f"xdotool windowmove $WID $(xdotool getdisplaygeometry --screen {screen} | "
            f"awk '{{print $1/4}}') 0"
        )
        return [OSAction(host, "bash", ["-lc", script])]
    wmctrl = _first_available(("wmctrl",))
    if wmctrl:
        return [OSAction(host, wmctrl, ["-r", title, "-e", "0,0,0,0,0"])]
    return [OSAction(host, "echo", [f"move:{title}:screen={screen}"])]


def _macos_window_move_actions(host: HostPlatform, *, title: str) -> list[OSAction]:
    script = (
        f'tell application "System Events" to set position of '
        f'first window of (first process whose name contains "{title}") '
        f"to {{100, 100}}"
    )
    return [OSAction(host, "osascript", ["-e", script])]


def _windows_window_move_actions(host: HostPlatform, *, title: str) -> list[OSAction]:
    ps = (
        f"$p = Get-Process -Name '{title}' -ErrorAction SilentlyContinue | "
        f"Select-Object -First 1; "
        f"if ($p) {{ Add-Type @' using System; using System.Runtime.InteropServices; "
        f"public class Win32 {{ [DllImport(\"user32.dll\")] public static extern bool "
        f"MoveWindow(IntPtr hWnd, int X, int Y, int nWidth, int nHeight, bool bRepaint); "
        f"}} '@; [Win32]::MoveWindow($p.MainWindowHandle, 0, 0, 800, 600, $true) }}"
    )
    return [OSAction(host, "powershell", ["-NoProfile", "-Command", ps])]


def _compile_window_move(
    host: HostPlatform,
    params: dict[str, str],
) -> list[OSAction]:
    title = params.get("title", "")
    screen = params.get("screen", "1")
    if not title:
        raise ValueError("desktop-window move requires title")

    if host == HostPlatform.LINUX:
        return _linux_window_move_actions(host, title=title, screen=screen)
    if host == HostPlatform.MACOS:
        return _macos_window_move_actions(host, title=title)
    if host == HostPlatform.WINDOWS:
        return _windows_window_move_actions(host, title=title)
    return [OSAction(host, "echo", [f"move:{title}:screen={screen}"])]


def _linux_window_focus_actions(host: HostPlatform, name: str) -> list[OSAction]:
    wmctrl = _first_available(("wmctrl",))
    if wmctrl:
        return [OSAction(host, wmctrl, ["-a", name])]
    xdotool = _first_available(("xdotool",))
    if xdotool:
        script = f"xdotool search --name {name} windowactivate"
        return [OSAction(host, "bash", ["-lc", script])]
    return _compile_launch_app(host, name)


def _macos_window_focus_actions(host: HostPlatform, name: str) -> list[OSAction]:
    script = f'tell application "{name}" to activate'
    return [OSAction(host, "osascript", ["-e", script])]


def _windows_window_focus_actions(host: HostPlatform, name: str) -> list[OSAction]:
    ps = (
        f"(Get-Process -Name '{name}' -ErrorAction SilentlyContinue | "
        f"Select-Object -First 1).MainWindowHandle"
    )
    return [OSAction(host, "powershell", ["-NoProfile", "-Command", ps])]


def _compile_window_focus(host: HostPlatform, name: str) -> list[OSAction]:
    if not name:
        raise ValueError("desktop-window focus requires name or title")
    if host == HostPlatform.LINUX:
        return _linux_window_focus_actions(host, name)
    if host == HostPlatform.MACOS:
        return _macos_window_focus_actions(host, name)
    if host == HostPlatform.WINDOWS:
        return _windows_window_focus_actions(host, name)
    return [OSAction(host, "echo", [name])]


def _compile_window(
    host: HostPlatform,
    authority: str,
    params: dict[str, str],
    uri: str,
) -> list[OSAction]:
    action = authority or "focus"
    name = params.get("name") or params.get("title", "")

    if action == "move":
        return _compile_window_move(host, params)

    if action != "focus":
        raise ValueError(f"unsupported desktop-window action: {uri}")

    return _compile_window_focus(host, name)


def _legacy_nlp2uri_settings(host: HostPlatform, _params: dict[str, str], _uri: str) -> list[OSAction]:
    return _compile_settings(host)


def _legacy_nlp2uri_app_open(
    host: HostPlatform,
    params: dict[str, str],
    _uri: str,
) -> list[OSAction]:
    return _compile_launch_app(host, params.get("name", ""))


def _legacy_nlp2uri_app_focus(
    host: HostPlatform,
    params: dict[str, str],
    uri: str,
) -> list[OSAction]:
    return _compile_window(host, "focus", params, uri)


def _legacy_nlp2uri_capture(
    host: HostPlatform,
    path: str,
    params: dict[str, str],
    uri: str,
) -> list[OSAction]:
    target = path.split("/", 1)[1]
    return _compile_screenshot(host, target, params, uri)


_LegacyNlp2UriHandler = Callable[[HostPlatform, dict[str, str], str], list[OSAction]]

_LEGACY_NLP2URI_PATHS: dict[str, _LegacyNlp2UriHandler] = {
    "settings/linux": _legacy_nlp2uri_settings,
    "app/open": _legacy_nlp2uri_app_open,
    "app/focus": _legacy_nlp2uri_app_focus,
}


def _compile_legacy_nlp2uri(host: HostPlatform, uri: str) -> list[OSAction]:
    parsed = urlparse(uri)
    segments = [parsed.netloc, parsed.path.lstrip("/")]
    path = "/".join(part for part in segments if part)
    params = _query_params(parsed)

    handler = _LEGACY_NLP2URI_PATHS.get(path)
    if handler is not None:
        return handler(host, params, uri)
    if path.startswith("capture/"):
        return _legacy_nlp2uri_capture(host, path, params, uri)

    raise ValueError(f"unsupported legacy nlp2uri path: {path}")


