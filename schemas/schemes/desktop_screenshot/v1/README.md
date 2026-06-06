# `desktop_screenshot://` — CQRS + ES (v1)

| Field | Value |
|-------|-------|
| Layer | `desktop` |
| Pattern | `desktop-screenshot://{target}` |
| Drivers | linux, darwin, windows |
| Status | active |
| IR | `—` |

## Aggregate

- **ID:** canonical URI string (`uri.raw`)
- **Stream:** `desktop_screenshotEventEnvelope` appended to `EventStore`

## Commands → Events

| Command | Event |
|---------|-------|
| `Register` | `DesktopScreenshotRegistered` |
| `Resolve` | `DesktopScreenshotResolved` |
| `Compile` | `DesktopScreenshotCompiled` |
| `Execute` | `DesktopScreenshotExecuted` |

## Codegen

```bash
cd schemas && ./codegen/generate.sh --scheme desktop_screenshot
```
