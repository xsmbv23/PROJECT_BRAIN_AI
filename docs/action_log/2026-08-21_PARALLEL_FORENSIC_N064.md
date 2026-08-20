# PARALLEL FORENSIC HANDOFF — N064

## Operating decision

A parallel Bot may work independently, but it must not create a second truth system.
The repository state, immutable action history, exact runtime anchors, and explicit gate evidence remain authoritative.

## Canonical interpretation

There is ONE `FORENSIC_STATE` containing a sequential database admission chain:

```text
DB_EXISTENCE
   -> DB_BINDING
      -> DB_TLS_ADMISSION
         -> DB_ROUND_TRIP
            -> PROMOTION
```

A PASS belongs only to the gate that produced it. It is never inherited as a PASS by a deeper gate.

## Required behavior for parallel agents

1. Read `state/current_state.json` and `state/next_action.json` before modifying foundation code.
2. Read `docs/architecture/FORENSIC_DATABASE_ADMISSION_CHAIN_V1.md` before touching DB admission.
3. Never rewrite or delete historical action logs.
4. Append corrections/evidence with a new action id.
5. Never treat local PASS as Render PASS.
6. Never treat database existence as service authorization.
7. Never expose or persist credentials.
8. Never open Layer 1 or the staircase while foundation promotion is DENY.
9. Preserve the 320 MiB guard and Render Free 512 MB boundary.
10. If another Bot is already changing the same path, do not overwrite its work; use a separate branch/path and reconcile through evidence.

## Current foundation truth

The database resource exists and is observable, but the exact-current Brain runtime has previously classified its service-side binding as `NOT_BOUND`. The safe connector surface does not provide a credential-free service-link mutation, so no credential has been fabricated or copied into GitHub.

## Parallelism rule

Parallel execution is allowed at the **action level**, not at the **truth level**.

```text
BOT-A ─┐
BOT-B ─┼──> same immutable evidence chain
BOT-C ─┘
```

They may inspect, test, document, and implement non-conflicting work concurrently. They may not independently redefine architecture, promote a gate, or overwrite a newer exact-runtime state.

## Successor instruction

The next agent must continue from the latest repository state rather than from chat memory. Chat is only an interface; persistent repository state and evidence are the durable handoff.
