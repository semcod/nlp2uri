"""getv:// URI builders, index, resolve, and compile."""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

from nlp2uri.models import HostPlatform, OSAction
from nlp2uri.systemmap.encode import encode_segment
from nlp2uri.systemmap.getv_load import (
    discover_profiles,
    getv_home,
    load_profile_dict,
    mask_var_value,
)
from nlp2uri.systemmap.index import UriMap, UriMapEntry, _add_entry


GETV_SCHEME = "getv"


def uri_for_getv_profile(category: str, profile: str) -> str:
    """``getv://{category}/{profile}`` — whole profile."""
    return f"getv://{encode_segment(category)}/{encode_segment(profile)}"


def uri_for_getv_var(category: str, profile: str, var_name: str) -> str:
    """``getv://{category}/{profile}/{VAR}`` — single variable."""
    return (
        f"getv://{encode_segment(category)}/"
        f"{encode_segment(profile)}/"
        f"{encode_segment(var_name)}"
    )


def is_getv_uri(uri: str) -> bool:
    return urlparse(uri).scheme.lower() == GETV_SCHEME


def _decode_segment(value: str) -> str:
    return unquote(value or "")


def build_getv_uri_index(*, home: str | None = None) -> UriMap:
    """Build UriMap from ~/.getv profile tree."""
    from pathlib import Path

    base = Path(home).expanduser().resolve() if home else getv_home()
    uri_map = UriMap(
        format="getv_uri.v1",
        example_id=str(base),
        system_map_format="getv.profiles",
    )

    for category, profiles in discover_profiles(base).items():
        for profile in profiles:
            vars_dict = load_profile_dict(category, profile, home=base)
            profile_uri = uri_for_getv_profile(category, profile)
            _add_entry(
                uri_map,
                uri=profile_uri,
                kind="getv_profile",
                ref_type="getv.Profile",
                name=f"{category}/{profile}",
                ref={
                    "category": category,
                    "profile": profile,
                    "path": str(base / category / f"{profile}.env"),
                    "keys": sorted(vars_dict.keys()),
                },
            )
            for key, value in sorted(vars_dict.items()):
                var_uri = uri_for_getv_var(category, profile, key)
                _add_entry(
                    uri_map,
                    uri=var_uri,
                    kind="getv_var",
                    ref_type="getv.EnvVar",
                    name=key,
                    ref={
                        "category": category,
                        "profile": profile,
                        "key": key,
                        "value_masked": mask_var_value(key, value),
                        "sensitive": key.upper().endswith("_KEY") or "TOKEN" in key.upper(),
                    },
                    links=(profile_uri,),
                )
                uri_map.by_name.setdefault(key, []).append(var_uri)

    return uri_map


@dataclass(frozen=True)
class ResolvedGetvUri:
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


def resolve_prompt_against_getv(
    prompt: str,
    *,
    uri_map: UriMap | None = None,
    max_results: int = 5,
) -> list[ResolvedGetvUri]:
    """Map NL text to getv:// URIs (env var names, profile hints)."""
    index = uri_map or build_getv_uri_index()
    normalized = re.sub(r"\s+", " ", prompt.lower().strip())
    if not normalized:
        return []

    hits: list[ResolvedGetvUri] = []

    for entry in index.entries.values():
        if entry.kind != "getv_var" or not entry.name:
            continue
        key_lower = entry.name.lower()
        if key_lower in normalized:
            hits.append(
                ResolvedGetvUri(
                    uri=entry.uri,
                    kind=entry.kind,
                    confidence=0.95,
                    match_reason=f"env_key:{entry.name}",
                    entry_name=entry.name,
                )
            )
            continue
        # "groq api key" → GROQ_API_KEY
        key_spaced = key_lower.replace("_", " ")
        if key_spaced in normalized:
            hits.append(
                ResolvedGetvUri(
                    uri=entry.uri,
                    kind=entry.kind,
                    confidence=0.88,
                    match_reason=f"env_key_spaced:{entry.name}",
                    entry_name=entry.name,
                )
            )

    for entry in index.entries.values():
        if entry.kind != "getv_profile" or not entry.name:
            continue
        if entry.name.lower() in normalized or entry.ref.get("profile", "").lower() in normalized:
            hits.append(
                ResolvedGetvUri(
                    uri=entry.uri,
                    kind=entry.kind,
                    confidence=0.8,
                    match_reason=f"profile:{entry.name}",
                    entry_name=entry.name,
                )
            )

    hits.sort(key=lambda h: h.confidence, reverse=True)
    return hits[:max_results]


def compile_getv_uri(uri: str, host: HostPlatform) -> list[OSAction]:
    """Compile getv:// to getv CLI commands."""
    if not is_getv_uri(uri):
        raise ValueError(f"not a getv uri: {uri}")

    getv_bin = shutil.which("getv") or "getv"
    parsed = urlparse(uri)
    category = _decode_segment(parsed.netloc)
    path_parts = [p for p in parsed.path.split("/") if p]
    profile = _decode_segment(path_parts[0]) if path_parts else ""
    var_name = _decode_segment(path_parts[1]) if len(path_parts) > 1 else ""
    params = {k: v[0] for k, v in parse_qs(parsed.query).items() if v}
    action = params.get("action", "get")

    if not category or not profile:
        raise ValueError(f"getv uri requires category and profile: {uri}")

    if var_name:
        if action == "export":
            return [OSAction(host, getv_bin, ["export", category, profile, "--format", "env"])]
        return [OSAction(host, getv_bin, ["get", category, profile, var_name])]

    if action == "exec":
        cmd = params.get("cmd", "env")
        return [OSAction(host, getv_bin, ["exec", category, profile, "--", cmd])]

    return [OSAction(host, getv_bin, ["export", category, profile, "--format", "env"])]


def get_getv_var_value(uri: str) -> dict[str, Any]:
    """Read a getv:// var URI — returns masked value metadata (not raw secrets in logs)."""
    parsed = urlparse(uri)
    category = _decode_segment(parsed.netloc)
    parts = [p for p in parsed.path.split("/") if p]
    profile = _decode_segment(parts[0]) if parts else ""
    var_name = _decode_segment(parts[1]) if len(parts) > 1 else ""
    if not category or not profile or not var_name:
        raise ValueError(f"getv var uri requires category/profile/VAR: {uri}")

    value = load_profile_dict(category, profile).get(var_name)
    if value is None:
        return {"uri": uri, "found": False, "key": var_name}

    return {
        "uri": uri,
        "found": True,
        "category": category,
        "profile": profile,
        "key": var_name,
        "value_masked": mask_var_value(var_name, value),
    }
