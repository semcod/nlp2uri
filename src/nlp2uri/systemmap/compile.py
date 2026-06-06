"""Compile SystemMap URIs to handoff / probe actions."""

from __future__ import annotations

import json
import os
from urllib.parse import unquote, urlparse

from nlp2uri.models import HostPlatform, OSAction
from nlp2uri.systemmap.index import UriMap

SYSTEM_MAP_SCHEMES = frozenset(
    {
        "command",
        "runtime",
        "resource",
        "access",
        "artifact",
        "conversation",
        "process",
        "validation",
        "schedule",
        "service",
        "deploy",
        "environment",
    }
)


def is_system_map_uri(uri: str) -> bool:
    parsed = urlparse(uri)
    return parsed.scheme.lower() in SYSTEM_MAP_SCHEMES


def _decode_segment(value: str) -> str:
    return unquote(value or "")


def _backend_url() -> str:
    return os.environ.get("NLP2DSL_BACKEND_URL", "http://localhost:8010").rstrip("/")


def _worker_url() -> str:
    return os.environ.get("NLP2DSL_WORKER_URL", "http://localhost:8020").rstrip("/")


def compile_system_map_uri(
    uri: str,
    host: HostPlatform,
    *,
    uri_map: UriMap | None = None,
    config: dict[str, str] | None = None,
) -> list[OSAction]:
    """Compile ``command://``, ``runtime://``, … to nlp2dsl handoff or probe actions."""
    parsed = urlparse(uri)
    scheme = parsed.scheme.lower()
    if scheme not in SYSTEM_MAP_SCHEMES:
        raise ValueError(f"unsupported system map uri scheme: {scheme}")

    if scheme == "command":
        return _compile_command(host, parsed, config=config)
    if scheme == "runtime":
        return _compile_runtime(host, parsed, uri_map=uri_map)
    if scheme == "resource":
        return _compile_resource(host, parsed, config=config)
    if scheme == "artifact":
        return _compile_artifact(host, parsed, config=config)
    if scheme in {"conversation", "process", "validation", "schedule", "service", "deploy", "environment"}:
        return _compile_metadata(host, scheme, parsed)
    if scheme == "access":
        return _compile_access(host, parsed)

    raise ValueError(f"unsupported system map uri: {uri}")


def _compile_command(
    host: HostPlatform,
    parsed,
    *,
    config: dict[str, str] | None,
) -> list[OSAction]:
    runtime_id = _decode_segment(parsed.netloc) or "unknown"
    command_name = _decode_segment(parsed.path.lstrip("/"))
    if not command_name:
        raise ValueError("command uri requires a command name path segment")

    body = {
        "action": command_name,
        "runtime": runtime_id,
        "config": dict(config or {}),
    }
    payload = json.dumps(body, separators=(",", ":"))
    endpoint = f"{_backend_url()}/workflow/run"
    return [
        OSAction(
            host,
            "curl",
            [
                "-sfX",
                "POST",
                endpoint,
                "-H",
                "Content-Type: application/json",
                "-d",
                payload,
            ],
        )
    ]


def _compile_runtime(
    host: HostPlatform,
    parsed,
    *,
    uri_map: UriMap | None,
) -> list[OSAction]:
    runtime_id = _decode_segment(parsed.path.lstrip("/")) or _decode_segment(parsed.netloc)
    health_url: str | None = None

    if uri_map is not None:
        entry = uri_map.lookup(f"runtime://{parsed.netloc}/{parsed.path.lstrip('/')}")
        if entry is None:
            for candidate in uri_map.find_by_kind("runtime"):
                if candidate.name == runtime_id:
                    entry = candidate
                    break
        if entry is not None:
            health_url = entry.ref.get("health") or entry.ref.get("url")

    if health_url:
        return [OSAction(host, "curl", ["-sf", str(health_url)])]

    if runtime_id.startswith("executor:"):
        return [OSAction(host, "curl", ["-sf", f"{_worker_url()}/health"])]
    if runtime_id.startswith("orchestrator:") or runtime_id.startswith("gateway:"):
        return [OSAction(host, "curl", ["-sf", f"{_backend_url()}/health"])]

    return [OSAction(host, "echo", [f"runtime-probe:{runtime_id}"])]


def _compile_resource(
    host: HostPlatform,
    parsed,
    *,
    config: dict[str, str] | None = None,
) -> list[OSAction]:
    from nlp2uri.host.resource import build_resource_actions

    uri = f"resource://{parsed.netloc}{parsed.path}"
    if parsed.query:
        uri = f"{uri}?{parsed.query}"
    return build_resource_actions(uri, host, config=config)


def _compile_artifact(
    host: HostPlatform,
    parsed,
    *,
    config: dict[str, str] | None = None,
) -> list[OSAction]:
    from nlp2uri.host.artifact import build_artifact_actions

    uri = f"artifact://{parsed.netloc}{parsed.path}"
    if parsed.query:
        uri = f"{uri}?{parsed.query}"
    return build_artifact_actions(uri, host, config=config)


def _compile_access(host: HostPlatform, parsed) -> list[OSAction]:
    agent = _decode_segment(parsed.netloc)
    area = _decode_segment(parsed.path.lstrip("/").split("/", 1)[0] if parsed.path else "")
    return [OSAction(host, "echo", [f"access:{agent}:{area}"])]


def _compile_metadata(host: HostPlatform, scheme: str, parsed) -> list[OSAction]:
    target = _decode_segment(parsed.netloc)
    suffix = _decode_segment(parsed.path.lstrip("/"))
    label = f"{target}/{suffix}" if suffix else target
    return [OSAction(host, "echo", [f"{scheme}:{label}"])]
