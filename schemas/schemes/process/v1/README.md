# `process://` — CQRS + ES (v1)

| Field | Value |
|-------|-------|
| Layer | `systemmap` |
| Pattern | `process://{example_id}/policy` |
| Drivers | policy |
| Status | active |
| IR | `ProcessPolicyIR` |

## Aggregate

- **ID:** canonical URI string (`uri.raw`)
- **Stream:** `processEventEnvelope` appended to `EventStore`

## Commands → Events

| Command | Event |
|---------|-------|
| `Register` | `ProcessRegistered` |
| `Resolve` | `ProcessResolved` |
| `Compile` | `ProcessCompiled` |
| `Execute` | `ProcessExecuted` |

## Codegen

```bash
cd schemas && ./codegen/generate.sh --scheme process
```
