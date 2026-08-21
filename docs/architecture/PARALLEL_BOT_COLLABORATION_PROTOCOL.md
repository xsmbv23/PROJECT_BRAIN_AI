# Parallel Bot Collaboration Protocol

## Purpose

Multiple Bot AI agents may work in parallel, but they are not parallel authorities.

The repository state is the canonical coordination boundary.

## Rule

```text
BOT A observation
      +
BOT B observation
      +
BOT C observation
      |
      v
PERSISTED EVIDENCE
      |
      v
CANONICAL FORENSIC FSM
```

A Bot may continue only inside the action space explicitly allowed by the current state.

## No split-brain

Two Bots must never independently promote the same gate.

They may:

- inspect code;
- inspect exact-current runtime evidence;
- run safe local tests;
- improve documentation;
- prepare non-mutating validators;
- prepare a successor action package.

They may not:

- invent external evidence;
- turn UNKNOWN into PASS;
- bypass a mandatory wait;
- overwrite historical forensic records;
- unlock Layer 1 while Foundation is DENY/FROZEN;
- treat a local PASS as Render PASS;
- treat another Bot's claim as evidence.

## Reconciliation

Before any state-changing action, a Bot must read:

```text
state/current_state.json
state/next_action.json
latest relevant action log
relevant architecture contract
```

The newest persisted canonical state wins over conversational memory.

## Concurrent work

When `ACTION_SPACE = 0` and `ACTION = MANDATORY_NO_OP`, parallel Bots may perform only safe engineering that does not mutate downstream state.

Examples:

```text
ALLOWED
  documentation
  schema validation
  static analysis
  test preparation
  forensic diagram maintenance
  non-mutating observability checks

DENIED
  promotion
  Layer 1 unlock
  staircase unlock
  production data mutation
  evidence fabrication
  state advancement
```

## Handoff

Every completed Bot action must be packaged with:

1. action ID;
2. exact commit;
3. exact deployment, when applicable;
4. evidence observed;
5. PASS/FAIL/UNKNOWN decision;
6. scope of the decision;
7. what the action does NOT prove;
8. next action;
9. immutable historical record.

A successor Bot must be able to continue from the repository without relying on the previous chat window.

## Core principle

```text
Parallel execution is allowed.
Parallel authority is forbidden.

Many workers.
One state machine.
One evidence chain.
One promotion authority.
```
