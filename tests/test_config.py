"""Config and auto platform detection tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from nlp2uri.config import (
    default_config,
    ensure_config,
    get_effective_platform,
    load_config,
    reset_config_cache,
    save_config,
)
from nlp2uri.models import HostPlatform
from nlp2uri.resolve import resolve_text


def test_auto_platform_detection():
    spec = resolve_text("open firefox")
    assert spec.uri.startswith("app://firefox/open")


def test_config_resolved_platform_auto():
    cfg = default_config()
    assert cfg.platform == "auto"
    assert cfg.resolved_platform() in {
        HostPlatform.LINUX,
        HostPlatform.MACOS,
        HostPlatform.WINDOWS,
    }


def test_env_platform_override(monkeypatch):
    monkeypatch.setenv("NLP2URI_PLATFORM", "darwin")
    reset_config_cache()
    assert get_effective_platform() == HostPlatform.MACOS


def test_save_and_load_yaml(tmp_path, monkeypatch):
    path = tmp_path / "nlp2uri.yaml"
    cfg = default_config()
    cfg.platform = "linux"
    cfg.locale = "pl-PL"
    save_config(cfg, path)
    monkeypatch.setenv("NLP2URI_CONFIG", str(path))
    reset_config_cache()
    loaded = load_config()
    assert loaded.platform == "linux"
    assert loaded.locale == "pl-PL"
    assert path.read_text(encoding="utf-8").startswith("# nlp2uri.yaml")


def test_ensure_config_writes_defaults(tmp_path, monkeypatch):
    path = tmp_path / "fresh.yaml"
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("NLP2URI_CONFIG", raising=False)
    reset_config_cache()
    cfg = ensure_config(path)
    assert path.is_file()
    assert cfg.platform == "auto"
    assert "host_platform:" in path.read_text(encoding="utf-8")
