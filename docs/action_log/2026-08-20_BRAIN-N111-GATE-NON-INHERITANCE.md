# BRAIN-N111 — Gate Non-Inheritance / One-FSM Canonicalization

## Trigger

Successor-facing clarification required after review of the current frozen foundation state.

## Canonical doctrine

There are NOT two independent Forensic state machines. There is exactly ONE FORENSIC FSM.

The database admission chain is a sequence of gates inside that FSM:

```text
DB_EXISTENCE
 -> DB_BINDING
 -> DB_TLS_ADMISSION
 -> DB_ROUND_TRIP
 -> PROMOTION
```

Each gate owns its own evidence. A PASS is local and is only a prerequisite for the next gate. PASS never inherits.

## Critical examples

```text
DB_EXISTS = PASS
    does not imply
DB_BOUND = PASS
```

```text
DB_BOUND = PASS
    does not imply
DB_TLS = PASS
```

```text
DB_TLS = PASS
    does not imply
ROUND_TRIP = PASS
```

```text
ROUND_TRIP = PASS
    does not automatically authorize any unrelated gate
```

The same rule applies to source/network/result/truth gates.

## Epistemic rule

`UNKNOWN_IS_NOT_PASS` and `DEFAULT_DENY` remain mandatory.

For a gate requiring fresh exact-current evidence:

```text
NO RECEIPT = NO PASS = NO STATE MUTATION
```

HTTP acknowledgement, source-code existence, local replay, proxy evidence, guessed endpoint, or modified probe output cannot substitute for the required receipt.

## Current frozen state

The current repository state says:

- one Forensic FSM;
- current deployment `LIVE_BUT_UNVERIFIED`;
- N109 is the sole admitted action;
- N109 exact-live transport execution is still externally blocked;
- transport receipt is not proven;
- Room 01 / Layer 1 / staircase remain locked;
- no source/proxy/local substitution is allowed.

## Successor instruction

Read this document before acting. Do not create a second state machine for database admission. Do not infer a PASS from another gate. Do not mutate state without the gate's own evidence.

The correct next action remains `BRAIN-N109` unless exact-current evidence changes the canonical state.
