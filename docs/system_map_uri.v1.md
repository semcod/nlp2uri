# system_map_uri.v1 — URI layer over env2llm SystemMapIR

**Status:** draft (2026-06-06)  
**Upstream IR:** `env2llm.system_map.v1` / `nlp2dsl.system_map.v1` (`SystemMapIR`)  
**Consumer:** `nlp2uri.systemmap`

## Purpose

`env2llm` is the **source of truth** for environment capabilities (runtimes, commands,
resources, policies). `nlp2uri` is the **addressing and execution router** on top of that map.

Pipeline:

```text
example dir
  → env2llm.generate_system_map()
  → SystemMapIR
  → nlp2uri.systemmap.build_uri_index()
  → UriMap (system_map_uri.v1)
  → NL / MCP / CLI prompt
  → resolve_prompt_against_system_map()
  → URI(s)
  → compile / handoff / OS execute (existing nlp2uri pipeline)
```

URIs are **derived deterministically** from IR — never hand-edited in maps.

## Schemes

| IR type | URI pattern | Example |
|---------|-------------|---------|
| `RuntimeSpecIR` | `runtime://{kind}/{id}` | `runtime://worker/executor%3Aworker` |
| `CommandSchemaIR` | `command://{runtime_id}/{name}` | `command://executor%3Aworker/send_invoice` |
| `ResourceSpecIR` | `resource://{connector}/{id}` | `resource://filesystem/user` |
| `AccessGrantIR` | `access://{agent}/{area}/{actions}` | `access://mail_agent/email/send,read` |
| `ArtifactSpecIR` | `artifact://{example_id}/{path}` | `artifact://01-invoice/invoices/out.pdf` |
| `ConversationPolicyIR` | `conversation://{example_id}/policy` | `conversation://01-invoice/policy` |
| `ProcessPolicyIR` | `process://{example_id}/policy` | `process://01-invoice/policy` |
| `ScheduleSpecIR` | `schedule://{id}` | `schedule://daily-invoice` |
| `GeneratedServiceIR` | `service://generated/{name}` | `service://generated/invoice-worker` |
| `DeploySpecIR` | `deploy://{example_id}` | `deploy://01-invoice` |
| `ProfileValidationIR` | `validation://{example_id}/{code}` | `validation://01-invoice/profile.dsl_action` |
| environment block | `environment://{example_id}` | `environment://01-invoice` |

Segments with `:` or spaces are percent-encoded per RFC 3986.

## UriMap record (`system_map_uri.v1`)

```yaml
format: system_map_uri.v1
version: 1
example_id: "01-invoice"
system_map_format: nlp2dsl.system_map.v1
entries:
  command://executor%3Aworker/send_invoice:
    kind: command
    ref_type: CommandSchemaIR
    name: send_invoice
    ref: { ... CommandSchemaIR dump ... }
    links:
      - runtime://worker/executor%3Aworker
by_name:
  send_invoice:
    - command://executor%3Aworker/send_invoice
```

## NL resolution (phase 1)

`resolve_prompt_against_system_map(prompt, ir)` heuristically matches:

- command `name` (underscore ↔ space),
- command `description`,
- resource `id` / `title`,
- runtime `id`.

Returns ranked `ResolvedSystemUri` list. Desktop/OS intents (`open firefox`, `screenshot`)
remain in `nlp2uri.parse_nl` — SystemMap resolution is **additive**, not a replacement.

## Round-trip

```python
from env2llm import generate_system_map
from nlp2uri.systemmap import build_uri_index, resolve_prompt_against_system_map

ir = generate_system_map("examples/01-invoice", example_id="01-invoice")
index = build_uri_index(ir)
hits = resolve_prompt_against_system_map("send invoice to client", ir, uri_map=index)
# → command://executor%3Aworker/send_invoice
```

DOQL round-trip (`environment.doql.less` ↔ IR) stays in `env2llm`; URI index is rebuilt on load.

## Boundaries

| Package | Responsibility |
|---------|----------------|
| `env2llm` | introspection, policies, masking, DOQL render/parse |
| `nlp2uri.systemmap` | URI derivation, index, NL→URI against IR |
| `nlp2uri.compile` | OS/desktop schemes (`app://`, `desktop-*`) |
| `nlp2uri` (future) | `command://` handoff → nlp2dsl worker / MCP |

## Compatibility

- **nlp2dsl:** command URIs align with `commands[].name` + `runtime` refs in DOQL.
- **koru:** `koru_desktop_uri_*` tools stay for OS actions; SystemMap tools can be added later.
- **MCP:** proposed tools: `nlp2uri_list_system_uris`, `nlp2uri_resolve_system_map`.

## Versioning

- `system_map_uri.v1` — initial scheme set (this document).
- Breaking URI scheme changes → `system_map_uri.v2`.
