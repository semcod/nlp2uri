"""HTTP event store — append CQRS events to todomat process-registry."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

from nlp2uri.cqrs.event_store import InMemoryEventStore, StoredEvent


class HttpEventStore(InMemoryEventStore):
    """In-memory store with async-safe HTTP mirror to process-registry /events."""

    def __init__(self, base_url: str | None = None) -> None:
        super().__init__()
        self.base_url = (base_url or os.getenv("PROCESS_REGISTRY_URL", "")).rstrip("/")

    def append(
        self,
        aggregate_id: str,
        *,
        scheme: str,
        event_type: str,
        payload: dict[str, Any] | None = None,
    ) -> StoredEvent:
        event = super().append(
            aggregate_id,
            scheme=scheme,
            event_type=event_type,
            payload=payload,
        )
        if self.base_url:
            self._post_remote(event)
        return event

    def _post_remote(self, event: StoredEvent) -> None:
        body = json.dumps(event.to_dict()).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/events",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=5.0) as resp:
                if resp.status >= 400:
                    pass
        except (urllib.error.URLError, TimeoutError):
            pass
