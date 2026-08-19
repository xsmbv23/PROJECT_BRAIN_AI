# FORENSIC GATE ADMISSION DOCTRINE

## Purpose

This document is a permanent successor-facing doctrine for the Forensic admission architecture.

It exists to prevent a future Bot AI from confusing **evidence about existence**, **evidence about authorization**, and **evidence about successful execution**.

## 1. One Forensic FSM

There is one Forensic state machine, not multiple competing forensic systems.

Each gate is a guarded transition inside that single state machine.

```text
FORENSIC FSM
    |
    +--> Gate A: EXISTENCE
    |       proposition: "Does the resource exist?"
    |
    +--> Gate B: BINDING / AUTHORIZATION
    |       proposition: "Does this service possess an admitted key/binding?"
    |
    +--> Gate C: SECURITY ADMISSION
    |       proposition: "Does the binding satisfy the required security policy?"
    |
    +--> Gate D: EXECUTION / ROUND-TRIP
    |       proposition: "Can the service perform the permitted operation and verify its evidence?"
    |
    +--> Gate E: PROMOTION
            proposition: "Has every required prior proposition been independently proven?"
```

## 2. Gate PASS semantics

A PASS is **local to the gate that produced it**.

```text
PASS(Gate A) != PASS(Gate B)
PASS(Gate B) != PASS(Gate C)
PASS(Gate C) != PASS(Gate D)
PASS(Gate D) != automatic PASS(Gate E)
```

A downstream gate may use an upstream PASS as a prerequisite, but it must still prove its own proposition with its own evidence.

### Absolute rules

- `PASS_IS_LOCAL_TO_GATE`
- `PASS_IS_PREREQUISITE_ONLY`
- `NO_PASS_INHERITANCE`
- `UNKNOWN_IS_NOT_PASS`
- `DEFAULT_DENY`

## 3. Example: database admission

Database existence is not database authorization.

```text
DB_EXISTS
   |
   | PASS means only: the database resource exists.
   v
DB_BINDING
   |
   | PASS means only: the service has the required binding.
   v
DB_TLS_ADMISSION
   |
   | PASS means only: the binding satisfies TLS policy.
   v
DB_ROUND_TRIP
   |
   | PASS means: compact metadata write/read + SHA-256 verification succeeded.
   v
PROMOTION
```

Therefore:

```text
DATABASE EXISTS = PASS
SERVICE BOUND   = NOT_BOUND
```

is a completely coherent state. It is not contradictory and it must not be collapsed into `DATABASE_PASS`.

## 4. Example: source independence admission

Source independence is a single proposition:

> "There is fresh evidence sufficient to establish that the candidate sources are operationally independent for the defined failure model."

Hostname difference is not proof.

HTML/content difference is not proof.

Different branding is not proof.

Independence evidence may include, where safely observable:

- fresh DNS resolution,
- IP/edge identity,
- ASN/network owner,
- CDN/edge provider,
- TLS certificate identity,
- infrastructure relationship,
- other bounded network evidence relevant to the declared failure model.

If evidence is unavailable:

```text
UNKNOWN -> DENY
```

It must **never** become:

```text
UNKNOWN -> INDEPENDENT
```

## 5. Gate isolation

No gate may silently upgrade another proposition.

Examples of forbidden inference:

```text
SOURCE_INDEPENDENCE = PASS
        X
        |
        +--> CANONICAL = PASS
        +--> TRUSTED = PASS
        +--> DATA_TRUTH = PASS
```

The correct model is:

```text
SOURCE_INDEPENDENCE
        |
        v
CANONICAL_QUORUM_GATE
        |
        v
TRUTH_ADMISSION_GATE
```

Each downstream gate requires its own evidence and receipt.

## 6. Security corridor semantics

Every protected room is reached through explicit capability boundaries:

```text
corridor_key + room_key + (inner_release when protected)
```

The keys are distinct capabilities.

Having a corridor key never implies possession of a room key.

Having a room key never implies the protected room has released its inner latch.

This is the same semantic model as the gate chain above.

## 7. Evidence hierarchy

When state sources disagree, use this priority:

```text
EXACT CURRENT RUNTIME EVIDENCE
        >
BRAIN PERSISTED STATE
        >
IMMUTABLE ACTION HISTORY
        >
OLD DOCUMENTATION
        >
HYPOTHESIS
```

Stale evidence cannot silently promote current state.

## 8. Promotion rule

Promotion is a terminal admission decision, not a convenience flag.

Promotion is allowed only when all required gates have independently produced valid evidence.

Otherwise:

```text
PROMOTION = DENY
```

A denied gate may be retried, but it may not be bypassed by changing terminology, reusing stale evidence, or interpreting silence as success.

## 9. Successor Bot instruction

A future Bot must read this doctrine before changing admission logic.

The Bot must preserve:

1. one Forensic FSM,
2. local gate PASS semantics,
3. no PASS inheritance,
4. UNKNOWN -> DENY,
5. default deny,
6. explicit evidence per proposition,
7. immutable action receipts,
8. current-runtime evidence priority,
9. locked Layer 1 until the foundation/admission gates explicitly open it.

If a proposed change makes two propositions collapse into one PASS state, treat that as an architectural regression unless a new evidence contract explicitly proves equivalence.
