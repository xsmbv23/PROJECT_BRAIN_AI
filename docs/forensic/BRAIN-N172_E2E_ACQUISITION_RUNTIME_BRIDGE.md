# BRAIN-N172 — E2E lawful acquisition runtime bridge

## Decision

`S1 = BLOCKED` remains unchanged.

N171 changed the S1 acquisition protocol so canonical evidence may arrive through:

- `AUTOMATED_SOURCE_WITH_EXPLICIT_PERMISSION`
- `MANUAL_AUTHORIZED_CAPTURE`
- `DURABLE_ARCHIVE_EXPORT`

N172 closes the implementation gap between that contract and the Render evidence-acquisition runtime.

## Runtime defect discovered

The read-only source-independence Web Service built successfully but failed at boot because `tools/source_independence_server.py` imported `tools.source_independence_probe` while Render executed the file as a script, leaving the repository root absent from `sys.path`.

This was an execution-boundary defect, not source-independence evidence.

## Repair

`source_independence_server.py` now resolves the repository root from `__file__` and inserts that root into `sys.path` before importing the probe. The service remains observation-only and promotion-deny.

## E2E continuation

```text
lawful acquisition protocol
        |
        v
read-only Render runtime
        |
        v
fresh /probe receipt
        |
        +--> cross-owner evidence
        +--> source provenance
        +--> timestamp
        +--> comparison receipt
        |
        v
S1_CANONICAL_EVIDENCE_V2
        |
        v
S1 PASS only after full manifest verification
        |
        v
S2 VALID_RESEARCH
        |
        v
S3 VALID_BACKTEST
```

No Render deploy status, service liveness, or memory metric may substitute for the S1 manifest.

## Current evidence

- Exact-current Brain runtime remains verified for the last known successful runtime.
- Quant/Brain runtime foundation evidence remains `PASS` where explicitly observed.
- `S1_CANONICAL_EVIDENCE_V2` now enforces acquisition channel, reference, timestamp, and channel-specific provenance evidence.
- Render source-independence probe had a concrete import-path boot failure; repair is committed and awaiting fresh runtime observation.
- No canonical dataset artifact has been admitted.

## Next exit criteria

1. Source-independence probe runtime is live on the repaired commit.
2. Fresh probe receipt is independently observable.
3. If independence is proven, lawful permission/provenance is also proven.
4. If independence is not proven, retain `DENY` and use manual/authorized or durable-archive acquisition.
5. Only a complete S1 V2 manifest can unlock S2.
