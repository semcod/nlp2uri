# uri_cqrs_es.v1 — CQRS + Event Sourcing over URI schemes (Protobuf)

**Status:** draft (2026-06-06)  
**Scope:** every `scheme://` in nlp2uri (desktop, getv, system_map, host)  
**Goal:** generate drivers, gRPC/REST APIs, MCP tool schemas from one source of truth

## Principles

| Principle | Rule |
|-----------|------|
| **URI = aggregate id** | `aggregate_id` is the canonical RFC 3986 URI string |
| **CQRS** | Commands mutate via event append; queries read projections |
| **ES** | `EventStore` is append-only per `aggregate_id`; snapshots optional |
| **Protobuf** | All commands, events, queries, driver contracts are `.proto` |
| **Drivers** | One `Driver` gRPC service per scheme × platform code-generated |
| **API** | `CommandService` + `QueryService` per scheme; OpenAPI from proto |

## Pipeline

```text
registry.yaml (schemes)
  → buf generate (protobuf → Python/Go/OpenAPI)
  → codegen/templates (driver, handler, MCP JSON Schema)
  → nlp2uri runtime adapters (linux, getv, nlp2dsl, …)
```

## Layer model

| Layer | Schemes | Index source |
|-------|---------|--------------|
| `desktop` | `app`, `desktop-screenshot`, `desktop-window`, `file`, `http` | NL parse + local discovery |
| `env` | `getv` | `~/.getv` profiles |
| `systemmap` | `command`, `runtime`, `resource`, `access`, `artifact`, … | env2llm SystemMapIR |
| `host` | `endpoint`, `device`, `container`, `mount` | OS introspection (future) |

## Command taxonomy (all schemes)

| Command | ES event(s) | Side effect |
|---------|-------------|-------------|
| `RegisterUri` | `UriRegistered` | Add to UriMap projection |
| `ResolvePrompt` | `UriResolved` | NL/heuristic → URI candidate |
| `CompileUri` | `UriCompiled` | URI → `OSAction[]` / handoff plan |
| `ExecuteUri` | `UriExecuted` / `UriExecutionFailed` | Run compiled plan |
| `RebuildIndex` | `IndexRebuilt` | Full re-scan from upstream IR |

Scheme-specific commands extend base (e.g. `getv.ExportVar`, `command.HandoffWorkflow`).

## Query taxonomy (all schemes)

| Query | Projection read |
|-------|-----------------|
| `GetUri` | UriMap entry by URI |
| `ListUris` | Filter by scheme/kind/tags |
| `SearchByName` | `by_name` index |
| `GetCompilePlan` | Last `UriCompiled` or live compile (read model) |
| `GetEventStream` | Raw ES replay for aggregate |

## Driver contract

Each scheme defines `driver.proto`:

```protobuf
service {Scheme}Driver {
  rpc Capabilities(DriverCapabilitiesQuery) returns (DriverCapabilities);
  rpc Compile(CompileUriCommand) returns (CompileUriResult);
  rpc Execute(ExecuteUriCommand) returns (ExecuteUriResult);
  rpc Probe(ProbeUriQuery) returns (ProbeUriResult);
}
```

Platform implementations (generated stubs):

| Target | Output path |
|--------|-------------|
| `linux` | `generated/python/drivers/{scheme}/linux.py` |
| `darwin` | `generated/python/drivers/{scheme}/darwin.py` |
| `windows` | `generated/python/drivers/{scheme}/windows.py` |
| `curl` | HTTP handoff (command, runtime, endpoint) |
| `getv_cli` | getv subprocess driver |
| `mcp` | MCP tool descriptor JSON |

## Versioning

- Package: `nlp2uri.cqrs.v1.{scheme}`
- Breaking change → new folder `v2/`
- `registry.yaml` pins active version per scheme

## Related

- [system_map_uri.v1.md](../docs/system_map_uri.v1.md)
- [getv_uri.v1.md](../docs/getv_uri.v1.md)
- [schemas/README.md](./README.md)
