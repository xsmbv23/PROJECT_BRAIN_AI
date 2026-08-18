# FORENSIC ADMISSION CHAIN — Successor Clarification

## Permanent rule

There is **ONE Forensic FSM**, not multiple independent Forensic states/systems.

The database admission gates are sequential evidence gates:

```text
DB_EXISTENCE
  -> DB_BINDING
  -> SECRET_RESOLUTION
  -> DB_TLS_ADMISSION
  -> NETWORK_ORIGIN_PROOF
  -> DB_ROUND_TRIP
  -> PROMOTION
```

## Critical invariant

A PASS at one gate is **only a prerequisite edge** to the next gate.
It is never inherited by the next gate.

```text
DB_EXISTENCE PASS
    != DB_BINDING PASS

DB_BINDING BOUND_TLS
    != SECRET_RESOLUTION PASS

DB_TLS_ADMISSION PASS
    != NETWORK_ORIGIN_PROOF PASS

NETWORK_ORIGIN_PROOF PASS
    != DB_ROUND_TRIP PASS
```

Every PASS requires evidence belonging specifically to that gate.

## Current safety consequence

The exact-current state is currently frozen in `WAIT_EXTERNAL_EVENT` / `MANDATORY_NO_OP` because `NETWORK_ORIGIN_PROOF` is not proven. Therefore the Brain must not attempt to manufacture or simulate that external event.

Permitted during the wait:

- observe exact-current evidence;
- monitor the declared external event;
- append non-mutating documentation;
- validate documentation integrity.

Forbidden:

- fabricate network proof;
- infer origin proof from BOUND_TLS;
- treat local/in-memory round-trip as durable evidence;
- mutate infrastructure credentials/network configuration without infrastructure authority;
- unlock downstream gates.

## Why this matters for Bot generations

A future Bot must not compress the chain into a single boolean such as `DATABASE_PASS=true`.

It must preserve the distinction between:

```text
resource existence
resource binding
secret resolution
transport security
runtime origin
actual durable round-trip
promotion authority
```

These are different evidence questions inside the **same** Forensic FSM.

## OOM preservation

No waiting-state documentation may load source datasets or bulk evidence. The Foundation remains dataset-free and retains the 320 MiB conservative Render guard.

## Authority

This clarification supplements `docs/architecture/FORENSIC_DATABASE_ADMISSION_CHAIN.md` and does not change the current action space.

```text
FOUNDATION = FROZEN
ACTION_SPACE = 0
ACTION = MANDATORY_NO_OP
PROMOTION = DENY
LAYER_1 = LOCKED
STAIRCASE = LOCKED
```
