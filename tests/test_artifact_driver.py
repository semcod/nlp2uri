"""artifact:// driver and path resolution."""

from __future__ import annotations

import tempfile
from pathlib import Path

from nlp2uri.cqrs import CqrsDispatcher
from nlp2uri.host.artifact import build_artifact_actions, resolve_artifact_path
from nlp2uri.models import HostPlatform


def test_resolve_artifact_path_with_example_dir() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        pdf = root / "invoices" / "out.pdf"
        pdf.parent.mkdir(parents=True)
        pdf.write_text("invoice", encoding="utf-8")
        uri = "artifact://01-invoice/invoices/out.pdf"
        resolved = resolve_artifact_path(uri, example_dir=str(root))
        assert resolved == pdf.resolve()


def test_build_artifact_actions_read() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        f = root / "data.txt"
        f.write_text("hello", encoding="utf-8")
        uri = "artifact://demo/data.txt"
        actions = build_artifact_actions(uri, HostPlatform.LINUX, config={"example_dir": str(root)})
        assert actions[0].command == "cat"
        assert str(root / "data.txt") in actions[0].args[0]


def test_build_artifact_actions_open() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        f = root / "doc.pdf"
        f.write_bytes(b"%PDF")
        uri = "artifact://demo/doc.pdf?action=open"
        actions = build_artifact_actions(uri, HostPlatform.LINUX, config={"example_dir": str(root)})
        assert actions[0].command.endswith(("xdg-open", "gio", "gnome-open"))


def test_cqrs_artifact_driver_compile() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "out.txt").write_text("x", encoding="utf-8")
        d = CqrsDispatcher(platform=HostPlatform.LINUX)
        result = d.compile_uri(
            "artifact://ex/out.txt",
            target="filesystem",
            config={"example_dir": str(root)},
        )
        assert result["ok"] is True
        assert result["actions"][0]["command"] == "cat"
