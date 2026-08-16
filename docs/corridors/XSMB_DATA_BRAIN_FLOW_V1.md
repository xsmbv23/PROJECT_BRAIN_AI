# XSMB DATA ↔ BRAIN — FORENSIC FLOW V1

```text
                         START
                           │
                           ▼
                    source artifact
                           │
                           ▼
                 preserve raw bytes
                           │
                           ▼
                    hash source
                           │
                 ┌─────────┴─────────┐
                 │                   │
              hash OK             hash FAIL
                 │                   │
                 ▼                   ▼
            parse/validate          DENY
                 │
                 ▼
             FULL_27 valid?
              /        \
            NO          YES
            │             │
            ▼             ▼
          DENY        provenance
                          │
                          ▼
                  quorum >= 2?
                    /       \
                  NO         YES
                  │            │
                  ▼            ▼
            CONFLICT LEDGER  canonicalize
                               │
                               ▼
                        derive TAIL_27
                               │
                               ▼
                     day shard + manifest
                               │
                               ▼
                       compact evidence
                               │
                               ▼
                      corridor security
                               │
                ┌──────────────┼───────────────┐
                │              │               │
             unknown        mismatch        valid
             corridor       /layer/cap       │
                │              │              ▼
                ▼              ▼        verify lineage
              DENY            DENY            │
                                             ▼
                                        verify hashes
                                             │
                                             ▼
                                      append evidence
                                             │
                                             ▼
                                     PROMOTION = DENY
                                             │
                                             ▼
                                            END
```

## Branch invariant

Every failure branch terminates in DENY or CONFLICT LEDGER. No failure branch is allowed to fall through into canonical acceptance.

## Room model

```text
RAW ROOM
  ↓ corridor
VALIDATION ROOM
  ↓ corridor
CANONICAL ROOM
  ↓ corridor
EVIDENCE ROOM
  ↓ corridor
BRAIN GOVERNANCE ROOM
```

Each transition requires explicit identity, layer, corridor, capability, freshness/nonce, lineage and payload integrity.

## L1 boundary

There is no arrow from this flow directly to L1.

```text
DATA → BRAIN → EVIDENCE → GOVERNANCE
                              │
                              ▼
                       STAIRCASE GATE
                              │
                         🔒 LOCKED
                              │
                              ▼
                             L1
```
