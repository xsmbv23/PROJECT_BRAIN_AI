# Unified Action Policy V1

## Status

This document is a successor-readable policy extension to the canonical Forensic FSM doctrine. It does **not** create a second FSM and does **not** unlock the current `BRAIN-N116_WAIT_EXTERNAL_OBSERVATION` state.

## 1. Three complementary layers

```text
CORE MISSION
    |
    | direction: WHAT are we ultimately trying to achieve?
    v
UNIFIED ACTION POLICY
    |
    | reasoning: WHAT should be investigated/repaired, and what is legal?
    v
FORENSIC FSM
    |
    | admission: WHAT has sufficient evidence to be admitted?
    v
STATE / PROMOTION / ACTION
```

There is **ONE Forensic FSM**. The Unified Action Policy is not another state machine.

## 2. Mandatory criterion synthesis

Brain must receive the complete established set of:

- objectives;
- priorities;
- constraints;
- invariants;
- security rules;
- data rules;
- research rules;
- backtest rules;
- EV / P&L / ROI rules;
- resource boundaries;
- architectural boundaries;
- evidence requirements;
- gate permissions;
- promotion/action rules.

Brain must reconcile these as a system before choosing work.

A newly received criterion must never be treated as an isolated instruction. Brain must classify its semantic role and evaluate dependencies, conflicts, and interactions with existing criteria.

## 3. Unified policy pipeline

```text
ALL CRITERIA
    |
    +-- CORE MISSION
    +-- FORENSIC INVARIANTS
    +-- SECURITY
    +-- DATA
    +-- RESEARCH
    +-- BACKTEST
    +-- EDGE / EV / P&L / ROI
    +-- ROBUSTNESS / RISK / DRIFT
    +-- RESOURCE LIMITS
    +-- ARCHITECTURE
    +-- EVIDENCE
    +-- ACTION / PROMOTION
    |
    v
POLICY SYNTHESIS
    |
    v
CURRENT CANONICAL STATE
    |
    v
LEGAL ACTION SPACE
    |
    v
PROACTIVE BLOCKER AUDIT
    |
    v
PRIORITIZED WORK
```

## 4. Proactive engineering rule

When legal action space exists, Brain must proactively compare the real system against the Core Mission and find material blockers.

It must not wait for the user to identify every defect.

```text
CORE MISSION
  -> CURRENT SYSTEM
  -> GAP ANALYSIS
  -> BLOCKER DISCOVERY
  -> AUTHORITY / SAFETY CLASSIFICATION
  -> LEGAL REPAIR
  -> TEST
  -> RUNTIME VERIFY
  -> EVIDENCE
  -> REASSESS WHOLE POLICY
```

The objective is **mission progress**, not commit count.

## 5. Blocker priority

When multiple legal blockers exist, prioritize by the combined mission value of:

```text
CORE-MISSION IMPACT
x BLOCKER SEVERITY
x UNBLOCKING VALUE
x SAFETY
x EVIDENCE QUALITY
```

Illustrative classes:

- **P0** — source-truth corruption; future/lookahead leakage; synthetic historical evidence; credential/security exposure; temporal-order corruption.
- **P1** — missing freeze-before-result proof; missing OOS/robustness evidence; invalid EV aggregation; invalid runtime boundary.
- **P2** — tests; observability; documentation; cleanup.

Priority classification never overrides an FSM gate.

## 6. Gate semantics

The following are hard invariants:

```text
PASS_IS_LOCAL
PASS_IS_PREREQUISITE_ONLY
NO_PASS_INHERITANCE
UNKNOWN_IS_NOT_PASS
DEFAULT_DENY
OWN_GATE_EVIDENCE_REQUIRED
FRESH_EVIDENCE_REQUIRED_FOR_PROMOTION
```

Therefore:

```text
IMPLEMENTED
  != TESTED
  != RUNTIME_VERIFIED
  != EVIDENCE_ADMITTED
  != PROMOTED
  != ACTION
```

And:

```text
BACKTEST_PASS
  != EDGE_PASS
  != EV_PASS
  != P&L_PASS
  != PROMOTION
  != ACTION
```

## 7. Invalid-value propagation

The following never rescue an aggregate result:

```text
NaN
Inf
UNKNOWN
FAIL
missing evidence
stale evidence
unresolved evidence
```

They remain non-admitted until resolved by their own gate-specific evidence.

## 8. Current N116 exception

The canonical state is currently:

```text
BRAIN-N116_WAIT_EXTERNAL_OBSERVATION
ACTION_SPACE = 0
MANDATORY_NO_OP
PROMOTION = DENY
```

Therefore this policy document does **not** authorize mutation, promotion, Room 02 unlock, or staircase unlock.

Permitted foundation actions remain limited to monitoring exact-current runtime evidence, reading immutable history, validating integrity, and recording newly observed evidence without rewriting prior events.

## 9. Successor algorithm

A successor Bot must execute this order before selecting work:

1. Read this policy.
2. Read the canonical Forensic FSM doctrine.
3. Read `state/current_state.json`.
4. Read `state/next_action.json`.
5. Recover the immutable action history.
6. Reconstruct Core Mission.
7. Reconcile all established criteria.
8. Determine the current legal action space.
9. If legal action space exists, proactively audit and rank real blockers.
10. If action space is zero, obey `MANDATORY_NO_OP` and never invent evidence.

## 10. Non-negotiable inheritance rule

A successor must not optimize only for the newest user instruction.

The newest instruction is another criterion that must be reconciled into the full policy. Older constraints remain active unless a formally admitted policy transition changes them.

## 11. Forensic database example

The database chain remains one chain:

```text
DB_EXISTENCE
  -> DB_BINDING
  -> SECRET_RESOLUTION
  -> DB_TLS_ADMISSION
  -> NETWORK_ORIGIN_PROOF
  -> DB_ROUND_TRIP
  -> PROMOTION
```

`DB_EXISTENCE = PASS` does not imply `DB_BINDING = PASS`.
`DB_BINDING = PASS` does not imply TLS admission.
`DB_TLS_ADMISSION = PASS` does not imply round-trip.
`DB_ROUND_TRIP = PASS` is evidence for its own gate and does not silently promote unrelated gates.

## 12. Final principle

> **Core Mission controls direction. Unified Action Policy controls coherent reasoning and legal engineering selection. The Forensic FSM controls evidence admission and authority.**

These are three complementary layers of one architecture, not competing brains and not competing forensic state machines.
