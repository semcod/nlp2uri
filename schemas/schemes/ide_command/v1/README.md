# `ide_command://` — CQRS + ES (v1)

| Field | Value |
|-------|-------|
| Layer | `control` |
| Pattern | `ide-command://{ide}/{action}` |
| Drivers | koru, koruide_socket |
| Status | active |
| IR | `—` |

## Aggregate

- **ID:** canonical URI string (`uri.raw`)
- **Stream:** `ide_commandEventEnvelope` appended to `EventStore`

## Commands → Events

| Command | Event |
|---------|-------|
| `Register` | `IdeCommandRegistered` |
| `Resolve` | `IdeCommandResolved` |
| `Compile` | `IdeCommandCompiled` |
| `Execute` | `IdeCommandExecuted` |

## Codegen

```bash
cd schemas && ./codegen/generate.sh --scheme ide_command
```
