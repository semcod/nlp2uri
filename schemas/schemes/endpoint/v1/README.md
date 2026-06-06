# `endpoint://` — CQRS + ES (v1)

| Field | Value |
|-------|-------|
| Layer | `host` |
| Pattern | `endpoint://{proto}/{host}/{port}/{path}` |
| Drivers | curl |
| Status | draft |
| IR | `—` |

## Aggregate

- **ID:** canonical URI string (`uri.raw`)
- **Stream:** `endpointEventEnvelope` appended to `EventStore`

## Commands → Events

| Command | Event |
|---------|-------|
| `Register` | `EndpointRegistered` |
| `Resolve` | `EndpointResolved` |
| `Compile` | `EndpointCompiled` |
| `Execute` | `EndpointExecuted` |

## Codegen

```bash
cd schemas && ./codegen/generate.sh --scheme endpoint
```
