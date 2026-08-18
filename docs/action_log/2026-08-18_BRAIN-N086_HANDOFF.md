# BRAIN-N086 — NETWORK_ORIGIN_PROOF WAIT / SUCCESSOR HANDOFF

## Canonical FSM

This is ONE Forensic admission FSM:

```text
DB_EXISTENCE
  -> DB_BINDING
  -> DB_TLS_ADMISSION
  -> NETWORK_ORIGIN_PROOF
  -> DB_ROUND_TRIP
  -> PROMOTION
```

There are not two independent Forensic systems. Each item is one gate in the same admission chain.

## Immutable rule

```text
PASS at Gate N != PASS at Gate N+1
```

A gate PASS is local evidence. It only permits the next gate to be evaluated. It never grants PASS to a later gate by inference.

## Exact current state

```text
DB_EXISTENCE          = PASS
DB_BINDING            = BOUND_TLS
DB_TLS_ADMISSION      = PASS
NETWORK_ORIGIN_PROOF  = NOT_PROVEN
DB_ROUND_TRIP         = NOT_PROVEN
PROMOTION             = HARD_DENY
ACTION_SPACE          = 0
MODE                  = MANDATORY_NO_OP
LAYER_1               = LOCKED
STAIRCASE             = LOCKED
```

The exact-current runtime's network-origin probe returned `OperationalError`. This proves only that the required network-origin evidence is absent at this moment. It must not be converted into a stronger claim about permanent network failure.

## Allowed actions while waiting

- observe exact-current runtime evidence;
- monitor the real external infrastructure event;
- append non-mutating forensic documentation;
- validate documentation/state integrity.

## Forbidden actions

- manufacture network evidence;
- self-create the missing external event;
- infer network reachability from BOUND_TLS;
- infer durable DB persistence from an in-memory round-trip;
- use an old deployment as exact-current evidence;
- workaround the gate;
- unlock Layer 1;
- unlock Staircase;
- store credentials in GitHub;
- grant downstream authorization from reporting or prediction.

## Successor Bot instruction

The user may grant permission to automatically take the next action. That permission does NOT override `MANDATORY_NO_OP`.

When `ACTION_SPACE = 0`, the next action is to remain observational until the required external evidence exists.

Read these before any DB-related action:

1. `docs/FORENSIC_DATABASE_ADMISSION_CHAIN.md`
2. `state/current_state.json`
3. `state/next_action.json`

Truth priority:

```text
EXACT_CURRENT_RUNTIME_EVIDENCE
  > PERSISTED_FORENSIC_RECORD
  > OLD_DOCUMENTATION
  > HYPOTHESIS
```

## Continuation trigger

Only when exact-current runtime evidence proves `NETWORK_ORIGIN_PROOF = PROVEN` may the chain advance to `DB_ROUND_TRIP`.

Only after a real compact durable PostgreSQL metadata envelope is written, read back, and SHA-256 matches may `PROMOTION` be evaluated.

Until then: **WAIT_EXTERNAL_EVENT / MANDATORY_NO_OP / HARD DENY**.
