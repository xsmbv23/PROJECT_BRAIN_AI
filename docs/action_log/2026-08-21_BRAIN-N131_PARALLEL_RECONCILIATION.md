# BRAIN-N131 — Parallel Quant Reconciliation

## Purpose

Record the safe parallel interaction with `xsmbv23/Quant_Engine` while preserving the single Forensic FSM and preventing evidence inheritance across repositories.

## Observed Quant state

`Quant_Engine/state/current_state.json` reports:

- Layer 1 / Room 01 Input Adapter
- Brain is the authority for promotion/state
- local state is read-only projection
- database promotion DENY
- source pair: `ketqua16.net` + `xsmb.com.vn`
- semantic quorum requires 2 distinct independent sources
- synthetic production data forbidden
- ads are non-truth content
- Render guard: 320 MiB
- runtime observed memory: 28,221,440 bytes
- Room 02 LOCKED
- Staircase LOCKED
- N010 workflow evidence is repository-execution evidence only
- external runtime truth remains NOT_PROVEN

## Brain interaction rule

Quant evidence does NOT mutate Brain state.

```text
QUANT WORKFLOW
    |
    | repository execution evidence
    v
QUANT ROOM 01
    |
    | scoped observation only
    v
BRAIN RECONCILIATION
    |
    | no PASS inheritance
    | no external-runtime substitution
    v
BRAIN FORENSIC FSM
```

The Quant repository explicitly identifies its local state as a read-only projection and forbids it from overriding Brain authority.

## Important invariant

The following is invalid:

```text
Quant workflow PASS
    -> Brain external runtime PASS
```

The correct interpretation is:

```text
Quant workflow PASS
    -> Quant repository-execution evidence = PASS
    -> Brain external runtime truth = unchanged
    -> Brain promotion = unchanged
```

## Current decision

No Brain promotion was performed.

No Layer 1 room was opened.

No staircase edge was opened.

No database admission gate was changed.

No credential was requested, copied, or stored.

## Successor instruction

Any Bot working in parallel repositories must reconcile evidence by **scope**, never by convenience. A repository execution receipt can satisfy only the gate whose contract explicitly names that evidence class.

One Forensic FSM remains authoritative.

`UNKNOWN_IS_NOT_PASS` and `PASS_IS_LOCAL` remain mandatory.
