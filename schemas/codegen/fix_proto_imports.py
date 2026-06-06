#!/usr/bin/env python3
"""Fix api.proto and driver.proto to use common CQRS commands (buf lint)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMES = ROOT / "schemes"


def _pascal(scheme: str) -> str:
    return "".join(p.capitalize() for p in scheme.replace("-", "_").split("_"))


def fix_api(path: Path, scheme: str) -> None:
    agg = _pascal(scheme)
    content = f'''syntax = "proto3";

package nlp2uri.cqrs.v1.{scheme.replace("-", "_")};

import "common/v1/commands.proto";
import "common/v1/queries.proto";

service {agg}CommandService {{
  rpc Register(nlp2uri.cqrs.v1.common.RegisterUriCommand) returns (nlp2uri.cqrs.v1.common.CommandResult);
  rpc Resolve(nlp2uri.cqrs.v1.common.ResolvePromptCommand) returns (nlp2uri.cqrs.v1.common.CommandResult);
  rpc Compile(nlp2uri.cqrs.v1.common.CompileUriCommand) returns (nlp2uri.cqrs.v1.common.CommandResult);
  rpc Execute(nlp2uri.cqrs.v1.common.ExecuteUriCommand) returns (nlp2uri.cqrs.v1.common.CommandResult);
  rpc RebuildIndex(nlp2uri.cqrs.v1.common.RebuildIndexCommand)
      returns (nlp2uri.cqrs.v1.common.CommandResult);
}}

service {agg}QueryService {{
  rpc GetUri(nlp2uri.cqrs.v1.common.GetUriQuery) returns (nlp2uri.cqrs.v1.common.GetUriResult);
  rpc ListUris(nlp2uri.cqrs.v1.common.ListUrisQuery) returns (nlp2uri.cqrs.v1.common.ListUrisResult);
  rpc SearchByName(nlp2uri.cqrs.v1.common.SearchByNameQuery)
      returns (nlp2uri.cqrs.v1.common.SearchByNameResult);
  rpc GetCompilePlan(nlp2uri.cqrs.v1.common.GetCompilePlanQuery)
      returns (nlp2uri.cqrs.v1.common.GetCompilePlanResult);
  rpc GetEventStream(nlp2uri.cqrs.v1.common.GetEventStreamQuery)
      returns (nlp2uri.cqrs.v1.common.GetEventStreamResult);
}}
'''
    path.write_text(content, encoding="utf-8")


def fix_driver(path: Path, scheme: str) -> None:
    agg = _pascal(scheme)
    content = f'''syntax = "proto3";

package nlp2uri.cqrs.v1.{scheme.replace("-", "_")};

import "common/v1/driver.proto";
import "common/v1/commands.proto";

service {agg}Driver {{
  rpc Capabilities(nlp2uri.cqrs.v1.common.DriverCapabilitiesQuery)
      returns (nlp2uri.cqrs.v1.common.DriverCapabilities);
  rpc Compile(nlp2uri.cqrs.v1.common.CompileUriCommand) returns (nlp2uri.cqrs.v1.common.CompileUriResult);
  rpc Execute(nlp2uri.cqrs.v1.common.ExecuteUriCommand) returns (nlp2uri.cqrs.v1.common.ExecuteUriResult);
  rpc Probe(nlp2uri.cqrs.v1.common.ProbeUriQuery) returns (nlp2uri.cqrs.v1.common.ProbeUriResult);
}}
'''
    path.write_text(content, encoding="utf-8")


def main() -> None:
    for scheme_dir in sorted(SCHEMES.iterdir()):
        if not scheme_dir.is_dir():
            continue
        scheme = scheme_dir.name
        v1 = scheme_dir / "v1"
        if not v1.exists():
            continue
        fix_api(v1 / "api.proto", scheme)
        fix_driver(v1 / "driver.proto", scheme)
        print(f"fixed: {scheme}")


if __name__ == "__main__":
    main()
