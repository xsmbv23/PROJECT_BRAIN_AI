# BRAIN-N177 — S1 → Worker lineage hardening

## Objective
Close the boundary between an admitted canonical S1 artifact and worker execution without changing canonical state or claiming S1 PASS.

## Changes
- Added `contracts/worker_execution_input.schema.json`.
- Added `core/worker_execution_guard.py`.
- Added `core/worker_execution_guard_test.py`.
- Guard is fail-closed and verifies allocation/cycle/task/worker/model lineage plus exact input artifact SHA-256.

## Invariants
- Worker execution cannot claim a different allocation, cycle, task, worker, or model version than the allocation.
- Input artifact must remain under the configured artifact root.
- Input bytes must match the declared SHA-256.
- Missing or mismatched lineage is DENY.
- This change does not promote S1 and does not mutate canonical state.

## Evidence status
Implementation committed to `main`; runtime CI execution remains the verification boundary. No S1 PASS is claimed.

## Next action
Integrate the guard into the actual worker entrypoint/allocation execution path, then run CI verification. After the guard is enforced, return to S1 real-data admission evidence gaps (authorized acquisition, full coverage, conflict=0, canonical freeze, admission receipt).
