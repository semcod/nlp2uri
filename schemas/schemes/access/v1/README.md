# `access://` — CQRS + ES (v1)

| Field | Value |
|-------|-------|
| Layer | `systemmap` |
| Pattern | `access://{agent}/{area}/{actions}` |
| Drivers | policy |
| Status | active |
| IR | `AccessGrantIR` |

## Aggregate

- **ID:** canonical URI string (`uri.raw`)
- **Stream:** `accessEventEnvelope` appended to `EventStore`

## Commands → Events

| Command | Event |
|---------|-------|
| `Register` | `AccessRegistered` |
| `Resolve` | `AccessResolved` |
| `Compile` | `AccessCompiled` |
| `Execute` | `AccessExecuted` |

## Codegen

```bash
cd schemas && ./codegen/generate.sh --scheme access
```
