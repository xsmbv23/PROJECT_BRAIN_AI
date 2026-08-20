# FORENSIC GATE ADMISSION MODEL

## Permanent successor doctrine

There are NOT multiple independent Forensic state machines.

There is exactly **ONE Forensic FSM**.

What may appear to be different Forensic states are actually **ordered admission gates inside the same FSM**.

## The critical distinction

Two observations must never be conflated:

```text
DB_EXISTENCE
"Does the database resource exist?"

DB_BINDING
"Does this service have an explicit binding/key path to that database?"
```

They are not two competing Forensic universes and they are not interchangeable statuses.

They are two different gates because they answer two different questions and therefore require two different evidence receipts.

### Gate 1 — Existence

`DB_EXISTENCE=PASS` means only:

> The database resource has been independently observed to exist and be available as a resource.

It grants **zero access rights**.

### Gate 2 — Binding

`DB_BINDING=PASS` means only:

> The service has an explicit runtime binding contract pointing to the approved database resource.

It does not prove:

- secret resolution
- TLS admission
- network reachability
- write permission
- forensic round-trip

## No PASS inheritance

The following are all invalid deductions:

```text
DB_EXISTENCE=PASS
    => DB_BINDING=PASS                 INVALID

DB_BINDING=PASS
    => SECRET_RESOLUTION=PASS         INVALID

DB_TLS_ADMISSION=PASS
    => NETWORK_ORIGIN_PROOF=PASS      INVALID

NETWORK_ORIGIN_PROOF=PASS
    => DB_ROUND_TRIP=PASS              INVALID

DB_ROUND_TRIP=PASS
    => PROMOTION=PASS                  INVALID
```

Every arrow means **permission to evaluate the next gate**, never donation of PASS.

## Complete database admission chain

```text
                    ONE FORENSIC FSM
                          │
                          ▼
                    DB_EXISTENCE
                          │
                 PASS allows evaluation
                          ▼
                     DB_BINDING
                          │
                 PASS allows evaluation
                          ▼
                  SECRET_RESOLUTION
                          │
                 PASS allows evaluation
                          ▼
                  DB_TLS_ADMISSION
                          │
                 PASS allows evaluation
                          ▼
                NETWORK_ORIGIN_PROOF
                          │
                 PASS allows evaluation
                          ▼
                    DB_ROUND_TRIP
                          │
                 PASS allows evaluation
                          ▼
                     PROMOTION
```

A failed, missing, stale, or unverifiable gate stops progression at that gate.

## Evidence ownership

Each gate owns its own evidence.

```text
Gate                 Evidence owner
------------------------------------------------
DB_EXISTENCE         Resource observation
DB_BINDING           Runtime binding observation
SECRET_RESOLUTION    Approved secret-store admission
DB_TLS_ADMISSION     Connection-policy observation
NETWORK_ORIGIN_PROOF Exact service-origin observation
DB_ROUND_TRIP        Real write/read/hash receipt
PROMOTION            Complete-chain admission receipt
```

A later gate may reference earlier receipts, but it must never replace its own evidence with an earlier receipt.

## Why this matters to Forensic immutability

Historical evidence remains immutable.

If at T1:

```text
DB_EXISTENCE = PASS
DB_BINDING   = DENY
```

and at T2 a binding is later established, the system must record a new event:

```text
T1: DB_BINDING = DENY
T2: DB_BINDING = PASS
```

It must never rewrite the T1 event to appear as though binding had existed earlier.

This preserves chronology, causality, and auditability.

## Interaction with N116

The current runtime action track remains authoritative:

```text
BRAIN-N116_WAIT_EXTERNAL_OBSERVATION
```

No database-gate PASS can unlock N116.

No Data Foundation PASS can manufacture the missing external observation.

No internal Brain request can substitute for the required independent external observation.

Therefore while N116 waits:

```text
ACTION_SPACE = 0
PROMOTION = DENY
```

## Successor instruction

Future Bots must treat this document together with:

- `docs/forensic/FORENSIC_FSM_GATE_SEMANTICS.md`
- `state/current_state.json`
- `state/next_action.json`

as the canonical doctrine.

The invariant is:

> **One Forensic FSM. Many ordered gates. Every gate owns its evidence. PASS is local. PASS may unlock evaluation, never inherit authorization. Historical evidence is immutable.**
