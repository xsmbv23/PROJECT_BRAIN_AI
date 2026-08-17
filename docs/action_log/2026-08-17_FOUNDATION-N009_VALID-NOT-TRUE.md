# FOUNDATION-N009 — Observation Semantic Hardening

## Trigger

The foundation review identified that an unqualified `VALID` receipt classification can be misread by a successor Bot as `DATA_IS_TRUE`.

## Decision

Freeze the stronger semantic:

```text
VALID ≠ TRUE
STRUCTURALLY_VALID ≠ DOMAIN_CORRECT
ROUNDTRIP_VALID ≠ DOMAIN_UNDERSTANDING
```

## Why

A first receipt only demonstrates that the system communicated with a real source and captured evidence according to the transport/integrity checks that were actually performed.

It does not prove the meaning of the source content.

## Required flow

```text
RECEIPT_1
   ↓
CLASSIFY
   ↓
STORE EXACT RAW + RECEIPT
   ↓
STOP
```

No parser, normalization, schema inference, 27-field mapping, or canonical promotion may originate from receipt_1.

## Canonical path

```text
SOURCE → EVIDENCE → ADMISSION → CANONICAL → CONSUMER
```

One-way only.

Hard minimum canonical quorum: 2 observations.
Preferred quorum: 3 observations.

Stability, variance, drift, and unresolved conflict remain mandatory gates.

## Forensic consequence

The state machine remains a **single forensic admission chain**. These are not separate forensic systems. Each PASS is only evidence for its own gate and a prerequisite for the next gate; PASS never inherits authority across gates.

## Successor instruction

Any Bot that sees an old `VALID` token must interpret it only under historical compatibility semantics. New code must emit `STRUCTURALLY_VALID` or `ROUNDTRIP_VALID` with the narrowest meaning actually proven.

Never silently upgrade the semantic strength of a receipt.

## Current architecture

- Brain = governance/control plane.
- Data repository = source truth.
- Quant Engine = calculation authority.
- Sensors = observation only.
- Chat = communication interface only.
- Layer 1 = separate Quant Engine rooms.
- Staircase = locked until foundation promotion gates are proven.
- Render Free 512 MB = hard boundary; 320 MiB guard remains.
