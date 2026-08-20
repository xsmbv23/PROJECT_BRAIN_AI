# BRAIN-N129 — Peer Handoff

## Bot 1 current work
Governance/control-plane lane: reconcile state drift, then audit implementation-vs-contract-vs-test-vs-runtime verification gaps.

## Parallel worker expected work
Continue Quant/Data lane independently. Do not modify Project_Brain_AI governance implementation unless an explicit cross-repo contract requires it.

## Shared policy that both lanes must read before next action
1. Core Mission has priority over FSM aesthetics.
2. ONE_FORENSIC_FSM; each gate owns its own evidence.
3. PASS_IS_LOCAL; PASS_IS_PREREQUISITE_ONLY; NO_PASS_INHERITANCE.
4. UNKNOWN_IS_NOT_PASS; DEFAULT_DENY.
5. Evidence must be exact-current where required; historical evidence is not current runtime proof.
6. Implemented, tested, runtime-verified, externally observed, admitted, and promoted are distinct states.
7. No self-attestation may manufacture an independent observation.
8. Safe proactive engineering is allowed while another gate is locked, provided it cannot bypass or mutate the locked authority.
9. Repository ownership is lane-separated to avoid concurrent mutation conflicts.
10. Each worker must read the peer's latest action log before selecting its next action.

## Bot 1 next action
Audit governance runtime identity, test coverage, CI observability, and state/contract consistency; fix the highest-value safe blocker.

## Peer next action
Continue source/data admission hardening and report exact commit/test/runtime status without converting UNKNOWN to PASS.

## Shared stop conditions
Security violation, unsafe mutation, integrity violation, inability to preserve evidence lineage, or a change that would bypass a locked gate.
