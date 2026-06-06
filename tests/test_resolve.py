"""Tests for NL → URI resolution."""

from __future__ import annotations

import pytest

from nlp2uri.models import HostPlatform
from nlp2uri.parse_nl import parse_text
from nlp2uri.resolve import nlp2uri, resolve_text


@pytest.mark.parametrize(
    ("text", "expected_uri_prefix", "expected_action"),
    [
        ("open firefox", "app://firefox/open", "open"),
        ("open https://example.com", "https://example.com", "navigate"),
        ("open file /tmp/demo.txt", "app://file/open", "open"),
        ("open cursor with project /home/user/proj", "app://cursor/open", "open"),
        ("screenshot window titled Terminal", "desktop-screenshot://window", "capture"),
        ("capture screen", "desktop-screenshot://screen", "capture"),
        ("focus firefox", "desktop-window://focus", "focus"),
        ("open settings", "app://settings/open", "open"),
    ],
)
def test_resolve_linux(text, expected_uri_prefix, expected_action):
    spec = resolve_text(text, platform=HostPlatform.LINUX)
    assert spec.uri.startswith(expected_uri_prefix)
    assert spec.action == expected_action


def test_polish_open_vscode_in_folder():
    spec = resolve_text(
        "otwórz VS Code w folderze ~/github/semcod/nlp2uri",
        platform=HostPlatform.LINUX,
    )
    assert spec.uri.startswith("app://vscode/open")
    assert "path=" in spec.uri


def test_polish_active_browser_screenshot():
    spec = resolve_text(
        "zrób screenshot aktywnego okna przeglądarki",
        platform=HostPlatform.LINUX,
    )
    assert spec.uri.startswith("desktop-screenshot://window")
    assert "mode=active" in spec.uri


def test_nlp2uri_returns_actions():
    result = nlp2uri("open firefox", os=HostPlatform.LINUX)
    assert result.intent == "open_app"
    assert result.slots["app"] == "firefox"
    assert len(result.actions) >= 1
    assert result.actions[0].os == HostPlatform.LINUX


def test_parse_absolute_uri_passthrough():
    intent = parse_text("cursor://file/tmp/x")
    spec = resolve_text("cursor://file/tmp/x", platform=HostPlatform.LINUX)
    assert intent.target == "cursor://file/tmp/x"
    assert spec.uri == "cursor://file/tmp/x"


def test_settings_windows():
    spec = resolve_text("open settings", platform=HostPlatform.WINDOWS)
    assert spec.uri == "ms-settings:"


def test_settings_macos():
    spec = resolve_text("open settings", platform=HostPlatform.MACOS)
    assert spec.uri == "x-apple.systempreferences:"


def test_empty_input_raises():
    with pytest.raises(ValueError):
        parse_text("   ")
