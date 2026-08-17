# DATA COLLECTION ≠ DATA ADMISSION

This is a permanent Forensic invariant for XSMB_FORENSIC.

## Core rule

> Data must be accumulated freely, but admitted strictly.

Collection and admission are different states of the **same evidence chain**. They are not two independent truth systems.

```text
SOURCE DISCOVERY
      ↓
RAW CAPTURE
      ↓
PROVENANCE ENRICHMENT
      ↓
DATA BUFFER / ACCUMULATION
      ↓
STRICT ADMISSION GATE
      ↓
CANONICAL FREEZE
      ↓
QUANT ENGINE
```

Only the strict admission gate may deny truth eligibility. Collection failures do not imply admission success; collection partiality is simply recorded as evidence state.

## Buffer rules

`data_buffer/` may contain partial real history and multiple independent source observations. It is never a Quant Engine input.

Allowed states:

- `UNVERIFIED`
- `PARTIAL`
- `READY`
- `CONFLICT`

Forbidden:

- synthetic history
- backfill
- interpolation
- silent fill
- silent replacement
- deletion of raw evidence
- merging conflicting sources into a fabricated truth

## Admission rules

Strict N003 admission requires:

- at least 10 consecutive real-source dates
- preferred 21–30 dates
- `coverage_ratio == 1.0`
- complete provenance
- raw response SHA-256 calculated before parsing
- unresolved source conflict = 0
- canonical input frozen

Collection coverage below 1.0 is allowed while accumulating. Admission coverage below 1.0 is DENY.

## Multi-source rule

Sources remain separate observations.

```text
A == B → quorum evidence may PASS
A != B → CONFLICT → DENY
```

Never merge A and B to manufacture a third truth.

## Promotion is one-way

```text
BUFFER → ADMISSION → CANONICAL → ENGINE
```

There is no reverse edge and no implicit cycle.

## Successor rule

A successor Bot must read this doctrine before changing N003 data acquisition or admission. `UNKNOWN_IS_NOT_PASS`, `DEFAULT_DENY`, and `PASS_IS_PREREQUISITE_ONLY` remain mandatory.
