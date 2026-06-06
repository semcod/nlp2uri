# `schedule://` — CQRS + ES (v1)

| Field | Value |
|-------|-------|
| Layer | `systemmap` |
| Pattern | `schedule://{id}` |
| Drivers | scheduler |
| Status | active |
| IR | `ScheduleSpecIR` |

## Aggregate

- **ID:** canonical URI string (`uri.raw`)
- **Stream:** `scheduleEventEnvelope` appended to `EventStore`

## Commands → Events

| Command | Event |
|---------|-------|
| `Register` | `ScheduleRegistered` |
| `Resolve` | `ScheduleResolved` |
| `Compile` | `ScheduleCompiled` |
| `Execute` | `ScheduleExecuted` |

## Codegen

```bash
cd schemas && ./codegen/generate.sh --scheme schedule
```
