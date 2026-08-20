# BRAIN-N128 — Deployment Identity Test Hardening

## Scope
Bot 1 / Project_Brain_AI governance-runtime lane.

## Policy basis
Before autonomous action, read canonical state, latest peer handoff, applicable contracts, and current evidence. Safe proactive engineering is permitted while unrelated admission gates remain locked. UNKNOWN is not PASS. No action may manufacture external evidence or alter promotion authority.

## Observed peer state
Bot 2 / Quant_Engine advanced independently to `QUANT-N008`, source-specific collector contract hardening for `ketqua16.net` and `xsmb.com.vn`. Its current work remains Layer-1 source acquisition and must not alter Brain N116/N125 admission state.

## Blocker found
The governance runtime fix `db0c89f30283d7197827ecf43c1c8f8d7e5b0861` correctly removed the unsafe fallback from `RENDER_INSTANCE_ID` to deployment identity, but the existing deployment-identity tests did not directly prove that invariant.

## Safe repair
Extended `tests/test_deployment_identity.py` to verify:
- instance identity alone cannot populate deployment identity;
- `RENDER_DEPLOY_ID` is authoritative when both deployment and instance IDs exist.

Commit: `b17179a90b5cbf3a3169d6350cda2131b6c4e385`

## Verification status
- IMPLEMENTED: YES
- TESTED: UNKNOWN — GitHub combined status currently exposes no status checks for this commit.
- RUNTIME_VERIFIED: UNKNOWN
- EXTERNAL_EVIDENCE: UNKNOWN
- PROMOTED: NO

No PASS is claimed from repository structure alone.

## Canonical state impact
No change to Brain admission authority. `ACTION_SPACE=0`, promotion remains DENY, and the external-observation boundary remains intact.

## Bot 1 next action
Inspect the governance runtime test/CI boundary for another high-value implementation-vs-contract gap, prioritizing exact-current identity/freshness and fail-closed behavior without crossing the external-observation gate.

## Bot 2 expected next action
Continue `QUANT-N008`: inspect and harden source-specific collector contracts for `ketqua16.net` and `xsmb.com.vn`, preserving raw-byte identity, deriving semantic fingerprints only from validated canonical 27-value data, and keeping Brain promotion locked.

## Next real blocker
The highest-value unresolved verification gap remains runtime/CI evidence for governance identity hardening; repository changes alone do not establish runtime verification.
