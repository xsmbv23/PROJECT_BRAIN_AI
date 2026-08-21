# E2E EVIDENCE ACQUISITION V1

## Purpose

Do not make progress depend on whether a particular website can be scraped automatically.
Acquisition is an interchangeable transport layer. Forensic admission is invariant.

## Three lawful acquisition channels

```text
                    SOURCE / EVIDENCE
                           |
            +--------------+--------------+
            |              |              |
            v              v              v
 AUTOMATED_EXPLICIT   MANUAL_AUTHORIZED   DURABLE_ARCHIVE_EXPORT
            |              |              |
            +--------------+--------------+
                           |
                           v
                  EVIDENCE_INTAKE_ROUTER
                           |
                           v
                COMMON FORENSIC CONTRACT
                           |
        +------------------+------------------+
        |                  |                  |
    provenance         raw identity       completeness
        |                  |                  |
        |              SHA-256/raw bytes     coverage=1.0
        |                  |                  |
        +------------------+------------------+
                           |
                     conflicts=0
                     synthetic=false
                           |
                           v
                    S1 ADMISSION GATE
                           |
                     PASS / DENY
                           |
                           v
                    S2 RESEARCH
                           |
                           v
                    S3 BACKTEST
                           |
                           v
                    S4 EDGE
                           |
                           v
                 S5 EV / P&L / ROI
                           |
                           v
              S6 ROBUSTNESS / RISK / DRIFT
                           |
                           v
                    S7 CONTROLLED ACTION
```

## Critical invariant

The transport channel is NOT evidence quality.

```text
AUTOMATED_EXPLICIT != more trusted
MANUAL_AUTHORIZED  != less trusted
ARCHIVE_EXPORT     != automatically trusted
```

All three must satisfy the same immutable admission contract.

## Website strategy

A source that blocks automated collection, requires a challenge, or has uncertain ownership does not become a reason to weaken the contract.
Instead:

1. preserve the source as a candidate;
2. do not fabricate or silently substitute data;
3. use a lawful authorized capture path when available;
4. archive the exact raw artifact;
5. attach provenance and acquisition timestamp;
6. hash the exact raw bytes;
7. submit the artifact through the same S1 gate.

## E2E stop conditions

The pipeline stops at the first failed gate.
No downstream layer may infer success from an upstream transport event.

```text
S1 DENY -> S2..S7 UNREACHED
S1 PASS -> S2 may execute
S2 DENY -> S3..S7 UNREACHED
...
S6 DENY -> S7 UNREACHED
```

## Memory invariant

The Brain runtime must remain dataset-free. Acquisition artifacts are chunked and hashed outside the Brain governance runtime. Only compact evidence envelopes cross the Brain boundary.

The Render Free 512 MB ceiling remains a hard constraint; the existing 320 MiB guard is not relaxed.

## Successor instruction

A future Bot must treat this document and `tools/evidence_intake_router.py` as one design unit. Never create a second admission contract for a new source channel. Extend the transport layer, then feed the same S1 contract.
