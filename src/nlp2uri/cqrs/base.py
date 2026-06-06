"""Driver protocol for uri_cqrs_es.v1."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from nlp2uri.models import HostPlatform, OSAction


@dataclass(frozen=True)
class DriverCapabilities:
    scheme: str
    target: str
    supports_compile: bool = True
    supports_execute: bool = True
    supports_probe: bool = False
    operations: tuple[str, ...] = ("compile", "execute")


@dataclass
class CompileResult:
    ok: bool
    uri: str
    actions: list[OSAction] = field(default_factory=list)
    error: str = ""


@dataclass
class ExecuteResult:
    ok: bool
    uri: str
    exit_code: int = 0
    output: str = ""
    error: str = ""


@dataclass
class ProbeResult:
    reachable: bool
    status: str = ""
    details: dict[str, str] = field(default_factory=dict)


class UriDriver(ABC):
    scheme: str
    target: str

    def capabilities(self) -> DriverCapabilities:
        return DriverCapabilities(
            scheme=self.scheme,
            target=self.target,
            supports_probe=hasattr(self, "probe") and type(self).probe is not UriDriver.probe,
        )

    @abstractmethod
    def compile(
        self,
        uri: str,
        *,
        platform: HostPlatform,
        config: dict[str, Any] | None = None,
    ) -> CompileResult:
        raise NotImplementedError

    def execute(
        self,
        uri: str,
        actions: list[OSAction],
        *,
        dry_run: bool = True,
        config: dict[str, Any] | None = None,
    ) -> ExecuteResult:
        if dry_run:
            lines = [" ".join(a.argv()) for a in actions]
            return ExecuteResult(ok=True, uri=uri, output="\n".join(lines))
        import subprocess

        outputs: list[str] = []
        last_code = 0
        for action in actions:
            proc = subprocess.run(action.argv(), capture_output=True, text=True, check=False)
            last_code = proc.returncode
            outputs.append(proc.stdout or proc.stderr or "")
            if last_code != 0:
                return ExecuteResult(
                    ok=False,
                    uri=uri,
                    exit_code=last_code,
                    output="\n".join(outputs),
                    error=proc.stderr or f"exit {last_code}",
                )
        return ExecuteResult(ok=True, uri=uri, exit_code=last_code, output="\n".join(outputs))

    def probe(self, uri: str, *, platform: HostPlatform) -> ProbeResult:
        return ProbeResult(reachable=False, status="probe not implemented")
