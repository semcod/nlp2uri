"""app://{ide}/open — abstract IDE opener with native deep-link."""

from __future__ import annotations

from pathlib import Path

from nlp2uri.models import UriIntent, UriSpec
from nlp2uri.schemes.util import abstract_url, normalize_path

_IDE_SCHEMES = {
    "cursor": "cursor",
    "vscode": "vscode",
    "code": "vscode",
}


def build_ide(intent: UriIntent) -> UriSpec:
    ide = (intent.params.get("ide") or "vscode").lower()
    path = intent.params.get("path") or intent.target
    if not path:
        raise ValueError("ide intent requires path")

    normalized = normalize_path(path)
    native_scheme = _IDE_SCHEMES.get(ide, ide)
    native_uri = f"{native_scheme}://file{Path(normalized).as_posix()}"
    uri = abstract_url("app", ide, "/open", params={"path": normalized})

    return UriSpec(
        uri=uri,
        scheme="app",
        action="open",
        platform_hints=("xdg-open", "open", "start"),
        metadata={"ide": ide, "path": normalized, "native_uri": native_uri},
        intent=intent,
    )
