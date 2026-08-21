# Forensic Admission Chain — Canonical Rule

## Purpose

This document is a permanent architectural rule for every future Brain/Quant bot.
The database gates below are **not separate forensic systems**. They are ordered gates
inside **ONE_FORENSIC_FSM**.

## Core invariant

> PASS at one gate is a local fact and a prerequisite for evaluating the next gate.
> PASS never transfers to another gate.

Therefore:

```text
PASS(G1) != PASS(G2)
PASS(G2) != PASS(G3)
```

A later gate must own and emit its own evidence.

## Database admission chain

```text
DB_EXISTENCE
    |
    v
DB_BINDING
    |
    v
SECRET_RESOLUTION
    |
    v
DB_TLS_ADMISSION
    |
    v
NETWORK_ORIGIN_PROOF
    |
    v
DB_ROUND_TRIP
    |
    v
PROMOTION
```

### Gate meanings

| Gate | What it proves | What it does NOT prove |
|---|---|---|
| DB_EXISTENCE | The database resource exists | The service can access it |
| DB_BINDING | The service has an intended binding | The credential is valid or usable |
| SECRET_RESOLUTION | The secret resolves inside the trusted runtime boundary | TLS or network origin |
| DB_TLS_ADMISSION | The transport satisfies the TLS policy | A successful database transaction |
| NETWORK_ORIGIN_PROOF | The connection reaches the intended database origin | Evidence durability |
| DB_ROUND_TRIP | Real compact evidence can be written, read and hash-verified | Governance permission by itself |
| PROMOTION | Governance permits the next architectural state | Any unproven downstream fact |

## Stop semantics

```text
FAIL(Gn)    -> later gates are UNREACHED
UNKNOWN(Gn) -> later gates are UNREACHED
PASS(Gn)    -> only Gn+1 may be evaluated
```

Never convert UNREACHED into PASS by inference.

## Architectural analogy

The DB is a secured room.

```text
corridor key
    +
room key
    +
secret resolution
    +
TLS admission
    +
origin proof
    +
inner evidence check
    =
actual admission
```

The existence of a room is not possession of its key.
Possession of a key is not proof that the key works.
A working key is not proof that the room contains the expected evidence.
A successful evidence round-trip is not permission to promote unless the promotion gate owns its own evidence.

## Interaction with the E2E mission

```text
REAL_DATA
  -> VALID_RESEARCH
  -> VALID_BACKTEST
  -> EDGE
  -> EV_PNL_ROI
  -> ROBUSTNESS_RISK_DRIFT
  -> CONTROLLED_ACTION
```

Each segment owns its exit evidence.
A PASS in an upstream segment is a prerequisite, never a downstream PASS.

## Forensic immutability

Corrections never overwrite an admitted observation.
They create a new immutable version with a new receipt/hash.

```text
observation_v1 --immutable
observation_v2 --new evidence
observation_v3 --new evidence
```

## Security rules

- `DATABASE_URL` and credentials never enter GitHub.
- Credentials never enter Brain state files.
- Credentials never enter logs or workflow receipts.
- Raw-byte hash and semantic hash have different meanings.
- Ads are non-truth content.
- Generic page numbers are not truth.
- Synthetic history is forbidden in production.
- Render Free 512 MB remains a hard boundary; 320 MiB is the conservative guard.
- Brain remains the governance control plane; Quant Engine remains the calculation/data-research plane.

## Successor instruction

If a future bot sees `DB_EXISTENCE=PASS`, it MUST NOT write `DB_BINDING=PASS`.
If it sees `DB_BINDING=PASS`, it MUST NOT write `DB_TLS_ADMISSION=PASS`.
If it sees `DB_ROUND_TRIP=PASS`, it MUST still evaluate the explicit promotion gate.

**Evidence is local. Permission is not inherited.**
