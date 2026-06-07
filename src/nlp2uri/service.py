"""Core service facade — single entry point for all adapters."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from nlp2uri.compile import compile_uri_to_actions
from nlp2uri.config import NLP2URIConfig, ensure_config, get_effective_platform, load_config
from nlp2uri.control_compile import is_control_uri
from nlp2uri.models import ActionResult, HostPlatform, NLP2URIResult, OSAction, UriSpec
from nlp2uri.resolve import nlp2uri, resolve_text
from nlp2uri.runtime import execute_uri
from nlp2uri.systemmap.fallback import resolve_prompt_with_fallback
from nlp2uri.systemmap.getv_uri import (
    build_getv_uri_index,
    get_getv_var_value,
    resolve_prompt_against_getv,
)
from nlp2uri.systemmap.index import UriMap, build_uri_index


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

    def from_prompt(
        self,
        prompt: str,
        *,
        locale: str | None = None,
        text: str | None = None,
    ) -> NLP2URIResult:
        loc = locale or self._cfg().locale
        return nlp2uri(prompt, os=self._host(), locale=loc, text=text)

    def resolve(self, prompt: str, *, text: str | None = None) -> UriSpec:
        spec = resolve_text(prompt, platform=self._host())
        payload_text = (text or "").strip()
        if payload_text:
            metadata = dict(spec.metadata)
            metadata["text"] = payload_text
            return UriSpec(
                uri=spec.uri,
                scheme=spec.scheme,
                action=spec.action,
                platform_hints=spec.platform_hints,
                metadata=metadata,
                intent=spec.intent,
            )
        return spec

    def compile(self, uri: str, *, text: str | None = None) -> list[OSAction]:
        extra_params = {"text": text} if (text or "").strip() else None
        return compile_uri_to_actions(uri, self._host(), extra_params=extra_params)

    def execute(
        self,
        uri: str,
        *,
        dry_run: bool | None = None,
        extra_params: dict[str, str] | None = None,
    ) -> ActionResult:
        run_dry = self._cfg().dry_run if dry_run is None else dry_run
        return execute_uri(
            uri,
            platform=self._host(),
            dry_run=run_dry,
            extra_params=extra_params,
        )

    def handle_prompt(
        self,
        prompt: str,
        *,
        dry_run: bool | None = None,
        text: str | None = None,
    ) -> dict[str, Any]:
        plan = self.from_prompt(prompt, text=text)
        run_dry = self._cfg().dry_run if dry_run is None else dry_run
        payload: dict[str, Any] = {
            "prompt": prompt,
            "platform": self._host().value,
            "plan": plan.to_dict(),
        }
        text_ref = (text or "").strip() or plan.spec.metadata.get("text") or plan.slots.get("text") or ""
        if plan.control_plan is not None and is_control_uri(plan.uri):
            from nlp2uri.control_execute import execute_control_plan

            control_results = execute_control_plan(
                plan.control_plan,
                text=text_ref or None,
                dry_run=run_dry,
            )
            payload["control_results"] = [r.to_dict() for r in control_results]
            payload["ok"] = all(r.ok for r in control_results)
            if not run_dry:
                return payload
        result = self.execute(plan.uri, dry_run=run_dry, extra_params={"text": text_ref} if text_ref else None)
        payload["result"] = result.to_dict()
        payload.setdefault("ok", result.ok)
        return payload

    def handle_uri(
        self,
        uri: str,
        *,
        dry_run: bool | None = None,
        text: str | None = None,
    ) -> dict[str, Any]:
        actions = self.compile(uri, text=text)
        extra_params = {"text": text} if (text or "").strip() else None
        result = self.execute(uri, dry_run=dry_run, extra_params=extra_params)
        return {
            "uri": uri,
            "platform": self._host().value,
            "actions": [a.to_dict() for a in actions],
            "result": result.to_dict(),
        }

    def list_koru_ide_uris(
        self,
        status: dict[str, Any],
        *,
        socket_path: str = "",
    ) -> dict[str, Any]:
        from nlp2uri.systemmap.koru_ide import build_koru_ide_uri_index

        index = build_koru_ide_uri_index(status, socket_path=socket_path)
        return {
            "source": "koru.autopilot.status",
            "socket": socket_path,
            "count": len(index.entries),
            **index.to_dict(),
        }

    def list_system_uris(self, ir: Any, *, uri_map: UriMap | None = None) -> dict[str, Any]:
        index = uri_map or build_uri_index(ir)
        return {
            "example_id": index.example_id,
            "format": index.format,
            "count": len(index.entries),
            "entries": [entry.to_dict() for entry in index.entries.values()],
            "by_name": dict(index.by_name),
        }

    def resolve_system_map(
        self,
        prompt: str,
        ir: Any,
        *,
        uri_map: UriMap | None = None,
        fallback_desktop: bool = True,
    ) -> dict[str, Any]:
        if fallback_desktop:
            return resolve_prompt_with_fallback(
                prompt,
                ir,
                uri_map=uri_map,
                platform=self._host(),
            )
        from nlp2uri.systemmap.resolve import resolve_prompt_against_system_map

        index = uri_map or build_uri_index(ir)
        matches = resolve_prompt_against_system_map(prompt, ir, uri_map=index)
        if not matches:
            return {"source": "system_map", "uri": None, "matches": []}
        top = matches[0]
        return {
            "source": "system_map",
            "uri": top.uri,
            "confidence": top.confidence,
            "match_reason": top.match_reason,
            "matches": [item.to_dict() for item in matches],
        }

    def list_getv_uris(self, *, getv_home: str | None = None, uri_map: UriMap | None = None) -> dict[str, Any]:
        index = uri_map or build_getv_uri_index(home=getv_home)
        return {
            "getv_home": index.example_id,
            "format": index.format,
            "count": len(index.entries),
            "entries": [entry.to_dict() for entry in index.entries.values()],
            "by_name": dict(index.by_name),
        }

    def resolve_getv(
        self,
        prompt: str,
        *,
        getv_home: str | None = None,
        uri_map: UriMap | None = None,
    ) -> dict[str, Any]:
        index = uri_map or build_getv_uri_index(home=getv_home)
        matches = resolve_prompt_against_getv(prompt, uri_map=index)
        if not matches:
            return {"source": "getv", "uri": None, "matches": []}
        top = matches[0]
        return {
            "source": "getv",
            "uri": top.uri,
            "confidence": top.confidence,
            "match_reason": top.match_reason,
            "matches": [item.to_dict() for item in matches],
        }

    def read_getv_var(self, uri: str) -> dict[str, Any]:
        return get_getv_var_value(uri)
