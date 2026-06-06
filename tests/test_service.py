"""Tests for NLP2URIService facade."""

from __future__ import annotations

from nlp2uri.models import HostPlatform
from nlp2uri.service import NLP2URIService


def test_from_prompt():
    svc = NLP2URIService.for_platform(HostPlatform.LINUX)
    plan = svc.from_prompt("open firefox")
    assert plan.uri.startswith("app://firefox/open")
    assert plan.actions


def test_handle_prompt_dry_run():
    svc = NLP2URIService.for_platform(HostPlatform.LINUX)
    payload = svc.handle_prompt("capture screen", dry_run=True)
    assert payload["plan"]["uri"].startswith("desktop-screenshot://")
    assert payload["result"]["ok"] is True


def test_handle_uri():
    svc = NLP2URIService.for_platform(HostPlatform.WINDOWS)
    payload = svc.handle_uri("ms-settings:", dry_run=True)
    assert payload["result"]["ok"] is True
