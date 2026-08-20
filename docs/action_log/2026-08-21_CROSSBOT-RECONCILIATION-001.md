# CROSSBOT-RECONCILIATION-001

## Purpose

Record the mandatory cross-Bot reconciliation performed before autonomous continuation.

## Brain authority observed

`Project_Brain_AI/state/current_state.json` currently establishes:

- ONE_FORENSIC_FSM
- PASS_IS_LOCAL
- PASS_IS_PREREQUISITE_ONLY
- NO_PASS_INHERITANCE
- UNKNOWN_IS_NOT_PASS
- DEFAULT_DENY
- OWN_GATE_EVIDENCE_REQUIRED
- FRESH_EVIDENCE_REQUIRED_FOR_PROMOTION
- database admission chain: DB_EXISTENCE -> DB_BINDING -> SECRET_RESOLUTION -> DB_TLS_ADMISSION -> NETWORK_ORIGIN_PROOF -> DB_ROUND_TRIP -> PROMOTION
- current promotion = DENY
- Brain action space = 0
- next Brain action = BRAIN-N125_WAIT_EXTERNAL
- safe parallel Quant work is explicitly allowed as LOCAL_PREREQUISITE_ONLY

## Quant authority observed

`Quant_Engine/state/current_state.json` reported QUANT-N008 as completed/hardened and pointed to QUANT-N009.

However `Quant_Engine/state/next_action.json` still declared QUANT-N008 as READY.

This was a real state-machine pointer divergence.

## Response

The divergence was NOT interpreted as permission to unlock Brain.

The safe interpretation is:

```text
Brain gate authority = WAIT_EXTERNAL / DENY
Quant Room 01        = allowed to continue local prerequisite work
```

The Quant Bot was allowed to complete QUANT-N009. Its stale next-action pointer was repaired and advanced to QUANT-N010.

## QUANT-N009 work performed

Two source-specific semantic parser contracts were added:

- ketqua16.net
- xsmb.com.vn

Both enforce:

- exact raw artifact + matching raw SHA
- source identity + runtime identity
- official result panel as sole truth-bearing page region
- advertising/navigation/header/footer/page-number chrome as non-truth
- ambiguous panel = DENY
- exactly 27 canonical XSMB positions
- missing/duplicate/unmapped position = DENY
- semantic SHA only over canonical 27-value domain
- compact failure receipt only
- immutable raw artifact
- promotion forbidden in Room 01

## Forensic challenge to existing CI

The existing Quant workflow generated a JSON artifact with `status=PASS` and `evidence_score=1` without executing the actual repository verifiers/tests. This is not equivalent to independent runtime evidence.

The workflow was hardened to:

1. execute source-contract verification,
2. execute semantic-parser-contract verification,
3. execute repository tests,
4. emit a receipt explicitly labeled `REPOSITORY_VERIFIER_EXECUTION`,
5. explicitly state `external_runtime_truth = NOT_PROVEN`.

This is an evidence-semantics correction, not a Brain promotion event.

## Immutable boundary

No Brain promotion state was changed.

No Room 02 unlock was performed.

No Staircase unlock was performed.

No credential was exposed.

## Rule for successor Bots

A successor must reconcile BOTH:

```text
Brain authoritative state
+
Quant local projected state
```

before acting.

If their pointers disagree, do not guess. Record the divergence, identify the authoritative gate, repair only the local projection if safe, and never convert a local prerequisite PASS into a Brain promotion.
