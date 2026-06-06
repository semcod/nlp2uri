"""container:// driver — Docker container inspect, logs, restart, exec."""

from __future__ import annotations

from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

from nlp2uri.cqrs.base import CompileResult, ProbeResult, UriDriver
from nlp2uri.models import HostPlatform, OSAction

_VALID_ACTIONS = frozenset({"status", "logs", "restart", "exec", "inspect", "running"})


def parse_container_uri(uri: str) -> tuple[str, str, str, dict[str, str]]:
    """container://docker/name/action?tail=100 → runtime, name, action, params."""
    parsed = urlparse(uri)
    runtime = unquote(parsed.netloc or "docker")
    parts = [unquote(p) for p in parsed.path.split("/") if p]
    name = parts[0] if parts else ""
    action = parts[1] if len(parts) > 1 else "status"
    params = {k: unquote(v[0]) for k, v in parse_qs(parsed.query).items() if v}
    return runtime, name, action, params


class ContainerDockerDriver(UriDriver):
    scheme = "container"
    target = "docker"

    def compile(
        self,
        uri: str,
        *,
        platform: HostPlatform,
        config: dict[str, Any] | None = None,
    ) -> CompileResult:
        runtime, name, action, params = parse_container_uri(uri)
        if runtime != "docker":
            return CompileResult(ok=False, uri=uri, error=f"unsupported container runtime: {runtime}")
        if not name:
            return CompileResult(ok=False, uri=uri, error="container name required")
        if action not in _VALID_ACTIONS:
            return CompileResult(ok=False, uri=uri, error=f"unsupported action: {action}")

        try:
            argv = self._docker_argv(name, action, params, config)
        except ValueError as exc:
            return CompileResult(ok=False, uri=uri, error=str(exc))
        return CompileResult(ok=True, uri=uri, actions=[OSAction(platform, "docker", argv)])

    def probe(self, uri: str, *, platform: HostPlatform) -> ProbeResult:
        _, name, _, _ = parse_container_uri(uri)
        return ProbeResult(
            reachable=bool(name),
            status="container_ref",
            details={"name": name, "runtime": "docker"},
        )

    @staticmethod
    def _docker_argv(
        name: str,
        action: str,
        params: dict[str, str],
        config: dict[str, Any] | None,
    ) -> list[str]:
        filter_name = (config or {}).get("filter") or name
        if action == "status":
            return ["inspect", "-f", "{{.State.Status}}", filter_name]
        if action == "inspect":
            return ["inspect", filter_name]
        if action == "running":
            return ["ps", "--filter", f"name={filter_name}", "--filter", "status=running", "-q"]
        if action == "logs":
            tail = params.get("tail", (config or {}).get("tail", "100"))
            follow = params.get("follow", "")
            argv = ["logs", "--tail", str(tail)]
            if follow in {"1", "true", "yes"}:
                argv.append("-f")
            argv.append(filter_name)
            return argv
        if action == "restart":
            return ["restart", filter_name]
        if action == "exec":
            cmd = params.get("cmd") or (config or {}).get("cmd")
            if not cmd:
                raise ValueError("container exec requires cmd query param")
            shell = params.get("shell", "sh")
            return ["exec", filter_name, shell, "-c", cmd]
        raise ValueError(f"unsupported action: {action}")
