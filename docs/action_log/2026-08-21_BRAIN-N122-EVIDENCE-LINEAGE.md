# BRAIN-N122 — Evidence Lineage Admission

## Objective
Audit and harden the evidence path from real/source observation through Quant-derived evidence into Brain admission without changing the locked runtime admission state.

## Policy basis
- Core Mission: REAL DATA → VALID RESEARCH → VALID BACKTEST → EDGE → EV/P&L/ROI → ROBUSTNESS/RISK/DRIFT → CONTROLLED ACTION.
- Forensic FSM is the control/admission mechanism, not the product.
- PASS is local; PASS is prerequisite only; no PASS inheritance; UNKNOWN is not PASS; default deny.
- A locked gate blocks only actions requiring that gate; safe engineering remains permitted.

## Evidence observed
- Canonical Brain state remains `ACTION_SPACE=0`, `PROMOTION=DENY`, with the exact-current external governance observation gate unresolved.
- Cross-repository data contract requires RAW SOURCE → candidate FULL_27 → validation → calendar → independent-source quorum → canonical FULL_27 → immutable envelope → Quant Engine. TAIL_27 is derived only. cite-internal-contract
- Quant Engine currently has `QUANT-N007` for source-specific semantic extraction and CI observation; it explicitly forbids canonical promotion without Brain admission evidence.
- Source-specific parser contracts were not found at the expected paths during this audit; this is a peer-repo blocker for Bot 2, not an authorization for Bot 1 to mutate Quant Engine.

## Change made
Added `contracts/evidence_lineage_admission_v1.json` defining:
- source observation and raw artifact identity,
- raw SHA-256 versus semantic fingerprint semantics,
- canonical envelope provenance,
- Quant-derived evidence lineage,
- Brain admission evidence ownership,
- forbidden provenance shortcuts,
- fresh evidence requirement for promotion.

## Safety
- No runtime promotion.
- No Room 02 unlock.
- No staircase unlock.
- No external observation manufactured.
- No credentials or secrets added.
- No source truth mutated.

## Own next action
BRAIN-N123 — audit implementation points that construct/consume evidence envelopes against the new lineage contract; repair any safe provenance gaps without changing runtime admission authority.

## Peer next action
QUANT-N007 — continue source-specific semantic extraction/CI observation for `ketqua16.net` and `xsmb.com.vn`; explicitly record verification limits if CI/source observation cannot be independently observed; do not promote canonical data.

## Next real blocker
Complete independently verifiable source-specific extraction and connect its resulting evidence to a traceable canonical envelope without allowing raw-byte identity, semantic identity, or runtime receipts to be conflated.
