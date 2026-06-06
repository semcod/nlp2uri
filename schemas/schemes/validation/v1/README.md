# `validation://` — CQRS + ES (v1)

| Field | Value |
|-------|-------|
| Layer | `systemmap` |
| Pattern | `validation://{example_id}/{code}` |
| Drivers | policy |
| Status | active |
| IR | `ProfileValidationIR` |

## Aggregate

- **ID:** canonical URI string (`uri.raw`)
- **Stream:** `validationEventEnvelope` appended to `EventStore`

## Commands → Events

| Command | Event |
|---------|-------|
| `Register` | `ValidationRegistered` |
| `Resolve` | `ValidationResolved` |
| `Compile` | `ValidationCompiled` |
| `Execute` | `ValidationExecuted` |

## Codegen

```bash
cd schemas && ./codegen/generate.sh --scheme validation
```
