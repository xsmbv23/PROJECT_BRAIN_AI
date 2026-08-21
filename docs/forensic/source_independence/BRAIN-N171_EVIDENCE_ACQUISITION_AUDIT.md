# BRAIN-N171 — Evidence Acquisition Audit

## Finding

The S1 blocker should not be reduced to repeated public-web scraping attempts.

`SOURCE_INDEPENDENCE` remains a valuable corroboration gate, but S1_CANONICAL_EVIDENCE_V2 can be satisfied through a lawful evidence channel that preserves real provenance and immutable bytes.

## New admissible route

The acquisition contract now permits:

- `AUTOMATED_SOURCE_WITH_EXPLICIT_PERMISSION`
- `MANUAL_AUTHORIZED_CAPTURE`
- `DURABLE_ARCHIVE_EXPORT`

The common S1 requirements remain unchanged: real provenance, immutable raw bytes, verifiable raw-byte SHA-256, complete real-date coverage, zero unresolved conflicts, observable admission receipt, frozen canonical hash, and `synthetic_data=false`.

## Peer coordination

Bot 2's N170 source-independence work is acknowledged. The source-independence deny is preserved as immutable history. Bot 1 is not reopening that decision; it is providing an alternate lawful acquisition path so the E2E pipeline is not permanently coupled to automated multi-site scraping.

## E2E continuation

S1 remains BLOCKED until one admissible evidence bundle satisfies the canonical evidence contract.

After S1 PASS:

`S2 VALID_RESEARCH` may open only with its own gate-local evidence.

`S3 VALID_BACKTEST` remains UNREACHED until S2 PASS.

## Constraints

No unauthorized scraping, no synthetic data, no mutation of raw artifacts, no inheritance of PASS from another gate, and no treating Render liveness or CI PASS as canonical-data evidence.
