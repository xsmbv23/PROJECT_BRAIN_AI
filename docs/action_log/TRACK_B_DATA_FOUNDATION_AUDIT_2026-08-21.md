# TRACK B — DATA FOUNDATION AUDIT — 2026-08-21

## Scope

This is a parallel preparation track. It does **not** advance, replace, or unlock the canonical Runtime Track A state.

Runtime Track A remains:

```text
N116_WAIT_EXTERNAL_OBSERVATION
ACTION_SPACE = 0
MANDATORY_NO_OP = TRUE
PROMOTION = DENY
```

No `/governance` self-call, self-attestation, synthetic external evidence, or receipt fabrication is permitted.

## Repository topology audited

```text
xsmbv23/xsmb-quant
    = DATA / SOURCE-TRUTH PLANE

xsmbv23/Project_Brain_AI
    = GOVERNANCE / FORENSIC CONTROL PLANE

xsmbv23/Quant_Engine
    = LAYER 1 RESEARCH / EXECUTION PLANE
```

## Data Foundation findings

`xsmb-quant` already defines the canonical source model:

```text
FULL_27 = canonical source truth
TAIL_27 = derived projection only
```

The prize topology is fixed at 27 values and TAIL_27 may never be reversed into FULL_27.

The data blueprint already includes:

```text
source registry
 -> raw byte artifact
 -> SHA-256
 -> content hygiene
 -> source-specific parser
 -> strict FULL_27 validator
 -> calendar gate
 -> source identity
 -> independent-source quorum
 -> Brain governance
 -> candidate canonical FULL_27
 -> derived TAIL_27
```

The registry includes `ketqua16` as a source candidate. Ads/scripts/navigation are explicitly non-truth content and must not become extracted data.

Calendar semantics are also explicit:

```text
DRAW_EXPECTED
DRAW_CONFIRMED
NON_DRAW_DAY
UNKNOWN_GAP
```

`missing data != NON_DRAW_DAY` and unknown gaps block canonical promotion.

The retained legacy reconciliation currently reports 4,172 rows from 2015-01-01 through 2026-08-12, with 70 unknown-gap days. The legacy workbook is not canonical FULL_27 truth.

## Quant Engine findings

Quant Engine already contains a frozen canonical-dataset boundary and a canonical-input SHA-256 freeze.

Its current Layer 1 doctrine correctly states:

```text
canonical dataset
 -> immutable freeze
 -> Quant Engine
```

and forbids reverse mutation.

However, the current minimal `input_adapter.py` exposes a generic positional `data[-n:]` helper. This is acceptable only as a bounded-memory utility; it must never become the authoritative temporal resolver. T-1/T-2/T-7 must remain date-aligned at the canonical input boundary.

## Required boundary doctrine

The following relationship is now authoritative:

```text
xsmb-quant
    owns SOURCE TRUTH
        |
        | explicit canonical admission receipt
        v
Quant_Engine
    owns CALCULATION / RESEARCH
        |
        | compact evidence only
        v
Project_Brain_AI
    owns GOVERNANCE / ADMISSION / FORENSIC STATE
```

Brain does not rewrite source data.
Quant does not reopen Brain gates.
Data does not execute Quant algorithms.
Chat is not authoritative state.

## Core Mission preparation

The research chain remains:

```text
REAL DATA
 -> VALID RESEARCH
 -> VALID BACKTEST
 -> EDGE
 -> EV / P&L / ROI
 -> ROBUSTNESS / RISK / DRIFT
 -> CONTROLLED ACTION
```

No edge claim is allowed from incomplete, unresolved, synthetic, leaked, or non-canonical data.

## Current blockers

1. Runtime Track A external exact-current observation is still required; Track B must not bypass it.
2. Historical `UNKNOWN_GAP` dates remain unresolved until authoritative calendar evidence is attached.
3. Canonical FULL_27 promotion requires independent-source quorum and conflict-free evidence.
4. Quant Engine must consume an explicit frozen canonical input envelope, not infer temporal identity from record position.
5. Render Free 512 MB remains a hard architectural boundary; heavy historical research must be sharded/streamed outside Brain runtime.

## Legal next move

Continue Track B with a **cross-repository canonical input admission contract and date-aligned bounded adapter**, while preserving Track A N116 as an untouched external-observation wait state.

This document is a successor handoff, not a new N-action.
