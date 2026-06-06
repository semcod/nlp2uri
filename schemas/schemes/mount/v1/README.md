# `mount://` — CQRS + ES (v1)

| Field | Value |
|-------|-------|
| Layer | `host` |
| Pattern | `mount://{device}/{path}` |
| Drivers | filesystem |
| Status | draft |
| IR | `—` |

## Aggregate

- **ID:** canonical URI string (`uri.raw`)
- **Stream:** `mountEventEnvelope` appended to `EventStore`

## Commands → Events

| Command | Event |
|---------|-------|
| `Register` | `MountRegistered` |
| `Resolve` | `MountResolved` |
| `Compile` | `MountCompiled` |
| `Execute` | `MountExecuted` |

## Codegen

```bash
cd schemas && ./codegen/generate.sh --scheme mount
```
