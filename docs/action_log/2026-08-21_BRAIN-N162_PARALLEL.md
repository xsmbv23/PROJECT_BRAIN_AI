# BRAIN-N162 — Parallel S1 Canonical Evidence Admission Hardening

## Why this action exists

N162 was the current READY action at the time of this parallel pass. Another Bot AI may continue independently. This action therefore avoids rewriting shared state files and records its work as an immutable action log only.

The central rule is preserved:

> One Forensic FSM. Each gate owns its evidence. PASS is local, prerequisite-only, and never inherited.

The canonical chain remains:

```text
DB_EXISTENCE
  -> DB_BINDING
  -> SECRET_RESOLUTION
  -> DB_TLS_ADMISSION
  -> NETWORK_ORIGIN_PROOF
  -> DB_ROUND_TRIP
  -> PROMOTION
```

For S1:

```text
REAL SOURCE
   -> RAW ARTIFACT
   -> RAW BYTE SHA256
   -> CONSECUTIVE DATE COVERAGE
   -> ZERO CONFLICTS
   -> REAL OBSERVABLE RECEIPT
   -> FROZEN CANONICAL SHA256
   -> S1 PASS
   -> ONLY THEN S2 MAY BE EVALUATED
```

## Changes made

### 1. S1 machine verifier

Added:

`tools/verify_s1_canonical_evidence.py`

It is fail-closed and checks:

- manifest existence/readability;
- required evidence fields;
- real-and-traceable source classification;
- explicit `synthetic_data == false`;
- SHA-256 format;
- date range consistency;
- observed consecutive-day count;
- exact `coverage_ratio == 1.0`;
- zero unresolved conflicts;
- real observable receipt shape;
- timezone-aware receipt timestamp and no future receipt;
- canonical artifact path confined inside the evidence root;
- canonical artifact existence;
- artifact SHA-256 against actual bytes.

It never manufactures hashes, receipts, dates, coverage, or artifacts.

### 2. Contract upgraded

`contracts/s1_canonical_evidence_manifest.schema.json` moved from V1 to V2 semantics.

The contract now explicitly requires:

- `artifact_path`;
- `raw_artifact_sha256`;
- `synthetic_data`;

in addition to the existing provenance, coverage, receipt, and frozen canonical hash requirements.

### 3. Forensic FSM bridge

Added:

`tools/s1_admission_bridge.py`

This translates verifier output into the single Forensic FSM vocabulary:

```text
PASS
  -> S2_VALID_RESEARCH_EVALUABLE
  -> does NOT mean promotion

DENY / UNKNOWN
  -> S2_VALID_RESEARCH_UNREACHED
  -> promotion DENY
```

No downstream PASS inheritance is possible through this adapter.

### 4. Tests

Added:

- `tests/test_s1_canonical_evidence.py`
- `tests/test_s1_admission_bridge.py`

Tests use explicitly marked TEST_ONLY temporary fixtures. They are not production data and cannot be used as S1 evidence.

Covered cases include:

- missing manifest;
- complete test-only contract;
- wrong artifact hash;
- incomplete coverage;
- synthetic flag;
- bridge terminal DENY;
- bridge PASS only unlocking evaluation of the next gate.

## Deployment

A Render deployment was triggered against the exact current commit:

```text
commit = e434fe9a5318d6ce6b3f71768fcabfed932e346f
deploy = dep-da3r652jobas739icv2g
```

The deployment was observed as `build_in_progress` at the time of this action log. No promotion decision is based on build state.

## Important non-result

This action did NOT create or admit a real canonical dataset.

Therefore it does NOT change:

```text
S1_CANONICAL_EVIDENCE = BLOCKED
PROMOTION = DENY
S2 = LOCKED / UNREACHED
S3-S7 = LOCKED / UNREACHED
```

No synthetic production evidence was added.

## Parallel-work safety

This action intentionally did not overwrite:

- `state/current_state.json`;
- `state/next_action.json`.

The shared successor state remains authoritative. A later Bot must reconcile this immutable action log with the current state before making another promotion decision.

## Handoff

If the real canonical evidence package becomes available, run the S1 verifier against that exact manifest. Do not copy this test fixture. Do not infer PASS from crawler existence, runtime liveness, or database availability.

The immutable rule is:

```text
LIVE runtime != valid data
valid data != admitted canonical data
admitted canonical data != valid research
```
