# SOURCE PROVENANCE PROTOCOL V1

## Purpose

A semantic match is not source provenance. A rendered page is not a raw artifact. Two domains are not automatically independent.

## Per-source receipt

Every provenance capture MUST preserve a compact receipt containing:

- `source_id`
- `request_url`
- `request_timestamp`
- `http_status`
- `content_type`
- `redirect_chain`
- `raw_artifact_path`
- `raw_response_bytes`
- `raw_sha256`
- `normalized_full27_sha256`
- `parser_version`
- `source_identity`
- `anti_ad_collision_identity`
- `independence_status`

Credentials, cookies containing secrets, authorization headers, and connection strings MUST NOT enter the receipt.

## Raw artifact rule

The exact HTTP response bytes are the source artifact. If exact bytes cannot be captured and retained, provenance is `NOT_PROVEN`.

A parser may derive FULL_27 from the raw artifact, but derived hashes never replace `raw_sha256`.

## Anti-ad collision identity

Advertising, analytics, CDN fragments, and shared third-party widgets MUST NOT be mistaken for source independence.

The identity record may include:

- canonical domain
- resolved IP(s), when observable
- HTML structural fingerprint
- response-server metadata, when observable
- obvious shared-provider markers

This identity is evidence only. It does not by itself prove independence.

## Independence rule

`independence_status = PROVEN` requires observable evidence that the two source paths do not merely mirror the same upstream artifact/provider.

Different domains alone are insufficient.

If independence cannot be proven:

```text
source_independence = NOT_PROVEN
canonical_quorum = DENY
```

## Ordered gate

```text
SEMANTIC_CONSENSUS
        ↓
RAW_PROVENANCE
        ↓
SOURCE_INDEPENDENCE
        ↓
SEMANTIC_RECONCILIATION
        ↓
CANONICAL_QUORUM
```

No later PASS inherits from an earlier PASS.

## Render memory rule

Capture is bounded and streamed. The adapter MUST NOT accumulate multiple full responses in memory. Raw artifacts are written incrementally and hashed incrementally.

The 320 MiB runtime guard remains mandatory.
