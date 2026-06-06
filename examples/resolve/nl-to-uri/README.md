# NL → abstract URI

Demonstrates `nlp2uri()` for English and Polish prompts across Linux, macOS, and Windows.

Output includes:

- `uri` — OS-neutral abstract URI (`app://`, `desktop-screenshot://`, …)
- `intent` + `slots`
- `actions` — compiled `OSAction` plan per platform

## Run

```bash
./e2e.sh
```

Or directly:

```bash
python main.py
```
