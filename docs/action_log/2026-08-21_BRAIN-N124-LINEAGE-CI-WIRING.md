# BRAIN-N124 — Lineage Validator CI Wiring

## Objective
Connect the non-authoritative evidence lineage validator to the repository's existing foundation CI without changing runtime admission authority.

## Changes
- Added unittest-compatible coverage at `tests/test_evidence_lineage_validator_unittest.py`.
- Updated `.github/workflows/foundation.yml` to execute the lineage validator tests.

## Concurrent-edit handling
A direct replacement of the earlier pytest-style test file was rejected with a GitHub 409 because the file had changed concurrently. The current file was re-read before adding a separate unittest-compatible test surface. No force overwrite was used.

## Verification status
- CI wiring implemented: YES
- Current CI execution receipt observed by this action: UNKNOWN
- Test PASS: NOT CLAIMED
- Runtime admission: unchanged / DENY
- Promotion: DENY

## Safety
No external observation was manufactured. No source truth was mutated. No Room 02/staircase unlock. No credentials or secrets. No promotion.

## Own next action
`BRAIN-N125` — inspect the current CI execution result for the new lineage tests and, if execution evidence is available, reconcile any failures against the validator/contract. Do not convert implementation into PASS without current execution evidence.

## Peer dependency
Peer remains `QUANT-N007`: source-specific semantic extraction and CI observation for `ketqua16.net` and `xsmb.com.vn`, with canonical promotion denied.
