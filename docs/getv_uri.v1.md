# getv_uri.v1 — URI layer over ~/.getv profiles

**Status:** draft (2026-06-06)  
**Upstream:** [getv](https://github.com/wronai/getv) profiles in `GETV_HOME` (default `~/.getv`)  
**Consumer:** `nlp2uri.systemmap.getv_uri`

## Purpose

Bridge browser-captured API keys (`getv grab`) to nlp2uri addressing:

```text
browser copy → getv grab → ~/.getv/llm/groq.env
  → build_getv_uri_index()
  → getv://llm/groq/GROQ_API_KEY
  → compile → getv get llm groq GROQ_API_KEY
```

## Schemes

| Kind | URI pattern | Example |
|------|-------------|---------|
| Profile | `getv://{category}/{profile}` | `getv://llm/groq` |
| Variable | `getv://{category}/{profile}/{VAR}` | `getv://llm/groq/GROQ_API_KEY` |

Query params (optional):

| Param | Effect |
|-------|--------|
| `action=export` | `getv export … --format env` |
| `action=exec&cmd=python` | `getv exec … -- python` |

## MCP tools

| Tool | Description |
|------|-------------|
| `nlp2uri_list_getv_uris` | Index all profiles/vars |
| `nlp2uri_resolve_getv` | NL → `getv://` URI |
| `nlp2uri_get_getv_var` | Read masked var metadata |

## Install

```bash
pip install 'nlp2uri[envmap]'   # includes getv + env2llm
```

## Todomat sync

```bash
~/github/wronai/todomat/scripts/sync-env-from-getv.sh llm/groq
```
