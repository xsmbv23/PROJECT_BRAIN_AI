# FORENSIC ADMISSION STATE CHAIN — INHERITANCE DOCTRINE

## Purpose

This document is a durable inheritance rule for every future Brain/Quant Bot. It prevents successors from treating one forensic state as permission to infer or inherit another state.

## 1. One forensic FSM only

There is exactly ONE authoritative forensic admission FSM. Do not create a second FSM for readiness, simulation, database existence, or any auxiliary subsystem.

A state at one gate is evidence only for that gate. It may become a prerequisite for the next gate, but it never inherits authority automatically.

## 2. Database admission chain

```text
DB_EXISTENCE
    |
    v
DB_BINDING
    |
    v
DB_TLS_ADMISSION
    |
    v
DB_ROUND_TRIP
    |
    v
PROMOTION
```

Semantics:

- `DB_EXISTENCE = PASS` means only that the database exists.
- `DB_BINDING = PASS` means only that the service has an explicit binding.
- `DB_TLS_ADMISSION = PASS` means only that the binding satisfies the TLS policy.
- `DB_ROUND_TRIP = PASS` requires a real compact metadata write, read-back, and SHA-256 match.
- `PROMOTION = PASS` is permitted only after the preceding required evidence is actually proven.

### Non-inheritance rule

```text
PASS_AT_GATE IS A PREREQUISITE ONLY.
NO_PASS_INHERITANCE.
UNKNOWN_IS_NOT_PASS.
DEFAULT_DENY.
```

Therefore:

```text
DB_EXISTS = PASS
!= DB_ACCESS = PASS

BOUND_TLS = PASS
!= ROUND_TRIP = PASS

ROUND_TRIP = PASS
!= PROMOTION = PASS
```

## 3. Invariant usefulness rule

Every new invariant must reduce uncertainty of a SPECIFIC gate in the authoritative FSM.

Formally:

```text
INVARIANT IS VALID
iff
it reduces uncertainty of a named gate
and
its effect is testable by evidence.
```

Cosmetic invariants, orphan rules, and rules that do not close a specific gate are prohibited because they create architectural drift and hardening loops without increasing forensic certainty.

## 4. Readiness has zero authority

Readiness is observability only.

```text
READINESS
   |
   +--> dashboard/status
   +--> compact diagnostics
   +--> operator visibility

READINESS -X-> ADMISSION
READINESS -X-> PROMOTION
READINESS -X-> EXECUTION
```

A green readiness signal can never open a forensic gate.

## 5. Dry-run is a shadow, never a path

Dry-run is rehearsal/debugging only.

```text
DRY_RUN_OUTPUT ∉ FORENSIC_EVIDENCE
```

Dry-run:

- cannot create canonical state;
- cannot promote data;
- cannot alter admission state;
- cannot feed a real Room/Engine path;
- cannot alter collector behavior;
- cannot create a reverse dependency into acquisition;
- may consume explicitly marked non-canonical rehearsal data only.

Allowed rehearsal:

```text
BUFFER / REJECTED DATA
        |
        v
FORCED DENY
        |
        v
SHADOW PIPELINE
        |
        v
NON_CANONICAL OUTPUT
```

This exists to test end-to-end mechanics and memory safety without converting partial or rejected data into truth.

## 6. Permanent boundary invariants

```text
BUFFER != ENGINE_INPUT
PARTIAL != TRUTH
COLLECTION != ADMISSION
SIMULATION != EVIDENCE
READINESS != AUTHORITY
DB_EXISTENCE != DB_AUTHORIZATION
```

## 7. Immutability

- Raw evidence is hashed before parsing.
- Existing-date raw-hash changes are drift and must deny.
- Conflicts are quarantined append-only.
- Canonical promotion is one-way.
- Failed history is immutable.
- No silent replacement, interpolation, synthetic backfill, or deletion.

## 8. Inheritance rule for successor Bots

Before executing a new action, the successor must:

1. read `state/current_state.json`;
2. read `state/next_action.json`;
3. read the latest action log;
4. identify the authoritative FSM gate affected;
5. state which uncertainty the action closes;
6. refuse to create a second FSM;
7. update state/action evidence before claiming promotion.

The repository state is the persistent authority. The chat window is only a communication interface.

## 9. Anti-confidence rule

> A system becomes dangerous not when it is wrong, but when it becomes confident without evidence.

No successor may convert `READY`, `PASS`, green readiness, successful dry-run, resource existence, or absence of an observed error into a stronger forensic claim without the evidence belonging to the stronger gate.
