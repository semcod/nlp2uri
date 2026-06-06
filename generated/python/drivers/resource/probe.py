"""Auto-generated driver stub — implement compile/execute/probe."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DriverContext:
    scheme: str
    target: str
    platform: str
    dry_run: bool = True


class ResourceProbeDriver:
    """Driver for `resource://` on target `probe`."""

    scheme = "resource"
    target = "probe"

    def capabilities(self) -> dict[str, Any]:
        return {
            "scheme": self.scheme,
            "target": self.target,
            "supports_compile": True,
            "supports_execute": True,
            "supports_probe": True,
        }

    def compile(self, uri: str, *, config: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        raise NotImplementedError(f"{self.__class__.__name__}.compile({uri!r})")

    def execute(self, uri: str, actions: list[dict[str, Any]], *, config: dict[str, Any] | None = None) -> dict[str, Any]:
        raise NotImplementedError(f"{self.__class__.__name__}.execute({uri!r})")

    def probe(self, uri: str) -> dict[str, Any]:
        raise NotImplementedError(f"{self.__class__.__name__}.probe({uri!r})")
