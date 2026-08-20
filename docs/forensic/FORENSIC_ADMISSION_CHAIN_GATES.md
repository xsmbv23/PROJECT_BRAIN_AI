# Forensic Admission Chain — Gate Semantics

## Purpose

This document is part of the durable successor doctrine for `Project_Brain_AI`.
It prevents future AI operators from interpreting individual PASS states as a global authorization state.

## One FSM, not multiple forensic systems

There is exactly **ONE FORENSIC FSM**.

The database admission chain is one ordered chain inside that FSM:

```text
DB_EXISTENCE
    -> DB_BINDING
    -> SECRET_RESOLUTION
    -> DB_TLS_ADMISSION
    -> NETWORK_ORIGIN_PROOF
    -> DB_ROUND_TRIP
    -> PROMOTION
```

A gate is a checkpoint, not an independent forensic universe.

## Gate meaning

### 1. DB_EXISTENCE

Question:

> Does the intended PostgreSQL resource actually exist and is its identity known?

PASS means only that the resource exists.

It does **not** mean the Brain service can access it.

### 2. DB_BINDING

Question:

> Is the Brain runtime explicitly bound to the intended database endpoint through the approved runtime secret mechanism?

PASS means a service-side binding exists.

It does **not** prove that the binding resolves correctly, uses TLS, or reaches the intended database.

### 3. SECRET_RESOLUTION

Question:

> Does the runtime resolve the binding without exposing or persisting the credential?

Credential values must never appear in GitHub, action logs, ordinary application logs, evidence envelopes, or successor documentation.

PASS proves safe resolution only.

### 4. DB_TLS_ADMISSION

Question:

> Does the resolved PostgreSQL connection satisfy the explicit TLS admission policy?

Accepted TLS modes are the policy-defined secure modes only.

PASS does not prove network origin or database round-trip.

### 5. NETWORK_ORIGIN_PROOF

Question:

> Is the runtime actually communicating with the intended database origin rather than merely parsing a plausible URL?

This gate prevents configuration syntax from being mistaken for real connectivity.

PASS does not prove evidence persistence.

### 6. DB_ROUND_TRIP

Question:

> Can the runtime perform the minimal approved durable evidence transaction and verify it by reading back the exact compact envelope and matching its hash?

The round-trip must remain compact and non-sensitive:

```text
compact metadata envelope
        -> WRITE
        -> READ
        -> SHA-256 recomputation
        -> MATCH
```

No bulk source dataset is required for this gate.
No credentials belong in the envelope.

### 7. PROMOTION

Promotion is the only gate that may authorize durable evidence usage as a trusted foundation capability.

Promotion requires fresh evidence from **all preceding gates**.

## The invariant

```text
PASS_IS_LOCAL
PASS_IS_PREREQUISITE_ONLY
NO_PASS_INHERITANCE
OWN_GATE_EVIDENCE_REQUIRED
FRESH_EVIDENCE_REQUIRED_FOR_PROMOTION
UNKNOWN_IS_NOT_PASS
DEFAULT_DENY
```

Therefore:

```text
DB_EXISTENCE = PASS
```

must never be interpreted as:

```text
DB_BINDING = PASS
SECRET_RESOLUTION = PASS
DB_TLS_ADMISSION = PASS
NETWORK_ORIGIN_PROOF = PASS
DB_ROUND_TRIP = PASS
PROMOTION = PASS
```

Likewise:

```text
DB_ROUND_TRIP = PASS
```

is evidence for that gate only; it does not retroactively manufacture missing evidence for another gate.

## Relationship to the house / corridor model

The physical analogy is:

```text
house
  |
  +-- corridor key
  |
  +-- room key
  |
  +-- special-room inner latch / owner release
  |
  +-- room-specific evidence
```

The existence of a room does not grant its key.
Having a key does not prove the door opened.
Opening the door does not prove the person reached the correct room.
Reaching the room does not grant owner-level release.

Forensic state transitions follow the same rule.

## Relationship to Core Mission

Forensic FSM is the **control/admission mechanism**.
Core Mission remains the long-term objective:

```text
REAL_DATA
 -> VALID_RESEARCH
 -> VALID_BACKTEST
 -> EDGE
 -> EV_PNL_ROI
 -> ROBUSTNESS_RISK_DRIFT
 -> CONTROLLED_ACTION
```

The FSM does not replace the mission.
It decides whether evidence and actions are admissible.

## Successor instruction

A successor AI must never:

- infer a missing PASS from another PASS;
- convert UNKNOWN into PASS;
- treat database existence as authorization;
- bypass a gate because a later gate is green;
- unlock Room 02 or the staircase from documentation alone;
- modify the canonical next action while an authoritative external-observation gate is pending.

Documentation can clarify doctrine.
Documentation cannot manufacture runtime evidence.
