# Forensic Admission Chain — Canonical Doctrine

## Status

This document is part of the permanent successor handoff. It defines one Forensic state machine, not multiple independent forensic systems.

## Core rule

A PASS at one gate is **only a prerequisite** for the next gate. PASS is never inherited.

```text
DB_EXISTENCE
    -> DB_BINDING
        -> DB_TLS_ADMISSION
            -> DB_ROUND_TRIP
                -> PROMOTION
```

Each gate proves a different fact:

- `DB_EXISTENCE`: the database resource exists.
- `DB_BINDING`: the service has the required runtime binding.
- `DB_TLS_ADMISSION`: the binding is an accepted PostgreSQL/TLS binding.
- `DB_ROUND_TRIP`: a real compact metadata envelope was written, read back, and matched by SHA-256.
- `PROMOTION`: only the completed admission chain can authorize durable-evidence promotion.

## Forbidden inference

```text
DATABASE EXISTS = PASS
```
never implies:

```text
DATABASE ACCESS = PASS
```

Likewise:

```text
BOUND_TLS = PASS
```
never implies:

```text
ROUND_TRIP = PASS
```

And:

```text
TEST_PASS = PASS
```
never implies:

```text
REAL_EVIDENCE = PROVEN
```

## State semantics

`UNKNOWN` is not `PASS`.

`NOT_PROVEN` is not `PASS`.

`DENY` is sticky until the corresponding gate produces fresh evidence.

A later gate cannot repair or reinterpret an earlier missing proof.

## Security analogy

The system is modeled as:

```text
correct corridor key
    + correct room key
    + inner release for protected rooms
    + successful admission evidence
```

Possessing evidence that a room exists is not possessing its key.

## N003-PROOF doctrine

The same admission semantics apply to Quant Engine proof:

```text
TEST SPEC != EVIDENCE
REPRODUCIBLE != CORRECTNESS PROOF
SAME RESULT != SAME EXECUTION PATH
ALL TESTS PASS != REAL-WORLD PROOF
```

N003-PROOF must therefore attack the execution path, not merely the final output.

## Required proof families

1. Multi-run identity: at least 10 exact executions where applicable.
2. Mutation matrix: key reorder, null/additional fields, value change, truncation, feature mutation, trace mutation, dependency mutation.
3. Trace collision: different semantic paths producing the same output must have different trace hashes.
4. Hash-preserving attack: semantic change must change the canonical evidence or be explicitly denied.
5. Fake-empty attack: different empty causes must remain distinguishable.
6. Input sensitivity: meaningful input perturbation must produce a changed result or an explicit, explainable invariant stability.
7. Partial corruption: one-byte corruption must be detected and denied.
8. Cross-environment replay: identical or explicitly non-comparable execution signatures.
9. Filesystem branch attack: uncontrolled filesystem state must not silently change the semantic path.
10. Dead-pipeline test: non-constant meaningful inputs must not collapse to an unexplained constant output.
11. Anti-hardcode test: the system must demonstrate that canonical input actually participates in the evidence/output chain.

## Promotion rule

The system may be useful before promotion. It may not be promoted merely because it is consistently wrong or consistently executable.

```text
BUILD -> HARDEN -> BREAK -> PROVE
```

Only proof unlocks the next room.
