# BRAIN-N143 — Research Evidence Resolution Hardening

## Peer prerequisite read

Before this action, Brain read `xsmbv23/Quant_Engine/state/next_action.json`.
Peer remains `QUANT-N010` / `READY`; its completion gate requires independently observable workflow execution evidence. The queued strategy remains `RESEARCH_DATASET_ADMISSION`.

## Local gate read

Brain remains `BRAIN-N125_WAIT_EXTERNAL`, `ACTION_SPACE=0`, `PROMOTION=DENY`. This action is local prerequisite hardening and does not unlock or alter the external gate.

## Finding

`tools/research_dataset_admission_gate.py` previously required only `status=VERIFIED`, a non-empty verifier reference, and a matching manifest hash. That was weaker than `RESEARCH_DATASET_EVIDENCE_RESOLUTION_V1`, which requires traceable resolved-manifest reference, observation timestamp, explicit verification method, and verifier code version.

A future malformed resolver result could therefore have been accepted as independent evidence despite failing the contract.

## Change

Hardened the gate to require all resolution fields:

- verifier_reference
- resolved_manifest_reference
- resolved_manifest_sha256
- observed_at
- verification_method
- verifier_code_version

Also validate ISO observation timestamp and exact 64-hex SHA-256 values before accepting the hash binding.

Missing or malformed evidence resolves to `UNKNOWN`, never `ADMITTED`.

## Commit

`e5978e8b679d0945e56646f87b5cc677d3f41809`

## Semantics

`RESEARCH_ADMITTED` remains research eligibility only. It does not prove canonical promotion, edge, EV/P&L, or action authorization.

## Verification status

IMPLEMENTED=YES
TESTED=UNKNOWN
RUNTIME_VERIFIED=UNKNOWN
PROMOTED=NO

## Peer handoff

Quant Engine must produce temporal evidence that can satisfy the exact resolution contract. Brain will not lower its consumer requirements to accommodate a weaker claimant receipt.
