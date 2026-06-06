# `app://` — CQRS + ES (v1)

| Field | Value |
|-------|-------|
| Layer | `desktop` |
| Pattern | `app://{app}/{action}` |
| Drivers | linux, darwin, windows |
| Status | active |
| IR | `—` |

## Aggregate

- **ID:** canonical URI string (`uri.raw`)
- **Stream:** `appEventEnvelope` appended to `EventStore`

## Commands → Events

| Command | Event |
|---------|-------|
| `Register` | `AppRegistered` |
| `Resolve` | `AppResolved` |
| `Compile` | `AppCompiled` |
| `Execute` | `AppExecuted` |

## Codegen

```bash
cd schemas && ./codegen/generate.sh --scheme app
```
