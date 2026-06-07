"""Koru IDE control URI integration."""

from __future__ import annotations

from nlp2uri.compile import compile_uri_to_actions
from nlp2uri.models import HostPlatform, IntentKind
from nlp2uri.parse_nl import parse_text
from nlp2uri.resolve import nlp2uri, resolve_text


def test_parse_polish_send_to_cursor_chat():
    intent = parse_text("wyślij prompt do Cursor w tym projekcie")

    assert intent.kind == IntentKind.IDE_CHAT_SEND
    assert intent.params["ide"] == "cursor"
    assert intent.params["text"] == "prompt"
    assert intent.params["workspace"] == "."


def test_resolve_ide_chat_send_uri():
    spec = resolve_text(
        "send refactor this to Cursor chat",
        platform=HostPlatform.LINUX,
    )

    assert spec.uri.startswith("ide-chat://cursor/send")
    assert "text=" not in spec.uri
    assert spec.action == "send"
    assert spec.metadata["text"] == "refactor this"
    assert spec.metadata["transport"] == "koruide_socket"


def test_compile_ide_chat_to_koru_drive():
    actions = compile_uri_to_actions(
        "ide-chat://cursor/send?submit=true&require_plugin=true&workspace=/home/user/proj",
        HostPlatform.LINUX,
        extra_params={"text": "hello"},
    )

    assert len(actions) == 1
    assert actions[0].command == "koru"
    assert actions[0].argv() == [
        "koru",
        "autopilot",
        "drive",
        "--ide",
        "cursor",
        "--require-plugin",
        "--project",
        "/home/user/proj",
        "--prompt",
        "hello",
    ]


def test_compile_ide_chat_no_submit():
    result = nlp2uri(
        "wklej draft do Windsurf, ale nie wysyłaj",
        os=HostPlatform.LINUX,
    )

    assert result.uri.startswith("ide-chat://windsurf/send")
    assert "--no-submit" in result.actions[0].argv()
    assert result.actions[0].argv()[-1] == "draft"


def test_resolve_and_compile_koru_control_status():
    spec = resolve_text("sprawdź status pluginu Cursor", platform=HostPlatform.LINUX)
    actions = compile_uri_to_actions(spec.uri, HostPlatform.LINUX)

    assert spec.uri == "koru-control://ide/status?ide=cursor"
    assert actions[0].argv() == [
        "koru",
        "autopilot",
        "status",
        "--ide",
        "cursor",
    ]
