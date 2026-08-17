# N003-PROOF — Real History Admission

This is a permanent successor-bot doctrine.

## One Forensic state machine

N003 proof is one chain, not a separate test universe.

```text
REAL HISTORY ADMISSION
        ↓
PROVENANCE
        ↓
TEMPORAL COVERAGE
        ↓
CANONICAL FREEZE
        ↓
FRESH / REPLAY
        ↓
MUTATION / SENSITIVITY / CAUSAL / ANTI-HARDCODE
        ↓
FORENSIC RECEIPT
        ↓
PROMOTION
```

## Invariant: NO_PARTIAL_TEMPORAL_CLAIM

A one-day real fixture may prove parser/runtime behavior for that day. It may not prove temporal causality, temporal sensitivity, feature evolution, or multi-day replay correctness.

Strict N003 admission requires:

```text
>= 10 consecutive real-source dates
coverage_ratio = 1.0
```

Preferred:

```text
21–30 consecutive real-source dates
```

## State semantics

```text
DATA_DEPTH_INSUFFICIENT = UNREACHED
DATA_DEPTH_SUFFICIENT   = eligible_for_execution
```

`UNREACHED` is not `PASS`.

`TEST_PASS` is not `REAL_EVIDENCE`.

`REPRODUCIBLE` is not `CORRECTNESS_PROOF`.

## Provenance required per day

- source identity
- source locator/reference
- retrieval timestamp
- business/data date
- raw-byte SHA-256
- parser/schema version
- canonical representation SHA-256
- provenance chain

No synthetic history, backfill, interpolation, silent fill, or silent replacement is admissible.

## Successor rule

If the real multi-day dataset is unavailable, the successor must stop at the data-admission gate and record `UNREACHED`. It must not manufacture a fixture to make N003 green.
