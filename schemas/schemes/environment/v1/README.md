# `environment://` — CQRS + ES (v1)

| Field | Value |
|-------|-------|
| Layer | `systemmap` |
| Pattern | `environment://{example_id}` |
| Drivers | metadata |
| Status | active |
| IR | `environment` |

## Aggregate

- **ID:** canonical URI string (`uri.raw`)
- **Stream:** `environmentEventEnvelope` appended to `EventStore`

## Commands → Events

| Command | Event |
|---------|-------|
| `Register` | `EnvironmentRegistered` |
| `Resolve` | `EnvironmentResolved` |
| `Compile` | `EnvironmentCompiled` |
| `Execute` | `EnvironmentExecuted` |

## Codegen

```bash
cd schemas && ./codegen/generate.sh --scheme environment
```
