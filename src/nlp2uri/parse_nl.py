"""Heuristic natural-language → UriIntent parsing (EN + PL)."""

from __future__ import annotations

import re
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
    r"(?:the\s+)?(?:(?:window|screen|desktop|okno|ekran)\s+)?"
    r"(?:titled|named|called|o\s+nazwie|z\s+tytu[łl]em)?\s*"
    r"(?P<title>[^.?!]+)?",
    re.IGNORECASE,
)
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
    r"(?:with\s+|w\s+folderze\s+|with\s+project\s+|project\s+)?(?P<path>[^\s'\"]+)",
    re.IGNORECASE,
)
_FILE_RE = re.compile(
    rf"\b{_OPEN}\s+(?:the\s+)?(?:file|folder|directory|plik|folder|katalog)\s+"
    r"(?P<path>[^\s'\"]+)",
    re.IGNORECASE,
)


def _strip_quotes(value: str) -> str:
    return value.strip().strip("\"'")


def _normalize_aliases(text: str) -> str:
    aliases = (
        (re.compile(r"\bvs\s*code\b", re.IGNORECASE), "vscode"),
        (re.compile(r"\bvisual\s+studio\s+code\b", re.IGNORECASE), "vscode"),
        (re.compile(r"\bedge\b", re.IGNORECASE), "microsoft-edge"),
    )
    normalized = text
    for pattern, replacement in aliases:
        normalized = pattern.sub(replacement, normalized)
    return normalized


def parse_text(text: str) -> UriIntent:
    raw = _normalize_aliases((text or "").strip())
    if not raw:
        raise ValueError("empty input")

    lowered = raw.lower()

    if _ABSOLUTE_URI_RE.match(raw):
        parsed = urlparse(raw)
        return UriIntent(
            kind=IntentKind.NAVIGATE,
            target=raw,
            params={"scheme": parsed.scheme},
            raw_text=raw,
            confidence=1.0,
        )

    if re.search(r"\bhttps?://\S+", raw, re.IGNORECASE):
        url_match = re.search(r"(https?://\S+)", raw, re.IGNORECASE)
        assert url_match is not None
        return UriIntent(
            kind=IntentKind.NAVIGATE,
            target=url_match.group(1),
            params={"scheme": "https"},
            raw_text=raw,
            confidence=0.95,
        )

    match = _IDE_PROJECT_RE.search(raw)
    if match:
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

    match = _FILE_RE.search(raw)
    if match:
        return UriIntent(
            kind=IntentKind.OPEN,
            target="file",
            params={"path": _strip_quotes(match.group("path"))},
            raw_text=raw,
            confidence=0.9,
        )

    if _SETTINGS_RE.search(lowered):
        return UriIntent(
            kind=IntentKind.OPEN,
            target="settings",
            raw_text=raw,
            confidence=0.85,
        )

    if _ACTIVE_WINDOW_RE.search(raw):
        params = {"mode": "active", "class": "browser"}
        if re.search(r"przegl[aą]darki|browser", lowered):
            params["class"] = "browser"
        return UriIntent(
            kind=IntentKind.CAPTURE,
            target="window",
            params=params,
            raw_text=raw,
            confidence=0.9,
        )

    match = _CAPTURE_RE.search(raw)
    if match:
        title = (match.group("title") or "").strip()
        title = _strip_quotes(title)
        if title.lower() in {"screen", "desktop", "window", "okno", "ekran"}:
            title = ""

        if re.search(r"\b(?:screen|desktop|ekran)\b", lowered):
            target = "screen"
        elif re.search(r"\b(?:window|okno)\b", lowered) or title:
            target = "window"
        else:
            target = "screen"
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

    match = _FOCUS_RE.search(raw)
    if match:
        return UriIntent(
            kind=IntentKind.FOCUS,
            target="app",
            params={"name": match.group("app").lower()},
            raw_text=raw,
            confidence=0.8,
        )

    match = _APP_RE.search(raw)
    if match:
        return UriIntent(
            kind=IntentKind.OPEN,
            target="app",
            params={"name": match.group("app").lower()},
            raw_text=raw,
            confidence=0.75,
        )

    path_match = _PATH_RE.search(raw)
    if path_match:
        return UriIntent(
            kind=IntentKind.OPEN,
            target="file",
            params={"path": _strip_quotes(path_match.group(1))},
            raw_text=raw,
            confidence=0.6,
        )

    if lowered.startswith(("open ", "otworz ", "otwórz ")):
        for prefix in ("otwórz ", "otworz ", "open "):
            if lowered.startswith(prefix):
                remainder = raw[len(prefix) :].strip()
                break
        else:
            remainder = ""
        if remainder:
            return UriIntent(
                kind=IntentKind.OPEN,
                target="app",
                params={"name": remainder.split()[0].lower()},
                raw_text=raw,
                confidence=0.5,
            )

    return UriIntent(
        kind=IntentKind.NAVIGATE,
        target=raw,
        raw_text=raw,
        confidence=0.3,
    )
