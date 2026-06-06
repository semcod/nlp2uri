# `runtime://` — CQRS + ES (v1)

| Field | Value |
|-------|-------|
| Layer | `systemmap` |
| Pattern | `runtime://{kind}/{id}` |
| Drivers | curl |
| Status | active |
| IR | `RuntimeSpecIR` |

## Aggregate

- **ID:** canonical URI string (`uri.raw`)
- **Stream:** `runtimeEventEnvelope` appended to `EventStore`

## Commands → Events

| Command | Event |
|---------|-------|
| `Register` | `RuntimeRegistered` |
| `Resolve` | `RuntimeResolved` |
| `Compile` | `RuntimeCompiled` |
| `Execute` | `RuntimeExecuted` |

## Codegen

```bash
cd schemas && ./codegen/generate.sh --scheme runtime
```
