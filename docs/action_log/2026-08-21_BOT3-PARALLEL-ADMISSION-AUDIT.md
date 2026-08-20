# BOT3 — PARALLEL FORENSIC ADMISSION AUDIT

## Purpose

This action runs in parallel with the other bot(s) without mutating their branches or inheriting their PASS states.

## Observation

BOT1 currently has open governance-envelope work on a separate branch. BOT2 has a separate Quant-side branch/workstream. This BOT3 work therefore remains documentation/audit-only until an exact evidence boundary is established.

## Canonical principle

There is one FORENSIC FSM.

Database states are sequential admission gates, not separate forensic systems:

```text
DB_EXISTS
   -> DB_BINDING
   -> DB_TLS_ADMISSION
   -> DB_ROUND_TRIP
   -> PROMOTION
```

A PASS at one gate is never inherited by the next gate, another repository, another bot, another layer, or another runtime.

## Parallel-work safety

BOT3 must not:

- alter `state/next_action.json` on the canonical branch merely to claim progress;
- merge or close BOT1/BOT2 work;
- promote Layer 1;
- unlock Room 02 or the staircase;
- fabricate Render evidence;
- use historical receipts as exact-current proof;
- copy credentials into GitHub, logs, receipts, or chat.

## Evidence levels

Maintain these levels independently:

```text
FOUND
FIXED
TESTED
RUNTIME_VERIFIED
EXTERNAL_EVIDENCE
PROMOTED
```

No lower level may be represented as a higher level.

## Current database boundary

The foundation has an explicit non-secret binding classification. The observed runtime status previously established was `NOT_BOUND`.

Therefore the valid state remains:

```text
DB_EXISTS       = PASS
DB_BINDING      = NOT_BOUND
DB_TLS          = UNREACHED
DB_ROUND_TRIP   = UNREACHED
PROMOTION       = DENY
```

## Next independent audit

Before any DB promotion is considered, verify the following exact chain at the same runtime anchor:

1. service binding exists;
2. PostgreSQL scheme is valid;
3. TLS admission is valid;
4. compact metadata transaction succeeds;
5. exact read-back SHA-256 matches;
6. evidence receipt is persisted without credentials or bulk data;
7. only then may the promotion gate evaluate.

## Successor instruction

Future bots must read this log and `docs/architecture/FORENSIC_DATABASE_ADMISSION_CHAIN_V1.md` before touching database admission. Parallel execution is allowed, but canonical state authority remains singular.
