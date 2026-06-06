"""Desktop operation URIs (abstract app://, desktop-screenshot://, desktop-window://)."""

from __future__ import annotations

from nlp2uri.models import HostPlatform, UriIntent, UriSpec
from nlp2uri.schemes.util import abstract_url, normalize_path

_NATIVE_SETTINGS: dict[HostPlatform, str] = {
    HostPlatform.LINUX: "app://settings/open",
    HostPlatform.MACOS: "x-apple.systempreferences:",
    HostPlatform.WINDOWS: "ms-settings:",
}


def build_capture(intent: UriIntent, *, platform: HostPlatform) -> UriSpec:
    target = intent.target or "screen"
    params = dict(intent.params)
    if target == "window" and "mode" not in params:
        params.setdefault("mode", "active")

    authority = "screen" if target == "screen" else "window"
    uri = abstract_url("desktop-screenshot", authority, params=params)

    hints = {
        HostPlatform.LINUX: ("portal-screenshot", "grim", "scrot"),
        HostPlatform.MACOS: ("screencapture",),
        HostPlatform.WINDOWS: ("powershell", "snippingtool"),
    }.get(platform, ("capture",))

    return UriSpec(
        uri=uri,
        scheme="desktop-screenshot",
        action="capture",
        platform_hints=hints,
        metadata={"capture_target": target, **params},
        intent=intent,
    )


def build_focus(intent: UriIntent, *, platform: HostPlatform) -> UriSpec:
    params = dict(intent.params)
    uri = abstract_url("desktop-window", "focus", params=params)

    hints = {
        HostPlatform.LINUX: ("wmctrl", "xdotool"),
        HostPlatform.MACOS: ("osascript",),
        HostPlatform.WINDOWS: ("powershell",),
    }.get(platform, ("focus",))

    return UriSpec(
        uri=uri,
        scheme="desktop-window",
        action="focus",
        platform_hints=hints,
        metadata=dict(params),
        intent=intent,
    )


def build_app_open(intent: UriIntent, *, platform: HostPlatform) -> UriSpec:
    name = intent.params.get("name") or intent.target
    if not name:
        raise ValueError("app open intent requires name")

    uri = abstract_url("app", name, "/open")

    hints = {
        HostPlatform.LINUX: ("xdg-open", "gtk-launch", "desktop-id"),
        HostPlatform.MACOS: ("open", "-a"),
        HostPlatform.WINDOWS: ("start", "shell:AppsFolder"),
    }.get(platform, ("open",))

    return UriSpec(
        uri=uri,
        scheme="app",
        action="open",
        platform_hints=hints,
        metadata={"app": name},
        intent=intent,
    )


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


def build_move(intent: UriIntent, *, platform: HostPlatform) -> UriSpec:
    params = dict(intent.params)
    uri = abstract_url("desktop-window", "move", params=params)

    hints = {
        HostPlatform.LINUX: ("wmctrl", "xdotool"),
        HostPlatform.MACOS: ("osascript",),
        HostPlatform.WINDOWS: ("powershell",),
    }.get(platform, ("move",))

    return UriSpec(
        uri=uri,
        scheme="desktop-window",
        action="move",
        platform_hints=hints,
        metadata=dict(params),
        intent=intent,
    )


def build_terminal(intent: UriIntent, *, platform: HostPlatform) -> UriSpec:
    params: dict[str, str] = {}
    if intent.params.get("path"):
        params["path"] = normalize_path(intent.params["path"])
    uri = abstract_url("app", "terminal", "/open", params=params)

    hints = {
        HostPlatform.LINUX: ("gnome-terminal", "konsole", "alacritty", "xterm"),
        HostPlatform.MACOS: ("open", "-a", "Terminal"),
        HostPlatform.WINDOWS: ("wt", "cmd"),
    }.get(platform, ("terminal",))

    return UriSpec(
        uri=uri,
        scheme="app",
        action="open",
        platform_hints=hints,
        metadata={"terminal": True, **params},
        intent=intent,
    )


def build_settings(*, platform: HostPlatform, intent: UriIntent) -> UriSpec:
    panel = intent.params.get("panel", "")
    if panel:
        uri = _WINDOWS_SETTINGS_PANELS.get(panel) if platform == HostPlatform.WINDOWS else None
        if uri is None and platform == HostPlatform.MACOS:
            uri = _MACOS_SETTINGS_PANELS.get(panel)
        if uri is None:
            uri = abstract_url("app", "settings", f"/{panel}")
        scheme = uri.split(":", 1)[0]
        metadata = {"settings": True, "panel": panel}
    else:
        uri = _NATIVE_SETTINGS.get(platform, "app://settings/open")
        scheme = uri.split(":", 1)[0]
        metadata = {"settings": True}

    return UriSpec(
        uri=uri,
        scheme=scheme,
        action="open",
        platform_hints=("xdg-open", "open", "start"),
        metadata=metadata,
        intent=intent,
    )
