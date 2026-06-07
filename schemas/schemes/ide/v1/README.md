# `ide://` — CQRS + ES (v1)

| Field | Value |
|-------|-------|
| Layer | `control` |
| Pattern | `ide://{ide}/{action}` |
| Drivers | koru, koruide_socket |
| Status | active |
| IR | `—` |

## Aggregate

- **ID:** canonical URI string (`uri.raw`)
- **Stream:** `ideEventEnvelope` appended to `EventStore`

## Commands → Events

| Command | Event |
|---------|-------|
| `Register` | `IdeRegistered` |
| `Resolve` | `IdeResolved` |
| `Compile` | `IdeCompiled` |
| `Execute` | `IdeExecuted` |

## Codegen

```bash
cd schemas && ./codegen/generate.sh --scheme ide
```
