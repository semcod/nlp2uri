"""Tests for Koru control plan execution."""

from __future__ import annotations

from nlp2uri.control_compile import compile_uri_to_control_plan
from nlp2uri.control_execute import (
    compile_and_execute_control_uri,
    execute_control_action,
    execute_control_plan,
)
from nlp2uri.models import ControlAction, ControlPlan, ControlVerification
from nlp2uri.parse_nl import parse_text
from nlp2uri.resolve import resolve_text
from nlp2uri.models import HostPlatform, IntentKind


class _FakeClient:
    def __init__(self, *, running: bool = True, drive_ok: bool = True) -> None:
        self.running = running
        self.drive_ok = drive_ok
        self.drive_calls: list[dict] = []

    def is_running(self) -> bool:
        return self.running

    def drive(self, text: str, **kwargs) -> dict:
        self.drive_calls.append({"text": text, **kwargs})
        return {"ok": self.drive_ok, "backend": "plugin", "message": text}

    def status(self) -> dict:
        return {"ok": True, "plugins": [{"ide": "cursor", "version": "0.2.34"}]}


def test_execute_control_action_dry_run():
    action = ControlAction(
        surface="ide_chat",
        transport="koruide_socket",
        operation="drive",
        ide="cursor",
        text_ref="hello",
    )
    result = execute_control_action(action, dry_run=True)
    assert result.ok is True
    assert result.dry_run is True
    assert result.verification_status == "planned"


def test_execute_control_action_via_fake_client():
    plan = compile_uri_to_control_plan(
        "ide-chat://cursor/send?submit=true&require_plugin=true",
        text="probe",
    )
    assert plan is not None
    results = execute_control_plan(
        plan,
        client_factory=lambda: _FakeClient(),
    )
    assert len(results) == 1
    assert results[0].ok is True
    assert results[0].backend == "koruide_socket"
    assert results[0].verification_status == "verified"


def test_execute_control_drive_missing_text_blocked():
    action = ControlAction(
        surface="ide_chat",
        transport="koruide_socket",
        operation="drive",
        ide="cursor",
    )
    result = execute_control_action(action, dry_run=False)
    assert result.ok is False
    assert result.verification_status == "blocked_missing_text"


def test_compile_and_execute_control_uri_dry_run():
    payload = compile_and_execute_control_uri(
        "koru-control://ide/status?ide=cursor",
        dry_run=True,
    )
    assert payload["ok"] is True
    assert payload["plan"]["actions"][0]["operation"] == "status"


def test_parse_ide_command_intent():
    intent = parse_text("run command workbench.action.chat.submit in cursor")
    assert intent.kind == IntentKind.IDE_COMMAND
    assert intent.params["command"] == "workbench.action.chat.submit"
    assert intent.params["ide"] == "cursor"


def test_resolve_ide_command_uri():
    spec = resolve_text("execute submit in windsurf", platform=HostPlatform.LINUX)
    assert spec.scheme == "ide-command"
    assert "capability=submit" in spec.uri or "command=submit" in spec.uri
