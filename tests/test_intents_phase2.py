"""Phase 2 NL intents: terminal, window move, settings panel, capture extensions."""

from __future__ import annotations

import pytest

from nlp2uri.compile import compile_uri_to_actions
from nlp2uri.models import HostPlatform
from nlp2uri.parse_nl import parse_text
from nlp2uri.resolve import resolve_text


@pytest.mark.parametrize(
    ("text", "expected_uri_prefix", "expected_action"),
    [
        ("open terminal in folder ~/proj", "app://terminal/open", "open"),
        ("otwórz terminal w folderze /tmp", "app://terminal/open", "open"),
        (
            "move window Slack to second monitor",
            "desktop-window://move",
            "move",
        ),
        (
            "przenieś okno Firefox na drugi monitor",
            "desktop-window://move",
            "move",
        ),
        ("open network settings", "app://settings/network", "open"),
        ("otwórz ustawienia sieci", "app://settings/network", "open"),
        (
            "zrób screenshot okna Edge",
            "desktop-screenshot://window",
            "capture",
        ),
    ],
)
def test_phase2_resolve_linux(text, expected_uri_prefix, expected_action):
    spec = resolve_text(text, platform=HostPlatform.LINUX)
    assert spec.uri.startswith(expected_uri_prefix)
    assert spec.action == expected_action


def test_terminal_path_in_uri():
    spec = resolve_text(
        "open terminal in folder ~/github/semcod/nlp2uri",
        platform=HostPlatform.LINUX,
    )
    assert "path=" in spec.uri


def test_window_move_screen_param():
    spec = resolve_text(
        "move window Slack to second monitor",
        platform=HostPlatform.LINUX,
    )
    assert "title=Slack" in spec.uri
    assert "screen=1" in spec.uri


def test_settings_panel_windows():
    spec = resolve_text("open wifi settings", platform=HostPlatform.WINDOWS)
    assert spec.uri == "ms-settings:network-wifi"


def test_settings_panel_macos():
    spec = resolve_text("open display settings", platform=HostPlatform.MACOS)
    assert spec.uri.startswith("x-apple.systempreferences:")


def test_polish_cursor_project_regression():
    spec = resolve_text(
        "otwórz Cursor z projektem ~/github/semcod/nlp2uri",
        platform=HostPlatform.LINUX,
    )
    assert spec.uri.startswith("app://cursor/open")
    assert "path=" in spec.uri


def test_capture_window_edge_title():
    intent = parse_text("zrób screenshot okna Edge")
    assert intent.kind.value == "capture"
    assert intent.params.get("title") == "Edge"


def test_compile_window_move_dry_run_linux():
    actions = compile_uri_to_actions(
        "desktop-window://move?title=Slack&screen=1",
        HostPlatform.LINUX,
    )
    assert len(actions) == 1
    assert actions[0].command in {"bash", "wmctrl", "echo", "xdotool"}


def test_compile_terminal_linux():
    actions = compile_uri_to_actions(
        "app://terminal/open?path=/tmp",
        HostPlatform.LINUX,
    )
    assert len(actions) == 1
    assert actions[0].command in {
        "gnome-terminal",
        "konsole",
        "alacritty",
        "xterm",
        "bash",
    }


def test_compile_settings_panel_windows():
    actions = compile_uri_to_actions("app://settings/network", HostPlatform.WINDOWS)
    assert "ms-settings:network" in actions[0].args
