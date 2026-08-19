# Source Quorum & Reconciliation V1

## Purpose

Protect canonical source truth when one source is incomplete, stale, unavailable, or only exposes a derived tail vector.

## Rules

1. Every source is an independent identity.
2. Every target date is independently proven.
3. Every FULL_27 vector requires raw-source provenance and a source hash.
4. `TAIL_27` is derived evidence only and can never become canonical source truth.
5. A source's general ability to expose FULL_27 does not prove FULL_27 for the target date.
6. Data from Source B must never be relabeled as Source A.
7. At least two independent exact-date FULL_27 vectors are required for canonical quorum.
8. Semantic equality is necessary but not sufficient; provenance and target-date identity must also pass.
9. Conflict means STOP and investigate; never average, merge, or choose silently.
10. Missing/unknown evidence means DENY.

## Reconciliation states

```text
RECONCILIATION_NOT_REQUIRED
        |
        v
RECONCILE_REQUIRED
        |
        +--> TARGET_DATE_UNPROVEN --> DENY
        |
        +--> SOURCE_COUNT_LT_2 --> DENY
        |
        +--> TWO_FULL27_AVAILABLE
                  |
                  v
             SEMANTIC_COMPARE
                  |
          +-------+-------+
          |               |
        MATCH           CONFLICT
          |               |
          v               v
     CANONICAL_PASS      DENY
```

## `RECONCILE_REQUIRED` exact meaning

For the current foundation it means:

> Reconcile the exact-current runtime version/protocol evidence with the persisted Brain state, and reconcile source vectors only when the exact target-date FULL_27 evidence is available.

It does **not** mean “the code is broken”.
It does **not** mean “rerun everything”.
It does **not** mean “trust the newest source”.

The reconciliation target must be named in every action receipt.

## Current target

Target date: `2026-08-12`.

Current known source state:

```text
Source-A ketqua16.net = FULL_27 target-date NOT_PROVEN
Source-B XSMB         = implemented, exact runtime observation pending
Quorum required       = 2
Canonical              = DENY until quorum
```

## Anti-shortcut doctrine

```text
SOURCE_A_CAPABLE
    != SOURCE_A_TARGET_DATE_PROVEN

SOURCE_B_TARGET_DATE_PROVEN
    != SOURCE_A_TARGET_DATE_PROVEN

TAIL_27_AVAILABLE
    != FULL_27_AVAILABLE

SEMANTIC_MATCH
    != CANONICAL_PASS
```

Canonical PASS requires all required evidence at the same gate.
