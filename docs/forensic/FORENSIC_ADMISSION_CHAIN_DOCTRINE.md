# Forensic Admission Chain Doctrine

## Status

This document is normative foundation doctrine. It does not create a second Forensic system.

There is exactly **ONE Forensic FSM**. Database admission is one chain inside that FSM.

```text
DB_EXISTENCE
    -> DB_BINDING
    -> SECRET_RESOLUTION
    -> DB_TLS_ADMISSION
    -> NETWORK_ORIGIN_PROOF
    -> DB_ROUND_TRIP
    -> PROMOTION
```

## Gate semantics

A gate result is **local evidence only**.

```text
PASS_IS_LOCAL
PASS_IS_PREREQUISITE_ONLY
NO_PASS_INHERITANCE
UNKNOWN_IS_NOT_PASS
DEFAULT_DENY
OWN_GATE_EVIDENCE_REQUIRED
FRESH_EVIDENCE_REQUIRED_FOR_PROMOTION
```

Therefore:

```text
DB_EXISTENCE = PASS
```
means only:

> The database resource is proven to exist.

It does **not** mean that the service is authorized to access it.

Likewise:

```text
DB_BINDING = PASS
```
means only that the service-side binding is proven. It does not prove TLS admission, network-origin proof, or a successful database round-trip.

Likewise:

```text
DB_TLS_ADMISSION = PASS
```
does not prove a real database transaction.

Only the evidence owned by `DB_ROUND_TRIP` can establish:

```text
WRITE -> READ -> SHA256 MATCH
```

and only that fresh evidence can satisfy the durable-evidence promotion gate.

## Interaction model

The gates are sequential admission conditions, not independent Forensic states:

```text
             ONE FORENSIC FSM
                    |
                    v
             [EXISTENCE GATE]
                    |
             prerequisite only
                    v
             [BINDING GATE]
                    |
             prerequisite only
                    v
             [TLS GATE]
                    |
             prerequisite only
                    v
          [NETWORK ORIGIN GATE]
                    |
             prerequisite only
                    v
          [ROUND-TRIP GATE]
                    |
             fresh evidence
                    v
           [PROMOTION GATE]
```

No gate may upgrade another gate's status by inference.

## Security analogy

The physical-house model is normative:

1. Corridor key grants access to the corridor.
2. Room key grants access to the room.
3. A protected room may require an inner latch / bell / human release.
4. Reaching the room does not prove permission to enter it.
5. Entering the room does not prove the evidence inside is valid.
6. Evidence must be observed at the gate that owns that evidence.

Thus:

```text
corridor_access != room_access != inner_release != evidence_validity != promotion
```

## Successor-Bot rule

A future Bot must never compress the chain into:

```text
DB_EXISTS -> DATABASE_PASS
```

or:

```text
BOUND_TLS -> ROUND_TRIP_PASS
```

or:

```text
ROUND_TRIP_PASS -> PROMOTION
```

without the exact evidence required by the promotion contract.

The correct rule is:

```text
previous PASS = permission to evaluate the next gate
next PASS     = evidence owned by the next gate
```

## Parallel-agent rule

Multiple Bots may work concurrently only in **disjoint safe lanes**.

A parallel Bot may:

- inspect code;
- repair registry/collector drift;
- add tests;
- add documentation;
- add non-promoting evidence tooling;
- measure memory;
- prepare an admission candidate.

A parallel Bot may not:

- change `action_space` from 0;
- promote evidence;
- unlock Room 02;
- unlock the staircase;
- weaken DEFAULT_DENY;
- infer external observation from public-web agreement;
- expose credentials;
- replace exact-current evidence with historical logs.

The repository's authoritative `state/current_state.json` and `state/next_action.json` remain the successor hand-off boundary.

## Immutable conclusion

There are not two Forensic systems.

There is one Forensic FSM containing multiple evidence gates. Their states interact by **ordered admission**, not by state inheritance.
