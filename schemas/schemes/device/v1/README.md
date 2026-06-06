# `device://` — CQRS + ES (v1)

| Field | Value |
|-------|-------|
| Layer | `host` |
| Pattern | `device://{bus}/{id}` |
| Drivers | linux, dbus |
| Status | draft |
| IR | `—` |

## Aggregate

- **ID:** canonical URI string (`uri.raw`)
- **Stream:** `deviceEventEnvelope` appended to `EventStore`

## Commands → Events

| Command | Event |
|---------|-------|
| `Register` | `DeviceRegistered` |
| `Resolve` | `DeviceResolved` |
| `Compile` | `DeviceCompiled` |
| `Execute` | `DeviceExecuted` |

## Codegen

```bash
cd schemas && ./codegen/generate.sh --scheme device
```
