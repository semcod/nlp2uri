"""Heuristic natural-language → UriIntent parsing (EN + PL)."""

from __future__ import annotations

import re
from collections.abc import Callable
from urllib.parse import urlparse

from nlp2uri.models import IntentKind, UriIntent

_OPEN = r"(?:open|otw[oó]rz|uruchom|launch|start|run)"
_IDE_NAME = r"(?:cursor|vscode|code|windsurf|jetbrains|pycharm|zed|ide)"
_ABSOLUTE_URI_RE = re.compile(
    r"^(?:https?|file|mailto|tel|sms|cursor|vscode|vscode-insiders|"
    r"ms-settings|x-apple\.systempreferences|nlp2uri|app|desktop-screenshot|desktop-window|"
    r"ide-chat|ide-command|koru-control)://\S+",
    re.IGNORECASE,
)
_PATH_RE = re.compile(r"(?:^|[\s'\"])(/?(?:[\w.\-~]+/)+[\w.\-~]+)")
_APP_RE = re.compile(
    rf"\b{_OPEN}\s+(?:the\s+)?(?P<app>[\w.\-+]+)\b",
    re.IGNORECASE,
)
_CAPTURE_RE = re.compile(
    r"\b(?:screenshot|capture|snap|zrzut(?:\s+ekranu)?|zr[oó]b\s+screenshot)\s+"
    r"(?:the\s+)?(?:(?:window|screen|desktop|okno|okna|ekran)\s+)?"
    r"(?:titled|named|called|o\s+nazwie|z\s+tytu[łl]em)?\s*"
    r"(?P<title>[^.?!]+)?",
    re.IGNORECASE,
)
_TERMINAL_RE = re.compile(
    rf"\b{_OPEN}\s+(?:a\s+)?terminal\b"
    r"(?:\s+(?:in\s+folder|in|w\s+folderze)\s+(?P<path>[^\s'\"]+))?",
    re.IGNORECASE,
)
_WINDOW_MOVE_RE = re.compile(
    r"\b(?:move|przenie[sś])\s+(?:the\s+)?(?:window\s+|okno\s+)?"
    r"(?P<title>[\w.\-+]+)\s+"
    r"(?:to\s+(?:the\s+)?(?:second|2(?:nd)?|drugi(?:\s+monitor)?)\s+(?:monitor|screen|ekran)"
    r"|na\s+(?:drugi(?:\s+monitor)?|monitor\s+(?P<screen>\d+))\s*(?:monitor|screen|ekran)?)",
    re.IGNORECASE,
)
_SETTINGS_PANEL_RE = re.compile(
    r"\b(?:open\s+)?(?P<panel_en>network|wifi|bluetooth|display|sound|privacy)\s+settings\b"
    r"|\b(?:open\s+)?(?:system\s+)?settings\s+for\s+(?P<panel_for>network|wifi|bluetooth|display|sound|privacy)\b"
    r"|\butawienia\s+(?P<panel_pl>sie[ćc]|sieci|wifi|bluetooth|wy[sś]wietlacz|d[zź]wi[eę]k|prywatno[sś][ćc])\b"
    r"|\botw[oó]rz\s+ustawienia\s+(?P<panel_pl2>sie[ćc]|sieci|wifi|bluetooth|wy[sś]wietlacz|d[zź]wi[eę]k|prywatno[sś][ćc])\b",
    re.IGNORECASE,
)
_PANEL_ALIASES: dict[str, str] = {
    "network": "network",
    "sieć": "network",
    "siec": "network",
    "sieci": "network",
    "wifi": "wifi",
    "wi-fi": "wifi",
    "bluetooth": "bluetooth",
    "display": "display",
    "wyświetlacz": "display",
    "wyswietlacz": "display",
    "sound": "sound",
    "dźwięk": "sound",
    "dzwiek": "sound",
    "privacy": "privacy",
    "prywatność": "privacy",
    "prywatnosc": "privacy",
}
_ACTIVE_WINDOW_RE = re.compile(
    r"\b(?:screenshot|capture|snap|zr[oó]b\s+screenshot)\s+"
    r"(?:aktywnego\s+okna|active\s+window)(?:\s+(?:przegl[aą]darki|browser))?",
    re.IGNORECASE,
)
_FOCUS_RE = re.compile(
    r"\b(?:focus|switch\s+to|bring\s+to\s+front|prze[łl][aą]cz\s+na|fokus)\s+"
    r"(?:the\s+)?(?P<app>[\w.\-+]+)\b",
    re.IGNORECASE,
)
_SETTINGS_RE = re.compile(
    r"\b(?:open\s+)?(?:system\s+)?(?:settings|ustawienia(?:\s+systemu)?)\b",
    re.IGNORECASE,
)
_IDE_PROJECT_RE = re.compile(
    rf"\b{_OPEN}\s+(?P<ide>cursor|vscode|code)\s+"
    r"(?:with\s+|w\s+folderze\s+|z\s+projektem\s+|with\s+project\s+|project\s+)?"
    r"(?P<path>[^\s'\"]+)",
    re.IGNORECASE,
)
_IDE_CHAT_SEND_RE = re.compile(
    rf"\b(?:send|wy[śs]lij|wyślij)\s+(?P<text>.+?)\s+"
    rf"(?:to|do)\s+(?P<ide>{_IDE_NAME})\b",
    re.IGNORECASE,
)
_IDE_CHAT_PASTE_RE = re.compile(
    rf"\b(?:paste|wklej)\s+(?:(?P<text>.+?)\s+)?"
    rf"(?:to|do)\s+(?P<ide>{_IDE_NAME})\b",
    re.IGNORECASE,
)
_IDE_STATUS_RE = re.compile(
    rf"\b(?:status|sprawd[zź](?:\s+status)?|check\s+status)\b"
    rf".*?(?:pluginu\s+|plugin\s+)?(?P<ide>{_IDE_NAME})\b",
    re.IGNORECASE,
)
_IDE_COMMAND_RE = re.compile(
    rf"\b(?:run|execute|uruchom)\s+(?:ide\s+)?(?:command\s+)?(?P<command>[\w.]+)\s+"
    rf"(?:in|w|on|na)\s+(?P<ide>{_IDE_NAME})\b",
    re.IGNORECASE,
)
_IDE_COMMAND_CAPABILITY_RE = re.compile(
    rf"\b(?:run|execute|uruchom|wykonaj)\s+(?P<capability>submit|paste|focus|open|wysy[łl]aj|wklej|fokus)\s+"
    rf"(?:in|w|on|na)\s+(?P<ide>{_IDE_NAME})\b",
    re.IGNORECASE,
)
_IDE_COMMAND_PL_RE = re.compile(
    rf"\b(?:uruchom|wykonaj)\s+komend[ęe]\s+(?P<command>[\w.]+)\s+"
    rf"(?:w|na)\s+(?P<ide>{_IDE_NAME})\b",
    re.IGNORECASE,
)
_FILE_RE = re.compile(
    rf"\b{_OPEN}\s+(?:the\s+)?(?:file|folder|directory|plik|folder|katalog)\s+"
    r"(?P<path>[^\s'\"]+)",
    re.IGNORECASE,
)
_OPEN_PREFIXES = ("otwórz ", "otworz ", "open ")
_KEYWORD_TARGETS = frozenset({"screen", "desktop", "window", "okno", "ekran"})


def _strip_quotes(value: str) -> str:
    return value.strip().strip("\"'")


def _normalize_ide_name(value: str | None) -> str:
    raw = (value or "auto").strip().lower()
    aliases = {
        "code": "vscode",
        "ide": "auto",
        "pycharm": "jetbrains",
    }
    return aliases.get(raw, raw)


def _bool_param(value: bool) -> str:
    return "true" if value else "false"


def _mentions_no_submit(lowered: str) -> bool:
    return bool(
        re.search(
            r"\b(?:do\s+not\s+submit|don't\s+submit|without\s+submit|no-submit|"
            r"nie\s+wysy[łl]aj|bez\s+wysy[łl]ania)\b",
            lowered,
            re.IGNORECASE,
        )
    )


def _mentions_require_plugin(lowered: str) -> bool:
    return bool(
        re.search(
            r"\b(?:require\s+plugin|plugin\s+only|only\s+plugin|"
            r"tylko\s+plugin|tylko\s+pluginu|bez\s+fallbacku)\b",
            lowered,
            re.IGNORECASE,
        )
    )


def _workspace_hint(raw: str) -> str:
    path_match = _PATH_RE.search(raw)
    if path_match:
        return _strip_quotes(path_match.group(1))
    if re.search(r"\b(?:this\s+project|current\s+project|tym\s+projekcie|bieżącym\s+projekcie)\b", raw, re.IGNORECASE):
        return "."
    return ""


def _normalize_aliases(text: str) -> str:
    aliases = (
        (re.compile(r"\bvs\s*code\b", re.IGNORECASE), "vscode"),
        (re.compile(r"\bvisual\s+studio\s+code\b", re.IGNORECASE), "vscode"),
    )
    normalized = text
    for pattern, replacement in aliases:
        normalized = pattern.sub(replacement, normalized)
    return normalized


def _parse_absolute_uri(raw: str, _lowered: str) -> UriIntent | None:
    if not _ABSOLUTE_URI_RE.match(raw):
        return None
    parsed = urlparse(raw)
    return UriIntent(
        kind=IntentKind.NAVIGATE,
        target=raw,
        params={"scheme": parsed.scheme},
        raw_text=raw,
        confidence=1.0,
    )


def _parse_http_url(raw: str, _lowered: str) -> UriIntent | None:
    url_match = re.search(r"(https?://\S+)", raw, re.IGNORECASE)
    if not url_match:
        return None
    return UriIntent(
        kind=IntentKind.NAVIGATE,
        target=url_match.group(1),
        params={"scheme": "https"},
        raw_text=raw,
        confidence=0.95,
    )


def _parse_ide_project(raw: str, _lowered: str) -> UriIntent | None:
    match = _IDE_PROJECT_RE.search(raw)
    if not match:
        return None
    return UriIntent(
        kind=IntentKind.OPEN,
        target="ide",
        params={
            "ide": match.group("ide").lower(),
            "path": _strip_quotes(match.group("path")),
        },
        raw_text=raw,
        confidence=0.95,
    )


def _parse_ide_chat_send(raw: str, lowered: str) -> UriIntent | None:
    match = _IDE_CHAT_SEND_RE.search(raw) or _IDE_CHAT_PASTE_RE.search(raw)
    if not match:
        return None
    text = _strip_quotes((match.group("text") or "").strip(" ,:"))
    ide = _normalize_ide_name(match.group("ide"))
    params = {
        "ide": ide,
        "submit": _bool_param(not _mentions_no_submit(lowered)),
        "require_plugin": _bool_param(_mentions_require_plugin(lowered)),
    }
    workspace = _workspace_hint(raw)
    if workspace:
        params["workspace"] = workspace
    if text:
        params["text"] = text
    return UriIntent(
        kind=IntentKind.IDE_CHAT_SEND,
        target="ide_chat",
        params=params,
        raw_text=raw,
        confidence=0.88,
    )


def _parse_ide_status(raw: str, _lowered: str) -> UriIntent | None:
    match = _IDE_STATUS_RE.search(raw)
    if not match:
        return None
    return UriIntent(
        kind=IntentKind.IDE_STATUS,
        target="ide",
        params={"ide": _normalize_ide_name(match.group("ide"))},
        raw_text=raw,
        confidence=0.82,
    )


def _normalize_command_capability(value: str) -> str:
    aliases = {
        "wysyłaj": "submit",
        "wysylaj": "submit",
        "wklej": "paste",
        "fokus": "focus",
    }
    return aliases.get(value.lower(), value.lower())


def _parse_ide_command(raw: str, lowered: str) -> UriIntent | None:
    match = (
        _IDE_COMMAND_RE.search(raw)
        or _IDE_COMMAND_PL_RE.search(raw)
        or _IDE_COMMAND_CAPABILITY_RE.search(raw)
    )
    if not match:
        return None
    ide = _normalize_ide_name(match.group("ide"))
    params: dict[str, str] = {
        "ide": ide,
        "require_plugin": _bool_param(_mentions_require_plugin(lowered)),
    }
    workspace = _workspace_hint(raw)
    if workspace:
        params["workspace"] = workspace
    command = match.groupdict().get("command")
    capability = match.groupdict().get("capability")
    if command:
        params["command"] = command
        target = command
    elif capability:
        normalized = _normalize_command_capability(capability)
        params["capability"] = normalized
        target = normalized
    else:
        return None
    return UriIntent(
        kind=IntentKind.IDE_COMMAND,
        target=target,
        params=params,
        raw_text=raw,
        confidence=0.84,
    )


def _parse_file_open(raw: str, _lowered: str) -> UriIntent | None:
    match = _FILE_RE.search(raw)
    if not match:
        return None
    return UriIntent(
        kind=IntentKind.OPEN,
        target="file",
        params={"path": _strip_quotes(match.group("path"))},
        raw_text=raw,
        confidence=0.9,
    )


def _normalize_panel(raw: str) -> str:
    key = raw.strip().lower()
    return _PANEL_ALIASES.get(key, key)


def _parse_settings_panel(raw: str, lowered: str) -> UriIntent | None:
    match = _SETTINGS_PANEL_RE.search(lowered)
    if not match:
        return None
    panel_raw = (
        match.group("panel_en")
        or match.group("panel_for")
        or match.group("panel_pl")
        or match.group("panel_pl2")
        or ""
    )
    return UriIntent(
        kind=IntentKind.OPEN,
        target="settings",
        params={"panel": _normalize_panel(panel_raw)},
        raw_text=raw,
        confidence=0.9,
    )


def _parse_terminal(raw: str, _lowered: str) -> UriIntent | None:
    match = _TERMINAL_RE.search(raw)
    if not match:
        return None
    params: dict[str, str] = {}
    if match.group("path"):
        params["path"] = _strip_quotes(match.group("path"))
    return UriIntent(
        kind=IntentKind.OPEN,
        target="terminal",
        params=params,
        raw_text=raw,
        confidence=0.9,
    )


def _parse_window_move(raw: str, _lowered: str) -> UriIntent | None:
    match = _WINDOW_MOVE_RE.search(raw)
    if not match:
        return None
    screen = match.group("screen") or "1"
    return UriIntent(
        kind=IntentKind.MOVE,
        target="window",
        params={"title": match.group("title"), "screen": screen},
        raw_text=raw,
        confidence=0.85,
    )


def _parse_settings(_raw: str, lowered: str) -> UriIntent | None:
    if not _SETTINGS_RE.search(lowered):
        return None
    return UriIntent(
        kind=IntentKind.OPEN,
        target="settings",
        raw_text=_raw,
        confidence=0.85,
    )


def _parse_active_window(raw: str, _lowered: str) -> UriIntent | None:
    if not _ACTIVE_WINDOW_RE.search(raw):
        return None
    params = {"mode": "active", "class": "browser"}
    return UriIntent(
        kind=IntentKind.CAPTURE,
        target="window",
        params=params,
        raw_text=raw,
        confidence=0.9,
    )


def _capture_target(lowered: str, title: str) -> str:
    if re.search(r"\b(?:screen|desktop|ekran)\b", lowered):
        return "screen"
    if re.search(r"\b(?:window|okno)\b", lowered) or title:
        return "window"
    return "screen"


def _parse_capture(raw: str, lowered: str) -> UriIntent | None:
    match = _CAPTURE_RE.search(raw)
    if not match:
        return None
    title = _strip_quotes((match.group("title") or "").strip())
    if title.lower() in _KEYWORD_TARGETS:
        title = ""
    target = _capture_target(lowered, title)
    params: dict[str, str] = {}
    if title:
        params["title"] = title
    if target == "window":
        params.setdefault("mode", "active")
    return UriIntent(
        kind=IntentKind.CAPTURE,
        target=target,
        params=params,
        raw_text=raw,
        confidence=0.85,
    )


def _parse_focus(raw: str, _lowered: str) -> UriIntent | None:
    match = _FOCUS_RE.search(raw)
    if not match:
        return None
    return UriIntent(
        kind=IntentKind.FOCUS,
        target="app",
        params={"name": match.group("app").lower()},
        raw_text=raw,
        confidence=0.8,
    )


def _normalize_app_name(name: str) -> str:
    lowered = name.lower()
    if lowered == "edge":
        return "microsoft-edge"
    return lowered


def _parse_app_open(raw: str, _lowered: str) -> UriIntent | None:
    match = _APP_RE.search(raw)
    if not match:
        return None
    return UriIntent(
        kind=IntentKind.OPEN,
        target="app",
        params={"name": _normalize_app_name(match.group("app"))},
        raw_text=raw,
        confidence=0.75,
    )


def _parse_path(raw: str, _lowered: str) -> UriIntent | None:
    path_match = _PATH_RE.search(raw)
    if not path_match:
        return None
    return UriIntent(
        kind=IntentKind.OPEN,
        target="file",
        params={"path": _strip_quotes(path_match.group(1))},
        raw_text=raw,
        confidence=0.6,
    )


def _parse_open_prefix(raw: str, lowered: str) -> UriIntent | None:
    if not lowered.startswith(_OPEN_PREFIXES):
        return None
    remainder = ""
    for prefix in _OPEN_PREFIXES:
        if lowered.startswith(prefix):
            remainder = raw[len(prefix) :].strip()
            break
    if not remainder:
        return None
    return UriIntent(
        kind=IntentKind.OPEN,
        target="app",
        params={"name": _normalize_app_name(remainder.split()[0])},
        raw_text=raw,
        confidence=0.5,
    )


def _parse_fallback(raw: str, _lowered: str) -> UriIntent:
    return UriIntent(
        kind=IntentKind.NAVIGATE,
        target=raw,
        raw_text=raw,
        confidence=0.3,
    )


_PARSERS: tuple[Callable[[str, str], UriIntent | None], ...] = (
    _parse_absolute_uri,
    _parse_http_url,
    _parse_ide_chat_send,
    _parse_ide_status,
    _parse_ide_command,
    _parse_ide_project,
    _parse_file_open,
    _parse_terminal,
    _parse_settings_panel,
    _parse_settings,
    _parse_window_move,
    _parse_active_window,
    _parse_capture,
    _parse_focus,
    _parse_app_open,
    _parse_path,
    _parse_open_prefix,
)


def parse_text(text: str) -> UriIntent:
    raw = _normalize_aliases((text or "").strip())
    if not raw:
        raise ValueError("empty input")

    lowered = raw.lower()
    for parser in _PARSERS:
        intent = parser(raw, lowered)
        if intent is not None:
            return intent
    return _parse_fallback(raw, lowered)
