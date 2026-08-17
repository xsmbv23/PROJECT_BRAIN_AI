# BRAIN-N067 — Forensic Admission Chain Rule Preservation

## Purpose

Preserve a critical architectural clarification for every successor Bot.

There are not two independent Forensic systems. Database admission is one Forensic chain composed of sequential gates.

## Non-inheritance invariant

`PASS_AT_GATE_IS_PREREQUISITE_ONLY; NEVER_INFER_DEEPER_PASS`

An earlier PASS authorizes evaluation of the next gate. It does not grant or imply the next gate's PASS.

Canonical chain:

```text
DB_EXISTENCE
    -> DB_BINDING
    -> DB_TLS_ADMISSION
    -> DB_ROUND_TRIP
    -> PROMOTION
```

Unknown or failure at any gate => `DENY`.

## Meaning of each gate

- DB_EXISTENCE: the database resource exists and is observable.
- DB_BINDING: the service has an explicit runtime binding to that database.
- DB_TLS_ADMISSION: the binding satisfies the protected TLS policy.
- DB_ROUND_TRIP: a real compact forensic metadata envelope was written, read back, and SHA-256 matched.
- PROMOTION: durable database evidence is permitted for the next architectural stage.

## Examples

`DB_EXISTENCE=PASS` + `DB_BINDING=NOT_BOUND` is valid and means the database exists but the service has no admitted access.

`DB_BINDING=PASS` + `DB_TLS_ADMISSION=DENY_TLS` is valid and means a binding exists but is not admitted for protected communication.

`DB_TLS_ADMISSION=BOUND_TLS` + `DB_ROUND_TRIP=NOT_PROVEN` is valid and means the protected access path exists but durable forensic interaction has not been proven.

Only `DB_ROUND_TRIP=MATCH` can satisfy the promotion gate.

## Security analogy

```text
correct corridor key
    + correct room key
    + inner release for protected rooms
    + actual successful entry/evidence transaction
    = admission
```

A key for one corridor/room must never be reused as a key for another room.

## Successor instruction

Never create a single aggregate boolean such as `DATABASE_PASS`.
Never promote from existence alone.
Never promote from binding alone.
Never promote from TLS alone.
Never treat documentation state as runtime evidence.
Never use absence of an error as proof of a gate.

The repository's `state/next_action.json` remains the continuation authority.
