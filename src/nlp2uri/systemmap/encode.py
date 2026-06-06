"""Percent-encoding helpers for SystemMap URI segments."""

from __future__ import annotations

from urllib.parse import quote


def encode_segment(value: str) -> str:
    """Encode a single URI path/authority segment (preserves unreserved)."""
    return quote(value, safe="")


def encode_path(value: str) -> str:
    """Encode a slash-separated path while keeping path separators."""
    return quote(value.lstrip("/"), safe="/")
