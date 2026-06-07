# `koru_control://` — CQRS + ES (v1)

| Field | Value |
|-------|-------|
| Layer | `control` |
| Pattern | `koru-control://{surface}/{operation}` |
| Drivers | koru, koru_ide_drive, koruide_socket |
| Status | active |
| IR | `—` |

## Aggregate

- **ID:** canonical URI string (`uri.raw`)
- **Stream:** `koru_controlEventEnvelope` appended to `EventStore`

## Commands → Events

| Command | Event |
|---------|-------|
| `Register` | `KoruControlRegistered` |
| `Resolve` | `KoruControlResolved` |
| `Compile` | `KoruControlCompiled` |
| `Execute` | `KoruControlExecuted` |

## Codegen

```bash
cd schemas && ./codegen/generate.sh --scheme koru_control
```
