# BRAIN-N139 — Temporal Evidence Hardening

## Peer prerequisite read

Before this action Brain read `Quant_Engine/state/next_action.json` and confirmed the peer remains at `QUANT-N010`, with `RESEARCH_DATASET_ADMISSION` queued after workflow evidence. No Brain promotion or external gate was opened.

## Finding

The Brain research-dataset consumer previously validated temporal claims from receipt fields such as `contiguous`, `missing_days`, `start_date`, and `actual_days`, but did not require a traceable temporal evidence reference or a date-manifest digest.

Those fields can be internally consistent while still being claimant-supplied assertions. Consistency is necessary but not sufficient for forensic admission.

## Change

Hardened `RESEARCH_DATASET_ADMISSION_CONSUMER_V1` to require:

- `temporal_evidence_reference`
- `date_manifest_sha256`

The validator now rejects malformed/non-SHA256 date-manifest hashes.

The contract explicitly distinguishes a date-manifest hash from a raw-byte hash.

## Gate semantics

This change only hardens the research-eligibility consumer gate.

It does NOT establish:

- canonical source truth
- source quorum
- edge
- EV/P&L
- promotion
- controlled action

## Required peer handoff

Quant Engine must produce a traceable temporal evidence artifact/reference and a deterministic SHA-256 over the date manifest before Brain can treat a future research-admission receipt as sufficiently evidenced.

The date-manifest digest is not itself proof of source truth; it is evidence that the temporal claim is bound to a concrete date set.

## Verification status

IMPLEMENTED = YES
TESTED = UNKNOWN
RUNTIME_VERIFIED = UNKNOWN
PROMOTED = NO

## Canonical Brain authority

`BRAIN-N125_WAIT_EXTERNAL` remains unchanged.
`ACTION_SPACE = 0`.
`PROMOTION = DENY`.

This action is parallel-safe engineering and does not unlock any blocked gate.
