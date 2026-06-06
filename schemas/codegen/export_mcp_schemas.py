#!/usr/bin/env python3
"""Export MCP tool input JSON schemas from registry.yaml."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
OUT = REPO / "generated" / "mcp"


def tool_schema(scheme: str, meta: dict) -> dict:
    return {
        "name": f"nlp2uri_{scheme.replace('-', '_')}_handle",
        "description": f"CQRS handle for {scheme}:// URIs ({meta['uri_pattern']})",
        "inputSchema": {
            "type": "object",
            "properties": {
                "uri": {"type": "string", "description": f"{scheme}://…"},
                "prompt": {"type": "string", "description": "NL resolve alternative"},
                "platform": {"type": "string", "enum": ["linux", "darwin", "windows"]},
                "dry_run": {"type": "boolean", "default": True},
                "config": {"type": "object"},
            },
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scheme")
    args = parser.parse_args()

    registry = yaml.safe_load((ROOT / "registry.yaml").read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)

    tools = []
    for name, meta in registry["schemes"].items():
        if args.scheme and name != args.scheme:
            continue
        tools.append(tool_schema(name, meta))

    (OUT / "tools.json").write_text(json.dumps(tools, indent=2), encoding="utf-8")
    print(f"wrote {OUT / 'tools.json'} ({len(tools)} tools)")


if __name__ == "__main__":
    main()
