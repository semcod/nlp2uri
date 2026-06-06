# `getv://` — CQRS + ES (v1)

| Field | Value |
|-------|-------|
| Layer | `env` |
| Pattern | `getv://{category}/{profile}/{var}` |
| Drivers | getv_cli |
| Status | active |
| IR | `getv_uri.v1` |

## Aggregate

- **ID:** canonical URI string (`uri.raw`)
- **Stream:** `getvEventEnvelope` appended to `EventStore`

## Commands → Events

| Command | Event |
|---------|-------|
| `Register` | `GetvRegistered` |
| `Resolve` | `GetvResolved` |
| `Compile` | `GetvCompiled` |
| `Execute` | `GetvExecuted` |

## Codegen

```bash
cd schemas && ./codegen/generate.sh --scheme getv
```
