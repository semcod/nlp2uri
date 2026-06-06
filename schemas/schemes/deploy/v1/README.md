# `deploy://` — CQRS + ES (v1)

| Field | Value |
|-------|-------|
| Layer | `systemmap` |
| Pattern | `deploy://{example_id}` |
| Drivers | deploy |
| Status | active |
| IR | `DeploySpecIR` |

## Aggregate

- **ID:** canonical URI string (`uri.raw`)
- **Stream:** `deployEventEnvelope` appended to `EventStore`

## Commands → Events

| Command | Event |
|---------|-------|
| `Register` | `DeployRegistered` |
| `Resolve` | `DeployResolved` |
| `Compile` | `DeployCompiled` |
| `Execute` | `DeployExecuted` |

## Codegen

```bash
cd schemas && ./codegen/generate.sh --scheme deploy
```
