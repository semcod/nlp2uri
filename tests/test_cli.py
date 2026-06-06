"""CLI smoke tests."""

from __future__ import annotations

import json

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
