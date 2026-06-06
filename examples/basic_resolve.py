#!/usr/bin/env python3
"""Resolve NL descriptions to abstract URIs (no execution)."""

from __future__ import annotations

import json

from nlp2uri import nlp2uri, resolve_text
from nlp2uri.models import HostPlatform

SAMPLES = [
    "open firefox",
    "open https://github.com/semcod",
    "open file /etc/hosts",
    "otwórz vscode w folderze /tmp/my-project",
    "screenshot window titled VS Code",
    "zrób screenshot aktywnego okna przeglądarki",
    "capture screen",
    "focus terminal",
    "open settings",
]


def main() -> None:
    for text in SAMPLES:
        for platform in (HostPlatform.LINUX, HostPlatform.MACOS, HostPlatform.WINDOWS):
            plan = nlp2uri(text, os=platform)
            print(
                json.dumps(
                    {
                        "text": text,
                        "platform": platform.value,
                        **plan.to_dict(),
                    },
                    indent=2,
                )
            )
            print("---")


if __name__ == "__main__":
    main()
