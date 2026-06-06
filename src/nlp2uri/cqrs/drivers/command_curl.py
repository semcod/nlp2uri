"""command:// driver — NLP2DSL workflow handoff via curl."""

from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

from nlp2uri.cqrs.base import CompileResult, ProbeResult, UriDriver
from nlp2uri.models import HostPlatform
from nlp2uri.systemmap.compile import compile_system_map_uri


class CommandCurlDriver(UriDriver):
    scheme = "command"
    target = "curl"

    def compile(
        self,
        uri: str,
        *,
        platform: HostPlatform,
        config: dict[str, Any] | None = None,
    ) -> CompileResult:
        try:
            cfg = {k: str(v) for k, v in (config or {}).items()}
            actions = compile_system_map_uri(uri, platform, config=cfg or None)
            return CompileResult(ok=True, uri=uri, actions=actions)
        except Exception as exc:
            return CompileResult(ok=False, uri=uri, error=str(exc))

    def probe(self, uri: str, *, platform: HostPlatform) -> ProbeResult:
        import os

        backend = os.environ.get("NLP2DSL_BACKEND_URL", "http://localhost:8010").rstrip("/")
        return ProbeResult(
            reachable=True,
            status="handoff",
            details={"backend": backend, "uri": uri},
        )
