#!/usr/bin/env python3
"""Generate Python driver stub classes per scheme × target."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
OUT = REPO / "generated" / "python" / "drivers"

STUB = '''"""Auto-generated driver stub — implement compile/execute/probe."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DriverContext:
    scheme: str
    target: str
    platform: str
    dry_run: bool = True


class {class_name}:
    """Driver for `{scheme}://` on target `{target}`."""

    scheme = "{scheme}"
    target = "{target}"

    def capabilities(self) -> dict[str, Any]:
        return {{
            "scheme": self.scheme,
            "target": self.target,
            "supports_compile": True,
            "supports_execute": True,
            "supports_probe": {supports_probe},
        }}

    def compile(self, uri: str, *, config: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        raise NotImplementedError(f"{{self.__class__.__name__}}.compile({{uri!r}})")

    def execute(self, uri: str, actions: list[dict[str, Any]], *, config: dict[str, Any] | None = None) -> dict[str, Any]:
        raise NotImplementedError(f"{{self.__class__.__name__}}.execute({{uri!r}})")

    def probe(self, uri: str) -> dict[str, Any]:
        raise NotImplementedError(f"{{self.__class__.__name__}}.probe({{uri!r}})")
'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scheme")
    args = parser.parse_args()

    registry = yaml.safe_load((ROOT / "registry.yaml").read_text(encoding="utf-8"))
    count = 0

    for scheme, meta in registry["schemes"].items():
        if args.scheme and scheme != args.scheme:
            continue
        for target in meta.get("drivers", []):
            class_name = "".join(p.capitalize() for p in scheme.replace("-", "_").split("_"))
            class_name += "".join(p.capitalize() for p in target.split("_")) + "Driver"
            path = OUT / scheme / f"{target}.py"
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.exists():
                continue
            supports_probe = target in {"curl", "getv_cli", "docker", "systemd", "filesystem", "dbus", "probe"}
            path.write_text(
                STUB.format(
                    class_name=class_name,
                    scheme=scheme,
                    target=target,
                    supports_probe=supports_probe,
                ),
                encoding="utf-8",
            )
            count += 1

    init_dirs = {p.parent for p in OUT.rglob("*.py")}
    for d in sorted({OUT, *init_dirs}):
        init = d / "__init__.py"
        if not init.exists():
            init.write_text('"""Generated URI drivers."""\n', encoding="utf-8")

    print(f"wrote {count} driver stubs under {OUT}")


if __name__ == "__main__":
    main()
