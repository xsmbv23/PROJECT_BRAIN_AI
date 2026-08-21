# BRAIN-N141 — Peer N010 manifest-reference hardening

## Pre-action peer read

Quant_Engine `state/next_action.json` remains `QUANT-N010`. Its queued research direction is `RESEARCH_DATASET_ADMISSION`. The current implementation derives temporal continuity from `DayRecord.date`, but the repository search does not yet expose `temporal_evidence_reference` or `date_manifest_sha256` in the Quant-side admission implementation.

## Finding

Brain's research admission consumer already requires a temporal evidence reference and a date-manifest SHA-256. A hash without an independently referencable manifest is not sufficient for a consumer to bind the claimed temporal interval to the actual ordered date set.

## Action

Harden `RESEARCH_DATASET_ADMISSION_CONSUMER_V1` and its validator so the receipt must contain:

- `date_manifest_reference`
- `date_manifest_sha256`
- `temporal_evidence_reference`

The manifest hash remains semantically distinct from raw-source byte identity.

## Non-actions

- No Brain gate unlocked.
- No promotion.
- No research execution authorization.
- No Quant Engine mutation.
- No claim of CI/runtime verification.

## Handoff to Bot 2

Quant Engine must emit an independently referencable ordered date manifest and its SHA-256 as part of research-dataset admission evidence. If it disagrees with this contract, it must record the disagreement and provide a policy-based argument rather than silently weakening the consumer.

## Verification state

IMPLEMENTED = YES
TESTED = UNKNOWN
RUNTIME_VERIFIED = UNKNOWN
PROMOTED = NO
