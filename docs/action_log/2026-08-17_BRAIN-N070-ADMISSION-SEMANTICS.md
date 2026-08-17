# BRAIN-N070 — Admission Semantics Preservation

## Canonical rule

The system has ONE forensic state, not multiple unrelated forensic states.
Database admission is a sequential gate chain inside that state.

A gate PASS is non-inheritable. It proves only that gate and unlocks evaluation
of the next gate. It never proves a deeper gate.

## Example

```text
DB_EXISTENCE=PASS
DB_BINDING=NOT_BOUND
DB_TLS_ADMISSION=UNREACHED
DB_ROUND_TRIP=UNREACHED
PROMOTION=DENY
```

This is the correct state and must not be collapsed into a generic
`DATABASE_PASS`.

## Why this is mandatory

Without this distinction a successor could observe that a database exists and
incorrectly infer service authorization. Or observe `BOUND_TLS` and incorrectly
infer durable forensic persistence. Both are invalid forensic shortcuts.

## Permanent successor constraints

- UNKNOWN_IS_NOT_PASS
- DEFAULT_DENY
- PASS_AT_GATE_IS_PREREQUISITE_ONLY
- LATER_GATES_ARE_UNREACHED_AFTER_FIRST_FAILURE
- FAIL_HISTORY_IS_IMMUTABLE
- LOCAL_PASS != RENDER_PASS
- RUNTIME_ANCHOR_COMMIT_REQUIRED
- CREDENTIALS ARE NEVER EVIDENCE

See `docs/architecture/FORENSIC_DATABASE_ADMISSION_CHAIN_V1.md` for the
canonical flow and promotion conditions.
