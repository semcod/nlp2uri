#!/usr/bin/env python3
"""Scaffold CQRS+ES protobuf tree per URI scheme from registry.yaml."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEMES_DIR = ROOT / "schemes"
REGISTRY = ROOT / "registry.yaml"


def _pascal(name: str) -> str:
    return "".join(part.capitalize() for part in name.replace("-", "_").split("_"))


def _proto_package(scheme: str, meta: dict) -> str:
    alias = meta.get("package_alias") or scheme.replace("-", "_")
    return f"nlp2uri.cqrs.v1.{alias}"


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return
    path.write_text(content, encoding="utf-8")


def aggregate_proto(scheme: str, meta: dict) -> str:
    pkg = _proto_package(scheme, meta)
    agg = _pascal(scheme.replace("-", "_"))
    ir = meta.get("ir_ref") or "n/a"
    return f'''syntax = "proto3";

package {pkg};

import "common/v1/uri.proto";

// Aggregate root: aggregate_id = uri.raw ({meta["uri_pattern"]})
// IR upstream: {ir}
message {agg}Aggregate {{
  nlp2uri.cqrs.v1.common.Uri uri = 1;
  int64 version = 2;
  string state = 3;
}}
'''


def commands_proto(scheme: str, meta: dict) -> str:
    pkg = _proto_package(scheme, meta)
    agg = _pascal(scheme.replace("-", "_"))
    return f'''syntax = "proto3";

package {pkg};

import "common/v1/commands.proto";
import "common/v1/uri.proto";
import "google/protobuf/struct.proto";

// Scheme-specific commands (extend common write model).
message {agg}RegisterCommand {{
  nlp2uri.cqrs.v1.common.CommandMetadata metadata = 1;
  nlp2uri.cqrs.v1.common.UriMapEntry entry = 2;
}}

message {agg}ResolveCommand {{
  nlp2uri.cqrs.v1.common.CommandMetadata metadata = 1;
  string prompt = 2;
  google.protobuf.Struct context = 3;
}}

message {agg}CompileCommand {{
  nlp2uri.cqrs.v1.common.CommandMetadata metadata = 1;
  nlp2uri.cqrs.v1.common.Uri uri = 2;
  google.protobuf.Struct config = 3;
}}

message {agg}ExecuteCommand {{
  nlp2uri.cqrs.v1.common.CommandMetadata metadata = 1;
  nlp2uri.cqrs.v1.common.Uri uri = 2;
  google.protobuf.Struct config = 3;
}}
'''


def events_proto(scheme: str, meta: dict) -> str:
    pkg = _proto_package(scheme, meta)
    agg = _pascal(scheme.replace("-", "_"))
    return f'''syntax = "proto3";

package {pkg};

import "common/v1/events.proto";
import "common/v1/uri.proto";
import "google/protobuf/struct.proto";

message {agg}Registered {{
  nlp2uri.cqrs.v1.common.EventMetadata metadata = 1;
  nlp2uri.cqrs.v1.common.UriMapEntry entry = 2;
}}

message {agg}Resolved {{
  nlp2uri.cqrs.v1.common.EventMetadata metadata = 1;
  string prompt = 2;
  nlp2uri.cqrs.v1.common.Uri uri = 3;
  float confidence = 4;
}}

message {agg}Compiled {{
  nlp2uri.cqrs.v1.common.EventMetadata metadata = 1;
  nlp2uri.cqrs.v1.common.Uri uri = 2;
  repeated nlp2uri.cqrs.v1.common.OSAction actions = 3;
}}

message {agg}Executed {{
  nlp2uri.cqrs.v1.common.EventMetadata metadata = 1;
  nlp2uri.cqrs.v1.common.Uri uri = 2;
  bool ok = 3;
  string output = 4;
}}

message {agg}EventEnvelope {{
  oneof payload {{
    {agg}Registered registered = 1;
    {agg}Resolved resolved = 2;
    {agg}Compiled compiled = 3;
    {agg}Executed executed = 4;
    nlp2uri.cqrs.v1.common.UriExecutionFailed failed = 5;
  }}
}}
'''


def queries_proto(scheme: str, meta: dict) -> str:
    pkg = _proto_package(scheme, meta)
    return f'''syntax = "proto3";

package {pkg};

import "common/v1/queries.proto";

// Scheme read model — aliases common queries; add filters in extensions if needed.
message List{ _pascal(scheme.replace("-", "_")) }Query {{
  nlp2uri.cqrs.v1.common.ListUrisQuery base = 1;
}}
'''


def driver_proto(scheme: str, meta: dict) -> str:
    pkg = _proto_package(scheme, meta)
    agg = _pascal(scheme.replace("-", "_"))
    drivers = ", ".join(meta.get("drivers", []))
    return f'''syntax = "proto3";

package {pkg};

import "common/v1/driver.proto";
import "common/v1/commands.proto";

// Generated driver targets: {drivers}
service {agg}Driver {{
  rpc Capabilities(nlp2uri.cqrs.v1.common.DriverCapabilitiesQuery)
      returns (nlp2uri.cqrs.v1.common.DriverCapabilities);
  rpc Compile(nlp2uri.cqrs.v1.common.CompileUriCommand) returns (nlp2uri.cqrs.v1.common.CompileUriResult);
  rpc Execute(nlp2uri.cqrs.v1.common.ExecuteUriCommand) returns (nlp2uri.cqrs.v1.common.ExecuteUriResult);
  rpc Probe(nlp2uri.cqrs.v1.common.ProbeUriQuery) returns (nlp2uri.cqrs.v1.common.ProbeUriResult);
}}
'''


def api_proto(scheme: str, meta: dict) -> str:
    pkg = _proto_package(scheme, meta)
    agg = _pascal(scheme.replace("-", "_"))
    return f'''syntax = "proto3";

package {pkg};

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


def openapi_yaml(scheme: str, meta: dict) -> str:
    agg = _pascal(scheme.replace("-", "_"))
    return f'''openapi: 3.1.0
info:
  title: nlp2uri {scheme} CQRS API
  version: "1.0.0"
  description: |
    REST projection of {agg}CommandService / {agg}QueryService.
    Generated from protobuf via buf; hand-maintained paths for MCP bridge.
servers:
  - url: http://localhost:8766/v1/{scheme}
paths:
  /commands/register:
    post:
      operationId: {scheme}Register
      tags: [commands]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
      responses:
        "200":
          description: CommandResult
  /commands/compile:
    post:
      operationId: {scheme}Compile
      tags: [commands]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                uri:
                  type: string
                platform:
                  type: string
                dry_run:
                  type: boolean
      responses:
        "200":
          description: CompileUriResult
  /queries/list:
    get:
      operationId: {scheme}ListUris
      tags: [queries]
      parameters:
        - name: kind
          in: query
          schema:
            type: string
      responses:
        "200":
          description: ListUrisResult
  /queries/{{uri}}:
    get:
      operationId: {scheme}GetUri
      tags: [queries]
      parameters:
        - name: uri
          in: path
          required: true
          schema:
            type: string
      responses:
        "200":
          description: GetUriResult
'''


def readme_md(scheme: str, meta: dict) -> str:
    layer = meta.get("layer", "?")
    drivers = ", ".join(meta.get("drivers", []))
    status = meta.get("status", "active")
    return f"""# `{scheme}://` — CQRS + ES (v1)

| Field | Value |
|-------|-------|
| Layer | `{layer}` |
| Pattern | `{meta["uri_pattern"]}` |
| Drivers | {drivers} |
| Status | {status} |
| IR | `{meta.get("ir_ref") or "—"}` |

## Aggregate

- **ID:** canonical URI string (`uri.raw`)
- **Stream:** `{scheme}EventEnvelope` appended to `EventStore`

## Commands → Events

| Command | Event |
|---------|-------|
| `Register` | `{_pascal(scheme.replace("-", "_"))}Registered` |
| `Resolve` | `{_pascal(scheme.replace("-", "_"))}Resolved` |
| `Compile` | `{_pascal(scheme.replace("-", "_"))}Compiled` |
| `Execute` | `{_pascal(scheme.replace("-", "_"))}Executed` |

## Codegen

```bash
cd schemas && ./codegen/generate.sh --scheme {scheme}
```
"""


def scaffold_scheme(scheme: str, meta: dict, *, force: bool = False) -> None:
    version = meta.get("version", "v1")
    base = SCHEMES_DIR / scheme / version

    files = {
        "aggregate.proto": aggregate_proto(scheme, meta),
        "commands.proto": commands_proto(scheme, meta),
        "events.proto": events_proto(scheme, meta),
        "queries.proto": queries_proto(scheme, meta),
        "driver.proto": driver_proto(scheme, meta),
        "api.proto": api_proto(scheme, meta),
        "openapi.yaml": openapi_yaml(scheme, meta),
        "README.md": readme_md(scheme, meta),
    }

    for name, content in files.items():
        path = base / name
        if path.exists() and not force:
            continue
        _write(path, content)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scheme", action="append", help="Scaffold only these schemes")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    schemes: dict = registry["schemes"]
    selected = set(args.scheme) if args.scheme else set(schemes)

    for name, meta in schemes.items():
        if name not in selected:
            continue
        scaffold_scheme(name, meta, force=args.force)
        print(f"scaffolded: schemes/{name}/{meta.get('version', 'v1')}/")

    print(f"done ({len(selected)} schemes)")


if __name__ == "__main__":
    main()
