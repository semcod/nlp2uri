"""artifact:// driver — filesystem read/open/stat."""

from __future__ import annotations

from typing import Any

from nlp2uri.cqrs.base import CompileResult, UriDriver
from nlp2uri.host.artifact import build_artifact_actions
from nlp2uri.models import HostPlatform
from nlp2uri.systemmap.compile import compile_system_map_uri


class ArtifactFilesystemDriver(UriDriver):
    scheme = "artifact"
    target = "filesystem"

    def compile(
        self,
        uri: str,
        *,
        platform: HostPlatform,
        config: dict[str, Any] | None = None,
    ) -> CompileResult:
        try:
            cfg = {k: str(v) for k, v in (config or {}).items()}
            try:
                actions = build_artifact_actions(uri, platform, config=cfg or None)
            except (ValueError, FileNotFoundError):
                actions = compile_system_map_uri(uri, platform, config=cfg or None)
            return CompileResult(ok=True, uri=uri, actions=actions)
        except Exception as exc:
            return CompileResult(ok=False, uri=uri, error=str(exc))
