# LAW-OBS-002 — VALID ≠ TRUE

## Status

**FROZEN / FOUNDATION LAW**

## Purpose

Prevent a successor Bot, collector, parser, or downstream component from interpreting a structurally successful communication receipt as proof that the observed domain content is correct.

## Core law

> **STRUCTURALLY_VALID (or ROUNDTRIP_VALID) does not mean DOMAIN_CORRECT or DOMAIN_TRUE.**

A receipt proves only the properties explicitly tested by that receipt's gate.

## First-receipt rule

`RECEIPT_1` proves:

```text
system ↔ real-world source communication is observable
```

It does **not** prove:

- the domain meaning is understood;
- the XSMB result is correct;
- the page layout is semantically correct;
- advertisements were absent;
- the parser mapping is correct;
- a 27-field schema is correct;
- the observation is canonical;
- the source is stable over time.

## Classification semantics

The generic word `VALID` is forbidden as an unqualified forensic state because it is semantically ambiguous.

Use these states instead:

| State | Meaning | Domain truth proven? |
|---|---|---|
| `ROUNDTRIP_VALID` | response/raw bytes and required transport checks succeeded | NO |
| `STRUCTURALLY_VALID` | evidence envelope has required structure/integrity | NO |
| `PARTIAL` | evidence is incomplete/truncated/insufficient | NO |
| `CONFLICT` | independent observations disagree | NO |
| `DRIFT` / `DRIFT_DETECTED` | previously observed source changed unexpectedly | NO |

A source may be `STRUCTURALLY_VALID` while containing wrong, polluted, incomplete, ad-heavy, or semantically misleading content.

## Gate rule

```text
RECEIPT_1
  ↓
CLASSIFY
  ↓
STORE EXACT RAW + RECEIPT
  ↓
STOP
```

No parser, normalizer, domain inference, 27-field mapping, or canonicalization may be triggered by `RECEIPT_1` alone.

## Interaction with canonicalization

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

The arrows are one-way. A receipt classification cannot promote itself into canonical truth.

Canonical admission requires the existing quorum/stability/drift/conflict gates. A minimum of 2 observations is hard; 3 is preferred.

## Forensic invariance

A later Bot must not weaken this law by renaming `STRUCTURALLY_VALID` back to `VALID`, by treating `ROUNDTRIP_VALID` as domain truth, or by adding an implicit promotion path.

Any code change that permits such inheritance is a **Forensic violation** and must be DENY.

## Transmission rule

This file is normative. Successor Bots must read it before changing receipt classification, acquisition, parsing, canonicalization, or promotion logic.
