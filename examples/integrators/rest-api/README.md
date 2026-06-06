# REST API integrator

Starts `nlp2uri-serve` (stdlib HTTP) exposing:

| Method | Path | Body |
|--------|------|------|
| GET | `/health` | — |
| POST | `/v1/plan` | `{"prompt":"...", "platform":"linux"}` |
| POST | `/v1/resolve` | `{"prompt":"..."}` |
| POST | `/v1/compile` | `{"uri":"app://..."}` |
| POST | `/v1/execute` | `{"uri":"...", "dry_run":true}` |
| POST | `/v1/handle` | `{"prompt":"...", "dry_run":true}` |

## Run

```bash
nlp2uri-serve --port 8766
./e2e.sh
```
