# FORENSIC ADMISSION SEMANTICS V1

## Status

FROZEN FOUNDATION INVARIANT. This document is normative for successor Bots.

## 1. One Forensic FSM

There is exactly one authoritative forensic admission state machine. Readiness, observability, rehearsal, and execution must never create a second admission FSM.

```text
OBSERVABILITY / READINESS
        |
        | visibility only
        v
AUTHORITATIVE ADMISSION FSM
        |
        | PASS is only a prerequisite for its own gate
        v
EXECUTION / ROOM
```

## 2. Readiness is non-evidential

`READINESS` is an observability-plane status only.

Examples:

- ACCUMULATING
- EARLY_FREEZE_CANDIDATE
- STRICT_ADMISSION_READY

These statuses:

- are not forensic evidence;
- have no promotion authority;
- must not alter execution paths;
- must not be copied into forensic receipts as proof;
- must not be used as an inference that admission is nearly passed;
- must not authorize replay, temporal testing, or canonical truth usage.

Formal invariant:

```text
READINESS ∉ FORENSIC_CHAIN
```

## 3. Three planes

### Observability Plane

Progress, coverage, quorum visibility, conflicts, missing dates, and memory telemetry. Human/operator visibility only.

### Admission Plane

The only authority for `PASS`, `DENY`, and `UNREACHED`.

### Execution Plane

Deterministic computation against admitted canonical inputs. It must not depend on readiness state.

## 4. Admission chain semantics

A resource can pass several gates, but PASS never inherits forward automatically.

```text
DB_EXISTENCE
    -> DB_BINDING
    -> DB_TLS_ADMISSION
    -> DB_ROUND_TRIP
    -> PROMOTION
```

`DB_EXISTENCE = PASS` means only that the database exists.

`DB_BINDING = PASS` means only that the service has an explicit binding.

`DB_TLS_ADMISSION = PASS` means only that the binding satisfies the accepted TLS policy.

`DB_ROUND_TRIP = PASS` requires real compact metadata write/read and SHA-256 match.

Only the final proven gate can authorize promotion.

## 5. Data acquisition chain

```text
SOURCE
  |
  v
RAW BYTES
  | exact bytes + SHA256 before parse
  v
BUFFER / QUARANTINE
  | append-only
  v
ADMISSION
  | strict complete real-source proof
  v
IMMUTABLE CANONICAL DATASET
  |
  v
ENGINE INPUT
```

Hard boundaries:

```text
BUFFER != ENGINE INPUT
PARTIAL != TRUTH
COLLECTION != ADMISSION
```

## 6. N006 collector contract

The collector objective is not simply "crawl data". It is:

```text
SOURCE -> RAW -> BUFFER -> PROVENANCE HARDENING
```

Each day/source artifact must preserve:

- source_id
- URL
- retrieved_at
- business_date
- raw_hash
- parser_version

Missing provenance is `DENY` at admission.

Day-level isolation:

```text
1 business day = 1 raw artifact per source
```

A request must not silently become a multi-day truth artifact.

## 7. Multi-source quorum

Sources may be collected in parallel for speed, but truth remains ordered and deterministic.

```text
Day D
├── Source A
├── Source B
└── Source C
```

Matching independent sources may satisfy quorum. Conflicting sources are quarantined and must never be merged into truth.

Speed comes from parallel truth accumulation, not relaxed admission.

## 8. Temporal invariants

No synthetic history, backfill, interpolation, silent fill, or silent replacement.

Required coverage ratio for strict admission remains 1.0.

Partial history must never be described as complete temporal truth.

## 9. Drift

If raw bytes for an already observed business date change:

```text
RAW_HASH_CHANGED
      -> DRIFT_DETECTED
      -> DENY
```

Do not overwrite the old evidence.

## 10. Successor rule

A successor Bot must read this document before modifying readiness, admission, collector, canonicalization, or promotion logic.

If a proposed change creates a second FSM, lets readiness influence authority, or makes one gate PASS implicitly authorize another gate, reject the change and record the reason in the action log.
