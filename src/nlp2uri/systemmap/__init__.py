"""URI addressing layer over env2llm SystemMapIR (system_map_uri.v1)."""

from nlp2uri.systemmap.compile import compile_system_map_uri, is_system_map_uri
from nlp2uri.systemmap.context import load_ir_from_arguments
from nlp2uri.systemmap.fallback import resolve_prompt_with_fallback
from nlp2uri.systemmap.index import UriMap, UriMapEntry, build_uri_index
from nlp2uri.systemmap.load import (
    env2llm_available,
    env2llm_missing_message,
    load_system_map_from_doql,
    load_system_map_from_example,
)
from nlp2uri.systemmap.resolve import ResolvedSystemUri, resolve_prompt_against_system_map
from nlp2uri.systemmap.uri import (
    uri_for_access,
    uri_for_artifact,
    uri_for_command,
    uri_for_conversation,
    uri_for_environment,
    uri_for_generated_service,
    uri_for_process,
    uri_for_resource,
    uri_for_runtime,
    uri_for_validation,
)

__all__ = [
    "ResolvedSystemUri",
    "UriMap",
    "UriMapEntry",
    "build_uri_index",
    "compile_system_map_uri",
    "env2llm_available",
    "env2llm_missing_message",
    "is_system_map_uri",
    "load_ir_from_arguments",
    "load_system_map_from_doql",
    "load_system_map_from_example",
    "resolve_prompt_against_system_map",
    "resolve_prompt_with_fallback",
    "uri_for_access",
    "uri_for_artifact",
    "uri_for_command",
    "uri_for_conversation",
    "uri_for_environment",
    "uri_for_generated_service",
    "uri_for_process",
    "uri_for_resource",
    "uri_for_runtime",
    "uri_for_validation",
]
