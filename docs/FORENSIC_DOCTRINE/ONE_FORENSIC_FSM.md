# ONE FORENSIC FSM — Local PASS / No-Op Doctrine

## Authority

This document is a successor-facing doctrine for the Brain foundation. It does not create a new FSM. It records the invariant already enforced by `state/current_state.json`.

## Core rule

```text
ONE_FORENSIC_FSM = ENFORCED
```

There is one forensic state machine. Individual gates produce local evidence states. Those states are not independent forensic machines and do not automatically grant authority to later gates.

## Gate semantics

```text
PASS = LOCAL
NO_PASS_INHERITANCE = TRUE
UNKNOWN = NOT_PASS
DEFAULT = DENY
```

A PASS at one gate is only evidence that that gate's own predicate was satisfied. It is a prerequisite for downstream evaluation, never inherited permission.

Example:

```text
DB_EXISTS = PASS
```

does not imply:

```text
DB_BINDING = PASS
DB_TLS = PASS
DB_ROUNDTRIP = PASS
PROMOTION = PASS
```

Each downstream gate must obtain its own evidence.

## External-event boundary

```text
STATE = WAIT_EXTERNAL_EVENT
```

An external event must originate outside the system's own inference loop. The system must not manufacture, simulate, infer, or cosmetically synthesize the event merely to escape a waiting state.

```text
IF NO EXTERNAL EVENT
    NO TRANSITION
    NO ACTION
    VALID
```

This is not a fallback state and not an implementation failure. It is the correct forensic decision under the current evidence boundary.

## No-op doctrine

```text
NO-OP = FORENSICALLY_CORRECT ACTION
```

When the FSM is waiting for an explicitly named external event and no such event is observed, doing nothing is a final decision under current evidence.

The system must not:

- manufacture a successful observation;
- replay an old observation as a new event;
- convert readiness into authority;
- convert structural validity into domain truth;
- convert one receipt into domain understanding;
- silently merge observations from different runtimes;
- open Layer 1 or the staircase because work is available;
- create a cosmetic hardening change merely to produce a new commit.

## Relationship to automation

The operator has granted permission to `next action`, but this permission is subordinate to the forensic FSM. Therefore:

```text
NEXT-ACTION AUTHORITY
        <
FORENSIC STATE AUTHORITY
```

Automation may select the next action only when the FSM has a valid transition. It may not manufacture a transition.

## Successor rule

A future Bot must read this doctrine together with:

```text
state/current_state.json
state/next_action.json
```

Before changing code, it must answer:

1. What is the current forensic state?
2. What named gate is unresolved?
3. What evidence is missing?
4. Is a real external event available through an allowed control surface?
5. If not, is NO-OP the correct decision?

If the answer to (4) is no and the FSM is waiting for that event, the correct result is NO-OP and no state transition.

## Immutable boundaries

```text
SYSTEM_DOES_NOT_CREATE_TRUTH
SYSTEM_ONLY_ADMITS_EVIDENCE
VALID_IS_NOT_TRUE
STRUCTURALLY_VALID_IS_NOT_DOMAIN_TRUE
ROUNDTRIP_VALID_IS_NOT_DOMAIN_UNDERSTANDING
PASS_IS_NOT_INHERITED_PERMISSION
EXTERNAL_EVENT_IS_NOT_SYSTEM_CREATED_FACT
```

These are foundation invariants, not suggestions.