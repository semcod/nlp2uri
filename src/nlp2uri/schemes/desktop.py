"""Desktop operation URIs (abstract app://, desktop-screenshot://, desktop-window://)."""

from __future__ import annotations

from nlp2uri.models import HostPlatform, UriIntent, UriSpec
from nlp2uri.schemes.util import abstract_url

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


def build_settings(*, platform: HostPlatform, intent: UriIntent) -> UriSpec:
    uri = _NATIVE_SETTINGS.get(platform, "app://settings/open")
    scheme = uri.split(":", 1)[0]

    return UriSpec(
        uri=uri,
        scheme=scheme,
        action="open",
        platform_hints=("xdg-open", "open", "start"),
        metadata={"settings": True},
        intent=intent,
    )
