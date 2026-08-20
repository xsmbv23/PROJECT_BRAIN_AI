# CORE MISSION RESEARCH PIVOT

## Purpose

This document is a durable successor handoff. It prevents future Bots from mistaking Forensic/evidence progress for Core Mission progress.

## One Forensic FSM, many local gates

There is ONE Forensic FSM. Database admission, source admission, evidence durability, and action receipt are local gate chains inside that FSM.

A gate PASS is local evidence only. It is a prerequisite for the next gate; it never inherits upward and never creates PASS in another gate.

```text
PASS(GATE_A)
    != PASS(GATE_B)
    != PROMOTION
```

## Core Mission is the product target

```text
REAL_DATA
  -> VALID_RESEARCH
  -> VALID_BACKTEST
  -> EDGE
  -> EV/P&L/ROI
  -> ROBUSTNESS/RISK/DRIFT
  -> CONTROLLED_ACTION
```

Forensic is the control mechanism protecting this path. Forensic is not the product target.

## Current strategic position

The evidence/data foundation is materially ahead of the research/quant path.

Brain current state reports:

- DB existence/binding/TLS/round-trip are evidenced, but promotion remains DENY.
- action space is 0.
- Layer 1 and the staircase remain locked.
- `BRAIN-N125_WAIT_EXTERNAL` remains the current external-observation blocker.
- `QUANT-N010_WORKFLOW_EVIDENCE_HARDENING` is explicitly allowed only as a parallel safe local prerequisite.

Quant Engine current state reports:

- Room 01 input-adapter/parser contracts hardened.
- Room 02 remains locked because canonical real data is not admitted.
- synthetic production data forbidden.
- lookahead forbidden.
- ads/navigation/chrome are non-truth content.
- official result panel required.
- Kelly is downstream-only after validated edge.
- multiple-testing correction required before promotion.
- heavy research execution must be external/bounded.
- Render Free memory guard is 320 MiB.

## Strategic correction

Do NOT spend the next cycle merely adding more evidence validators unless they directly remove a Core Mission blocker.

The highest-value next research blocker is:

```text
CANONICAL REAL DATA
       |
       v
DATE-ALIGNED RESEARCH DATASET
       |
       v
NO-LOOKAHEAD VALIDATION
       |
       v
REPRODUCIBLE BASELINE RESEARCH
       |
       v
BOUNDED BACKTEST
       |
       v
EDGE
       |
       v
EV / P&L / ROI
```

The transition into this path remains DENY until the upstream admission gates are genuinely satisfied.

## Research dataset admission contract

A research dataset may be created only when all of the following are independently evidenced:

1. Source truth is admitted through the canonical source/quorum chain.
2. Every observation has an explicit event/result date and source identity.
3. Dataset construction has a declared information timestamp boundary.
4. No feature may use data that was unavailable at the decision timestamp.
5. Raw byte identity and semantic identity remain separate concepts.
6. Historical fixtures are explicitly marked; fixtures never become reality by default.
7. The dataset is reproducible from immutable source/evidence references.
8. The same inputs reproduce the same canonical dataset hash.
9. Missing/unknown fields remain unknown; they are never silently imputed with synthetic truth.
10. Dataset creation is bounded so Render 512 MB cannot be exceeded; heavy work is externalized or chunked.

## Backtest admission contract

No backtest may be promoted merely because it runs.

Minimum evidence must include:

```text
research_dataset_hash
parameter/config hash
feature availability boundary
train/test or walk-forward boundary
execution assumptions
transaction-cost assumptions
missing-data policy
lookahead audit
baseline result
P&L distribution
EV estimate
multiple-testing correction
```

## Future Bot rule

If a future Bot sees many green Forensic tests but no research/backtest/EV evidence, it must report:

> "Forensic foundation is healthy; Core Mission evidence is still missing."

It must not create fake progress by adding validators solely to increase the apparent completion level.

## Safety and immutability

No change in this pivot document may unlock Layer 1, Room 02, or Controlled Action. Unlocks require their own fresh evidence and the existing admission chain.
