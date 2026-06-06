"""Core service facade — single entry point for all adapters."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from nlp2uri.compile import compile_uri_to_actions
from nlp2uri.config import NLP2URIConfig, ensure_config, get_effective_platform, load_config
from nlp2uri.models import ActionResult, HostPlatform, NLP2URIResult, OSAction, UriSpec
from nlp2uri.resolve import nlp2uri, resolve_text
from nlp2uri.runtime import execute_uri


@dataclass
class NLP2URIService:
    """Reusable facade: prompt → URI → compile → execute."""

    platform: HostPlatform | None = None
    config: NLP2URIConfig | None = field(default=None, repr=False)

    @classmethod
    def default(cls) -> NLP2URIService:
        cfg = ensure_config()
        return cls(config=cfg)

    @classmethod
    def for_platform(cls, platform: HostPlatform | str) -> NLP2URIService:
        if isinstance(platform, str):
            platform = HostPlatform(platform)
        return cls(platform=platform, config=load_config())

    def _cfg(self) -> NLP2URIConfig:
        return self.config or load_config()

    def _host(self) -> HostPlatform:
        return get_effective_platform(self.platform)

    def from_prompt(self, prompt: str, *, locale: str | None = None) -> NLP2URIResult:
        loc = locale or self._cfg().locale
        return nlp2uri(prompt, os=self._host(), locale=loc)

    def resolve(self, prompt: str) -> UriSpec:
        return resolve_text(prompt, platform=self._host())

    def compile(self, uri: str) -> list[OSAction]:
        return compile_uri_to_actions(uri, self._host())

    def execute(self, uri: str, *, dry_run: bool | None = None) -> ActionResult:
        run_dry = self._cfg().dry_run if dry_run is None else dry_run
        return execute_uri(uri, platform=self._host(), dry_run=run_dry)

    def handle_prompt(self, prompt: str, *, dry_run: bool | None = None) -> dict[str, Any]:
        plan = self.from_prompt(prompt)
        result = self.execute(plan.uri, dry_run=dry_run)
        return {
            "prompt": prompt,
            "platform": self._host().value,
            "plan": plan.to_dict(),
            "result": result.to_dict(),
        }

    def handle_uri(self, uri: str, *, dry_run: bool | None = None) -> dict[str, Any]:
        actions = self.compile(uri)
        result = self.execute(uri, dry_run=dry_run)
        return {
            "uri": uri,
            "platform": self._host().value,
            "actions": [a.to_dict() for a in actions],
            "result": result.to_dict(),
        }
