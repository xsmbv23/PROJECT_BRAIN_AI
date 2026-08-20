# BRAIN-N130 — Action Receipt Nonce Hardening

## Pre-action reads
- Canonical state: `state/current_state.json`
- Canonical next action: `state/next_action.json`
- Proactive policy: `contracts/proactive_engineering_policy_v1.json`
- Peer handoff: `docs/action_log/2026-08-21_BRAIN-N129_PEER_HANDOFF.md`
- Prior Bot 1 work: `BRAIN-N128_DEPLOYMENT_IDENTITY_TEST_HARDENING`

## Blocker found
`tools/action_receipt_store.py` already issued `execution_nonce` and `issued_at`, but `tools/action_receipt_validator.py` did not validate either field. A forged or malformed receipt could therefore carry a syntactically valid receipt hash while bypassing the nonce/timestamp consistency intended by the receipt schema.

## Safe repair
Hardened `validate_action_receipt()` to require:
- `issued_at` exists and is parseable as an ISO timestamp;
- `execution_nonce` exists;
- `execution_nonce` exactly matches the deterministic nonce derived from action, commit, deployment, and issued timestamp.

Updated `tests/test_action_receipt_validator.py` with positive, missing-timestamp, and nonce-mismatch coverage.

Commits:
- validator: `7e3d8f28d68a1f9d46e1732ee53c1c544fb51afc`
- tests: `e024f4d4bee851ba092751d358d4cdea4970d3ed`

## Verification
GitHub combined status for `e024f4d4bee851ba092751d358d4cdea4970d3ed` currently exposes no status checks.

Therefore:
- IMPLEMENTED = YES
- TESTED = UNKNOWN
- RUNTIME_VERIFIED = UNKNOWN
- EXTERNAL_EVIDENCE = UNKNOWN
- PROMOTED = NO

## Admission impact
No change to `ACTION_SPACE=0`, `PROMOTION=DENY`, Room 02, staircase, or external-observation authority.
This repair only strengthens evidence validation.

## Freshness boundary
This change validates receipt timestamp structure and nonce integrity. It does NOT claim that the receipt is independently observed or that its timestamp is sufficiently fresh for an external-observation gate. Freshness remains a separate evidence requirement.

## Bot 1 next action
Re-read canonical state and peer handoff, then audit the next highest-value governance evidence-integrity gap that can be safely repaired without crossing the locked external-observation gate.

## Bot 2 expected next action
Continue the Quant/Data source-admission lane and report exact implementation/test/runtime status through its action log; do not alter Brain admission authority.

## Next real blocker
Runtime/CI observation remains unverified. Repository implementation and local test structure alone cannot promote this hardening to runtime PASS.
