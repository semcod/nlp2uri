"""Isolate nlp2uri.yaml per test run."""

from __future__ import annotations

import pytest

from nlp2uri.config import default_config, reset_config_cache, save_config


@pytest.fixture(autouse=True)
def isolated_config(tmp_path, monkeypatch):
    path = tmp_path / "nlp2uri.yaml"
    save_config(default_config(), path)
    monkeypatch.setenv("NLP2URI_CONFIG", str(path))
    reset_config_cache()
    yield
    reset_config_cache()
