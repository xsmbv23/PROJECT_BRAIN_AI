# CHAT RELAY EXAMPLE V1

This example is the operational format the user can use when carrying a Bot message between ChatGPT sessions.

```text
[CHAT_RELAY]
message_id: CHAT-20260821-001
from_bot: BOT3_EXECUTION
to_bots: BOT1_LEAD,BOT2_QUANT
relayed_at: 2026-08-21T11:00:00Z

content:
"HistoricalFetcher must not be used for canonical backfill until durable evidence is solved."
[/CHAT_RELAY]
```

The receiving bots must not treat `content` as evidence. They should:

1. Preserve the message verbatim and hash it.
2. Mark its initial epistemic status as `REPORTED`.
3. Acknowledge receipt independently.
4. Re-evaluate the claim against current state, contracts, code, and evidence.
5. Record `AGREE`, `CHALLENGE`, `CONDITIONAL`, or `UNKNOWN`.
6. If action is warranted, create or join a Multi-Bot Deliberation V2 record.
7. Persist the resulting next action through the normal action-record protocol.

The chat relay is therefore a **transport envelope**, not a truth source.
