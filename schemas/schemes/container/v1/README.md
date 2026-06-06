# `container://` — CQRS + ES (v1)

| Field | Value |
|-------|-------|
| Layer | `host` |
| Pattern | `container://{runtime}/{name}` |
| Drivers | docker |
| Status | draft |
| IR | `—` |

## Aggregate

- **ID:** canonical URI string (`uri.raw`)
- **Stream:** `containerEventEnvelope` appended to `EventStore`

## Commands → Events

| Command | Event |
|---------|-------|
| `Register` | `ContainerRegistered` |
| `Resolve` | `ContainerResolved` |
| `Compile` | `ContainerCompiled` |
| `Execute` | `ContainerExecuted` |

## Codegen

```bash
cd schemas && ./codegen/generate.sh --scheme container
```
