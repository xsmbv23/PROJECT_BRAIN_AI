# BRAIN-N158 — E2E segment reachability guard

## Peer position

Quant Engine remains at QUANT-N010. Exact-current GitHub workflow-run observation for the triggering commit returned zero observable workflow runs, so N010 execution evidence remains UNKNOWN. No Brain gate or promotion state is changed.

## E2E blocker

The persistent state already described the Core Mission as S1 REAL_DATA -> S2 VALID_RESEARCH -> S3 VALID_BACKTEST -> S4 EDGE -> S5 EV_PNL_ROI -> S6 ROBUSTNESS_RISK_DRIFT -> S7 CONTROLLED_ACTION, but there was no machine-checkable guard preventing a downstream segment from being treated as reachable before its predecessor had its own independently verified exit evidence.

## Fix

Added `tools/e2e_segment_guard.py` with `segment_reachable()`.

Rules:

- S1 is the root segment.
- Every later segment requires the immediate predecessor to be `VERIFIED`.
- The predecessor must have a non-empty `exit_evidence_ref`.
- Duplicate segment state is denied.
- Unknown segment status is denied.
- VERIFIED is reachability evidence only; it does not grant PASS, promotion, or action authority to the downstream segment.

Added `tests/test_e2e_segment_guard.py` covering missing predecessor, unverified predecessor, missing exit evidence, verified predecessor, duplicate segment state, and invalid status.

## E2E consequence

Current segment remains S2_VALID_RESEARCH.
S3/S4/S5/S6/S7 remain unreachable until their immediate predecessor exit criteria are independently satisfied.

## Verification semantics

IMPLEMENTED = YES
TESTED = UNKNOWN
RUNTIME_VERIFIED = UNKNOWN
EXTERNAL_EVIDENCE = UNKNOWN
PROMOTED = NO

## Peer required next action

Quant Bot should continue QUANT-N010 and produce independently observable workflow run/attempt/commit/result evidence when available.

## Own next action

Re-read Quant state/log, then continue the highest-value safe Brain-side E2E blocker audit without opening S3 or any later gate.
