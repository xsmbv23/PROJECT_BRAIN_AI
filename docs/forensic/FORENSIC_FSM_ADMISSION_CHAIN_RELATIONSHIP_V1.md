# Forensic FSM Admission Chain Relationship V1

## Purpose

This document permanently clarifies a recurring source of successor-Bot misunderstanding:
there are not multiple independent Forensic state machines for database admission.
There is **one Forensic FSM** containing ordered gates.

A gate result is local evidence about that gate only.
A PASS never becomes another gate's PASS.

## One chain, multiple gates

```text
ONE_FORENSIC_FSM
      |
      +-- DB_EXISTENCE
      |       |
      |       +-- PASS => database existence is proven
      |               |
      |               v
      +-- DB_BINDING
      |       |
      |       +-- must prove service binding independently
      |               |
      |               v
      +-- DB_TLS_ADMISSION
      |       |
      |       +-- must prove accepted TLS independently
      |               |
      |               v
      +-- DB_ROUND_TRIP
      |       |
      |       +-- WRITE -> READ -> SHA256 MATCH
      |               |
      |               v
      +-- PROMOTION
              |
              +-- fresh evidence required
```

## Relationship semantics

`DB_EXISTENCE=PASS` means only:

> The database resource exists and its existence has evidence.

It does **not** mean:

- the service is bound to it;
- credentials are available;
- TLS admission is valid;
- the service can execute a real DB operation;
- durable evidence round-trip is proven;
- promotion is permitted.

Likewise:

```text
DB_BINDING=PASS
    != DB_TLS_ADMISSION=PASS
    != DB_ROUND_TRIP=PASS
    != PROMOTION=PASS
```

Each later gate consumes the earlier result only as a **prerequisite to evaluation**.
It must produce its own evidence.

## Why the separation exists

The three statements below describe three different facts:

```text
DATABASE EXISTS
```
= resource fact.

```text
SERVICE IS BOUND TO DATABASE
```
= authorization/binding fact.

```text
SERVICE COMPLETED REAL WRITE/READ/HASH ROUND-TRIP
```
= execution/evidence-integrity fact.

Conflating them would create a false forensic promotion path.

## Quant equivalent

The same law applies to Quant:

```text
CANONICAL_DATA
 -> FEATURE_ADMISSION
 -> HYPOTHESIS
 -> CONTROLLED_TEST
 -> REPLAY
 -> OOS
 -> STABILITY
 -> EDGE
 -> PROBABILITY
 -> PAYOUT_COST
 -> EV
 -> PREDICTION_LEDGER
 -> ACTUAL_RESULT
 -> P&L/ROI
```

A PASS at one stage never proves the next stage.

Examples:

```text
EDGE_PASS      != PROBABILITY_PASS
PROBABILITY_PASS != EV_PASS
EV_PASS        != BACKTEST_PASS
BACKTEST_PASS  != REALIZED_ROI_PASS
```

## Mandatory successor reasoning

Never reason:

```text
previous PASS => current PASS
```

Reason only:

```text
previous PASS
    => current gate is eligible for evaluation
    => current gate must obtain its own evidence
```

## Immutability

This V1 document is append-only doctrine. Later changes must create V2+.
The successor Bot must preserve the distinction between:

- DOCTRINE
- EVIDENCE
- STATE
- HISTORY
- HYPOTHESIS

No one category may silently substitute for another.
