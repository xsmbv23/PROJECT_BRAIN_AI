# FORENSIC FSM — EPISTEMIC SEPARATION STANDARD V1

## Status

CANONICAL FOUNDATION DOCTRINE.

This document does not create a new FSM and does not create a new gate. It constrains interpretation of the existing ONE FORENSIC FSM.

## 1. One FSM only

There is exactly one Forensic FSM.

Database admission, source admission, transport admission, and later promotion paths are ordered gate chains inside that one FSM. They are not independent forensic state machines.

## 2. Three distinct layers of truth

Never merge these three concepts:

```text
DOCTRINE
   !=
EVIDENCE
   !=
STATE
```

### Doctrine

Doctrine defines what a gate means, what evidence is required, what transitions are legal, and which shortcuts are forbidden.

Doctrine does not prove that a gate has passed.

### Evidence

Evidence is an observable artifact produced by the exact execution path under examination.

Evidence belongs to the gate that produced it. It must be sufficiently specific to prove that gate and must not be substituted by evidence from another gate.

### State

State is a mutable projection derived from valid current evidence plus the legal transition rules of the FSM.

State is not evidence by itself.

Historical state is not current evidence.

## 3. No inference from doctrine to state

The following transition is forbidden:

```text
DOCTRINE SAYS GATE SHOULD PASS
            ↓
        STATE = PASS
```

The correct direction is:

```text
EXACT CURRENT EVIDENCE
        ↓
GATE-SPECIFIC VALIDATION
        ↓
LEGAL FSM TRANSITION
        ↓
CURRENT STATE PROJECTION
```

## 4. No evidence inheritance

```text
PASS(A) != EVIDENCE(B)
PASS(A) != PASS(B)
```

A gate PASS is local to that gate. It only establishes a prerequisite for evaluating the next gate.

The destination gate must obtain and validate its own Atomic Evidence Artifact.

## 5. Epistemic ordering

```text
UNKNOWN
   ↓
NOT_PROVEN
   ↓
HARD_DENY
```

`UNKNOWN` must never be silently normalized to `PASS`.

`NOT_PROVEN` is an explicit forensic result, not a missing-progress marker.

A blocked capability boundary is a valid state when the required exact execution capability is unavailable. It must not be converted into PASS merely because the implementation exists in source.

## 6. Database admission example

Inside the ONE FORENSIC FSM:

```text
DB_EXISTENCE
    ↓
DB_BINDING
    ↓
DB_TLS_ADMISSION
    ↓
DB_ROUND_TRIP
    ↓
PROMOTION_AUTHORIZED
```

Their evidence is independent:

```text
DB_EXISTS
   !=
SERVICE_BOUND
   !=
TLS_ADMITTED
   !=
REAL_WRITE_READ_HASH_MATCH
   !=
PROMOTION_AUTHORIZED
```

## 7. Runtime evidence boundary

Source inspection can prove implementation properties.

It cannot prove exact-current runtime execution.

Likewise:

- local curl is not exact Render runtime evidence;
- proxy execution is not exact target execution;
- replayed receipt is not fresh execution evidence;
- synthetic receipt is not probe evidence;
- HTTP 202 is not forensic PASS;
- HTML hashing is not transport receipt proof;
- source modification to force a probe is forbidden.

## 8. TransportReceipt rule

When a gate requires a TransportReceipt, the receipt must remain the raw artifact produced by the unchanged probe.

A separate runtime-identity envelope may cryptographically bind:

```text
receipt_hash + commit + deployment + container/runtime identity
```

but that envelope is not a replacement for the receipt.

## 9. Mutable state and immutable history

```text
EXACT CURRENT EVIDENCE
        ├────────→ CURRENT STATE PROJECTION
        └────────→ IMMUTABLE HISTORY APPEND
```

Current state may move only through legal transitions supported by current evidence.

History is append-only and must never be rewritten to make a later state appear historically true.

## 10. Security model

Forensic admission follows the physical-room model:

```text
CORRIDOR KEY
    +
ROOM KEY
    +
INNER RELEASE (protected rooms)
    +
GATE-SPECIFIC EVIDENCE
    =
LEGAL ACCESS / PROMOTION
```

Possessing one key never implies possession of another key.

A visible room never implies permission to enter it.

A correct route never implies successful entry.

Successful entry never implies permission to promote evidence.

## 11. Successor-Bot rule

A successor AI must read this document together with:

1. `state/current_state.json`
2. `state/next_action.json`
3. immutable action history
4. gate-specific contracts
5. exact runtime evidence artifacts

The successor must read source before making architectural claims, but must never use source-only knowledge to fabricate runtime state.

If current evidence and documentation conflict, exact current evidence governs only when it is itself valid and cryptographically bound; otherwise the conflict remains unresolved and the gate stays `NOT_PROVEN` / `HARD_DENY`.

## Canonical sentence

> Forensic does not ask whether the architecture says a gate should be open. Forensic asks whether the exact gate has its own current evidence proving that it is open.
