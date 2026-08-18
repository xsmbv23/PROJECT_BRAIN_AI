# Forensic Database Admission Chain

## Canonical interpretation

There are NOT two independent Forensic state machines for database access.

There is ONE `ONE_FORENSIC_FSM`, and database admission is a sequence of local gates inside that single machine.

The canonical chain is:

```text
DB_EXISTENCE
    -> DB_BINDING
    -> SECRET_RESOLUTION
    -> DB_TLS_ADMISSION
    -> NETWORK_ORIGIN_PROOF
    -> DB_ROUND_TRIP
    -> PROMOTION
```

## Meaning of each gate

| Gate | Question | PASS means | PASS does NOT mean |
|---|---|---|---|
| `DB_EXISTENCE` | Does the database resource actually exist? | Resource existence is evidenced | Service may access it |
| `DB_BINDING` | Is the service configured with the required binding name? | Binding presence is evidenced | Credential is valid |
| `SECRET_RESOLUTION` | Is the secret resolved from the authorized secret store? | Authorized secret resolution is evidenced | TLS/network admission is proven |
| `DB_TLS_ADMISSION` | Does the resolved PostgreSQL connection satisfy TLS policy? | TLS admission is evidenced | Network origin is proven |
| `NETWORK_ORIGIN_PROOF` | Did the connection originate from the authorized runtime path? | Runtime-origin evidence exists | Database read/write is proven |
| `DB_ROUND_TRIP` | Can the runtime write/read a compact metadata envelope and verify SHA-256 equality? | Durable evidence round-trip is proven | Domain truth is automatically promoted |
| `PROMOTION` | Are all preceding gates fresh, valid, and consistent? | Durable evidence sink may be admitted | Future gates may be skipped |

## No pass inheritance

The most important invariant is:

> **PASS is local to the gate that produced it. PASS is a prerequisite for the next gate, never inherited permission.**

Therefore:

```text
DB_EXISTENCE = PASS
        !=
DB_BINDING = PASS
```

and:

```text
DB_BINDING = PASS
        !=
DB_TLS_ADMISSION = PASS
```

and:

```text
DB_TLS_ADMISSION = PASS
        !=
DB_ROUND_TRIP = PASS
```

and:

```text
DB_ROUND_TRIP = PASS
        !=
CANONICAL_DOMAIN_TRUTH = PASS
```

Every transition requires fresh observable evidence appropriate to that transition.

## Failure semantics

```text
UNKNOWN -> DENY
FAIL    -> DENY
MISSING EVIDENCE -> DENY
INVALID EVIDENCE -> DENY
```

A previous PASS may never be reused to manufacture a later PASS.

A later gate cannot overwrite, erase, or reinterpret a prior failure.

## Edge semantics

Every edge in the Forensic graph must identify:

```text
SOURCE NODE
TARGET NODE
OBSERVABLE RECEIPT
```

If an edge has no observable receipt, it is not an admitted edge.

```text
unknown_edge = DENY
broken_edge = DENY
cross_layer_edge_without_contract = DENY
```

## Relation to the security-room model

The same principle applies to the corridor/room model:

```text
corridor_key
    -> room_key
        -> protected-room inner release
            -> operation admission
```

Having a corridor key does not grant a room key.
Having a room key does not defeat an inner latch.
Opening the room does not grant permission to perform every operation inside it.

## Current concrete state

The current runtime evidence records `database_binding_status = NOT_BOUND`.
Render Postgres exists, but the service-side binding has not been proven.
Therefore the database admission chain remains below `DB_BINDING` and promotion remains `DENY`.

A screenshot showing an empty `DATABASE_URL` field is supporting human-visible evidence of the same boundary, but it is not by itself a runtime promotion receipt. The machine-readable runtime probe remains authoritative for runtime state.

## Prohibited shortcuts

Never:

- fabricate `DATABASE_URL`
- copy credentials into GitHub
- log credentials
- treat database existence as authorization
- treat unit-test success as a durable DB round-trip
- treat a durable DB round-trip as canonical XSMB domain truth
- unlock Room 02 from a stale PASS
- bypass the admission chain because an intermediate gate is inconvenient

## Successor instruction

A successor Bot must read this document before modifying database admission logic.
If state says `WAIT_EXTERNAL_EVENT` and `action_space = 0`, the correct action is a mandatory no-op until a genuine external event appears. Do not manufacture an event to make progress.
