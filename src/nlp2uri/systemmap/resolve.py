"""Resolve natural-language prompts against a SystemMap URI index."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from nlp2uri.systemmap.index import UriMap, build_uri_index


@dataclass(frozen=True)
class ResolvedSystemUri:
    """One NL match against the SystemMap."""

    uri: str
    kind: str
    confidence: float
    match_reason: str
    entry_name: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "uri": self.uri,
            "kind": self.kind,
            "confidence": self.confidence,
            "match_reason": self.match_reason,
            "entry_name": self.entry_name,
        }


def _normalize_token(text: str) -> str:
    lowered = text.lower().strip()
    lowered = re.sub(r"[^\w\s:/.-]", " ", lowered, flags=re.UNICODE)
    return re.sub(r"\s+", " ", lowered).strip()


def _name_variants(name: str) -> set[str]:
    base = name.lower()
    variants = {base, base.replace("_", " "), base.replace("-", " ")}
    return {v for v in variants if v}


def resolve_prompt_against_system_map(
    prompt: str,
    ir: Any,
    *,
    uri_map: UriMap | None = None,
    max_results: int = 5,
) -> list[ResolvedSystemUri]:
    """Map NL text to canonical SystemMap URIs (commands, resources, runtimes)."""
    index = uri_map or build_uri_index(ir)
    normalized = _normalize_token(prompt)
    if not normalized:
        return []

    hits: list[ResolvedSystemUri] = []

    for entry in index.entries.values():
        if entry.kind == "command" and entry.name:
            for variant in _name_variants(entry.name):
                if variant in normalized or normalized in variant:
                    hits.append(
                        ResolvedSystemUri(
                            uri=entry.uri,
                            kind=entry.kind,
                            confidence=0.95 if variant == normalized else 0.85,
                            match_reason=f"command_name:{entry.name}",
                            entry_name=entry.name,
                        )
                    )
                    break
            desc = str(entry.ref.get("description") or "").lower()
            if desc and desc in normalized:
                hits.append(
                    ResolvedSystemUri(
                        uri=entry.uri,
                        kind=entry.kind,
                        confidence=0.75,
                        match_reason="command_description",
                        entry_name=entry.name,
                    )
                )

        if entry.kind == "resource" and entry.name:
            title = str(entry.ref.get("title") or "").lower()
            for candidate in (entry.name.lower(), title):
                if candidate and candidate in normalized:
                    hits.append(
                        ResolvedSystemUri(
                            uri=entry.uri,
                            kind=entry.kind,
                            confidence=0.8,
                            match_reason="resource_id_or_title",
                            entry_name=entry.name,
                        )
                    )
                    break

        if entry.kind == "runtime" and entry.name:
            for variant in _name_variants(entry.name):
                if variant in normalized:
                    hits.append(
                        ResolvedSystemUri(
                            uri=entry.uri,
                            kind=entry.kind,
                            confidence=0.7,
                            match_reason=f"runtime_id:{entry.name}",
                            entry_name=entry.name,
                        )
                    )
                    break

    # Deduplicate by URI, keep highest confidence
    best: dict[str, ResolvedSystemUri] = {}
    for hit in hits:
        prev = best.get(hit.uri)
        if prev is None or hit.confidence > prev.confidence:
            best[hit.uri] = hit

    ordered = sorted(best.values(), key=lambda item: (-item.confidence, item.uri))
    return ordered[:max_results]
