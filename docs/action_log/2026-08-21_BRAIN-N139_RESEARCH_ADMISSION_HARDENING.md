# BRAIN-N139 — Research Dataset Admission Hardening

## Peer synchronization

Before acting, Brain read the peer Quant Engine `state/next_action.json` and confirmed `QUANT-N010` remains active, with `RESEARCH_DATASET_ADMISSION` queued next. Brain also read its own current state: `BRAIN-N125_WAIT_EXTERNAL`, `action_space=0`, `promotion=DENY`.

## Finding

The Brain-side research-dataset consumer accepted a caller-controlled `required_days` value as the admission threshold. That allowed a malformed receipt to lower the threshold below the policy minimum. The validator also did not reject empty provenance/identity fields or malformed ISO dates.

This was a real admission-integrity blocker because research eligibility must be derived from the policy contract, not from a value supplied by the evidence claimant.

## Repair

Hardened `tools/research_dataset_admission_validator.py`:
- policy minimum required history is fixed at 41 calendar days;
- provenance, dataset identity, canonical input reference and code version must be non-empty strings;
- counts must be exact integers;
- start/end dates must be valid ISO dates;
- train/test minimums remain 20/20;
- temporal policy remains `DATE_ALIGNED_NO_LOOKAHEAD`;
- contiguity and empty missing-day set remain mandatory;
- admission remains research-eligibility-only.

Added regression tests for threshold tampering, empty provenance, and invalid dates.

## Commits

- validator: `b1e30a84adee34165193eb80f2f2a03f14434a9a`
- tests: `6f833f7efdc3650279dec7e465e973600fcf11f7`

## Verification semantics

IMPLEMENTED = YES
TESTED = UNKNOWN
RUNTIME_VERIFIED = UNKNOWN
PROMOTED = NO

No claim of test execution is made by this log.

## Peer handoff

Quant Engine must continue its own `QUANT-N010` execution/evidence work and, when producing a research-dataset admission receipt, must not rely on Brain's validator as proof of dataset truth. Brain will validate the resulting receipt independently.

## Next action

Read the newest Quant Engine action log and exact research-dataset admission implementation before any further mutation. If the peer's implementation introduces a conflicting temporal or admission rule, record a reconciliation/objection before changing Brain. Otherwise continue with the highest-value safe blocker on the REAL DATA -> RESEARCH -> BACKTEST path without unlocking the external Brain gate.
