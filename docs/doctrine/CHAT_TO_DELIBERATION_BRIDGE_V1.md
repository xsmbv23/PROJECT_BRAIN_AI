# CHAT-TO-DELIBERATION BRIDGE V1

## Purpose

User-relayed Bot messages are a coordination input. They are not authority, evidence, or canonical state.

The bridge exists because Bot 1, Bot 2, and Bot 3 do not share a native chat session. The user can relay a Bot's message to the other Bots; the bridge turns that relay into a persistent, hash-addressed deliberation input.

## Flow

```text
USER RELAYS BOT MESSAGE
        |
        v
INGEST + message_id + SHA256
        |
        v
ALL TARGET BOTS ACKNOWLEDGE
        |
        v
INDEPENDENT INTERPRETATION
        |
        +---- claim
        +---- proposal
        +---- challenge
        +---- requested action
        +---- evidence references
        +---- epistemic status
        |
        v
DELIBERATION V2
        |
        v
SYNTHESIS / RECOMMENDATION
        |
        v
NEXT ACTION
        |
        v
PERSISTENT ACTION RECORD
```

## Mandatory rules

1. The exact relayed content is retained and hashed before interpretation.
2. A relay is attributed to `USER_RELAY`; it is not presented as a direct Bot-to-Bot message.
3. Each participating Bot records its own interpretation. One Bot may not write another Bot's position.
4. Claims copied from chat are marked `REPORTED` until independently verified.
5. Evidence references must resolve outside chat to persistent evidence records.
6. A user relay cannot directly mutate canonical state or create a gate PASS.
7. A disagreement remains visible in the deliberation record even if synthesis accepts another proposal.
8. Replaying the same `message_id` must not silently create a duplicate action. A changed interpretation requires a new revision/action record.
9. `NEXT_ACTION` is a recommendation until the owning execution stream persists it.
10. Gate outcomes remain local to their gate and are never inherited from deliberation or chat.

## Three-Bot behavior

### Bot 1 — Lead

Reads the relay, checks current state/contract/evidence first, identifies the E2E segment and blocker, then synthesizes rather than assuming the relayed Bot is correct.

### Bot 2 — Quant

Reads the same relay independently and looks for quantitative, temporal, source, statistical, and bias defects.

### Bot 3 — Execution

Reads the same relay independently and looks for implementation, runtime, deployment, resource, security, and race-condition defects.

## Transmission rule

A successor Bot must read, in order:

```text
current_state
next_action
action records
chat relay record
contracts / schemas
evidence receipts
code
```

The relay preserves rationale and dissent. It does not transmit truth.

## Example

```text
USER_RELAY
message_id = CHAT-20260821-001
content_sha256 = ...

Bot 2 said:
"HistoricalFetcher must not be used for canonical backfill until durable evidence is solved."
```

Bot 1 records:

```text
interpretation.epistemic_status = REPORTED
proposal = "audit canonical acquisition path"
```

Bot 3 may record:

```text
challenge = "fetcher still uses unbounded response.read()"
```

The system then creates one deliberation record. No PASS is created by the relay itself.
