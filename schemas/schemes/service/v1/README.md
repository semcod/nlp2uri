# `service://` — CQRS + ES (v1)

| Field | Value |
|-------|-------|
| Layer | `systemmap` |
| Pattern | `service://generated/{name}` |
| Drivers | curl, systemd, docker |
| Status | active |
| IR | `GeneratedServiceIR` |

## Aggregate

- **ID:** canonical URI string (`uri.raw`)
- **Stream:** `serviceEventEnvelope` appended to `EventStore`

## Commands → Events

| Command | Event |
|---------|-------|
| `Register` | `ServiceRegistered` |
| `Resolve` | `ServiceResolved` |
| `Compile` | `ServiceCompiled` |
| `Execute` | `ServiceExecuted` |

## Codegen

```bash
cd schemas && ./codegen/generate.sh --scheme service
```
