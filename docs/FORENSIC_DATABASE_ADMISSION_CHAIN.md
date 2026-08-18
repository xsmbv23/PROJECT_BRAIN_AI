# Forensic Database Admission Chain

## Canonical rule

The database admission states are **not independent Forensic systems**. They are sequential gates in one `FORENSIC DATABASE ADMISSION CHAIN`.

A PASS at an earlier gate is only a prerequisite for evaluating the next gate. **PASS is never inherited by inference.**

> UNKNOWN_IS_NOT_PASS
> DEFAULT_DENY
> NO_INFERENCE_ACROSS_GATES

## Chain

```text
FORENSIC DATABASE ADMISSION CHAIN
            |
            +--> DB_EXISTENCE
            |      |
            |    PASS
            |      v
            +--> DB_BINDING
            |      |
            |    PASS
            |      v
            +--> DB_TLS_ADMISSION
            |      |
            |  BOUND_TLS
            |      v
            +--> NETWORK_ORIGIN_PROOF
            |      |
            |   PROVEN / UNKNOWN
            |      v
            +--> DB_ROUND_TRIP
            |      |
            |    MATCH
            |      v
            +--> PROMOTION
```

Any failure or unknown state terminates admission with `DENY`.

## Critical distinctions

```text
DATABASE EXISTS
    !=
SERVICE IS BOUND
    !=
SERVICE IS TLS-ADMITTED
    !=
NETWORK PATH IS PROVEN
    !=
DURABLE ROUND-TRIP IS PROVEN
    !=
PROMOTION IS ALLOWED
```

These are observations about different admission questions, not contradictory states.

## Gate semantics

- `DB_EXISTENCE`: proves the PostgreSQL resource exists and is available. It does not grant service access.
- `DB_BINDING`: proves the service possesses an explicit binding (`DATABASE_URL`). It does not prove safe communication.
- `DB_TLS_ADMISSION`: proves the binding satisfies the accepted TLS policy (`require`, `verify-ca`, `verify-full`). It does not prove a reachable database path.
- `NETWORK_ORIGIN_PROOF`: proves the exact-current deployed runtime can establish the declared network path to the database origin. A generic IP allowlist is not proof of a successful path.
- `DB_ROUND_TRIP`: proves a real compact metadata envelope was written, read back, and SHA-256 verified as identical. The payload must contain no credentials and no bulk/source data.
- `PROMOTION`: may pass only after all required preceding gates have independently produced their evidence.

## State interaction rule

These gates form a **single monotonic admission chain**, not a collection of independent booleans.

A gate may emit evidence that enables evaluation of the next gate, but it may never mutate or promote the state of a later gate by inference.

```text
Earlier PASS = prerequisite
Later PASS   = separately observed fact

PASS inheritance by inference = FORBIDDEN
```

The chain is compositional:

```text
DB_EXISTENCE PASS
    -> permits DB_BINDING evaluation

DB_BINDING PASS
    -> permits DB_TLS_ADMISSION evaluation

DB_TLS_ADMISSION BOUND_TLS
    -> permits NETWORK_ORIGIN_PROOF evaluation

NETWORK_ORIGIN_PROOF PROVEN
    -> permits DB_ROUND_TRIP evaluation

DB_ROUND_TRIP MATCH
    -> permits PROMOTION evaluation
```

A failure/unknown at any stage terminates admission and does not contaminate earlier observations.

## Exact-current truth priority

```text
EXACT_CURRENT_RUNTIME_EVIDENCE
        >
PERSISTED_FORENSIC_RECORD
        >
OLD_DOCUMENTATION
        >
HYPOTHESIS
```

If an old deployment says `BOUND_TLS` but the exact-current runtime cannot prove network origin, the effective state remains `NETWORK_ORIGIN_PROOF = NOT_PROVEN` and promotion remains denied.

## Door/key analogy

- `DB_EXISTENCE`: the room exists.
- `DB_BINDING`: the service has the room's key.
- `DB_TLS_ADMISSION`: the key is accepted for protected communication.
- `NETWORK_ORIGIN_PROOF`: the exact-current route to the room is proven.
- `DB_ROUND_TRIP`: the door actually opened and the forensic interaction was proven intact.
- `PROMOTION`: only after the full chain succeeds may durable DB evidence be promoted.

A service must never infer a later gate from an earlier PASS.

## Current canonical handoff

```text
DB_EXISTENCE          = PASS
DB_BINDING            = BOUND_TLS
DB_TLS_ADMISSION      = PASS
NETWORK_ORIGIN_PROOF  = NOT_PROVEN
DB_ROUND_TRIP         = NOT_PROVEN
PROMOTION             = HARD_DENY
```

The current state machine declares `MANDATORY_NO_OP` while waiting for the real external infrastructure event that can produce network-origin evidence. `MANDATORY_NO_OP` is an **active safety state**, not inactivity.

## Allowed while waiting

```text
ALLOW:
  - read exact-current runtime evidence
  - monitor the declared external infrastructure event
  - append non-mutating forensic documentation
  - validate documentation integrity

DENY:
  - fabricate network proof
  - inherit PASS between gates
  - treat BOUND_TLS as network-origin proof
  - treat in-memory round-trip as durable DB evidence
  - advance downstream work without promotion
  - unlock Layer 1
  - unlock staircase
  - store credentials in GitHub
  - self-manufacture the external event
```

## Forbidden transitions

```text
DB_EXISTENCE = PASS
    -> DB_BINDING = PASS          FORBIDDEN BY INFERENCE

DB_BINDING = PASS
    -> DB_TLS_ADMISSION = PASS   FORBIDDEN BY INFERENCE

DB_TLS_ADMISSION = BOUND_TLS
    -> NETWORK_ORIGIN_PROOF = PROVEN   FORBIDDEN BY INFERENCE

NETWORK_ORIGIN_PROOF = PROVEN
    -> DB_ROUND_TRIP = MATCH      FORBIDDEN BY INFERENCE
```

Each transition requires its own observable evidence.

## Forensic invariants

1. `UNKNOWN_IS_NOT_PASS`.
2. `DEFAULT_DENY`.
3. No credential is stored in GitHub.
4. No credential is emitted in logs or evidence envelopes.
5. `psycopg` remains outside Brain `core/`.
6. Compact metadata only for admission probes.
7. Real write/read/hash evidence is required for durable round-trip PASS.
8. Layer 1 remains locked until the foundation promotion gate is explicitly satisfied.
9. The successor action log is authoritative for continuation.
10. A database resource's existence is never treated as an authorization grant.
11. A successful binding is never treated as proof of TLS admission.
12. TLS admission is never treated as proof of network reachability.
13. Network reachability is never treated as proof of durable evidence persistence.
14. Exact-current evidence outranks historical deployment descriptions.
15. A waiting safety state permits documentation/observation only; it does not authorize operational mutation.

## Successor instruction

Every future Bot must read this file and `state/next_action.json` before touching the database admission path.

Never collapse the chain into a single boolean such as `DATABASE_PASS`.

If a future Bot sees:

```text
DB_EXISTENCE = PASS
DB_BINDING = NOT_BOUND
```

the correct interpretation is **database exists but service has no admitted access**. It is not an inconsistency.

If:

```text
DB_BINDING = PASS
DB_TLS_ADMISSION = DENY_TLS
```

the correct interpretation is **binding exists but is not admitted for protected communication**.

If:

```text
DB_TLS_ADMISSION = BOUND_TLS
NETWORK_ORIGIN_PROOF = NOT_PROVEN
```

the correct interpretation is **the key/TLS path is admitted, but the exact-current network path remains unproven**.

Only:

```text
NETWORK_ORIGIN_PROOF = PROVEN
AND
DB_ROUND_TRIP = MATCH
```

may reach `PROMOTION`.
