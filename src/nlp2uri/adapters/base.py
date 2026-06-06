"""Base adapter protocol."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from nlp2uri.models import HostPlatform
from nlp2uri.config import load_config
from nlp2uri.service import NLP2URIService


@dataclass
class AdapterRequest:
    operation: str
    prompt: str = ""
    uri: str = ""
    platform: HostPlatform | None = None
    dry_run: bool = False
    locale: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class AdapterResponse:
    ok: bool
    data: dict[str, Any] = field(default_factory=dict)
    error: str = ""
    status_code: int = 200

    def to_dict(self) -> dict[str, Any]:
        payload = dict(self.data)
        if self.error:
            payload["error"] = self.error
        payload["ok"] = self.ok
        return payload


class BaseAdapter(ABC):
    name: str = "base"

    def __init__(self, service: NLP2URIService | None = None) -> None:
        self.service = service or NLP2URIService(config=load_config())

    def with_platform(self, platform: HostPlatform | str | None) -> BaseAdapter:
        if platform is None:
            return self
        clone = self.__class__(NLP2URIService.for_platform(platform))
        return clone

    @abstractmethod
    def handle(self, request: AdapterRequest) -> AdapterResponse:
        raise NotImplementedError

    def _service_for(self, request: AdapterRequest) -> NLP2URIService:
        if request.platform is None:
            return self.service
        return NLP2URIService.for_platform(request.platform)
