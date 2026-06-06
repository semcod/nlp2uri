# `http://` — CQRS + ES (v1)

| Field | Value |
|-------|-------|
| Layer | `desktop` |
| Pattern | `http(s)://{host}/{path}` |
| Drivers | curl |
| Status | active |
| IR | `—` |

## Aggregate

- **ID:** canonical URI string (`uri.raw`)
- **Stream:** `httpEventEnvelope` appended to `EventStore`

## Commands → Events

| Command | Event |
|---------|-------|
| `Register` | `HttpRegistered` |
| `Resolve` | `HttpResolved` |
| `Compile` | `HttpCompiled` |
| `Execute` | `HttpExecuted` |

## Codegen

```bash
cd schemas && ./codegen/generate.sh --scheme http
```
