# `artifact://` — CQRS + ES (v1)

| Field | Value |
|-------|-------|
| Layer | `systemmap` |
| Pattern | `artifact://{example_id}/{path}` |
| Drivers | filesystem |
| Status | active |
| IR | `ArtifactSpecIR` |

## Aggregate

- **ID:** canonical URI string (`uri.raw`)
- **Stream:** `artifactEventEnvelope` appended to `EventStore`

## Commands → Events

| Command | Event |
|---------|-------|
| `Register` | `ArtifactRegistered` |
| `Resolve` | `ArtifactResolved` |
| `Compile` | `ArtifactCompiled` |
| `Execute` | `ArtifactExecuted` |

## Codegen

```bash
cd schemas && ./codegen/generate.sh --scheme artifact
```
