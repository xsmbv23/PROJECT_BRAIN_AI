# BRAIN-N116 — Doctrine Freeze / Core Mission Separation

## Action type

Doctrine preservation. This action does **not** advance the Forensic FSM.

## Canonical state remains

```text
BRAIN-N116_WAIT_EXTERNAL_OBSERVATION
```

```text
ACTION_SPACE = 0
ACTION = MANDATORY_NO_OP
PROMOTION = DENY
```

## Critical doctrine preserved

There is ONE Forensic FSM.

The system has two distinct concepts:

1. **Core Mission** — the long-term objective:

```text
REAL DATA -> VALID RESEARCH -> VALID BACKTEST -> EDGE -> EV/P&L/ROI -> ROBUSTNESS/RISK/DRIFT -> CONTROLLED ACTION
```

2. **Forensic FSM** — the admission/control mechanism that decides whether enough exact evidence exists to enter the next state.

The Forensic FSM is not the product and must not replace the Core Mission.

## Gate invariant

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
DB_EXISTENCE PASS
    != DB_BINDING PASS
    != SECRET_RESOLUTION PASS
    != DB_TLS_ADMISSION PASS
    != NETWORK_ORIGIN_PROOF PASS
    != DB_ROUND_TRIP PASS
    != PROMOTION PASS
```

Each is an admission gate in the same FSM and each requires its own evidence.

## N116 blocker

The missing evidence is an independently observable, exact-current `/governance` receipt event.

A chat statement is not evidence. A startup log is not equivalent to an independently observed HTTP receipt. A self-call cannot be treated as independent proof.

## Allowed while waiting

- monitor exact-current runtime evidence;
- read immutable historical action logs;
- validate state/document integrity;
- record newly observed evidence without mutating prior events.

## Forbidden while waiting

- manufacture the external event;
- invent a PASS;
- inherit PASS from another gate;
- unlock Room 02;
- unlock the staircase;
- promote;
- expose credentials;
- download or parse source data.

## Successor handoff

Do not create N117 until the required external observation becomes independently observable. When it arrives, verify runtime identity, commit, action, nonce, and freshness before any promotion decision.

## Immutable-history note

This document records doctrine; it does not alter the canonical FSM state. The successor must treat `state/current_state.json` and `state/next_action.json` as canonical runtime authority.
