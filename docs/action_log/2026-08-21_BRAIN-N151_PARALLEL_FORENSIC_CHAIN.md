# BRAIN-N151 — Canonical Single-FSM Admission Semantics

## Type

SAFE PARALLEL FOUNDATION DOCUMENTATION ONLY.

This action does not unlock any room, change promotion, change action space, or substitute for independently observable execution evidence.

## Decision recorded

The database admission model is **one Forensic FSM**, not multiple independent Forensic states.

Canonical ordered chain:

```text
DB_EXISTENCE
 -> DB_BINDING
 -> SECRET_RESOLUTION
 -> DB_TLS_ADMISSION
 -> NETWORK_ORIGIN_PROOF
 -> DB_ROUND_TRIP
 -> PROMOTION
```

Each gate owns its own evidence. A PASS is local and only establishes reachability to the next gate. PASS never inherits into a later gate.

If a gate is FAIL or UNKNOWN, later gates are UNREACHED for that evaluation. They must not be fabricated as PASS.

## Why this matters

These statements have distinct meanings:

```text
DATABASE EXISTS
SERVICE IS AUTHORIZED/BINDed
DATABASE ROUND-TRIP IS PROVEN
PROMOTION IS GRANTED
```

They are sequential evidence layers inside one state machine, not peer permissions.

## Successor instruction

A future Bot must preserve:

```text
PASS_IS_LOCAL
PASS_IS_PREREQUISITE_ONLY
NO_PASS_INHERITANCE
UNKNOWN_IS_NOT_PASS
DEFAULT_DENY
OWN_GATE_EVIDENCE_REQUIRED
FRESH_EVIDENCE_REQUIRED_FOR_PROMOTION
```

A Bot must never turn an earlier PASS into a later PASS merely because the earlier condition makes the later condition plausible.

## Current safety interaction

The current Brain state remains under an external-observation wait. This documentation action does not change that wait and does not change promotion reachability.

```text
ACTION_SPACE = 0
PROMOTION = DENY
LAYER_1 = LOCKED
STAIRCASE = LOCKED
```

## Forensic immutability

This record is a new historical action. It does not rewrite the meaning of any previous action, PASS, FAIL, UNKNOWN, or DENY.
