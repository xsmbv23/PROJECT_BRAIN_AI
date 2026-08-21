# E2E Parallel Execution Doctrine

## Purpose

Allow the Brain and Quant Engine streams to progress continuously without creating a second authority system or bypassing the Forensic FSM.

## Authority split

```text
Project_Brain_AI
    = GOVERNANCE CONTROL PLANE
    = CURRENT STATE AUTHORITY
    = ADMISSION / PROMOTION AUTHORITY

Quant_Engine
    = RESEARCH / CALCULATION PLANE
    = LOCAL PREREQUISITE PRODUCER
    = NO BRAIN STATE MUTATION

xsmb-quant
    = SOURCE-TRUTH OWNER
    = RAW DATA AUTHORITY
```

## Parallel rule

Parallel execution is allowed only where the current Brain state explicitly permits it.

A parallel stream may:

- implement code;
- harden contracts;
- add bounded tests;
- improve evidence schemas;
- improve workflow security;
- document findings;
- prepare downstream prerequisites.

A parallel stream may not:

- promote Brain state;
- unlock a Brain room;
- unlock the staircase;
- convert UNKNOWN to PASS;
- use its own PASS as Brain PASS;
- overwrite source truth;
- manufacture external runtime evidence.

## E2E chain

```text
S1 REAL_DATA
  owner: xsmb-quant
       |
       v
S2 VALID_RESEARCH
  owner: Quant_Engine
       |
       v
S3 VALID_BACKTEST
  owner: Quant_Engine
       |
       v
S4 EDGE
  owner: Quant_Engine
       |
       v
S5 EV_PNL_ROI
  owner: Quant_Engine
       |
       v
S6 ROBUSTNESS_RISK_DRIFT
  owner: Quant_Engine
       |
       v
S7 CONTROLLED_ACTION
  owner: Project_Brain_AI
```

Each segment has its own exit evidence. Downstream implementation may be prepared while upstream admission is blocked, but downstream admission cannot inherit upstream PASS.

## External-wait rule

When Brain reports:

```text
WAIT_EXTERNAL_OBSERVATION
action_space=0
```

Brain must wait for the missing independent observation.

Quant Engine may continue only the safe parallel work explicitly named by Brain. That work is recorded in Quant's own execution stream and remains non-promotional.

## Current handoff

At the current foundation boundary:

```text
Brain:
  CI exact-current observation = UNKNOWN
  promotion = DENY
  Room 02 = LOCKED
  staircase = LOCKED

Quant:
  QUANT-N010 = workflow-evidence hardening pending external CI
  QUANT-N011 = workflow permission/runtime-bound hardening completed
  next safe local preparation = QUANT-N012
```

The Quant local state is a projection and cannot override Brain authority.

## Successor procedure

Every successor Bot must:

1. read Brain `state/current_state.json`;
2. read Brain `state/next_action.json`;
3. read latest Brain action log;
4. read this doctrine;
5. inspect the current Quant parallel-progress record if parallel work is named;
6. verify exact-current evidence before changing any gate;
7. record its own action before handing over.

The chat window is not the memory authority. Persistent repository state and forensic evidence are.
