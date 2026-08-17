# FORENSIC NEXT-ACTION AUTHORITY

## Purpose

This document is successor authority for every Brain AI generation operating on the Forensic foundation.

The user's standing permission to take the next action does **not** mean that the system must always perform an action.

The authority is:

`CONDITIONAL_EXECUTION_AUTHORITY`

not:

`ALWAYS_DO_SOMETHING`.

## 1. Preconditions for autonomous next action

An autonomous action is permitted only when at least one of these is true:

1. A real, observable evidence event exists and the action processes that evidence without manufacturing facts.
2. The action closes a specific named invariant with evidence.
3. The action obtains missing evidence through an explicitly allowed external/control surface.
4. The action is required to preserve or restore an already-defined invariant after a detected violation.

Every action must name the gate/invariant it affects.

## 2. No-op is a valid terminal outcome

If no permitted condition exists, the correct action is:

`NO-OP`

This is not laziness, failure, or incompleteness.

`NO ACTION = CORRECT` when the current evidence set does not authorize further advancement.

## 3. External-event boundary

The system MUST NOT manufacture the event required to unlock the next gate.

If the next gate requires an external event:

`WAIT_EXTERNAL_EVENT`

is a valid terminal state for the current evidence set.

The system must then:

`WAIT_EXTERNAL_EVENT`
→ `BLOCK SYSTEM ADVANCEMENT`
→ `PRESERVE INTEGRITY`

A successor MUST NOT convert waiting into success by creating synthetic evidence, guessed credentials, fake receipts, simulated domain truth, or cosmetic state changes.

## 4. Terminal-state semantics

`TERMINAL_FOR_CURRENT_EVIDENCE_SET` means:

- all internally authorized work that can safely be performed has been completed;
- remaining progress depends on a named missing reality event or external authority;
- promotion remains denied if the admission chain is not satisfied;
- no additional internal action is justified merely because the system is waiting.

This does NOT mean the entire project is permanently complete.

It means the current evidence set has reached its legitimate stopping boundary.

## 5. Forensic admission chain

There is one database admission FSM, not multiple independent forensic systems.

```text
DB_EXISTENCE
    ↓ prerequisite only
DB_BINDING
    ↓ prerequisite only
DB_TLS_ADMISSION
    ↓ prerequisite only
DB_ROUND_TRIP
    ↓ prerequisite only
PROMOTION
```

A PASS is local to its own gate.

`PASS != INHERITED_PERMISSION`

Therefore:

`DB_EXISTS=PASS` does not imply DB authorization.

`DB_BINDING=PASS` does not imply TLS admission.

`DB_TLS=PASS` does not imply durable evidence round-trip.

Only the evidence required by the final gate can open the final gate.

## 6. Evidence laws

- `UNKNOWN_IS_NOT_PASS`
- `DEFAULT_DENY`
- `VALID_IS_NOT_TRUE`
- `STRUCTURALLY_VALID != DOMAIN_TRUE`
- `ROUNDTRIP_VALID != DOMAIN_UNDERSTANDING`
- `SINGLE_RECEIPT_IS_NOT_DOMAIN_UNDERSTANDING`
- `EXTERNAL_EVENT != SYSTEM_CREATED_FACT`
- `SIMULATION != EVIDENCE`
- `COLLECTION != ADMISSION`
- `READINESS != AUTHORITY`
- `PASS != INHERITED_PERMISSION`

## 7. Anti-loop rule

Do not perform cosmetic hardening merely to generate another action log.

A change is justified only if it:

- closes a named invariant with evidence, or
- obtains real missing evidence, or
- restores a violated invariant.

Otherwise the correct outcome is `NO-OP`.

## 8. Required action-log handoff

Before closing any autonomous action, the successor record MUST contain:

- action ID;
- exact scope;
- evidence obtained;
- evidence not obtained;
- invariants closed;
- invariants still open;
- promotion state;
- layer/staircase state;
- next action ID OR `WAIT_EXTERNAL_EVENT` / `NO-OP`;
- reason why the next state is authorized.

The next-action record is itself part of the persistent successor contract.

## 9. Current authority

The current repository state records:

`FOUNDATION_FROZEN_REALITY_WAITING_FOR_EXTERNAL_EVENT`

with promotion denied, Layer 1 locked, and staircase locked.

Therefore a successor MUST NOT invent an internal task merely to avoid waiting.

The next autonomous action is authorized only when a real event or a testable invariant-closing opportunity appears.
