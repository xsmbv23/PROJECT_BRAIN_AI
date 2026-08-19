# BRAIN-N098 — Pre-Execution Gate Result

## Decision

`CANONICAL_QUORUM = DENY`

This is a **pre-execution DENY**, not a source-result FAIL.

## Immutable-state conflict

The current persistent state declares the N098 source identities as:

- SOURCE_A = `Minh Ngoc`
- SOURCE_B = `Xo so Phonix`

The proposed execution plan declares:

- SOURCE_A = `ketqua16.net`
- SOURCE_B = `xsmb.com.vn`

N098 explicitly requires the predeclared sources to remain unchanged during execution. Therefore the runtime cannot silently replace the persisted source registry with the proposed pair. Doing so would mutate the identity of the execution after the execution was already registered in persistent state.

## Exact-current external observation

`ketqua16.net` currently exposes a redirect notice directing visitors to `goketqua.net`. This is a direct anti-ad/source-boundary signal: a redirect target is not automatically the same source identity. The source capture contract therefore requires the requested URL, redirect chain, final URL, and final-host identity to be preserved before any semantic result is admitted.

`xsmb.com.vn` has indexed result pages, but the currently observable indexed page used in this check does not expose a direct artifact for target date `2026-08-12`. No alternate source was substituted because N098 forbids fallback substitution during an execution.

## Forensic semantics

The following distinctions are now canonical:

```text
DB_EXISTENCE PASS
    != DB_BINDING PASS
    != DB_TLS_ADMISSION PASS
    != DB_ROUND_TRIP PASS
    != PROMOTION PASS
```

Likewise:

```text
HTTP 200
    != SOURCE VALID
    != TARGET_DATE PROVEN
    != RESULT_BOUNDARY PROVEN
    != SOURCE INDEPENDENCE PROVEN
    != CANONICAL_QUORUM PASS
```

`UNKNOWN` remains distinct from `FAIL`.
Both deny promotion, but they retain different forensic causes.

## No execution was started

No raw artifact was claimed for N098.
No source was swapped.
No target date was changed.
No canonical hash was fabricated.
No state was changed to make the gate appear green.

## Required successor action

`BRAIN-N099` must reconcile the persistent source registry and the requested N098 plan **before any capture starts**. The reconciliation must itself be an explicit state transition with provenance. After reconciliation, a fresh execution ID must be created; the original N098 predeclared identity must not be mutated retroactively.

## Promotion

```text
N098 = CLOSED_WITH_DENY_PREEXEC
CANONICAL_QUORUM = DENY
LAYER_1 = LOCKED
STAIRCASE = LOCKED
```
