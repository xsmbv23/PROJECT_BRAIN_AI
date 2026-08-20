# FORENSIC GATE NON-INHERITANCE STANDARD V2

## Purpose

This is a canonical successor document for the Brain AI foundation. It exists to prevent future Bots from interpreting individual PASS states as global authorization or as evidence for another gate.

## One FSM only

There is exactly **ONE FORENSIC FSM**.

Database admission is not a second forensic state machine. Source admission is not a second forensic state machine. Security, transport, truth, and promotion are gates within the same FSM.

## Gate semantics

Every gate has four immutable properties:

1. it owns its own evidence;
2. PASS is local to that gate;
3. PASS is only a prerequisite for the next gate;
4. PASS never transfers or inherits into another gate.

Canonical rules:

```text
PASS_IS_LOCAL
PASS_IS_PREREQUISITE_ONLY
NO_PASS_INHERITANCE
UNKNOWN_IS_NOT_PASS
DEFAULT_DENY
OWN_GATE_EVIDENCE_REQUIRED
```

## Database admission chain

```text
DB_EXISTENCE
    -> DB_BINDING
    -> DB_TLS_ADMISSION
    -> DB_ROUND_TRIP
    -> PROMOTION
```

Meaning:

- `DB_EXISTENCE`: the database resource exists and its identity is independently established.
- `DB_BINDING`: the running service possesses an explicit runtime binding. Resource existence does not imply binding.
- `DB_TLS_ADMISSION`: the binding satisfies the approved TLS policy.
- `DB_ROUND_TRIP`: the exact runtime performs the real compact metadata write/read and independently verifies SHA-256 equality.
- `PROMOTION`: only after the preceding gates have their own current evidence may durable evidence promotion occur.

Examples of forbidden inference:

```text
DB_EXISTENCE = PASS
    != DB_BINDING = PASS

DB_BINDING = PASS
    != DB_TLS_ADMISSION = PASS

DB_TLS_ADMISSION = PASS
    != DB_ROUND_TRIP = PASS

DB_ROUND_TRIP = PASS
    != arbitrary future gate = PASS
```

## Source admission chain

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

The same non-inheritance rule applies. A successful network-origin proof does not prove result correctness. A transported result does not prove official-panel identity. A candidate does not become truth without its own matching/quorum evidence.

## Runtime evidence hierarchy

```text
EXACT_CURRENT_RUNTIME_EVIDENCE
    > BRAIN_PERSISTED_STATE
    > IMMUTABLE_ACTION_HISTORY
    > OLD_DOCUMENTATION
    > HYPOTHESIS
```

A persisted PASS is historical state, not a substitute for fresh exact-current runtime evidence when the gate explicitly requires fresh evidence.

## No receipt rule

```text
NO_RECEIPT
    = NO PASS
    = NO STATE MUTATION
```

A HTTP acknowledgement such as `202` is not a Forensic receipt. Source code proving that a probe exists is not execution proof. A locally replayed receipt is forbidden. A proxy receipt is forbidden.

## Physical execution bridge

For gates requiring exact-live transport evidence, the sole unlock path is the authorized external execution primitive defined by the current action contract. If the exact-live primitive is unavailable, the state remains DENY/READY-BUT-BLOCKED; the system must not substitute local curl, proxy calls, guessed endpoints, source modification, or fabricated evidence.

## Promotion semantics

Promotion is an explicit transition, never an emergent side effect:

```text
Gate N PASS
   |
   | only as prerequisite
   v
Gate N+1 evidence production
   |
   +-- evidence missing --> DENY / remain frozen
   |
   +-- evidence proven --> local PASS
```

## Architectural consequence

The Brain remains a **governance control plane**. It records and evaluates evidence and controls admission. It does not silently become the data source, calculation engine, or generic execution shell.

The chat window is only a communication interface. Persistent repository state, immutable history, contracts, and exact runtime evidence remain authoritative across future Bots.

## Current frozen implication

Current state is `LIVE_BUT_UNVERIFIED`; N109 is the sole admitted action; Room 01 / Layer 1 / staircase remain locked until exact-current runtime transport evidence is independently captured and cryptographically bound.
