# `file://` — CQRS + ES (v1)

| Field | Value |
|-------|-------|
| Layer | `desktop` |
| Pattern | `file://{path}` |
| Drivers | linux, darwin, windows |
| Status | active |
| IR | `—` |

## Aggregate

- **ID:** canonical URI string (`uri.raw`)
- **Stream:** `fileEventEnvelope` appended to `EventStore`

## Commands → Events

| Command | Event |
|---------|-------|
| `Register` | `FileRegistered` |
| `Resolve` | `FileResolved` |
| `Compile` | `FileCompiled` |
| `Execute` | `FileExecuted` |

## Codegen

```bash
cd schemas && ./codegen/generate.sh --scheme file
```
