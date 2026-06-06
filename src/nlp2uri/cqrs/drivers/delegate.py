"""Generic driver — delegates to nlp2uri.compile for desktop schemes."""

from __future__ import annotations

from typing import Any

from nlp2uri.cqrs.base import CompileResult, UriDriver
from nlp2uri.models import HostPlatform


class DelegateCompileDriver(UriDriver):
    def __init__(self, scheme: str, target: str) -> None:
        self.scheme = scheme
        self.target = target

    def compile(
        self,
        uri: str,
        *,
        platform: HostPlatform,
        config: dict[str, Any] | None = None,
    ) -> CompileResult:
        try:
            from nlp2uri.compile import compile_uri_to_actions

            actions = compile_uri_to_actions(uri, os=platform)
            return CompileResult(ok=True, uri=uri, actions=actions)
        except Exception as exc:
            return CompileResult(ok=False, uri=uri, error=str(exc))
