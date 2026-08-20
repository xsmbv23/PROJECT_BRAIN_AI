# FORENSIC ADMISSION CHAIN V1

## Purpose

This document is canonical architecture guidance for successor bots. It clarifies a critical invariant:

> There is ONE Forensic FSM. Database existence, service binding, TLS admission, durable round-trip, and promotion are gates inside the same admission chain. They are not independent forensic systems and PASS is never inherited between gates.

## Core invariant

```text
PASS(GATE_N) != PASS(GATE_N+1)
```

A previous gate only establishes the prerequisite needed to evaluate the next gate.

No bot, chat session, service, repository, or subsystem may infer a later PASS from an earlier PASS.

## Database admission chain

```text
                 ONE FORENSIC FSM
                        |
              DATABASE ADMISSION
                        |
          +-------------+-------------+
          |                           |
   EXISTENCE GATE               AUTHORIZATION GATE
   "does the room exist?"       "do we have its key?"
          |                           |
      DB_EXISTS                  DATABASE_URL
          |                           |
        PASS                    TLS admission
                                      |
                                  BOUND_TLS
                                      |
                                      v
                              ROUND-TRIP GATE
                                      |
                             WRITE -> READ -> SHA256
                                      |
                            +---------+---------+
                            |                   |
                         MISMATCH             MATCH
                            |                   |
                           DENY                PASS
                                                |
                                                v
                                           PROMOTION
```

## Gate meanings

### DB_EXISTENCE
Evidence that the PostgreSQL resource exists and is available.

This does NOT grant the service access.

```text
DB_EXISTS = PASS
DB_ACCESS = UNKNOWN / NOT_PROVEN
```

### DB_BINDING
Evidence that the runtime has a database binding under the approved secret-management boundary.

Expected binding name:

```text
DATABASE_URL
```

The credential itself must never appear in GitHub, action logs, governance payloads, or forensic documents.

### DB_TLS_ADMISSION
The binding is accepted only when the PostgreSQL scheme and TLS mode satisfy the binding contract.

Accepted TLS modes:

```text
require
verify-ca
verify-full
```

`BOUND_TLS` is evidence that the runtime binding classification is admissible. It is NOT evidence that a real database round-trip has succeeded.

### DB_ROUND_TRIP
A real compact metadata envelope is written to the database, read back, and verified by SHA-256 equality.

The payload must contain no source dataset and no credential.

Only this gate proves actual durable evidence-path operation.

### PROMOTION
Promotion is the final controlled transition. It is forbidden unless the required preceding evidence is independently proven.

## Non-inheritance rules

The following are explicitly forbidden:

```text
DB_EXISTS PASS
    -> DB_BINDING PASS                 FORBIDDEN

DB_BINDING PASS
    -> DB_TLS_ADMISSION PASS           FORBIDDEN

BOUND_TLS
    -> DB_ROUND_TRIP PASS              FORBIDDEN

DB_ROUND_TRIP PASS
    -> SOURCE_TRUTH PASS               FORBIDDEN

SOURCE_TRUTH PASS
    -> RESEARCH PASS                   FORBIDDEN

RESEARCH PASS
    -> BACKTEST PASS                   FORBIDDEN

BACKTEST PASS
    -> EDGE PASS                       FORBIDDEN

EDGE PASS
    -> CONTROLLED_ACTION              FORBIDDEN
```

Every arrow requires its own gate and evidence.

## Cross-repository rule

Bot 1 (Brain) and Bot 2 (Quant Engine) are separate control domains.

A PASS in Quant Engine is a local prerequisite only. It cannot silently promote a Brain gate.

A PASS in Brain is a local governance prerequisite only. It cannot silently promote Quant source truth or calculation truth.

```text
BOT 2 PASS
   |
   | evidence envelope only
   v
BOT 1 evaluates its own gate
   |
   | separate evidence required
   v
BOT 1 PASS
```

## Chat is not state authority

The chat window is a communication interface only. Persistent state, action authority, contracts, and evidence live in the repositories and durable evidence stores.

A successor bot must read the canonical state and current action contract before taking dependent action.

## N116 / current lock semantics

If `ACTION_SPACE = 0` and `MANDATORY_NO_OP = true`, no promotion or unlock may occur merely because engineering work is complete.

Safe independent engineering, tests, documentation, bounded infrastructure preparation, and forensic instrumentation may continue when explicitly allowed by policy.

## Protected room semantics

A protected room requires:

```text
corridor key
+ room key
+ correct direction/layer
+ inner release when required
```

Possessing the first keys never bypasses an inner latch.

## Successor handoff requirement

Every action that changes architecture or evidence must leave:

1. exact action ID;
2. previous canonical state reference;
3. evidence level (`FOUND`, `FIXED`, `TESTED`, `RUNTIME_VERIFIED`, `EXTERNAL_EVIDENCE`, `PROMOTED`);
4. files changed;
5. hashes/commit identifiers where available;
6. explicit `NEXT_ACTION`;
7. explicit `OTHER_BOT_REQUIRED_NEXT_ACTION` when cross-repository coordination exists;
8. explicit reason for any DENY;
9. no credential material.

## OOM rule

Render Free 512 MB is a hard operational boundary. Brain remains dataset-free and must use compact evidence envelopes. Large source artifacts and Quant calculations belong outside Brain runtime.

## Canonical sentence for successor bots

> **One Forensic FSM; many gates. No PASS inheritance. Every transition requires its own evidence.**
