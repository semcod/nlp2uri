"""Resolve prompts: SystemMap first, desktop NL fallback."""

from __future__ import annotations

from typing import Any

from nlp2uri.models import HostPlatform
from nlp2uri.systemmap.index import UriMap, build_uri_index
from nlp2uri.systemmap.resolve import ResolvedSystemUri, resolve_prompt_against_system_map


def resolve_prompt_with_fallback(
    prompt: str,
    ir: Any | None = None,
    *,
    uri_map: UriMap | None = None,
    platform: HostPlatform | None = None,
    max_results: int = 5,
) -> dict[str, Any]:
    """Try SystemMap URI resolution; fall back to desktop ``parse_nl`` pipeline."""
    matches: list[ResolvedSystemUri] = []
    if ir is not None:
        index = uri_map or build_uri_index(ir)
        matches = resolve_prompt_against_system_map(
            prompt,
            ir,
            uri_map=index,
            max_results=max_results,
        )
        if matches:
            top = matches[0]
            return {
                "source": "system_map",
                "uri": top.uri,
                "confidence": top.confidence,
                "match_reason": top.match_reason,
                "entry_name": top.entry_name,
                "matches": [item.to_dict() for item in matches],
                "uri_map_format": index.format,
                "example_id": index.example_id,
            }

    from nlp2uri.resolve import resolve_text

    spec = resolve_text(prompt, platform=platform)
    return {
        "source": "desktop",
        "uri": spec.uri,
        "confidence": spec.intent.confidence if spec.intent else 0.5,
        "spec": spec.to_dict(),
        "matches": [],
    }
