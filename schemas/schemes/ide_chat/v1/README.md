# `ide_chat://` — CQRS + ES (v1)

| Field | Value |
|-------|-------|
| Layer | `control` |
| Pattern | `ide-chat://{ide}/{action}` |
| Drivers | koru, koru_ide_drive, koruide_socket |
| Status | active |
| IR | `—` |

## Aggregate

- **ID:** canonical URI string (`uri.raw`)
- **Stream:** `ide_chatEventEnvelope` appended to `EventStore`

## Commands → Events

| Command | Event |
|---------|-------|
| `Register` | `IdeChatRegistered` |
| `Resolve` | `IdeChatResolved` |
| `Compile` | `IdeChatCompiled` |
| `Execute` | `IdeChatExecuted` |

## Codegen

```bash
cd schemas && ./codegen/generate.sh --scheme ide_chat
```
