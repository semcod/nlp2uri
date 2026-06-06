"""CQRS dispatcher — compile/execute with event append."""

from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

import os

from nlp2uri.cqrs.event_store import InMemoryEventStore
from nlp2uri.cqrs.http_store import HttpEventStore
from nlp2uri.cqrs.registry import DriverRegistry, default_registry
from nlp2uri.models import HostPlatform
from nlp2uri.platform_detect import detect_platform


class CqrsDispatcher:
    def __init__(
        self,
        *,
        registry: DriverRegistry | None = None,
        event_store: InMemoryEventStore | None = None,
        platform: HostPlatform | None = None,
    ) -> None:
        self.registry = registry or default_registry()
        if event_store is not None:
            self.events = event_store
        elif os.getenv("PROCESS_REGISTRY_URL"):
            self.events = HttpEventStore()
        else:
            self.events = InMemoryEventStore()
        self.platform = platform or detect_platform()

    def compile_uri(
        self,
        uri: str,
        *,
        target: str | None = None,
        config: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        scheme = urlparse(uri).scheme.lower()
        driver = self.registry.driver_for_uri(uri, target)
        result = driver.compile(uri, platform=self.platform, config=config)

        self.events.append(
            uri,
            scheme=scheme,
            event_type="UriCompiled" if result.ok else "UriCompileFailed",
            payload={
                "uri": uri,
                "driver": f"{driver.scheme}/{driver.target}",
                "ok": result.ok,
                "actions": [a.to_dict() for a in result.actions],
                "error": result.error,
            },
        )
        return {
            "ok": result.ok,
            "uri": uri,
            "driver": f"{driver.scheme}/{driver.target}",
            "actions": [a.to_dict() for a in result.actions],
            "error": result.error,
        }

    def execute_uri(
        self,
        uri: str,
        *,
        target: str | None = None,
        dry_run: bool = True,
        config: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        compiled = self.compile_uri(uri, target=target, config=config)
        if not compiled["ok"]:
            return compiled

        driver = self.registry.driver_for_uri(uri, target)
        from nlp2uri.models import OSAction

        actions = [
            OSAction(HostPlatform(a["os"]), a["command"], list(a.get("args", [])))
            for a in compiled["actions"]
        ]
        result = driver.execute(uri, actions, dry_run=dry_run, config=config)
        scheme = urlparse(uri).scheme.lower()

        self.events.append(
            uri,
            scheme=scheme,
            event_type="UriExecuted" if result.ok else "UriExecutionFailed",
            payload={
                "uri": uri,
                "dry_run": dry_run,
                "ok": result.ok,
                "exit_code": result.exit_code,
                "output": result.output,
                "error": result.error,
            },
        )
        return {
            "ok": result.ok,
            "uri": uri,
            "dry_run": dry_run,
            "exit_code": result.exit_code,
            "output": result.output,
            "error": result.error,
        }

    def probe_uri(self, uri: str, *, target: str | None = None) -> dict[str, Any]:
        driver = self.registry.driver_for_uri(uri, target)
        result = driver.probe(uri, platform=self.platform)
        return {
            "uri": uri,
            "reachable": result.reachable,
            "status": result.status,
            "details": result.details,
        }
