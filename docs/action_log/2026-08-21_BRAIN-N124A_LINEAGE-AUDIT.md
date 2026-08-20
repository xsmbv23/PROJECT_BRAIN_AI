# BRAIN-N124A — Lineage Contract Authority / Producer Audit

## Pre-action coordination

Read shared dual-bot coordination contract and BOT_2 latest action log before acting.

BOT_2 latest observed action: `2026-08-21_QUANT-N006.md`.
It fixes semantic quorum semantics, requires distinct source IDs, separates raw byte identity from semantic meaning, and keeps canonical promotion blocked.

## Finding

There were two lineage contract schemas:

1. `contracts/evidence_lineage_admission_v1.json` — current admission schema used by the lineage validator.
2. `contracts/evidence_lineage_v1.json` — older schema using `raw_sha256` / `semantic_sha256` names.

Rewriting the historical contract would violate Forensic immutability.

## Action

Created `contracts/evidence_lineage_contract_registry_v1.json` to explicitly classify:

- admission contract = `CURRENT_AUTHORITY`
- older lineage contract = `HISTORICAL_EVIDENCE`

Added regression test ensuring exactly one current lineage authority exists.

## Producer audit

`tools/network_evidence_collector.py` emits external observation metadata including URL, resolved IP, TLS version, certificate hash, HTTP status, response SHA-256, timestamp and byte count.

`tools/n104c1_transport_inspection.py` consumes that receipt and performs bounded transport/panel inspection. It does not admit candidates or canonical truth.

Created `tools/lineage_bridge.py` to normalize the observed network receipt into the current lineage schema without fetching, fabricating, mutating source truth, or promoting state.

The bridge copies observed `response_sha256` into `raw_artifact_sha256`, preserves the external observation timestamp, identifies the producer component, and marks the evidence as source observation rather than derived evidence.

Added `tests/test_lineage_bridge.py` and wired it into Foundation CI.

## Security / memory

The bridge is metadata-only and does not load historical datasets. It does not store credentials. The 320 MiB Render engineering guard remains unchanged.

## Verification

Code is wired into CI. Exact-current CI result for the latest commit remains unobserved through the available safe observation surface, therefore verification level is `WIRED_TO_CI / UNKNOWN_EXECUTION` until an actual run receipt is observed.

## State

```text
ACTION_SPACE = 0
PROMOTION = DENY
ROOM_02 = LOCKED
STAIRCASE = LOCKED
```

## Next

Continue with `BRAIN-N125`: observe exact-current CI execution and reconcile any real failure. No execution receipt may be manufactured from code inspection.
