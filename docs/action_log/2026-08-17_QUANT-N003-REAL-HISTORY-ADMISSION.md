# QUANT-N003-REAL-HISTORY-ADMISSION

## Decision

The next proof action is DATA ADMISSION, not additional test writing.

The current architecture already distinguishes reproducibility from correctness and contains mutation/trace/anti-hardcode proof families. The remaining blocker is sufficiently strong real-source temporal evidence.

## Immutable finding

The available real rehearsal fixture is one day. Therefore:

```text
TEMPORAL_PROOF = UNREACHED
CAUSAL_PROOF   = UNREACHED
SENSITIVITY_PROOF = UNREACHED
```

This is not a failure of the engine. It is an evidence-depth boundary.

## Hard invariant

```text
NO_PARTIAL_TEMPORAL_CLAIM
```

Never convert a one-day PASS into a multi-day claim.

## Admission threshold

Strict:

```text
>= 10 consecutive real-source dates
coverage_ratio = 1.0
```

Preferred:

```text
21–30 consecutive real-source dates
```

## Forbidden shortcuts

No synthetic temporal data.
No backfill.
No interpolation.
No silent fill.
No silent replacement.
No deletion of raw source evidence.

## Required evidence

For every admitted source artifact retain:

```text
source_id
source_locator
retrieval_timestamp
business_date
raw_bytes_sha256
parser_version
canonical_representation_sha256
provenance_chain
```

Then freeze the canonical input and only then execute N003.

## Required sequence

```text
REAL HISTORY
  ↓
PROVENANCE
  ↓
CONTIGUITY + COVERAGE
  ↓
RAW HASH
  ↓
CANONICAL FREEZE
  ↓
FRESH_1
  ↓
REPLAY_1
  ↓
REPLAY_2
  ↓
FRESH_2
  ↓
BREAK / MUTATE / PROVE
  ↓
COMPACT FORENSIC RECEIPT
```

## Successor instruction

A future Bot must not restart by writing more tests merely because N003 is still red. First inspect the real-history admission gate and obtain the required real-source data through the DATA layer. Brain remains dataset-free and remains the governance control plane.

## State

```text
N003 = IMPLEMENTED_NOT_PROVEN
DATA_ADMISSION = BLOCKED
N004 = LOCKED
PROMOTION = DENY
STAIRCASE = LOCKED
```
