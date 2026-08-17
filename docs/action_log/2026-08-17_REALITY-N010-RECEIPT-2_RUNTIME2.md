# REALITY-N010 — RECEIPT_2 second-runtime protocol

## Purpose

Acquire the second independent observation from real world transport without changing the canonical collector.

## Runtime 2

GitHub Actions `ubuntu-latest` is used only as an independent execution surface.

It invokes the exact repository collector:

```text
python tools/real_world_collector.py
```

No forked collector logic is introduced.

## Invariants

```text
SOURCE       = https://ketqua16.net/
METHOD       = GET
RAW_BYTES    = captured before parsing
HASH         = SHA-256 of exact raw bytes
PARSE        = FORBIDDEN
NORMALIZE    = FORBIDDEN
MAPPING      = FORBIDDEN
DOMAIN_TRUTH = FORBIDDEN
```

The workflow only validates receipt shape and uploads the raw artifact plus compact receipt. It does not alter the source bytes before hashing.

## Current status

Workflow definition committed at:

```text
c0f9894dad1b86f4e6807d63e20c33cb58d32482
```

The receipt itself is **NOT YET CAPTURED/PROVEN** until the resulting GitHub Actions run is observed and its receipt artifact is retrieved.

Therefore:

```text
RECEIPT_1 = CAPTURED
RECEIPT_2 = PENDING_RUNTIME_OBSERVATION
COMPARE   = NOT_STARTED
PROMOTION = DENY
```

## Comparison gate

When receipt 2 exists, compare only:

- HTTP status
- Content-Type
- final URL
- raw byte count
- SHA-256
- observed timestamp

Then stop.

No interpretation of the page content is permitted at this stage.
