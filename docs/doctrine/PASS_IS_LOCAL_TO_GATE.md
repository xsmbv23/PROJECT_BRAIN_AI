# PASS_IS_LOCAL_TO_GATE

## FROZEN SUCCESSOR INVARIANT

This file is a mandatory architectural rule for every future Brain Bot.

The system must reason in this order:

`CLAIM -> REQUIRED EVIDENCE -> EVIDENCE VALIDITY -> GATE STATE -> ACTION`

Never begin from the desired action and search backward for justification.

## One Forensic FSM

There is one Forensic admission FSM. It contains multiple gates, but those gates are not independent systems and their PASS states are not globally interchangeable.

```text
DB_EXISTENCE
    -> DB_BINDING
    -> SECRET_RESOLUTION
    -> DB_TLS_ADMISSION
    -> NETWORK_ORIGIN_PROOF
    -> DB_ROUND_TRIP
    -> PROMOTION
```

## Local PASS rule

`PASS_IS_LOCAL_TO_GATE` means:

```text
PASS(GATE_N)
    !=
PASS(GATE_N+1)
```

A PASS at gate N is only proof of the proposition belonging to gate N.

It is a prerequisite that permits evaluation of the next gate. It is not inherited authorization.

Examples:

```text
DB_EXISTENCE=PASS
    does not imply
DB_BINDING=PASS
```

```text
DB_BINDING=PASS
    does not imply
SECRET_RESOLUTION=PASS
```

```text
DB_TLS_ADMISSION=PASS
    does not imply
NETWORK_ORIGIN_PROOF=PASS
```

```text
NETWORK_ORIGIN_PROOF=PASS
    does not imply
DB_ROUND_TRIP=PASS
```

Only evidence specifically required by a gate may move that gate's state.

## Why this exists

Without this rule a future Bot may commit a forensic escalation bug such as:

```text
DATABASE EXISTS
      -> DATABASE PASS
      -> WRITE EVIDENCE
      -> PROMOTION
```

That is forbidden.

The correct chain is:

```text
RESOURCE EXISTS
      -> prove binding
      -> prove secret resolution
      -> prove TLS admission
      -> prove network origin
      -> prove durable round-trip
      -> then and only then promotion
```

## Wrong-gate evidence

Evidence that proves another proposition is not valid evidence for the requested gate.

```text
WRONG_GATE_EVIDENCE -> DENY
```

Examples:

- runtime boot PASS cannot prove source truth;
- parser PASS cannot prove source identity;
- HTTP 200 cannot prove canonical result content;
- a database connector being available cannot prove service authorization;
- a Quant result cannot prove the correctness of its input data.

## Unknown / deny / wait

```text
UNKNOWN          = evidence insufficient or unavailable
NOT_PROVEN       = required evidence has not been captured
WAIT_EXTERNAL_EVENT = safe progress requires an external infrastructure event
DENY             = action is forbidden until the gate is proven
PASS             = exact gate evidence is valid
```

For promotion purposes:

```text
UNKNOWN != PASS
NOT_PROVEN != PASS
WAIT_EXTERNAL_EVENT != PASS
DENY != PASS
```

## Equivalence rule

There is no forensic concept of “equivalent enough”.

If artifact A is claimed to equal artifact B, the system must prove identity/provenance. Otherwise:

```text
UNPROVEN_EQUIVALENCE -> DENY
```

## Source independence rule

Different hostnames are not sufficient proof of independent sources.

If common upstream/provider/mirror/syndication/fetch path cannot be established:

```text
INDEPENDENCE = NOT_PROVEN
```

and any quorum requiring independence remains DENY.

## Boundary rule

If the result boundary is ambiguous:

```text
RESULT_BOUNDARY_UNKNOWN -> DENY
```

Advertising, redirects, widgets, tracking blocks, and unrelated page content must never redefine the canonical source-result boundary. If the parser cannot establish the boundary safely, it must not promote the artifact.

## Brain role

```text
DATA   = source truth
ENGINE = calculation
SENSOR = observation
BRAIN  = governance/admission
CHAT   = communication interface only
```

Brain must not become the source of truth or the Quant calculation engine.

## Room analogy is architectural, not decorative

Every protected room has its own lock/key boundary.

```text
corridor key + room key + optional inner release
```

Likewise every Forensic gate has its own evidence boundary.

```text
prior gate PASS != successor gate PASS
```

Passing the corridor does not open the room. Having the room key does not prove the room's contents. Reaching the room does not prove the evidence inside it.

## Successor obligation

A future Bot must read this file before modifying foundation admission logic.

When asked to continue, it must first identify the current gate and its exact evidence. If the gate is not proven, it must not manufacture progress, infer success, substitute a different artifact, or unlock a downstream gate.

The correct next action is always the smallest safe action that can produce the missing evidence.
