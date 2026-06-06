"""In-memory event store for uri_cqrs_es.v1 testing."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


@dataclass
class StoredEvent:
    event_id: str
    aggregate_id: str
    scheme: str
    event_type: str
    sequence: int
    occurred_at: str
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "aggregate_id": self.aggregate_id,
            "scheme": self.scheme,
            "event_type": self.event_type,
            "sequence": self.sequence,
            "occurred_at": self.occurred_at,
            "payload": self.payload,
        }


class InMemoryEventStore:
    def __init__(self) -> None:
        self._streams: dict[str, list[StoredEvent]] = {}
        self._seq: dict[str, int] = {}

    def append(
        self,
        aggregate_id: str,
        *,
        scheme: str,
        event_type: str,
        payload: dict[str, Any] | None = None,
    ) -> StoredEvent:
        seq = self._seq.get(aggregate_id, 0) + 1
        self._seq[aggregate_id] = seq
        event = StoredEvent(
            event_id=uuid4().hex,
            aggregate_id=aggregate_id,
            scheme=scheme,
            event_type=event_type,
            sequence=seq,
            occurred_at=datetime.now(UTC).isoformat(),
            payload=dict(payload or {}),
        )
        self._streams.setdefault(aggregate_id, []).append(event)
        return event

    def get_stream(self, aggregate_id: str, *, from_sequence: int = 0) -> list[StoredEvent]:
        return [e for e in self._streams.get(aggregate_id, []) if e.sequence >= from_sequence]

    def all_events(self) -> list[StoredEvent]:
        out: list[StoredEvent] = []
        for stream in self._streams.values():
            out.extend(stream)
        return sorted(out, key=lambda e: (e.aggregate_id, e.sequence))
