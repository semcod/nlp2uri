"""Public resolve API: natural language text → UriSpec / NLP2URIResult."""

from __future__ import annotations

from nlp2uri.compile import compile_uri_to_actions
from nlp2uri.config import get_effective_platform, load_config
from nlp2uri.models import HostPlatform, NLP2URIResult, UriSpec
from nlp2uri.parse_nl import parse_text
from nlp2uri.schemes.build import build_uri


def resolve_text(
    text: str,
    *,
    platform: HostPlatform | None = None,
) -> UriSpec:
    intent = parse_text(text)
    return build_uri(intent, platform=platform or get_effective_platform())


def nlp2uri(
    prompt: str,
    *,
    os: HostPlatform | None = None,
    locale: str | None = None,
) -> NLP2URIResult:
    """Full compiler: NL → abstract URI + OS action plan."""
    loc = locale or load_config().locale
    _ = loc  # reserved for future NLP locale routing
    host = get_effective_platform(os)
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
