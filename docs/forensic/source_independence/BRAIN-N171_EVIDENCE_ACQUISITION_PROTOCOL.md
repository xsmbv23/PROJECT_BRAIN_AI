# BRAIN-N171 — S1 Evidence Acquisition Protocol

## Decision

S1 must not depend on automatic scraping of multiple public websites.

Automatic source independence remains a valuable corroboration signal, but it is not the only admissible route to real, traceable canonical evidence.

## Admissible channels

1. `AUTOMATED_SOURCE_WITH_EXPLICIT_PERMISSION`
2. `MANUAL_AUTHORIZED_CAPTURE`
3. `DURABLE_ARCHIVE_EXPORT`

## Required evidence for every channel

- real source provenance;
- exact acquisition timestamp;
- immutable raw artifact;
- raw-byte SHA-256;
- resolved artifact path inside the evidence root;
- consecutive-date coverage with `coverage_ratio = 1.0`;
- zero unresolved conflicts;
- real observable admission receipt;
- frozen canonical SHA-256;
- `synthetic_data = false`.

## Channel-specific evidence

### Automated source with explicit permission

The evidence bundle must include a permission reference, source identity, retrieval timestamp, and raw artifact identity.

### Manual authorized capture

The evidence bundle must include operator identity, authorization reference, capture timestamp, and immutable raw artifact identity.

### Durable archive export

The evidence bundle must include archive identity, export timestamp, archive provenance, and immutable raw artifact identity.

## Independence semantics

`SOURCE_INDEPENDENCE = DENY` does not imply `REAL_DATA = DENY` when an independently authorized/manual/archive evidence path satisfies the full S1 contract.

Conversely, network-owner diversity alone never implies canonical truth.

## Prohibited shortcuts

- scraping a source whose terms prohibit automation;
- treating matching web tables as independent truth;
- using ChatGPT/chat logs as evidence;
- generating synthetic history to fill missing dates;
- modifying raw artifacts to remove advertisements or other non-truth content;
- converting runtime liveness, test PASS, or Render deployment status into S1 PASS.

## E2E consequence

Once a lawful evidence bundle satisfies S1_CANONICAL_EVIDENCE_V2, S2 may be opened. Until then S1 remains DENY and S2-S7 remain locked.

## Next action

Collect or receive one lawful evidence bundle through one admissible channel, validate it against `contracts/s1_canonical_evidence_manifest.schema.json`, and produce a fresh S1 admission receipt. Do not alter the historical N170 DENY decision.
