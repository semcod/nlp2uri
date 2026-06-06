"""Natural language to URI resolution and cross-platform execution."""

from nlp2uri.compile import compile_uri_to_actions
from nlp2uri.models import ActionResult, HostPlatform, NLP2URIResult, OSAction, UriIntent, UriSpec
from nlp2uri.resolve import nlp2uri, resolve_text
from nlp2uri.runtime import execute_uri, get_executor

__all__ = [
    "ActionResult",
    "HostPlatform",
    "NLP2URIResult",
    "OSAction",
    "UriIntent",
    "UriSpec",
    "compile_uri_to_actions",
    "execute_uri",
    "get_executor",
    "nlp2uri",
    "resolve_text",
]

__version__ = "0.1.1"
