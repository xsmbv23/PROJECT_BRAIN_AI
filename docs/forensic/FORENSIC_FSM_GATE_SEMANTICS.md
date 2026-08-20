# FORENSIC FSM — Gate Semantics & Dual-Track Doctrine

## Purpose

This document is a permanent successor-facing contract. It prevents future Bots from confusing local gate PASS states, inheriting PASS between unrelated gates, or promoting the runtime merely because another subsystem is healthy.

## One Forensic FSM

There is exactly **ONE Forensic FSM**. Database admission, runtime action admission, and source admission are chains inside that FSM. They are not separate Forensic universes.

A gate may only change its own state using evidence owned by that gate.

### Immutable gate rules

1. `PASS_IS_LOCAL` — PASS proves only the gate that produced it.
2. `PASS_IS_PREREQUISITE_ONLY` — a PASS may permit evaluation of the next gate; it does not PASS the next gate.
3. `NO_PASS_INHERITANCE` — no gate may copy another gate's PASS.
4. `OWN_GATE_EVIDENCE_REQUIRED` — every gate must possess its own evidence receipt.
5. `FRESH_EVIDENCE_REQUIRED_FOR_PROMOTION` — promotion requires current evidence, not historical evidence.
6. `UNKNOWN_IS_NOT_PASS` — missing observation is not failure and is not success.
7. `DEFAULT_DENY` — unresolved admission remains denied.
8. Historical receipts are immutable and are never rewritten to make a later check green.

## Database admission chain

```text
DB_EXISTENCE
    -> DB_BINDING
    -> SECRET_RESOLUTION
    -> DB_TLS_ADMISSION
    -> NETWORK_ORIGIN_PROOF
    -> DB_ROUND_TRIP
    -> PROMOTION
```

Semantics:

- `DB_EXISTENCE=PASS`: the database resource exists. It does **not** grant access.
- `DB_BINDING=PASS`: the service has an explicit runtime binding. It does **not** prove TLS or network reachability.
- `SECRET_RESOLUTION=PASS`: the binding resolves from the approved secret store. It does **not** expose or persist the secret.
- `DB_TLS_ADMISSION=PASS`: the connection policy is TLS-admissible.
- `NETWORK_ORIGIN_PROOF=PASS`: the actual service origin/path is proven.
- `DB_ROUND_TRIP=PASS`: a real compact metadata envelope was written, read back, and SHA-256 matched.
- `PROMOTION=PASS`: only the complete chain can promote the durable evidence sink.

Therefore:

```text
DB_EXISTS = PASS
    != DB_ACCESS = PASS
    != DB_ROUND_TRIP = PASS
    != PROMOTION = PASS
```

## Runtime action admission

The current canonical action track is:

```text
BRAIN-N116
    -> EXTERNAL_HTTP_OBSERVATION
    -> exact-current /governance
    -> READ_ONLY_RECEIPT_VERIFICATION
    -> ACTION_RECEIPT
    -> PASS_LOCAL
```

Verification must reject:

- missing receipt
- old instance
- wrong commit
- wrong deploy
- replayed evidence

The verifier must **not manufacture its own receipt** while verifying the receipt.

Until independent external observation exists:

```text
EXTERNAL_HTTP_OBSERVATION = NOT_OBTAINED
ACTION_RECEIPT            = NOT_YET_PROVEN_CURRENT
PASS_LOCAL                = DENY
ACTION_SPACE              = 0
MANDATORY_NO_OP           = TRUE
PROMOTION                 = DENY
```

`NOT_OBTAINED` is not equivalent to `ENDPOINT_FAIL` and is not equivalent to `RENDER_DOWN`.

## Dual-track execution rule

There are two tracks, but only one controls runtime admission.

### Track A — Runtime Admission

```text
N116
 -> external observation
 -> exact-current /governance
 -> receipt verification
 -> PASS_LOCAL
```

Until this completes, action space remains zero.

### Track B — Data Foundation

Track B may be prepared in parallel but **cannot unlock Track A** and cannot change `NEXT_ACTION`.

```text
xsmb_ground_truth.xlsx
    -> HUMAN_REFERENCE_INGEST_V1
    -> deterministic normalization
    -> frozen ingest code
    -> coverage audit
    -> missing-date detection
    -> human canonical

Crawler source A/B
    -> independent raw receipts
    -> crawler canonical

Human canonical + crawler canonical
    -> reconciliation
    -> conflict investigation
    -> canonical dataset
```

Human Excel and crawler output are independent evidence lineages.

**Crawler output must never be used to silently repair Human Reference. Human Reference must never be used to silently repair crawler evidence.**

If they disagree:

```text
CONFLICT
 -> investigate evidence
 -> do not auto-select either side
```

## Data Foundation boundary

The target coverage window is:

```text
2015-01-01 -> current
```

Before building `HUMAN_REFERENCE_INGEST_V1`, the original Excel artifact must be inspected as-is. The implementation must not invent a schema from the crawler JSON.

The ingest must inspect at minimum:

- sheets
- headers
- date representation
- 27 prize fields
- text vs numeric cells
- whitespace
- blank rows/columns
- merged cells
- date formats
- missing values
- extra values
- duplicates
- ambiguous values

Normalization must be deterministic and frozen, producing a canonical SHA-256 artifact.

Any denied cell must produce an actionable forensic event containing:

```text
error_code
sheet
row
cell
raw_value
expected_form
fix_guidance
evidence
```

## Promotion rule

No feature, Edge, Probability, EV, Quant, backtest, prediction, or P&L layer may infer that Data Foundation is admitted merely because another gate passed.

The progression remains:

```text
Canonical Dataset
 -> Lineage
 -> Feature Snapshot
 -> Temporal Replay
 -> Hypothesis
 -> Edge
 -> Probability
 -> EV
 -> OOS / Robustness
 -> Prediction Receipt
 -> P&L / ROI
```

No jumping layers.

## Successor instruction

When a future Bot starts work, it must first read this document and `state/next_action.json`.

The authoritative rule is:

> **A PASS belongs to the gate that earned it. A gate may unlock evaluation of the next gate, but it may never donate its PASS to the next gate.**

This rule is part of the Forensic foundation and must not be weakened for convenience, speed, or to obtain a green deployment.
