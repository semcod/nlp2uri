"""URI helper utilities (RFC 3986)."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import quote, urlencode


def abstract_url(
    scheme: str,
    authority: str,
    path: str = "",
    params: dict[str, str] | None = None,
) -> str:
    """Build an OS-neutral abstract URI: scheme://authority/path?query."""
    scheme = scheme.lower()
    authority = authority.strip("/")
    path = path if path.startswith("/") else f"/{path}" if path else ""
    if authority and path == "/":
        path = ""
    base = f"{scheme}://{authority}{path}"
    query = urlencode({k: v for k, v in (params or {}).items() if v})
    return f"{base}?{query}" if query else base


def nlp2uri_url(path: str, params: dict[str, str] | None = None) -> str:
    """Legacy nlp2uri:// scheme (backward compatible)."""
    query = urlencode({k: v for k, v in (params or {}).items() if v})
    base = f"nlp2uri://{path.lstrip('/')}"
    return f"{base}?{query}" if query else base


def normalize_path(path: str) -> str:
    expanded = Path(path).expanduser()
    try:
        return str(expanded.resolve())
    except OSError:
        return str(expanded)


def file_uri(path: str) -> str:
    normalized = normalize_path(path)
    return Path(normalized).as_uri()


def percent_encode_segment(value: str) -> str:
    return quote(value, safe="")
