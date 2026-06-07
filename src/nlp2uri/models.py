"""Core data models for nlp2uri."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class HostPlatform(str, Enum):
    LINUX = "linux"
    MACOS = "darwin"
    WINDOWS = "windows"
    UNKNOWN = "unknown"


class IntentKind(str, Enum):
    OPEN = "open"
    CAPTURE = "capture"
    FOCUS = "focus"
    MOVE = "move"
    NAVIGATE = "navigate"
    IDE_OPEN = "ide_open"
    IDE_CHAT_SEND = "ide_chat_send"
    IDE_COMMAND = "ide_command"
    IDE_STATUS = "ide_status"
    KORU_CONTROL = "koru_control"


INTENT_NAMES: dict[IntentKind, str] = {
    IntentKind.OPEN: "open_app",
    IntentKind.CAPTURE: "screenshot",
    IntentKind.FOCUS: "focus_window",
    IntentKind.MOVE: "move_window",
    IntentKind.NAVIGATE: "navigate",
    IntentKind.IDE_OPEN: "ide_open",
    IntentKind.IDE_CHAT_SEND: "ide_chat_send",
    IntentKind.IDE_COMMAND: "ide_command",
    IntentKind.IDE_STATUS: "ide_status",
    IntentKind.KORU_CONTROL: "koru_control",
}

CONTROL_COMMAND_VERSION = "koru.control.v1"


@dataclass(frozen=True)
class UriIntent:
    """Structured intent parsed from natural language."""

    kind: IntentKind
    target: str
    params: dict[str, str] = field(default_factory=dict)
    raw_text: str = ""
    confidence: float = 1.0

    def with_params(self, **extra: str) -> UriIntent:
        merged = dict(self.params)
        merged.update({k: v for k, v in extra.items() if v})
        return UriIntent(
            kind=self.kind,
            target=self.target,
            params=merged,
            raw_text=self.raw_text,
            confidence=self.confidence,
        )

    @property
    def intent_name(self) -> str:
        if self.kind == IntentKind.OPEN and self.target == "file":
            return "open_file"
        if self.kind == IntentKind.OPEN and self.target == "settings":
            return "open_settings"
        if self.kind == IntentKind.OPEN and self.target == "terminal":
            return "open_terminal"
        if self.kind == IntentKind.OPEN and self.target == "ide":
            return "open_app"
        return INTENT_NAMES.get(self.kind, self.kind.value)

    def to_slots(self) -> dict[str, Any]:
        slots: dict[str, Any] = {"target": self.target}
        slots.update(self.params)
        if self.kind in {IntentKind.CAPTURE, IntentKind.MOVE}:
            window = {}
            if "title" in self.params:
                window["title"] = self.params["title"]
            if "mode" in self.params:
                window["mode"] = self.params["mode"]
            if "class" in self.params:
                window["class"] = self.params["class"]
            if "screen" in self.params:
                window["screen"] = self.params["screen"]
            if window:
                slots["window"] = window
        if self.kind in {IntentKind.IDE_CHAT_SEND, IntentKind.IDE_STATUS}:
            slots["app"] = self.params.get("ide") or self.target
            if self.params.get("workspace"):
                slots["resource"] = self.params["workspace"]
        if self.target == "ide" or self.params.get("ide"):
            slots["app"] = self.params.get("ide") or self.target
        elif self.params.get("name"):
            slots["app"] = self.params["name"]
        if self.params.get("path"):
            slots["resource"] = self.params["path"]
        return slots


@dataclass(frozen=True)
class UriSpec:
    """Resolved abstract URI ready for execution or MCP handoff."""

    uri: str
    scheme: str
    action: str
    platform_hints: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
    intent: UriIntent | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "uri": self.uri,
            "scheme": self.scheme,
            "action": self.action,
            "platform_hints": list(self.platform_hints),
            "metadata": dict(self.metadata),
            "intent": None
            if self.intent is None
            else {
                "name": self.intent.intent_name,
                "kind": self.intent.kind.value,
                "target": self.intent.target,
                "slots": self.intent.to_slots(),
                "confidence": self.intent.confidence,
            },
        }


@dataclass(frozen=True)
class ControlVerification:
    expect_ack: bool = True
    expect_message_sent: bool = False
    timeout_ms: int = 120_000

    def to_dict(self) -> dict[str, Any]:
        return {
            "expect_ack": self.expect_ack,
            "expect_message_sent": self.expect_message_sent,
            "timeout_ms": self.timeout_ms,
        }


@dataclass(frozen=True)
class ControlAction:
    """Structured Koru control command (koru.control.v1)."""

    surface: str
    transport: str
    operation: str
    ide: str = "auto"
    workspace: str = ""
    submit: bool = True
    require_plugin: bool = False
    strategy_hint: str = ""
    text_ref: str = ""
    verification: ControlVerification = field(default_factory=ControlVerification)
    replay_cli: tuple[str, ...] = ()
    replay_mcp: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    kind: str = "control"
    command_version: str = CONTROL_COMMAND_VERSION

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "kind": self.kind,
            "command_version": self.command_version,
            "surface": self.surface,
            "transport": self.transport,
            "operation": self.operation,
            "ide": self.ide,
            "workspace": self.workspace,
            "submit": self.submit,
            "require_plugin": self.require_plugin,
            "verification": self.verification.to_dict(),
            "replay": {
                "cli": list(self.replay_cli),
                "mcp": self.replay_mcp,
            },
        }
        if self.strategy_hint:
            payload["strategy_hint"] = self.strategy_hint
        if self.text_ref:
            payload["text_ref"] = self.text_ref
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        return payload


@dataclass(frozen=True)
class ControlPlan:
    uri: str
    actions: tuple[ControlAction, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "uri": self.uri,
            "actions": [action.to_dict() for action in self.actions],
        }


@dataclass(frozen=True)
class OSAction:
    """Concrete host command derived from an abstract URI."""

    os: HostPlatform
    command: str
    args: list[str] = field(default_factory=list)

    def argv(self) -> list[str]:
        return [self.command, *self.args]

    def to_dict(self) -> dict[str, Any]:
        return {
            "os": self.os.value,
            "command": self.command,
            "args": list(self.args),
            "argv": self.argv(),
        }


@dataclass(frozen=True)
class NLP2URIResult:
    """Full compiler output: NL → URI + OS action plan."""

    uri: str
    intent: str
    slots: dict[str, Any]
    spec: UriSpec
    actions: tuple[OSAction, ...] = ()
    control_plan: ControlPlan | None = None

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "uri": self.uri,
            "intent": self.intent,
            "slots": dict(self.slots),
            "spec": self.spec.to_dict(),
            "actions": [a.to_dict() for a in self.actions],
        }
        if self.control_plan is not None:
            payload["control_plan"] = self.control_plan.to_dict()
        return payload


@dataclass
class ActionResult:
    ok: bool
    uri: str
    output: str = ""
    error: str = ""
    returncode: int = 0
    platform: HostPlatform = HostPlatform.UNKNOWN
    actions: tuple[OSAction, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "uri": self.uri,
            "output": self.output,
            "error": self.error,
            "returncode": self.returncode,
            "platform": self.platform.value,
            "actions": [a.to_dict() for a in self.actions],
        }
