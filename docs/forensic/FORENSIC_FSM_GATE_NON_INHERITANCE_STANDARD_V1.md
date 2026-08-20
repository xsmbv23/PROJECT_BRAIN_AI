# Forensic FSM Gate Non-Inheritance Standard V1

## Purpose

Define the mandatory semantics for every gate in the Forensic admission chain.

## Core invariants

1. `PASS_IS_LOCAL`: a PASS proves only the gate that produced it.
2. `PASS_IS_PREREQUISITE_ONLY`: a PASS may permit evaluation of the next gate; it does not pass the next gate.
3. `NO_PASS_INHERITANCE`: no gate may promote another gate's PASS into its own PASS.
4. `OWN_GATE_EVIDENCE_REQUIRED`: every PASS must have evidence owned by that gate.
5. `UNKNOWN_IS_NOT_PASS`: missing, stale, historical, inferred, or unavailable evidence cannot become PASS.
6. `DEFAULT_DENY`: any failed or unknown prerequisite denies promotion.
7. `CURRENT_BEATS_HISTORY`: historical PASS is never current runtime evidence.
8. `HYPOTHESIS_NEVER_COUNTS_AS_EVIDENCE`: a hypothesis can only become admissible through its controlled promotion chain.

## Five epistemic categories

```text
DOCTRINE   = rule the system must obey
EVIDENCE   = observation that can prove a gate
STATE      = current mutable projection from exact evidence
HISTORY    = immutable record of what happened
HYPOTHESIS = proposition awaiting controlled testing
```

No category may silently substitute for another.

## Database admission example

```text
DB_EXISTENCE
    PASS
      |
      v
DB_BINDING
    must prove its own evidence
      |
      v
DB_TLS_ADMISSION
    must prove its own evidence
      |
      v
DB_ROUND_TRIP
    WRITE -> READ -> SHA256 MATCH
      |
      v
PROMOTION
```

`DB_EXISTENCE=PASS` does not mean `DB_BINDING=PASS`.
`DB_BINDING=PASS` does not mean `DB_TLS_ADMISSION=PASS`.
`DB_TLS_ADMISSION=PASS` does not mean `DB_ROUND_TRIP=PASS`.

## Quant admission example

```text
CANONICAL_DATASET
      |
      v
FEATURE_ADMISSION
      |
      v
HYPOTHESIS
      |
      v
CONTROLLED_TEST
      |
      v
REPLAY
      |
      v
OOS
      |
      v
STABILITY
      |
      v
EDGE
      |
      v
PROBABILITY
      |
      v
PAYOUT_COST
      |
      v
EV
```

`EDGE` cannot be inferred from a signal.
`EV` cannot inherit PASS from Edge.
`P&L/ROI` cannot retroactively promote a failed prediction.

## Forensic consequence

A successor Bot must never reason:

> "The previous gate passed, therefore this gate is probably safe."

The only valid reasoning is:

> "The previous gate passed, therefore this gate is now eligible to be evaluated using its own evidence."

## Promotion rule

Promotion is a separate gate and must possess fresh evidence for the exact promotion target.

```text
PASS != PROMOTION
```

## Succession rule

This document is part of the successor read-order and must be preserved append-only. Any future revision must create a new version rather than silently mutating the semantics of V1.
