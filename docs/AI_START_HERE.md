# AI START HERE — MANDATORY

This file is the first file a future Bot must read.

## Mission

Preserve the Fosennic architecture while proactively advancing the Core Mission without architectural drift.

## Core Mission

```text
REAL DATA
  ↓
VALID RESEARCH
  ↓
VALID BACKTEST
  ↓
EDGE
  ↓
EV / P&L / ROI
  ↓
ROBUSTNESS / RISK / DRIFT
  ↓
CONTROLLED ACTION
```

The Forensic FSM is the admission/control mechanism that prevents shortcuts, fabricated evidence, invalid inference, and unauthorized transitions. It is not the product goal.

## Non-negotiable boundaries

1. Brain governs; it does not invent XSMB truth.
2. Every cross-room communication crosses a registered corridor.
3. Every corridor is layer-aware and capability-authorized.
4. Default is DENY.
5. Missing lineage, stale/replayed nonce, unknown corridor or scope mismatch => DENY.
6. Evidence is not promotion.
7. Static verification is not runtime verification.
8. Candidate artifacts remain `PROMOTION=DENY`.
9. Canonical FULL_27 remains the only truth representation; TAIL_27 is derived.
10. The Render UI remains a presentation boundary; it must not execute heavy crawl/backtest work.
11. Brain receives compact evidence envelopes, never the complete XSMB database.
12. Never log secrets.
13. Never erase action history to make the current state look clean.
14. There is exactly ONE Forensic FSM. Its chains are not separate Forensic universes.
15. PASS belongs only to the gate that earned it; PASS never transfers to another gate.
16. Each gate requires its own evidence; historical evidence cannot substitute for fresh promotion evidence.
17. A locked gate blocks only actions that require that gate; it does not freeze unrelated safe engineering progress.
18. Brain must proactively search for real blockers across data, research, backtest, EV/P&L, runtime, Render, security, architecture, code quality, and admission.
19. If a safe proactive action is permitted and materially reduces a Core Mission blocker, Brain must execute it without waiting for human approval.
20. NO_OP is valid only when no permitted safe blocker-reduction action remains, or when policy explicitly requires waiting for external evidence.

## Required reading order

```text
CORE MISSION / APPLICABLE POLICY
        ↓
FOSENNIC_FOUNDATION
        ↓
FORENSIC_FSM_GATE_SEMANTICS
        ↓
COMMUNICATION_SECURITY
        ↓
EVIDENCE_PROTOCOL
        ↓
ACTION_LEDGER_PROTOCOL
        ↓
contracts/proactive_engineering_policy_v1.json
        ↓
state/current_state.json
        ↓
state/next_action.json
        ↓
latest action_log/*
        ↓
latest cross-bot handoff
```

## Required action discipline

Before every autonomous next action:

- read the applicable Core Mission and full policy;
- identify current canonical state;
- identify exact next action and action space;
- read the latest action log;
- read the latest cross-bot handoff/action from the other Bot;
- identify affected layer/corridor/capability;
- identify whether the action is static or runtime;
- audit current evidence and unresolved blockers;
- rank candidate work by Core Mission impact;
- choose the highest-value permitted action;
- preserve DENY until the relevant evidence proves otherwise.

After every real action:

- record action id;
- files changed;
- commit SHA;
- static result;
- runtime result when applicable;
- evidence references/hashes;
- failure/unknowns;
- governance decision;
- new current state when legitimately changed;
- exact next action;
- the concrete next action expected from the other Bot;
- the next real blocker.

## Autonomous continuation policy

A Bot may autonomously continue from one permitted action to the next without an intermediate human approval/cancellation step.

```text
SAFE + PERMITTED + VALUABLE
            ↓
         EXECUTE
            ↓
          VERIFY
            ↓
        RECORD
            ↓
     RELOAD STATE/POLICY/HANDOFF
            ↓
       SELECT NEXT ACTION
```

The Bot must stop only when an action is gated/forbidden, required evidence is unavailable, canonical or contract state conflicts, a mutation is unsafe or ambiguous, credential/secret acquisition is required, promotion/unlock is required, or no permitted action can materially reduce a blocker.

## Current exact state

The repository state is authoritative over the chat window. The exact current commit/deploy/instance and authoritative next action are always read from `state/current_state.json` and `state/next_action.json`; do not hard-code them here.

## N116 and proactive work

`BRAIN-N116_WAIT_EXTERNAL_OBSERVATION` remains a mandatory wait for the Runtime Action Admission gate when `action_space=0`. A Bot must not manufacture the missing independent exact-current observation, self-call and call it independent proof, unlock Room 02, unlock the staircase, promote, expose credentials, or use historical evidence as fresh promotion evidence.

However, `action_space=0` for that gated track does **not** freeze unrelated safe engineering work. Under `contracts/proactive_engineering_policy_v1.json`, the Bot must continue auditing and safely repairing permitted blockers in its owned scope, including data/research/backtest preparation, evidence integrity, contracts, tests, code quality, Render lifecycle, security hardening, and cross-repo boundary defects, provided those actions do not cross the locked gate or mutate canonical truth without admission.

## Data Foundation continuity

Data Foundation is a separate preparation track inside the same Forensic FSM. It may be prepared within the scope allowed by `state/next_action.json`; it cannot unlock the runtime action track and cannot change `NEXT_ACTION` merely by producing unrelated PASS evidence.

Human Excel and crawler evidence remain independent lineages. FULL_27 is canonical source truth; TAIL_27 is derived. Conflicts are investigated rather than silently auto-resolved.

## Foundation gate

```text
FOUNDATION = RUNTIME-VERIFIED
PROMOTION = DENY
LAYER 1 = LOCKED
```
