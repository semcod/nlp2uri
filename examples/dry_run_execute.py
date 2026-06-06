#!/usr/bin/env python3
"""Dry-run OSActions for resolved URIs."""

from __future__ import annotations

from nlp2uri import compile_uri_to_actions, nlp2uri
from nlp2uri.models import HostPlatform

CASES = [
    ("open firefox", HostPlatform.LINUX),
    ("capture screen", HostPlatform.MACOS),
    ("open settings", HostPlatform.WINDOWS),
    ("otwórz plik invoice-2025.pdf", HostPlatform.LINUX),
]


def main() -> None:
    for text, platform in CASES:
        plan = nlp2uri(text, os=platform)
        actions = compile_uri_to_actions(plan.uri, platform)
        print(f"text={text!r} platform={platform.value}")
        print(f"  uri={plan.uri}")
        for action in actions:
            print(f"  action={action.argv()}")
        print()


if __name__ == "__main__":
    main()
