"""http(s):// URI builder."""

from __future__ import annotations

from nlp2uri.models import UriIntent, UriSpec


def build_http(intent: UriIntent, *, uri: str | None = None) -> UriSpec:
    target = uri or intent.target
    if not target.startswith(("http://", "https://")):
        target = f"https://{target.lstrip('/')}"

    scheme = "https" if target.startswith("https://") else "http"

    return UriSpec(
        uri=target,
        scheme=scheme,
        action="navigate",
        platform_hints=("webbrowser", "xdg-open", "open", "start"),
        metadata={"url": target},
        intent=intent,
    )
