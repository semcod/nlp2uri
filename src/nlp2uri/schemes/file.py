"""app://file/open — abstract file opener."""

from __future__ import annotations

from nlp2uri.models import UriIntent, UriSpec
from nlp2uri.schemes.util import abstract_url, file_uri, normalize_path


def build_file(intent: UriIntent) -> UriSpec:
    path = intent.params.get("path") or intent.target
    if not path:
        raise ValueError("file intent requires path")

    normalized = normalize_path(path)
    native = file_uri(normalized)
    uri = abstract_url("app", "file", "/open", params={"path": normalized})

    return UriSpec(
        uri=uri,
        scheme="app",
        action="open",
        platform_hints=("xdg-open", "open", "start"),
        metadata={"path": normalized, "native_uri": native},
        intent=intent,
    )
