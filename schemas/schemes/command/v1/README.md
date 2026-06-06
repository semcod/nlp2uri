# `command://` — CQRS + ES (v1)

| Field | Value |
|-------|-------|
| Layer | `systemmap` |
| Pattern | `command://{runtime_id}/{name}` |
| Drivers | curl, mcp |
| Status | active |
| IR | `CommandSchemaIR` |

## Aggregate

- **ID:** canonical URI string (`uri.raw`)
- **Stream:** `commandEventEnvelope` appended to `EventStore`

## Commands → Events

| Command | Event |
|---------|-------|
| `Register` | `CommandRegistered` |
| `Resolve` | `CommandResolved` |
| `Compile` | `CommandCompiled` |
| `Execute` | `CommandExecuted` |

## Codegen

```bash
cd schemas && ./codegen/generate.sh --scheme command
```
