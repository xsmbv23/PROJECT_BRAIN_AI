# BRAIN-N161 — E2E S1/S2 data evidence blocker

## Peer context

Bot 2 remains on QUANT-N010. Brain continues to observe peer work without modifying Quant_Engine ownership. The Render runtime boundary is live, but runtime liveness is not research-data evidence.

## E2E position

S1 REAL_DATA
  -> S2 VALID_RESEARCH [CURRENT BLOCKER]
  -> S3 VALID_BACKTEST [UNREACHED]
  -> S4 EDGE [UNREACHED]
  -> S5 EV_PNL_ROI [UNREACHED]
  -> S6 ROBUSTNESS_RISK_DRIFT [UNREACHED]
  -> S7 CONTROLLED_ACTION [UNREACHED]

## Blocker found

The `xsmb-quant` repository currently exposes the data-foundation scaffold (contracts, ingestion, calendar, reconciliation, forensic crawler and source registry), but the inspected repository tree does not show a canonical FULL_27 dataset artifact or a durable evidence manifest proving calendar-complete, provenance-backed, quorum-admitted history. The `evidence/` tree currently exposes `external/` and `runtime/` directories rather than a visible admitted canonical dataset artifact.

This does NOT prove that no data exists outside Git. It proves only that repository inspection does not provide the evidence required to treat S1 as admitted.

## Policy consequence

- Repository structure is not data evidence.
- Render liveness is not data evidence.
- Source registry entries are not observed source results.
- Parser implementation is not canonical history.
- Historical Excel is reconciliation/reference only.
- S1 must remain unverified until durable raw artifacts, FULL_27 validation, calendar state, provenance and >=2-source quorum evidence are independently observable.
- S2 cannot be verified before its own date-aligned/no-lookahead evidence exists.
- S3 may be prepared safely but remains UNREACHED.

## Safe parallel work

Bot 2 may continue QUANT-N010 workflow-evidence hardening and bounded research-admission implementation. Brain may continue S2 admission/governance hardening and S3 preparation. Neither may infer S1/S2 PASS or unlock downstream gates.

## Peer required next action

Quant/data side: produce an independently observable durable data-foundation evidence package (or an explicit external evidence reference) containing at minimum canonical date coverage, FULL_27 validation receipts, raw artifact identity, source independence/quorum, conflict/unknown ledger and a reproducible manifest. If the data is intentionally stored outside Git, record the authoritative sink and exact observable receipt; do not add fake data to the repository just to satisfy the gate.

## Own next action

Continue E2E from S1/S2: audit the admission boundary for whether these evidence requirements are machine-checkable, then prepare the S3 backtest contract and ordering/OOS guard without marking S3 reachable.

## Verification semantics

IMPLEMENTED = YES (policy/log only)
DATA_EVIDENCE = UNKNOWN
S1 = UNKNOWN
S2 = UNKNOWN
S3 = UNREACHED
PROMOTED = NO
