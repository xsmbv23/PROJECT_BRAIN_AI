# NETWORK EVIDENCE PIPELINE V1

## Purpose

Replace the legacy scrape model with a deterministic forensic evidence collector.
The collector may observe and package evidence. It may not decide truth.

## Pipeline

```text
SOURCE WEB
   |
   v
HTTP/TLS TRANSPORT
   |
   +--> resolved IP
   +--> TLS version
   +--> peer certificate SHA-256
   +--> HTTP status/headers
   |
   v
RAW PAYLOAD STREAM
   |
   +--> 64 KiB chunks
   +--> payload SHA-256
   +--> capture timestamp UTC
   |
   v
NETWORK_ORIGIN_PROOF
   |
   +--> missing evidence ----> HARD DENY
   |
   v
WEB CANDIDATE EVIDENCE
   |
   v
EXCEL_VS_WEB_GATE
   |
   +--> mismatch -----------> DENY
   +--> unknown ------------> DENY
   +--> match + proof ------> CANONICAL DATA CANDIDATE
   |
   v
DATA DOMAIN
   |
   +--> downstream engines/sensors
```

## Authority boundaries

### Scraper / Evidence Collector

Can:

- make network requests;
- capture transport metadata;
- capture raw response evidence;
- hash payloads;
- record immutable receipts;
- identify candidate fields using selector allowlists.

Cannot:

- declare PASS/FAIL for truth;
- produce trading signals;
- produce risk decisions;
- overwrite Excel Ground Truth;
- infer missing values;
- silently normalize conflicting source data.

### NETWORK_ORIGIN_PROOF

This is a transport-authenticity gate, not a data-truth gate.

Minimum evidence:

1. resolved IP;
2. TLS version;
3. peer certificate SHA-256;
4. response SHA-256;
5. capture timestamp.

If any required component is missing, state is `NOT_PROVEN`, never PASS.

### EXCEL_VS_WEB_GATE

This is the data-content reconciliation gate.
It owns the decision whether the web candidate can become canonical data.

The network collector must never bypass it.

## Advertising rule

Lottery-result pages may contain advertisements, banners, tracking elements,
recommendation widgets, or injected HTML.

The collector therefore uses an allowlist of result selectors and a denylist of
known advertisement/container patterns. Ad content is not evidence.

Important:

```text
visible text != evidence
DOM text != evidence
advertisement text != result data
```

Only data captured from an approved result selector is eligible for the candidate
payload. Ambiguous selector matches produce `UNKNOWN` and stop promotion.

## Memory / Render rule

The collector must not build a giant in-memory history.

Use streaming/chunking:

```text
HTTP response
   |
   +--> chunk <= 64 KiB
   |
   +--> incremental SHA-256
   |
   +--> append evidence store
   |
   +--> release chunk
```

This preserves the 320 MiB Render safety guard.

## Interaction with DB admission

Network evidence and database admission are independent chains.

```text
NETWORK_ORIGIN_PROOF
          |
          v
EXCEL_VS_WEB_GATE

DATABASE_EXISTENCE
          |
          v
DATABASE_BINDING
          |
          v
DATABASE_TLS_ADMISSION
          |
          v
DATABASE_ROUND_TRIP
```

Neither chain can grant the other chain a PASS.

## Immutable receipt

Each capture receives a compact receipt containing metadata and hashes.
The receipt is append-only. It must never contain credentials.

## Successor rule

A future Bot must treat this document and
`contracts/network_evidence_collector_v1.json` as the authoritative replacement
for any legacy scraper that parses first and judges later.
