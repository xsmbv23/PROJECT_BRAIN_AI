# Forensic State Machine Doctrine — Successor Law

## Status

IMMUTABLE FOUNDATION LAW

This document is normative. A successor Bot must read it before modifying the foundation.

## 1. One Forensic system, not multiple Forensic systems

The database admission states are NOT independent Forensic systems. They are sequential gates in one `FORENSIC_DATABASE_ADMISSION_CHAIN`.

```text
DB_EXISTENCE
    ↓
DB_BINDING
    ↓
DB_TLS_ADMISSION
    ↓
DB_ROUND_TRIP
    ↓
PROMOTION
```

A PASS at one gate is only evidence for that gate. It is never a PASS for any later gate.

```text
DB_EXISTENCE = PASS
≠ DB_BINDING = PASS

DB_BINDING = PASS
≠ DB_TLS_ADMISSION = PASS

DB_TLS_ADMISSION = PASS
≠ DB_ROUND_TRIP = PASS

DB_ROUND_TRIP = PASS
→ eligible for PROMOTION consideration
```

## 2. No inferred promotion

No successor may infer a later state from:

- existence of a resource;
- existence of credentials without a runtime observation;
- an old receipt;
- a copied observation;
- a test fixture standing in for a live external event;
- a chat assertion;
- a successful deployment alone.

Only the evidence required by the specific gate may produce that gate's PASS.

## 3. Reality is an authority boundary

The system may define a valid transition, but it cannot manufacture the external event required to prove that transition.

```text
CHAT / BRAIN
    │
    │ can define, validate, govern
    │ cannot manufacture Reality
    ▼
REAL EXTERNAL EVENT
    │
    ▼
OBSERVATION
    │
    ▼
RECEIPT / EVIDENCE
    │
    ▼
STATE TRANSITION
```

Therefore:

`EXTERNAL_EVENT_CANNOT_BE_MANUFACTURED = TRUE`

A commit, deployment, synthetic trigger, replayed receipt, or copied observation must never be treated as the missing external event.

## 4. WAIT_EXTERNAL_EVENT

When all internally valid work is complete but the next transition requires an external event that has not occurred, the correct state is:

```text
WAIT_EXTERNAL_EVENT
```

This is a valid terminal state for the current evidence set. It is NOT:

- a bug;
- an incomplete state machine;
- permission to invent a trigger;
- permission to reuse an old receipt;
- permission to bypass a gate.

The successor must preserve the wait state until Reality supplies new evidence.

## 5. Machine authority hierarchy

```text
STATE / MACHINE AUTHORITY
        ↓
DOCTRINE / NORMATIVE LAW
        ↓
ACTION BOUNDARY
        ↓
EXECUTION
        ↓
OBSERVATION
        ↓
RECEIPT
```

No lower layer may silently override a higher layer.

Chat is an interface only. Chat content does not become persistent authority unless encoded into the repository's explicit state/doctrine/action structures through a legitimate action.

## 6. Admission security

The corridor/room model remains mandatory:

```text
corridor_key + room_key
        ↓
optional protected-room inner release
        ↓
actual room admission
```

Each room has its own lock/key. Corridor access does not imply room access. Room access does not imply permission to mutate room state. Protected rooms may require an inner release/chime before admission.

## 7. Forensic evidence fields

Each gate evidence record should preserve, where applicable:

- gate name;
- input evidence identity;
- output state;
- timestamp;
- commit identity;
- evidence hash;
- failure reason;
- provenance;
- whether the evidence came from Reality or from an internal verifier.

Internal verification evidence must never be mislabeled as a real external event.

## 8. Promotion rule

Promotion is monotonic only when every prerequisite gate has independently produced admissible evidence.

```text
UNKNOWN → DENY
MISSING → DENY
MISMATCH → DENY
STALE → DENY
UNVERIFIED → DENY
PASS → next gate only
```

No `FORCE`, `OVERRIDE`, or `ADMIN` path may silently convert an unproven state into PASS.

## 9. Successor handoff rule

Every completed action must leave:

1. a human-readable action log;
2. a machine-readable state update;
3. an explicit `next_action` or `WAIT_EXTERNAL_EVENT` state;
4. evidence identity/hash where evidence exists;
5. a statement of what is deliberately NOT proven.

A successor Bot must continue from those artifacts rather than reconstructing intent from chat history.

## 10. Current foundation interpretation

The database can exist while the service is not bound to it. The service can be bound while TLS admission is denied. TLS can pass while durable round-trip remains unproven.

These are not contradictory states. They are intentionally separated evidence gates inside one immutable Forensic admission chain.

## 11. Final invariant

> **Only Reality can supply the missing Reality evidence. The system may wait, but it may never fabricate.**
