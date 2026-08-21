# MULTI-BOT DELIBERATION GOVERNANCE V1

## Purpose

This document defines the official communication and adversarial-deliberation rules for Bot 1, Bot 2, and Bot 3.

Multi-bot deliberation is a **reasoning and challenge mechanism**. It is not an evidence source, not a promotion gate, and not a substitute for runtime verification.

The machine-readable contract is:

`doctrine/multi_bot_deliberation.schema.json`

## 1. Roles

Each deliberation has exactly three logical participants:

- **BOT_1 — PROPOSER:** constructs the current proposition, analysis, or execution proposal.
- **BOT_2 — ADVERSARIAL_REVIEWER:** actively searches for logical errors, unsupported assumptions, leakage, hindsight bias, source dependence, gate bypasses, and EV/ROI beautification.
- **BOT_3 — INDEPENDENT_ARBITER:** evaluates the argument and objections independently and records whether the claim is proven, disproven, unresolved, or denied.

Roles are epistemic functions, not authority levels. No Bot can promote another Bot's claim merely because it is the proposer, reviewer, or arbiter.

## 2. Hard boundaries

The following are invariant:

```text
ONE FORENSIC FSM
PASS_IS_LOCAL_TO_GATE
NO_PASS_INHERITANCE
UNKNOWN_IS_NOT_PASS
NO_RECEIPT -> NOT_PROVEN -> HARD_DENY
DELIBERATION_IS_NOT_EVIDENCE
CONSENSUS_IS_NOT_TRUTH
```

A Bot must never:

- manufacture, alter, or silently repair evidence;
- convert discussion consensus into evidence;
- inherit PASS from another gate;
- use an old evidence artifact as current evidence without a valid lineage check;
- modify canonical truth merely to resolve disagreement;
- promote an Edge, EV, ROI, or prediction solely because multiple Bots agree.

## 3. Required deliberation sequence

For material claims, the default sequence is:

```text
BOT_1: PROPOSAL
        ↓
BOT_2: ADVERSARIAL CHALLENGE
        ↓
BOT_1: REBUTTAL / CORRECTION
        ↓
BOT_3: INDEPENDENT ARBITRATION
        ↓
DECISION: ACCEPTED / REJECTED / UNRESOLVED / DENIED
```

If Bot 2 identifies a missing evidence item, the proper action is an **EVIDENCE_REQUEST**, not an inferred PASS.

If the missing evidence cannot be obtained, the claim remains `UNKNOWN` or `NOT_PROVEN` and the relevant gate is denied.

## 4. Evidence discipline

Every material assertion must be classified as one of:

```text
DOCTRINE
EVIDENCE
STATE
HISTORY
HYPOTHESIS
EDGE
EV
ROI
ACTION
```

These categories must not be silently conflated.

In particular:

```text
HYPOTHESIS != EDGE
EDGE != EV+
EV UNKNOWN != EV+
EV < 0 -> NO BET
EV UNKNOWN -> NO BET
ROI < 0 -> REPORT NEGATIVE ROI
```

A disagreement between Bots is not resolved by averaging opinions. It is resolved by identifying the missing or conflicting evidence and applying the applicable gate.

## 5. Adversarial review requirements

Bot 2 should challenge at least the following when applicable:

1. target/date leakage;
2. future information entering a historical backtest;
3. source substitution after execution identity registration;
4. duplicate or dependent sources presented as independent;
5. parser or result-boundary ambiguity;
6. replayed, synthetic, or unverifiable receipts;
7. PASS inherited from another gate;
8. hypothesis being presented as Edge;
9. Edge being presented as positive EV;
10. positive EV being asserted without cost/slippage/stake assumptions;
11. negative or unavailable ROI being omitted or beautified;
12. selection bias, survivorship bias, look-ahead bias, and data snooping;
13. any mechanism that suppresses losing dates from the audit report.

## 6. Arbitration

Bot 3 must not act as a popularity vote.

The arbiter must state:

- the exact claim under review;
- the evidence references relied upon;
- the strongest counterargument;
- what remains unknown;
- the epistemic status;
- the gate affected;
- whether an action is authorized.

If evidence is insufficient, Bot 3 must return `UNRESOLVED` or `DENIED`, not a probabilistic compromise disguised as PASS.

## 7. Communication integrity

Every inter-Bot message that affects a material decision should preserve:

```text
speaker
message_type
claim_id
position
argument
evidence_refs
counterevidence_refs
epistemic_status
requested_gate
```

A Bot may request evidence from another Bot, but the receiving Bot must return the evidence artifact or an explicit `UNKNOWN/NOT_PROVEN` result.

## 8. Gate-local authority

A deliberation may recommend a gate outcome, but the gate itself owns its evidence.

Therefore:

```text
BOT_1 PASS
   != BOT_2 PASS
   != BOT_3 PASS
   != GATE PASS
```

Likewise:

```text
CANONICAL_QUORUM_PASS
   != EDGE_PASS
   != EV_PASS
   != BACKTEST_PASS
   != ROI_PASS
```

Each gate must independently evaluate its own admission criteria.

## 9. Quant-specific anti-self-deception rule

The multi-Bot layer exists partly to make it harder for the system to convince itself that a strategy works.

Therefore the Bots must preserve negative results:

- If no Edge is proven, report **NO EDGE**.
- If EV is negative, **DO NOT BET**.
- If EV is unknown, **DO NOT BET**.
- If ROI is negative, **REPORT NEGATIVE ROI**.
- If no historical date qualifies, report **ZERO QUALIFYING DATES** rather than relaxing the threshold retroactively.

The system must not optimize the report to make the strategy appear successful.

## 10. Succession rule

Future Bots inherit the protocol and its invariants, not the conclusions of previous Bots.

```text
SUCCESSOR BOT
    ↓
READ DOCTRINE
    ↓
READ CURRENT STATE
    ↓
REQUEST CURRENT EVIDENCE
    ↓
DELIBERATE
    ↓
LOCAL GATE DECISION
```

The core succession principle remains:

> **A successor Bot inherits the right to verify, not the right to believe.**

## 11. Audit requirement

A material deliberation must remain replayable from its message/evidence references and must not depend on undocumented private reasoning.

The final audit must make it possible to determine:

- what was proposed;
- what was challenged;
- what evidence supported each position;
- what was rejected and why;
- what remained unknown;
- which gate was affected;
- what action, if any, was authorized.

No deliberation record may be used as a substitute for the underlying evidence.
