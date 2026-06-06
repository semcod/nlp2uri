"""endpoint:// driver — TCP/HTTP endpoint health via curl."""

from __future__ import annotations

from typing import Any
from nlp2uri.cqrs.base import CompileResult, ProbeResult, UriDriver
from nlp2uri.host.endpoint import build_endpoint_actions, build_endpoint_url, is_endpoint_uri
from nlp2uri.models import HostPlatform


class EndpointCurlDriver(UriDriver):
    scheme = "endpoint"
    target = "curl"

    def compile(
        self,
        uri: str,
        *,
        platform: HostPlatform,
        config: dict[str, Any] | None = None,
    ) -> CompileResult:
        try:
            actions = build_endpoint_actions(uri, platform)
            return CompileResult(ok=True, uri=uri, actions=actions)
        except Exception as exc:
            return CompileResult(ok=False, uri=uri, error=str(exc))

    def probe(self, uri: str, *, platform: HostPlatform) -> ProbeResult:
        result = self.compile(uri, platform=platform)
        if not result.ok:
            return ProbeResult(reachable=False, status="invalid", details={"error": result.error})
        url = build_endpoint_url(uri)
        return ProbeResult(reachable=True, status="configured", details={"url": url})
