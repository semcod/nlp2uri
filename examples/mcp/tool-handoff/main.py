#!/usr/bin/env python3
"""Example MCP tool payloads (text/uri-list + structured plan)."""

from __future__ import annotations

import json

from nlp2uri.mcp import mcp_handoff_payload, tool_resolve_desktop_action
from nlp2uri.models import HostPlatform


def main() -> None:
    samples = [
        "screenshot window titled Firefox",
        "otwórz vscode w folderze ~/github/semcod/nlp2uri",
        "focus slack",
        "zrób screenshot aktywnego okna przeglądarki",
    ]
    for text in samples:
        print(json.dumps(mcp_handoff_payload(text, platform=HostPlatform.LINUX), indent=2))
        print("---")
        print(json.dumps(tool_resolve_desktop_action(text, platform=HostPlatform.LINUX), indent=2))
        print()


if __name__ == "__main__":
    main()
