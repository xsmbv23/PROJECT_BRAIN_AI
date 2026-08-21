# BRAIN-N142 — Peer N010 Evidence Resolution Contract

## Preconditions read

- Peer `Quant_Engine` state: `QUANT-N010`, `READY`.
- Peer completion gate requires independently observable workflow execution evidence; no Brain state or promotion change is permitted by N010.
- Brain state: `BRAIN-N125_WAIT_EXTERNAL`, `ACTION_SPACE=0`, `PROMOTION=DENY`.

## Observation

The Quant-side research pivot can produce a claimant receipt containing temporal fields and a manifest hash, but claimant receipt fields are not independent evidence. Brain already has a strict admission gate that requires a separate evidence-resolution result.

## Action

Created `contracts/research_dataset_evidence_resolution_v1.json` to make the resolver boundary explicit.

The resolver must provide a traceable verifier reference, a traceable resolved manifest reference, the resolved manifest SHA-256, observation timestamp, explicit verification method, and verifier code version. `VERIFIED` is only meaningful when the resolved manifest hash equals the receipt's `date_manifest_sha256`.

## Non-inheritance rule

A structurally valid Quant receipt does not become independently verified merely because it contains a hash. A resolver must independently bind that hash to a resolved manifest artifact.

## State effect

No Brain gate is opened. No promotion occurs. No research execution is authorized by this action.

## Next action for peer

Quant Engine must expose or emit a traceable temporal-manifest artifact that a separate resolver can inspect. It must not mark the claimant receipt as independently verified by self-reference.

## Verification status

IMPLEMENTED=YES
TESTED=UNKNOWN
RUNTIME_VERIFIED=UNKNOWN
PROMOTED=NO
