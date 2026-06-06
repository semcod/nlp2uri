"""Linux x-scheme-handler integration (Docker / NLP2URI_INTEGRATION=1)."""

from __future__ import annotations

import os
import shutil
import subprocess
import textwrap
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
HANDLER = ROOT / "scripts" / "testapp-handler.sh"


@pytest.mark.integration
def test_xdg_custom_scheme_handler(tmp_path):
    if os.environ.get("NLP2URI_INTEGRATION") != "1":
        pytest.skip("set NLP2URI_INTEGRATION=1 to run handler integration test")
    if shutil.which("xdg-open") is None:
        pytest.skip("xdg-open not available")

    log_file = tmp_path / "handler.log"
    data_home = tmp_path / ".local" / "share"
    apps_home = data_home / "applications"
    config_home = tmp_path / ".config"
    apps_home.mkdir(parents=True, exist_ok=True)
    config_home.mkdir(parents=True, exist_ok=True)

    handler_copy = tmp_path / "testapp-handler.sh"
    handler_copy.write_text(HANDLER.read_text())
    handler_copy.chmod(0o755)

    desktop = textwrap.dedent(
        f"""\
        [Desktop Entry]
        Type=Application
        Name=NLP2URI Test Handler
        Exec={handler_copy} %u
        MimeType=x-scheme-handler/testapp;
        NoDisplay=true
        """
    )
    (apps_home / "nlp2uri-testapp.desktop").write_text(desktop)

    mimeapps = (
        "[Default Applications]\n"
        "x-scheme-handler/testapp=nlp2uri-testapp.desktop\n"
        "\n"
        "[Added Associations]\n"
        "x-scheme-handler/testapp=nlp2uri-testapp.desktop;\n"
    )
    (apps_home / "mimeapps.list").write_text(mimeapps)
    (config_home / "mimeapps.list").write_text(mimeapps)

    env = os.environ.copy()
    env["HOME"] = str(tmp_path)
    env["XDG_DATA_HOME"] = str(data_home)
    env["XDG_CONFIG_HOME"] = str(config_home)
    env["NLP2URI_HANDLER_LOG"] = str(log_file)

    subprocess.run(
        ["xdg-mime", "default", "nlp2uri-testapp.desktop", "x-scheme-handler/testapp"],
        check=False,
        env=env,
        capture_output=True,
    )
    subprocess.run(
        ["update-desktop-database", str(apps_home)],
        check=False,
        env=env,
        capture_output=True,
    )

    uri = "testapp://something?from=nlp2uri-test"

    # Required: handler contract (simulates x-scheme-handler Exec dispatch)
    direct = subprocess.run(
        [str(handler_copy), uri],
        env=env,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert direct.returncode == 0, direct.stderr
    assert "testapp://something" in log_file.read_text()

    # Best-effort: xdg-open dispatch (needs desktop mime DB; may fail in headless Docker)
    proc = subprocess.run(
        ["xdg-open", uri],
        env=env,
        capture_output=True,
        text=True,
        timeout=10,
    )
    if proc.returncode == 0:
        assert log_file.read_text().count("testapp://something") >= 2
