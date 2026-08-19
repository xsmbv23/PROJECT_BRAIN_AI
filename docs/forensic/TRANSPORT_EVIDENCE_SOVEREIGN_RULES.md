# TRANSPORT EVIDENCE — SOVEREIGN RULES

These rules are immutable foundation law for the Transport Evidence layer.

## Rule T1 — Raw Payload Immutability

The raw transport byte sequence is sovereign evidence.

A received HTTP body is preserved exactly as transported. HTML wrappers, advertising, banners, tracking markup, scripts, boilerplate, and other non-target material are still part of the raw transport byte sequence.

At Transport Evidence:

- DO NOT parse semantic content.
- DO NOT strip HTML.
- DO NOT remove advertisements.
- DO NOT normalize whitespace.
- DO NOT decode-and-reencode as a substitute for the original bytes.
- DO NOT infer which bytes are useful.
- DO NOT promote any candidate truth.

Filtering, extraction, normalization, canonicalization, and semantic interpretation belong to a later **derived transformation** layer and must reference the immutable transport receipt.

Therefore:

```text
RAW TRANSPORT
     = evidence
     != cleaned data
     != canonical truth
```

An advertisement is not “noise” at this layer. It is part of what the source actually returned.

## Rule T2 — Bounded Buffer Protection

Transport reads have a hard maximum of:

```text
MAX_BYTES = 131072
          = 128 KiB
```

The probe reads at most `MAX_BYTES + 1` solely to detect truncation. If the payload exceeds the bound, the verdict is `DENY_TRUNCATED`; the oversized payload is never admitted as a valid transport receipt.

The 128 KiB ceiling is a hard OOM-control boundary for Render Free. It is not a tuning suggestion.

Observed foundation/runtime memory remains materially below the 320 MiB Render guard; transport buffering must never become a route to Buffer Bloat.

## Admission conditions

A Transport Evidence receipt may be PASS only when all are true:

```text
HTTP status = 200
bytes <= 128 KiB
truncated = false
body is non-empty
SHA-256 is computed from the exact admitted bytes
```

Otherwise:

```text
DENY
```

## Security / Forensic interaction

Transport PASS does NOT imply:

- canonical source truth,
- semantic correctness,
- data completeness,
- database persistence,
- Layer 1 permission,
- staircase unlock.

Transport PASS only proves:

> The exact bounded byte sequence was successfully received from the specified source under the transport rules.

## Inheritance rule

No later gate may mutate the raw receipt. Derived artifacts must point back to the raw receipt by immutable evidence identity (SHA-256 + receipt metadata).

## Source target

Current probe target:

```text
https://ketqua16.net/
```

The same rules apply to every future XSMB source.
