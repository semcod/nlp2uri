"""resource:// driver — connector probes."""

from __future__ import annotations

from typing import Any

from nlp2uri.cqrs.base import CompileResult, ProbeResult, UriDriver
from nlp2uri.host.resource import build_resource_actions
from nlp2uri.models import HostPlatform


class ResourceProbeDriver(UriDriver):
    scheme = "resource"
    target = "probe"

    def compile(
        self,
        uri: str,
        *,
        platform: HostPlatform,
        config: dict[str, Any] | None = None,
    ) -> CompileResult:
        try:
            cfg = {k: str(v) for k, v in (config or {}).items()}
            actions = build_resource_actions(uri, platform, config=cfg or None)
            return CompileResult(ok=True, uri=uri, actions=actions)
        except Exception as exc:
            return CompileResult(ok=False, uri=uri, error=str(exc))

    def probe(self, uri: str, *, platform: HostPlatform) -> ProbeResult:
        result = self.compile(uri, platform=platform)
        if not result.ok:
            return ProbeResult(reachable=False, status="compile_failed", details={"error": result.error})
        cmd = " ".join(result.actions[0].argv()) if result.actions else ""
        return ProbeResult(reachable=True, status="probe_ready", details={"command": cmd})
