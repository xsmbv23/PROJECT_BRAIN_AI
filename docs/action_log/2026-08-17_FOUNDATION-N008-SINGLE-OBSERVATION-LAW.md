# FOUNDATION-N008 — Single Observation Is Not Domain Understanding

## Purpose

Freeze a rule that protects the Forensic foundation from a subtle but severe failure mode: turning the first real receipt into a canonical domain schema.

## Foundation law

> **SINGLE RECEIPT ≠ DOMAIN UNDERSTANDING**
>
> **NO CANONICAL FROM SINGLE OBSERVATION.**

The system does not create truth. It only admits evidence.

Therefore a first real receipt is not permission to infer the domain, normalize the source, map prize fields, or define a canonical schema.

## Required first-receipt behavior

```text
RECEIPT_1
   ↓
FORENSIC CLASSIFICATION
   ↓
VALID / PARTIAL / CONFLICT / DRIFT
   ↓
STORE EXACT RAW + RECEIPT
   ↓
STOP
```

No schema inference occurs at this point.

## What Receipt 1 is allowed to answer

- Did the collector reach a real source?
- Were exact response bytes captured?
- Can provenance be recorded?
- Is the evidence complete, partial, conflicting, or drifting?
- Does the system's admission machinery correctly classify reality?

## What Receipt 1 is forbidden to answer

- final domain schema
- canonical field mapping
- 27-prize semantic mapping
- normalization rules
- parser assumptions
- source-merging rules
- domain interpretation

## Quorum / stability rule

Canonicalization remains `UNREACHED` when observations are insufficient.

Hard minimum:

```text
receipts_count < 2 → CANONICAL = UNREACHED
```

Preferred minimum:

```text
receipts_count < 3 → CANONICAL = UNREACHED
```

The transition after multiple observations is:

```text
RECEIPTS
   ↓
STABILITY CHECK
   ↓
VARIANCE CHECK
   ↓
DRIFT PATTERN CHECK
   ↓
CANONICAL CONTRACT
```

Even multiple receipts do not authorize canonicalization if they conflict or exhibit unresolved drift.

## One-way trust flow

```text
SOURCE
  ↓
EVIDENCE
  ↓
ADMISSION
  ↓
CANONICAL
  ↓
CONSUMER
```

No downstream stage may write truth backward into an upstream stage.

## Critical interpretation

The first receipt is a **test of whether the system understands reality correctly**, not a definition of what reality must look like.

## Interaction with existing Forensic FSM

This law is subordinate to and consistent with the single Forensic Database Admission FSM:

- `PASS` at a gate is only a prerequisite for the next gate.
- PASS is never inherited.
- `UNKNOWN` is not PASS.
- `UNREACHED` is not PASS.
- Collection is not admission.
- Readiness is not authority.
- Database existence is not database authorization.
- A real receipt is evidence, not canonical truth.

## Successor instructions

A successor Bot must read this file before implementing any collector parser or canonical schema.

If `RECEIPT_1` exists, the default action is **classification + exact storage + stop**.

Do not 'make the data nicer' merely because the first receipt looks regular.

## Current state

```text
FOUNDATION = FROZEN
PROMOTION  = DENY
LAYER 1    = READY / SEPARATE
STAIRCASE  = LOCKED
NEXT       = QUANT-N007
```
