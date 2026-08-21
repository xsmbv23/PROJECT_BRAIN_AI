# BRAIN-N142 — Strict Research Admission Evidence Gate

## Peer-first requirement

Bot 1 first read the current Quant Engine `state/next_action.json` and `QUANT-N010_EXECUTION.md`. Quant N010 remains READY and its completion gate requires an independently observable GitHub workflow execution receipt. Brain remains `BRAIN-N125_WAIT_EXTERNAL`, `ACTION_SPACE=0`, `PROMOTION=DENY`.

## Finding

The existing research-dataset validator can establish structural/internal consistency of a claimant-supplied receipt, but a non-empty temporal evidence reference and claimant-supplied manifest SHA-256 do not independently prove that the referenced date manifest exists or resolves to the claimed hash.

## Action

Added `tools/research_dataset_admission_gate.py` as a strict consumer boundary. It requires a separately produced evidence-resolution result with:

- `status=VERIFIED`
- non-empty `verifier_reference`
- `resolved_manifest_sha256` exactly matching the receipt's `date_manifest_sha256`

Without that independent resolution, result is `UNKNOWN`, never `ADMITTED`.

Added regression tests in `tests/test_research_dataset_admission_gate.py` covering absent, unverified, and verified/matching evidence resolution.

## Semantics

`SCHEMA_VALID` or an existing validator `ADMITTED` result is not treated as independent admission. Only the strict gate may produce `ADMITTED`, and that means research eligibility only.

`ADMITTED` still does not imply canonical promotion, edge, EV/P&L, or action authorization.

## Handoff to Quant Engine

Quant Engine must eventually emit a deterministically derived, independently resolvable temporal evidence artifact/reference from actual `DayRecord.date` values. The Brain gate will consume the independently resolved evidence; it will not accept self-attested existence as proof.

## Verification state

IMPLEMENTED = YES
TESTED = UNKNOWN
RUNTIME_VERIFIED = UNKNOWN
PROMOTED = NO
