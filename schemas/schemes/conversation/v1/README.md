# `conversation://` — CQRS + ES (v1)

| Field | Value |
|-------|-------|
| Layer | `systemmap` |
| Pattern | `conversation://{example_id}/policy` |
| Drivers | policy |
| Status | active |
| IR | `ConversationPolicyIR` |

## Aggregate

- **ID:** canonical URI string (`uri.raw`)
- **Stream:** `conversationEventEnvelope` appended to `EventStore`

## Commands → Events

| Command | Event |
|---------|-------|
| `Register` | `ConversationRegistered` |
| `Resolve` | `ConversationResolved` |
| `Compile` | `ConversationCompiled` |
| `Execute` | `ConversationExecuted` |

## Codegen

```bash
cd schemas && ./codegen/generate.sh --scheme conversation
```
