"""Map UriIntent → UriSpec."""

from __future__ import annotations

from urllib.parse import urlparse

from nlp2uri.models import HostPlatform, IntentKind, UriIntent, UriSpec
from nlp2uri.platform_detect import detect_platform
from nlp2uri.schemes import desktop, file as file_scheme, http as http_scheme, ide


def build_uri(intent: UriIntent, *, platform: HostPlatform | None = None) -> UriSpec:
    host = platform or detect_platform()

    if intent.kind == IntentKind.NAVIGATE:
        return _build_navigate(intent)

    if intent.kind == IntentKind.CAPTURE:
        return desktop.build_capture(intent, platform=host)

    if intent.kind == IntentKind.FOCUS:
        return desktop.build_focus(intent, platform=host)

    if intent.kind == IntentKind.MOVE:
        return desktop.build_move(intent, platform=host)

    if intent.kind == IntentKind.IDE_CHAT_SEND:
        return ide.build_ide_chat_send(intent)

    if intent.kind == IntentKind.IDE_STATUS:
        return ide.build_ide_status(intent)

    if intent.kind == IntentKind.IDE_COMMAND:
        return ide.build_ide_command(intent)

    if intent.kind == IntentKind.KORU_CONTROL:
        return ide.build_koru_control_drive(intent)

    if intent.kind == IntentKind.IDE_OPEN:
        return ide.build_ide(intent.with_params(path=intent.params.get("path") or intent.target))

    if intent.kind == IntentKind.OPEN:
        if intent.target == "file":
            return file_scheme.build_file(intent)
        if intent.target == "ide":
            return ide.build_ide(intent)
        if intent.target == "settings":
            return desktop.build_settings(platform=host, intent=intent)
        if intent.target == "terminal":
            return desktop.build_terminal(intent, platform=host)
        if intent.target == "app":
            return desktop.build_app_open(intent, platform=host)

    # Fallback: treat target as URL or search-like string.
    if "://" in intent.target:
        return _build_navigate(intent.with_params(scheme=urlparse(intent.target).scheme))

    return desktop.build_app_open(intent.with_params(name=intent.target), platform=host)


def _build_navigate(intent: UriIntent) -> UriSpec:
    target = intent.target
    parsed = urlparse(target)
    scheme = parsed.scheme or "https"

    if scheme in {"http", "https"}:
        return http_scheme.build_http(intent, uri=target)

    if scheme == "file":
        return file_scheme.build_file(intent.with_params(path=parsed.path))

    return UriSpec(
        uri=target,
        scheme=scheme,
        action="navigate",
        platform_hints=("open",),
        metadata={"passthrough": True},
        intent=intent,
    )
