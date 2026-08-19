# FORENSIC GATE SEMANTICS — NEXT HARDENING

## Action

Hardened the canonical Forensic FSM so the non-inheritance law is machine-readable and test-enforced across both the database admission chain and source admission chain.

## Core invariant

There is ONE Forensic FSM.

A PASS is local to the gate that produced it. It is only a prerequisite for the next gate. It never inherits into another gate's PASS.

```text
PASS(A) != PASS(B)
PASS(A) -> permission to RUN(B)
PASS(A) -X-> PASS(B)
```

## Database chain

```text
DB_EXISTENCE
  -> DB_BINDING
  -> DB_TLS_ADMISSION
  -> DB_ROUND_TRIP
  -> PROMOTION
```

Each node has a distinct semantic meaning and its own evidence requirement.

```text
DB_EXISTENCE(PASS)       !=> DB_BINDING(PASS)
DB_BINDING(PASS)         !=> DB_TLS_ADMISSION(PASS)
DB_TLS_ADMISSION(PASS)   !=> DB_ROUND_TRIP(PASS)
DB_ROUND_TRIP(PASS)      !=> PROMOTION(PASS)
```

## Source chain

```text
SOURCE_INDEPENDENCE
  -> NETWORK_ORIGIN_PROOF
  -> RESULT_TRANSPORT
  -> OFFICIAL_RESULT_PANEL
  -> CANDIDATE
  -> EXCEL_VS_WEB_MATCH
  -> CANONICAL_QUORUM
  -> TRUTH_ADMISSION
```

Explicitly enforced:

```text
SOURCE_INDEPENDENCE(PASS) !=> NETWORK_ORIGIN_PROOF(PASS)
NETWORK_ORIGIN_PROOF(PASS) !=> RESULT_TRANSPORT(PASS)
RESULT_TRANSPORT(PASS) !=> OFFICIAL_RESULT_PANEL(PASS)
OFFICIAL_RESULT_PANEL(PASS) !=> CANDIDATE(PASS)
CANDIDATE(PASS) !=> EXCEL_VS_WEB_MATCH(PASS)
EXCEL_VS_WEB_MATCH(PASS) !=> CANONICAL_QUORUM(PASS)
CANONICAL_QUORUM(PASS) !=> TRUTH_ADMISSION(PASS)
```

## History law

A later PASS cannot rewrite the forensic meaning of an earlier DENY, BLOCKED, or NOT_PROVEN event.

Historical action records remain append-only. A successor creates a new action record.

## Security law

Keys authorize access; keys do not manufacture evidence.

```text
corridor_key + room_key + optional_inner_release
    != forensic PASS
```

Forensic evidence authorizes state transition only after the corresponding gate produces its own evidence.

## OOM law

Render Free 512 MB remains a hard boundary. The 320 MiB conservative guard remains active. Brain remains dataset-free.

## Current foundation state

`BRAIN-N104C.1D-INFRA` remains:

```text
BLOCKED / PAUSED / ARMED
PROMOTION = DENY
LAYER_1 = LOCKED
STAIRCASE = LOCKED
```

The missing exact-runtime execution primitive remains the only legal resume condition.

## Successor protocol

The next Bot must:

1. read `state/current_state.json`;
2. read `state/next_action.json`;
3. read `docs/forensic/FORENSIC_GATE_SEMANTICS_V1.json` and `.md`;
4. treat this action log as historical evidence, not as mutable state;
5. continue only from the recorded next action;
6. preserve the BLOCKED terminal state if the exact primitive is unavailable;
7. never infer a PASS from code existence, deployment identity, local curl, proxy output, or an earlier gate PASS.
