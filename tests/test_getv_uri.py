"""Tests for getv:// URI layer."""

from __future__ import annotations

from pathlib import Path

import pytest

from nlp2uri.compile import compile_uri_to_actions
from nlp2uri.models import HostPlatform
from nlp2uri.systemmap.getv_uri import (
    build_getv_uri_index,
    compile_getv_uri,
    get_getv_var_value,
    is_getv_uri,
    resolve_prompt_against_getv,
    uri_for_getv_profile,
    uri_for_getv_var,
)


@pytest.fixture
def getv_home(tmp_path: Path) -> Path:
    llm = tmp_path / "llm"
    llm.mkdir()
    (llm / "groq.env").write_text("GROQ_API_KEY=gsk_test123456789\nLLM_MODEL=llama\n")
    tokens = tmp_path / "tokens"
    tokens.mkdir()
    (tokens / "github.env").write_text("GITHUB_TOKEN=ghp_abcdefghijklmnop\n")
    return tmp_path


def test_uri_for_getv_var() -> None:
    uri = uri_for_getv_var("llm", "groq", "GROQ_API_KEY")
    assert uri == "getv://llm/groq/GROQ_API_KEY"
    assert is_getv_uri(uri)


def test_build_getv_uri_index(getv_home: Path) -> None:
    index = build_getv_uri_index(home=str(getv_home))
    assert index.format == "getv_uri.v1"
    assert index.find_by_kind("getv_var")
    assert "GROQ_API_KEY" in index.by_name
    profile_uri = uri_for_getv_profile("llm", "groq")
    assert index.lookup(profile_uri) is not None


def test_resolve_prompt_env_key(getv_home: Path) -> None:
    index = build_getv_uri_index(home=str(getv_home))
    hits = resolve_prompt_against_getv("ustaw GROQ_API_KEY dla modelu", uri_map=index)
    assert hits
    assert hits[0].entry_name == "GROQ_API_KEY"


def test_get_var_masked(getv_home: Path) -> None:
    uri = uri_for_getv_var("llm", "groq", "GROQ_API_KEY")
    out = get_getv_var_value(uri)
    assert out["found"] is True
    assert "gsk_" in out["value_masked"]
    assert "test123456789" not in out["value_masked"]


def test_compile_get_var() -> None:
    uri = uri_for_getv_var("llm", "groq", "GROQ_API_KEY")
    actions = compile_getv_uri(uri, HostPlatform.LINUX)
    assert actions[0].args[:3] == ["get", "llm", "groq"]
    assert actions[0].args[3] == "GROQ_API_KEY"


def test_compile_getv_via_top_level() -> None:
    uri = uri_for_getv_profile("llm", "groq")
    actions = compile_uri_to_actions(uri, HostPlatform.LINUX)
    assert actions[0].args[0] == "export"
