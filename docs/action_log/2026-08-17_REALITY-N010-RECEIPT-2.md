# REALITY-N010-RECEIPT-2 — Successor Handoff

## Meaning

`RECEIPT_1` proves one real observation. `RECEIPT_2` must prove that the same runtime capture path can reach Reality again. N010 is therefore a **repeatability/capture capability gate**, not a semantic comparison gate.

## Current exact state

```text
RECEIPT_1              = CAPTURED
RECEIPT_1 TRANSPORT    = ROUNDTRIP_VALID
RECEIPT_1 DOMAIN_TRUTH = UNREACHED
RECEIPT_2              = NOT_CAPTURED
REPEATABILITY          = NOT_PROVEN
PROMOTION              = DENY
```

The canonical state file records that direct container raw HTTP for `https://ketqua16.net/` is blocked by the current DNS/network boundary. No Receipt-2 hash was fabricated. No browser-visible HTML was substituted for exact raw bytes.

## N010 rule

```text
RECEIPT_1
  -> proves capture capability once

RECEIPT_2
  -> proves capture path can repeat

RECEIPT_1 + RECEIPT_2
  -> permits transport-level comparison only
```

Allowed comparison fields:

- HTTP status
- content type
- final URL
- raw byte count
- SHA-256
- observation timestamp

Forbidden at N010:

- HTML parsing
- 27-field extraction
- normalization
- domain mapping
- business-date inference
- cross-source merge
- canonical truth claim

## Hard rule

No Receipt-2 means no transport comparison and no N011. Do not manufacture Receipt-2 from browser output, copied HTML, a synthetic payload, or a manually supplied hash.

## Successor action

The next Bot must either:

1. restore a controlled runtime with exact raw-byte access to the same source path; or
2. execute the same collector code in a second controlled runtime and capture Receipt-2 with explicit `runtime_origin`.

In either case, the evidence must contain at minimum:

```text
sha256
byte_length
timestamp
runtime_origin
```

Then stop and classify. Do not jump into parsing or Layer 1.
