"""CLI smoke tests."""

from __future__ import annotations

import json

import pytest

from nlp2uri.cli import main


def test_cli_resolve_json(capsys):
    rc = main(["resolve", "open firefox", "--platform", "linux", "--json"])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["uri"].startswith("app://firefox/open")


def test_cli_execute_dry_run(capsys):
    rc = main(
        [
            "execute",
            "capture screen",
            "--platform",
            "linux",
            "--dry-run",
            "--json",
        ]
    )
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["result"]["ok"] is True


def test_cli_version(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])

    assert exc.value.code == 0
    assert "nlp2uri" in capsys.readouterr().out


def test_cli_plan_ide_chat_with_text_flag(capsys):
    rc = main(
        [
            "plan",
            "wyślij prompt do cursor",
            "--text",
            "refaktoruj moduł X",
            "--json",
        ]
    )
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["uri"].startswith("ide-chat://cursor/send")
    assert payload["slots"]["text"] == "refaktoruj moduł X"
    assert payload["control_plan"]["actions"][0]["text_ref"] == "refaktoruj moduł X"


def test_cli_compile_ide_chat_with_text_flag(capsys):
    rc = main(
        [
            "compile",
            "ide-chat://cursor/send?submit=true",
            "--text",
            "hello",
            "--json",
        ]
    )
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["actions"][0]["args"][-1] == "hello"


def test_cli_execute_raw_ide_chat_with_text_flag(capsys):
    rc = main(
        [
            "execute",
            "ide-chat://cursor/send?submit=false",
            "--text",
            "hello raw",
            "--uri-only",
            "--dry-run",
            "--json",
        ]
    )
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["result"]["ok"] is True
    assert "--no-submit" in payload["actions"][0]["argv"]
    assert payload["actions"][0]["args"][-1] == "hello raw"
