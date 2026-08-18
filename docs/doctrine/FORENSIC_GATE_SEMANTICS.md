# FORENSIC GATE SEMANTICS — PERMANENT DOCTRINE

## Status

This document is a successor-facing architectural doctrine. It is not a runtime receipt and it does not grant promotion authority.

## Core rule

**PASS IS LOCAL TO THE GATE.**

A successful gate proves only the proposition represented by that gate. It does not prove any downstream proposition.

Formally:

```text
Evidence(Gate A) -> PASS(A)
PASS(A) -> permission to evaluate Gate B
PASS(A) != PASS(B)
```

Therefore:

```text
PASS inheritance = FORBIDDEN
```

## Database admission chain

There is exactly **one** Forensic database-admission FSM:

```text
DB_EXISTENCE
    -> DB_BINDING
    -> DB_TLS_ADMISSION
    -> DB_ROUND_TRIP
    -> PROMOTION
```

Each arrow is a guarded transition, not a claim that the previous PASS proves the next PASS.

### Gate A — DB_EXISTENCE

Question:

```text
Does the database resource actually exist?
```

A PASS here means only that the resource exists and is observable.

It does **not** imply:

- the service has a credential;
- the service is authorized;
- TLS admission is valid;
- a connection can be established;
- evidence can be persisted;
- promotion is allowed.

### Gate B — DB_BINDING

Question:

```text
Does the protected runtime possess the explicitly authorized database binding?
```

The binding identity is `DATABASE_URL`, but the secret itself must never enter GitHub, Brain logs, action receipts, or successor documentation.

`NOT_BOUND` is a valid forensic state, not an error and not permission to improvise.

### Gate C — DB_TLS_ADMISSION

Question:

```text
Does the binding satisfy the accepted PostgreSQL TLS policy?
```

Accepted modes are explicitly constrained by the binding contract.

A binding with the wrong scheme or TLS mode is DENY even if the credential exists.

### Gate D — DB_ROUND_TRIP

Question:

```text
Can the authorized runtime perform one compact forensic metadata
WRITE -> READ -> SHA-256 MATCH cycle?
```

Only a real round-trip receipt can prove this gate.

Existence, binding, or TLS PASS cannot substitute for it.

### Gate E — PROMOTION

Promotion is the final authorization to treat the database as a durable evidence sink for the protected workflow.

Promotion requires fresh evidence for every preceding gate and the final round-trip proof.

## External-event semantics

A real event can still be the **wrong type of evidence**.

For example:

```text
workflow_dispatch admission receipt
        !=
Quant Engine Tests unit-test receipt
```

Both may be real GitHub Actions events. They prove different propositions.

Strict type matching is mandatory:

```text
Evidence(type A) != required Evidence(type B)
=> WAIT_EXTERNAL_EVENT or DENY
```

## WAIT_EXTERNAL_EVENT

`WAIT_EXTERNAL_EVENT` is a governed FSM state.

It means:

```text
required evidence does not yet exist
AND
no safe internal action may manufacture it
```

It is **not**:

- stuck;
- unfinished by default;
- permission to retry endlessly;
- permission to reuse an old receipt;
- permission to manufacture an event;
- permission to use an alternate path around the gate.

While `ACTIVE_HOLD` is set:

```text
protected-gate action space = 0
```

## Freshness

A receipt is admissible only when it matches the required:

- repository identity;
- runtime identity;
- workflow identity;
- commit identity;
- evidence type;
- current gate;
- freshness boundary.

Old receipts may remain archived for history but cannot be silently promoted to current evidence.

## Successor protocol

A successor Bot must execute this sequence:

```text
1. Read state/current_state.json.
2. Read state/next_action.json.
3. Read the latest action log.
4. Identify the current gate.
5. Identify the exact required evidence type.
6. Verify whether a fresh external event exists.
7. If absent and state=WAIT_EXTERNAL_EVENT: NO-OP.
8. If present: classify it independently.
9. Persist the receipt before changing state.
10. Evaluate only the current gate.
11. Never inherit PASS into the next gate.
12. Never unlock the staircase merely because a gate passed.
```

## Architectural invariant

```text
EVIDENCE -> STATE -> ACTION
```

Never:

```text
ASSUMPTION -> STATE -> ACTION
```

The Chat UI is only a communication interface. Persistent repository state and forensic evidence remain the successor authority.
