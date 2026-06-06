"""Public resolve API: natural language text → UriSpec / NLP2URIResult."""

from __future__ import annotations

from nlp2uri.compile import compile_uri_to_actions
from nlp2uri.models import HostPlatform, NLP2URIResult, UriSpec
from nlp2uri.parse_nl import parse_text
from nlp2uri.platform_detect import detect_platform
from nlp2uri.schemes.build import build_uri


def resolve_text(
    text: str,
    *,
    platform: HostPlatform | None = None,
) -> UriSpec:
    intent = parse_text(text)
    return build_uri(intent, platform=platform)


def nlp2uri(
    prompt: str,
    *,
    os: HostPlatform | None = None,
    locale: str | None = None,
) -> NLP2URIResult:
    """Full compiler: NL → abstract URI + OS action plan."""
    _ = locale  # reserved for future NLP locale routing
    host = os or detect_platform()
    intent = parse_text(prompt)
    spec = build_uri(intent, platform=host if host != HostPlatform.UNKNOWN else None)
    actions = tuple(compile_uri_to_actions(spec.uri, host if host != HostPlatform.UNKNOWN else None))
    return NLP2URIResult(
        uri=spec.uri,
        intent=intent.intent_name,
        slots=intent.to_slots(),
        spec=spec,
        actions=actions,
    )
