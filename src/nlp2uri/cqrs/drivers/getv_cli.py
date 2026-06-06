"""getv:// driver — getv CLI compile."""

from __future__ import annotations

from typing import Any

from nlp2uri.cqrs.base import CompileResult, UriDriver
from nlp2uri.models import HostPlatform
from nlp2uri.systemmap.getv_uri import compile_getv_uri


class GetvCliDriver(UriDriver):
    scheme = "getv"
    target = "getv_cli"

    def compile(
        self,
        uri: str,
        *,
        platform: HostPlatform,
        config: dict[str, Any] | None = None,
    ) -> CompileResult:
        try:
            actions = compile_getv_uri(uri, platform)
            return CompileResult(ok=True, uri=uri, actions=actions)
        except Exception as exc:
            return CompileResult(ok=False, uri=uri, error=str(exc))
