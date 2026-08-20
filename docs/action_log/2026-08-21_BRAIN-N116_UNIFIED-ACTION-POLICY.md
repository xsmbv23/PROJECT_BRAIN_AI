# BRAIN-N116 — Unified Action Policy Synthesis

## Purpose

Persist the mandatory distinction discovered during N116 doctrine work:

- Core Mission = direction.
- Unified Action Policy = coherent reasoning and legal engineering selection.
- Forensic FSM = evidence admission and authority.

There is one Forensic FSM, not multiple forensic state machines.

## Mandatory rule

Every criterion received by Brain must be reconciled against the complete existing set of objectives, constraints, invariants, security rules, data rules, research rules, backtest rules, resource boundaries, architecture boundaries, evidence requirements, and action/promotion rules.

The result is one Unified Action Policy.

## Proactive engineering rule

When action space is legally available, Brain must proactively audit the entire system against the Core Mission, identify real blockers, classify them by authority and safety, and repair the highest-value legal blocker. It must then test, runtime-verify, capture evidence, and reassess the whole policy.

It must not optimize for commit count or wait for the user to discover every defect.

## Gate invariants

```text
PASS_IS_LOCAL
PASS_IS_PREREQUISITE_ONLY
NO_PASS_INHERITANCE
UNKNOWN_IS_NOT_PASS
DEFAULT_DENY
OWN_GATE_EVIDENCE_REQUIRED
FRESH_EVIDENCE_REQUIRED_FOR_PROMOTION
```

## State distinction

```text
IMPLEMENTED != TESTED != RUNTIME_VERIFIED != EVIDENCE_ADMITTED != PROMOTED != ACTION
```

`NaN`, `Inf`, `UNKNOWN`, `FAIL`, missing, stale, or unresolved evidence cannot be used to rescue downstream aggregates.

## Current canonical state preserved

```text
BRAIN-N116_WAIT_EXTERNAL_OBSERVATION
ACTION_SPACE = 0
MANDATORY_NO_OP
PROMOTION = DENY
```

This policy extension does not alter the canonical next action and does not unlock Room 02 or the staircase.

## Successor instruction

A successor Bot must read this action log plus `docs/forensic/UNIFIED_ACTION_POLICY_V1.md`, then recover `state/current_state.json`, `state/next_action.json`, and immutable action history before selecting any future action.
