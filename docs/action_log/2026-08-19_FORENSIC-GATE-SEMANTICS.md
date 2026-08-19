# Forensic Gate Semantics — Permanent Successor Rule

## Canonical rule

There is ONE Forensic FSM. Database existence, service binding, TLS admission and durable round-trip are not separate Forensic systems. They are sequential gates inside one admission chain.

```text
DB_EXISTENCE
 -> DB_BINDING
 -> SECRET_RESOLUTION
 -> DB_TLS_ADMISSION
 -> NETWORK_ORIGIN_PROOF
 -> DB_ROUND_TRIP
 -> PROMOTION
```

## Non-inheritance law

A PASS at one gate is only a prerequisite edge to the next declared gate. It never inherits permission or PASS status.

```text
DB_EXISTENCE PASS != DB_BINDING PASS
DB_BINDING PASS != DB_TLS PASS
DB_TLS PASS != NETWORK_ORIGIN PASS
NETWORK_ORIGIN PASS != ROUND_TRIP PASS
ROUND_TRIP PASS != automatic downstream room authority
```

The first FAIL or UNKNOWN stops downstream reachability. Later gates are UNREACHED.

## Why this matters

`DB_EXISTS` means the secured room exists.

`DB_BINDING` means the service has a candidate key through the approved boundary.

`DB_ROUND_TRIP` means the exact runtime demonstrably entered the room and preserved evidence integrity.

These are different evidence claims but one FSM.

## Successor instruction

Never interpret the presence of a resource as authorization to use it. Never infer a deeper PASS from a shallower PASS. Only gate-local evidence may promote a gate.

## Quant Engine boundary

Quant Engine may observe real-source receipts but cannot promote canonical truth from raw-byte equality. Independent sites can legitimately have different HTML bytes due to markup, ads, tracking and transport details. Raw SHA equality is BYTE_IDENTITY only. Semantic quorum requires independently produced semantic hashes for the same explicit business date/domain contract.

## Current policy

```text
FIXTURE_IS_NOT_REALITY
UNKNOWN_IS_NOT_PASS
UNREACHED_IS_NOT_PASS
DEFAULT_DENY
LAYER_1_LOCKED
STAIRCASE_LOCKED
```
