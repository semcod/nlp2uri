# `resource://` — CQRS + ES (v1)

| Field | Value |
|-------|-------|
| Layer | `systemmap` |
| Pattern | `resource://{connector}/{id}` |
| Drivers | probe |
| Status | active |
| IR | `ResourceSpecIR` |

## Aggregate

- **ID:** canonical URI string (`uri.raw`)
- **Stream:** `resourceEventEnvelope` appended to `EventStore`

## Commands → Events

| Command | Event |
|---------|-------|
| `Register` | `ResourceRegistered` |
| `Resolve` | `ResourceResolved` |
| `Compile` | `ResourceCompiled` |
| `Execute` | `ResourceExecuted` |

## Codegen

```bash
cd schemas && ./codegen/generate.sh --scheme resource
```
