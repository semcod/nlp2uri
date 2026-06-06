# `desktop_window://` — CQRS + ES (v1)

| Field | Value |
|-------|-------|
| Layer | `desktop` |
| Pattern | `desktop-window://{action}` |
| Drivers | linux, darwin, windows |
| Status | active |
| IR | `—` |

## Aggregate

- **ID:** canonical URI string (`uri.raw`)
- **Stream:** `desktop_windowEventEnvelope` appended to `EventStore`

## Commands → Events

| Command | Event |
|---------|-------|
| `Register` | `DesktopWindowRegistered` |
| `Resolve` | `DesktopWindowResolved` |
| `Compile` | `DesktopWindowCompiled` |
| `Execute` | `DesktopWindowExecuted` |

## Codegen

```bash
cd schemas && ./codegen/generate.sh --scheme desktop_window
```
