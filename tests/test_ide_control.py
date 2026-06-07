"""Tests for Koru IDE control URIs and koru.control.v1 plans."""

from __future__ import annotations

import pytest

from nlp2uri.compile import compile_uri_to_actions
from nlp2uri.control_compile import compile_uri_to_control_plan, is_control_uri
from nlp2uri.models import CONTROL_COMMAND_VERSION, HostPlatform, IntentKind
from nlp2uri.parse_nl import parse_text
from nlp2uri.resolve import nlp2uri, resolve_text
from nlp2uri.schemes.build import build_uri


def test_parse_ide_chat_send_polish():
    intent = parse_text("wyślij prompt do Cursor w tym projekcie")
    assert intent.kind == IntentKind.IDE_CHAT_SEND
    assert intent.params["ide"] == "cursor"
    assert intent.params.get("workspace") == "."


def test_parse_ide_chat_paste_no_submit():
    intent = parse_text("wklej do Windsurf, ale nie wysyłaj")
    assert intent.kind == IntentKind.IDE_CHAT_SEND
    assert intent.params["ide"] == "windsurf"
    assert intent.params["submit"] == "false"


def test_parse_ide_status():
    intent = parse_text("sprawdź status pluginu Cursor")
    assert intent.kind == IntentKind.IDE_STATUS
    assert intent.params["ide"] == "cursor"


def test_build_ide_chat_uri_without_embedded_text():
    intent = parse_text("send hello to cursor")
    intent = intent.with_params(text="hello world")
    spec = build_uri(intent, platform=HostPlatform.LINUX)
    assert spec.uri.startswith("ide-chat://cursor/send")
    assert "text=" not in spec.uri
    assert spec.metadata.get("text") == "hello world"


def test_control_plan_ide_chat_send():
    uri = (
        "ide-chat://cursor/send?"
        "workspace=/home/tom/github/semcod/koru&submit=true&require_plugin=true"
    )
    plan = compile_uri_to_control_plan(uri, text="probe test")
    assert plan is not None
    assert len(plan.actions) == 1
    action = plan.actions[0]
    assert action.command_version == CONTROL_COMMAND_VERSION
    assert action.surface == "ide_chat"
    assert action.transport == "koruide_socket"
    assert action.operation == "drive"
    assert action.ide == "cursor"
    assert action.require_plugin is True
    assert action.text_ref == "probe test"
    assert action.replay_mcp == "koru_ide_drive"
    assert "koru" in action.replay_cli
    assert action.verification.expect_ack is True
    assert action.verification.expect_message_sent is True
    assert action.strategy_hint == "submit_alt_glass_first"


def test_control_plan_cursor_submit_default_strategy_hint():
    uri = "ide-chat://cursor/send?submit=true"
    plan = compile_uri_to_control_plan(uri, text="hello")
    assert plan is not None
    assert plan.actions[0].strategy_hint == "submit_alt_glass_first"


def test_control_plan_no_strategy_hint_when_no_submit():
    uri = "ide-chat://cursor/send?submit=false"
    plan = compile_uri_to_control_plan(uri, text="hello")
    assert plan is not None
    assert plan.actions[0].strategy_hint == ""


def test_control_plan_koru_control_status():
    uri = "koru-control://ide/status?ide=cursor"
    plan = compile_uri_to_control_plan(uri)
    assert plan is not None
    action = plan.actions[0]
    assert action.operation == "status"
    assert action.ide == "cursor"
    assert action.verification.expect_ack is False


def test_nlp2uri_round_trip_includes_control_plan():
    result = nlp2uri(
        "wyślij test do cursor",
        os=HostPlatform.LINUX,
    )
    assert result.uri.startswith("ide-chat://cursor/send")
    assert result.control_plan is not None
    assert result.control_plan.actions[0].surface == "ide_chat"
    payload = result.to_dict()
    assert "control_plan" in payload


def test_compile_ide_chat_os_action_with_extra_text():
    uri = "ide-chat://cursor/send?workspace=/tmp/koru&submit=true"
    actions = compile_uri_to_actions(
        uri,
        HostPlatform.LINUX,
        extra_params={"text": "hello"},
    )
    assert len(actions) == 1
    assert actions[0].command == "koru"
    assert "drive" in actions[0].args
    assert "--prompt" in actions[0].args
    assert "hello" in actions[0].args


def test_compile_ide_chat_requires_text():
    uri = "ide-chat://cursor/send?workspace=/tmp/koru"
    with pytest.raises(ValueError, match="requires text"):
        compile_uri_to_actions(uri, HostPlatform.LINUX)


def test_is_control_uri():
    assert is_control_uri("ide-chat://cursor/send")
    assert is_control_uri("koru-control://ide/status")
    assert not is_control_uri("app://firefox/open")


def test_resolve_ide_status_uri():
    spec = resolve_text("check status of cursor plugin", platform=HostPlatform.LINUX)
    assert spec.scheme == "koru-control"
    assert spec.action == "status"
