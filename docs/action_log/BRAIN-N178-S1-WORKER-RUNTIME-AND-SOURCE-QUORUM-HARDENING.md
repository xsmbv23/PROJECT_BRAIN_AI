# BRAIN-N178 — S1 Worker Runtime + Source Quorum Hardening

## Objective
Continue N175 autonomously without promotion. Close false-positive paths between worker reachability, runtime execution evidence, source quorum, and durable evidence.

## Changes

### Project_Brain_AI
- Added `contracts/worker_runtime_receipt.schema.json`.
- Added `core/worker_runtime_receipt.py` and tests.
- Added CI workflow `.github/workflows/worker-runtime-receipt-verifier.yml`.
- Hardened `.github/workflows/n175-triple-worker-probe.yml` so HTTP reachability + identity alone can no longer yield PASS. Runtime PASS now requires task/worker/input/model lineage and a fresh runtime PASS result.
- Existing worker execution guard remains fail-closed on allocation/cycle/task/worker/input/hash/model mismatch.

### Quant_Engine
- Hardened `bot2_headless_worker.py`: missing allocation lineage, missing input artifact, path escape, or SHA-256 mismatch now yields HOLD.
- Hardened `verification/real_source_quorum_probe.py` to accept an explicit target date and record semantic SHA-256 separately from raw-byte SHA-256.
- Added `.github/workflows/real-source-quorum.yml` for manual/scheduled/push-triggered two-source candidate evidence.

## Current Evidence
- N175 canonical state remains DATA_ADMISSION / IN_PROGRESS.
- Required S1 evidence remains: lawful provenance, acquisition channel/reference, timestamp, raw SHA-256, complete consecutive coverage, coverage_ratio=1.0, zero unresolved conflicts, fresh admission receipt, frozen canonical hash.
- Existing raw capture inventory is OBSERVATION_ONLY/PARTIAL and therefore not admissible.
- A live web cross-check for 2026-08-12 shows ketqua16 and xsmb.com.vn publish the same FULL_27 result; this is contextual candidate evidence only and does not replace exact raw-byte capture or durable admission evidence.

## Denial Boundary
S1 remains DENY. No state mutation, promotion, or downstream research claim is authorized by this action.

## Next Action
1. Verify the new worker runtime guard against deployed Render entrypoints.
2. Obtain a fresh two-source acquisition run with exact raw artifacts, semantic hashes, and complete coverage.
3. Persist the compact admission envelope through the configured durable sink.
4. Only after all own-gate predicates are fresh and independently evidenced may S1 be reconsidered.
