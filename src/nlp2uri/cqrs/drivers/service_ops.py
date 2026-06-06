"""service:// driver — health/restart for generated microservices."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

from nlp2uri.cqrs.base import CompileResult, ProbeResult, UriDriver
from nlp2uri.models import HostPlatform, OSAction

# Todomat compose service name → host health URL (when ports are exposed).
_TODOMAT_HEALTH: dict[str, str] = {
    "process-registry": "http://localhost:8083/health",
    "trigger-gateway": "http://localhost:8084/health",
    "pipeline-router": "http://localhost:9099/health",
    "nlp2uri-adapter": "http://localhost:8086/health",
}


def parse_service_name(uri: str) -> str:
    parsed = urlparse(uri)
    suffix = unquote(parsed.path.lstrip("/"))
    netloc = unquote(parsed.netloc)
    if netloc == "generated" and suffix:
        return suffix
    return f"{netloc}/{suffix}" if suffix else netloc


def _compose_dir(config: dict[str, Any] | None) -> Path:
    raw = (config or {}).get("compose_dir") or os.environ.get(
        "TODOMAT_COMPOSE_DIR", os.path.expanduser("~/github/wronai/todomat")
    )
    return Path(raw).expanduser()


class ServiceCurlDriver(UriDriver):
    scheme = "service"
    target = "curl"

    def compile(
        self,
        uri: str,
        *,
        platform: HostPlatform,
        config: dict[str, Any] | None = None,
    ) -> CompileResult:
        name = parse_service_name(uri)
        health = (config or {}).get("health_url") or _TODOMAT_HEALTH.get(name)
        if health:
            return CompileResult(ok=True, uri=uri, actions=[OSAction(platform, "curl", ["-sf", health])])
        from nlp2uri.systemmap.compile import compile_system_map_uri

        try:
            actions = compile_system_map_uri(uri, platform, config=config)
            return CompileResult(ok=True, uri=uri, actions=actions)
        except Exception as exc:
            return CompileResult(ok=False, uri=uri, error=str(exc))

    def probe(self, uri: str, *, platform: HostPlatform) -> ProbeResult:
        name = parse_service_name(uri)
        health = _TODOMAT_HEALTH.get(name)
        if health:
            return ProbeResult(reachable=True, status="health_configured", details={"url": health, "name": name})
        return ProbeResult(reachable=True, status="metadata_only", details={"name": name})


class ServiceDockerDriver(UriDriver):
    scheme = "service"
    target = "docker"

    def compile(
        self,
        uri: str,
        *,
        platform: HostPlatform,
        config: dict[str, Any] | None = None,
    ) -> CompileResult:
        name = parse_service_name(uri)
        compose = _compose_dir(config)
        compose_file = compose / "docker-compose.yml"
        if not compose_file.is_file():
            return CompileResult(ok=False, uri=uri, error=f"compose file not found: {compose_file}")
        return CompileResult(
            ok=True,
            uri=uri,
            actions=[
                OSAction(
                    platform,
                    "docker",
                    ["compose", "-f", str(compose_file), "ps", name, "--status", "running", "-q"],
                )
            ],
        )

    def probe(self, uri: str, *, platform: HostPlatform) -> ProbeResult:
        name = parse_service_name(uri)
        compose = _compose_dir(None)
        return ProbeResult(
            reachable=compose.joinpath("docker-compose.yml").is_file(),
            status="compose_ready",
            details={"name": name, "compose_dir": str(compose)},
        )


class ServiceSystemdDriver(UriDriver):
    scheme = "service"
    target = "systemd"

    def compile(
        self,
        uri: str,
        *,
        platform: HostPlatform,
        config: dict[str, Any] | None = None,
    ) -> CompileResult:
        name = parse_service_name(uri)
        unit = (config or {}).get("unit") or f"{name}.service"
        return CompileResult(
            ok=True,
            uri=uri,
            actions=[OSAction(platform, "systemctl", ["is-active", unit])],
        )

    def probe(self, uri: str, *, platform: HostPlatform) -> ProbeResult:
        name = parse_service_name(uri)
        return ProbeResult(reachable=True, status="unit_probe", details={"unit": f"{name}.service"})
