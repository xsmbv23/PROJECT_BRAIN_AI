# PASS Locality and Gate-Prerequisite Semantics

## Status

**FROZEN FOUNDATION RULE — SUCCESSOR BOTS MUST NOT CHANGE THIS SEMANTIC WITHOUT A FORMAL ARCHITECTURE VERSION.**

## Core rule

The system has **one Forensic FSM**, not multiple independent Forensic state machines.

A gate result is local to that gate.

```text
PASS(GATE_A)
   !=
PASS(GATE_B)
```

A PASS at Gate A is only a **prerequisite/evidence condition** allowing Gate B to be evaluated. It does not inherit, imply, or manufacture PASS at Gate B.

## Database example

```text
DB_EXISTENCE
    PASS
      |
      v
DB_BINDING
    PASS / NOT_BOUND
      |
      v
DB_TLS_ADMISSION
    PASS / DENY
      |
      v
DB_ROUND_TRIP
    PASS / NOT_PROVEN
      |
      v
PROMOTION
    PASS / DENY
```

Therefore:

- `DB_EXISTS = PASS` does not mean the service has a key.
- `DB_BINDING = PASS` does not mean TLS admission passed.
- `DB_TLS_ADMISSION = PASS` does not mean a real write/read round-trip occurred.
- `DB_ROUND_TRIP = PASS` is evidence for promotion but does not bypass other independent admission gates.

## Data example

```text
SOURCE
  -> RAW
  -> PARSE
  -> FULL_27_VALID
  -> INDEPENDENT_QUORUM
  -> CANONICAL
  -> ENGINE_INPUT
```

A source being fetched does not make it canonical.
A valid FULL_27 from one source does not satisfy a two-source quorum.
A TAIL_27 match does not substitute for FULL_27 semantic agreement.

## Three different runtime meanings

```text
VERIFIED
```
Current gate has sufficient evidence.

```text
RECONCILE_REQUIRED
```
The current runtime is known, but an explicit reconciliation condition remains before the logical action can proceed. This is **not automatically logical corruption**.

```text
HARD_DENY
```
Authority, protocol, schema, or required-rule integrity is broken.

## Authority rule

```text
BRAIN CURRENT STATE
        = logical authority

QUANT PROJECTION
        = read-only evidence

DATA-PLANE PROJECTION
        = read-only evidence

RENDER RUNTIME
        = evidence only

ACTION LOG
        = immutable history only
```

A newer deployment commit must never rewrite logical state merely because it differs from the last verified runtime commit.

```text
runtime_commit_drift
      -> RECONCILE_REQUIRED

logical_authority/protocol violation
      -> HARD_DENY
```

## Forbidden shortcuts

Never:

- infer a deeper PASS from a shallower PASS;
- treat `UNKNOWN` as PASS;
- use a deployment ID as logical identity;
- let runtime evidence become state authority;
- use a legacy tail-only workbook as FULL_27 canonical truth;
- unlock Research because Data Admission passed;
- unlock Room 02 because Room 01 passed;
- unlock the staircase because any room passed.

## Required transition model

```text
EVIDENCE -> STATE -> ACTION
```

Every transition must have observable evidence at the transition being authorized.

## Successor instruction

When continuing this project, read this file together with:

- `state/current_state.json`
- `state/next_action.json`
- the latest `docs/action_log/BRAIN-N*.md`
- the frozen admission contracts

The current action is authoritative only after checking those persistent artifacts. The chat window is not the memory authority.
