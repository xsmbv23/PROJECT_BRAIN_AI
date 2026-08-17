# QUANT-N003 — ACTIVE REAL-HISTORY ACQUISITION ARCHITECTURE

## Decision

N003 must not remain a passive `BLOCKED_ON_REAL_HISTORY` wait state.

The acquisition pipeline is now an active Layer 1 process that may accumulate partial real-source evidence while the strict admission gate remains closed.

## State separation

```text
COLLECTION STATE
  PARTIAL / ACCUMULATING / READY / CONFLICT

                !=

ADMISSION STATE
  DENY / ADMITTED
```

A partial collection is not a partial truth claim. It is merely accumulated evidence that cannot yet enter the canonical dataset.

## Pipeline

```text
SOURCE DISCOVERY
      ↓
RAW CAPTURE (exact bytes)
      ↓
PROVENANCE ENRICHMENT
      ↓
DATA BUFFER
      ↓
STRICT ADMISSION
      ↓
CANONICAL FREEZE
      ↓
N003 PROOF EXECUTION
```

## Raw capture invariant

Hash exact response bytes before parsing:

```text
sha256(raw_bytes)
```

Do not hash parsed JSON as a substitute for the raw evidence hash.

Capture at minimum:

- business date
- source id
- source URL
- retrieval timestamp UTC
- raw-byte SHA-256
- raw artifact path
- HTTP status
- non-secret response headers

Never persist credentials or authorization headers.

## Buffer

`xsmbv23/Quant_Engine/data_buffer/` is accumulation-only and forbidden as Quant Engine input.

## Canonical

`xsmbv23/Quant_Engine/canonical_dataset/` is the only data boundary Layer 1 may consume.

Promotion is one-way and requires strict admission.

## Contiguity

`check_contiguity()` calculates:

```text
start
end
expected_days
actual_days
coverage_ratio
missing
```

No function fills missing dates.

## Source quorum

Independent source hashes are compared without merging payloads.

```text
< quorum       → DENY
all equal      → PASS candidate
any conflict   → DENY
```

## Resource invariant

The collector is bounded:

- response capture limit: 2 MiB
- chunked reads: 64 KiB
- no whole multi-day dataset materialization
- Render Free 512 MB boundary remains absolute
- Brain remains dataset-free

## Completion gate

Only after >=10 consecutive real-source dates with coverage ratio 1.0, provenance verification, raw hash freeze, conflict resolution, and canonical freeze may N003 proof execute.

Preferred history: 21–30 real dates.

## Next action

`QUANT-N003-PROOF-DATA-EXECUTION` remains unreachable until the admission receipt proves the completion gate.
