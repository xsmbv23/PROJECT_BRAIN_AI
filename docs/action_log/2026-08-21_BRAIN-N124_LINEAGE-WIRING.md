# BRAIN-N124 — Evidence Lineage Wiring / Schema Audit

## SESSION
DUAL-BOT-2026-08-21

## BOT
BOT_1 / Project_Brain_AI

## MANDATORY PRE-ACTION READS
- Brain current state: `state/current_state.json` — exact-current state says one Forensic FSM, PASS-is-local, no PASS inheritance, default deny, Brain = governance control plane, and current promotion DENY. 
- Brain next action: `state/next_action.json` — N124 READY; explicit scope is lineage validator wiring and producer/consumer audit.
- Shared coordination contract: `contracts/dual_bot_coordination_v1.json` — independent safe engineering may run in parallel; locked gates block only dependent actions; every action must record ownership/evidence/handoff.
- Forensic doctrine: `docs/forensic/FORENSIC_FSM_VS_CORE_MISSION.md` — ONE Forensic FSM; Core Mission remains primary direction; every gate owns its own evidence; DB_EXISTENCE != DB_BINDING != DB_TLS_ADMISSION != DB_ROUND_TRIP != PROMOTION.
- Other bot latest log: `xsmbv23/Quant_Engine/docs/action_log/2026-08-21_QUANT-N006.md` — BOT_2 fixed semantic quorum so independent-source agreement uses semantic fingerprint rather than raw byte hash; same-source duplicates cannot satisfy quorum; canonical promotion remains blocked.

## OBJECTIVE
Wire evidence-lineage validation into the current CI surface and remove a real provenance/schema mismatch without opening any locked gate.

## OBSERVED BLOCKER
The canonical lineage contract uses `raw_artifact_sha256` and `semantic_fingerprint`, while the validator primarily used legacy aliases `raw_sha256` and `semantic_sha256`. This created a schema drift risk: a correctly emitted canonical evidence object could be evaluated differently from the contract.

## ACTION TAKEN
1. Updated `tools/evidence_lineage_validator.py` to make canonical contract field names authoritative.
2. Kept legacy hash aliases readable for backward-compatible fixtures only.
3. Added explicit DENY when a declared raw artifact has no raw artifact SHA-256.
4. Added explicit DENY when semantic quorum is declared without a semantic fingerprint.
5. Preserved the hard rule that raw byte identity and semantic meaning are distinct.
6. Added regression coverage proving same-value raw/semantic hashes are rejected unless explicitly declared distinct.
7. Added regression coverage proving the validator does not mutate supplied evidence.
8. Confirmed the existing `foundation.yml` workflow already executes the lineage validator test suite; no second competing CI path was created.

## EVIDENCE
- Canonical contract: `contracts/evidence_lineage_admission_v1.json` requires raw artifact hash when raw artifacts exist, semantic fingerprint for semantic quorum, upstream evidence IDs/derivation contract for derived evidence, runtime identity/gate evidence ID for runtime admission, and canonical payload SHA for promoted canonical envelopes.
- Current CI workflow runs `tests/test_evidence_lineage_validator_unittest.py` as part of Foundation verification.
- Other bot N006 confirms the cross-source semantic quorum contract and explicitly forbids promotion inheritance.

## VERIFICATION LEVEL
FIXED + WIRED_TO_CI; CI observation is still required before claiming TESTED/RUNTIME_VERIFIED for this exact commit.

## PROMOTION
DENY. No state, Room 02, staircase, or action authority was opened.

## UNRESOLVED
- Exact-current external governance observation gate remains unresolved.
- Real-source semantic extraction for ketqua16.net and xsmb.com.vn remains BOT_2 domain work.
- Durable action receipt current-observation proof remains separate from lineage validation.

## BOT_2 HANDOFF
Continue source-specific semantic extraction/quorum work under QUANT-N007; do not promote canonical source truth. The semantic fingerprint produced by BOT_2 is an input prerequisite only and must carry upstream evidence IDs into derived evidence.

## BOT_1 NEXT
`BRAIN-N125` — observe the exact-current CI result for this commit, then perform a machine-readable producer/consumer audit report. If CI is not observable, mark verification UNKNOWN rather than PASS.

## COMPLETION GATE
N124 is structurally complete when the validator is in the current Foundation CI path and all known lineage schema requirements are represented by tests; final verification remains UNKNOWN until the exact commit's CI result is independently observed.
