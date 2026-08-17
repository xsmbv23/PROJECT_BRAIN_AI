# N003 — Replay Truth / Forensic Invariants

This is an architecture-level invariant contract shared with `xsmbv23/Quant_Engine`.
It is not a room implementation detail.

## Mandatory invariants

1. **Typed hash domain** — `INT != FLOAT`, `INT != STRING`, `BOOL != INT`, `DECIMAL != INT`. Non-finite floats are forbidden. Scalar type identity must survive canonicalization.
2. **Deterministic list order** — list/tuple order is semantic and hashed. Unordered sets are forbidden in the canonical domain.
3. **Float discipline** — Layer 1 prefers integer/fixed-domain values. Any unavoidable float uses an explicit type tag and fixed precision; it must never silently collapse into another scalar type.
4. **Execution signature** — room version, code hash, Python version, implementation, OS, platform and architecture, plus dependency hash. No wall-clock values.
5. **Read-only input boundary** — replay reads one frozen byte snapshot and verifies file identity metadata around acquisition. Input mutation is DENY.
6. **Pure replay** — after acquisition, replay operates only on frozen input and explicit configuration. Network, subprocess, random, wall clock, environment lookups and hidden filesystem reads are forbidden.

## Equality target

```text
FRESH_1 == REPLAY_1 == REPLAY_2 == FRESH_2
```

## Non-negotiable semantic rule

```text
REPRODUCIBLE != CORRECT
```

A matching hash proves consistency with the declared execution path. It does not prove correctness.

The valid state below MUST remain representable:

```json
{"reproducibility":"PASS","correctness":"NOT_PROVEN"}
```

## Promotion

N003 PASS permits consideration of `QUANT-N004`.
N003 FAIL or UNKNOWN keeps `QUANT-N004` locked.

Any successor AI must read this document before modifying canonicalization, replay, receipts, or Layer 1 rooms. Changes require a new numbered forensic action.
