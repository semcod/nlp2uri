"""Heuristic natural-language → UriIntent parsing (EN + PL)."""

from __future__ import annotations

import re
from collections.abc import Callable
from urllib.parse import urlparse

from nlp2uri.models import IntentKind, UriIntent

_OPEN = r"(?:open|otw[oó]rz|uruchom|launch|start|run)"
_ABSOLUTE_URI_RE = re.compile(
    r"^(?:https?|file|mailto|tel|sms|cursor|vscode|vscode-insiders|"
    r"ms-settings|x-apple\.systempreferences|nlp2uri|app|desktop-screenshot|desktop-window)://\S+",
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
_FILE_RE = re.compile(
    rf"\b{_OPEN}\s+(?:the\s+)?(?:file|folder|directory|plik|folder|katalog)\s+"
    r"(?P<path>[^\s'\"]+)",
    re.IGNORECASE,
)
_OPEN_PREFIXES = ("otwórz ", "otworz ", "open ")
_KEYWORD_TARGETS = frozenset({"screen", "desktop", "window", "okno", "ekran"})


def _strip_quotes(value: str) -> str:
    return value.strip().strip("\"'")


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
