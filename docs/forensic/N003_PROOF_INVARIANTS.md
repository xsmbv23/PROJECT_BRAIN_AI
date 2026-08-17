# N003-PROOF — Forensic Reproducibility Doctrine

## Status

`N003 = READY_FOR_PROOF`

`N004 = LOCKED`

`LAYER_2 = NOT_ALLOWED`

This document is a successor-authoritative contract. A later Bot AI must read it before changing replay, receipt, hashing, serialization, or promotion logic.

## Core principle

```text
SAME RESULT != SAME EXECUTION PATH
```

A reproducible output hash alone is insufficient. A pipeline can produce the same output through different branches and still have semantic execution drift.

## Required invariants

### 1. Deterministic execution

For a fixed canonical input, fixed code/dependency environment, and fixed permitted runtime context, execution must be deterministic.

### 2. Deterministic serialization

Equivalent semantic objects must use one canonical serialization form before hashing.

### 3. Typed hash domains

Hashes must identify what they hash. Input, output, feature snapshot, execution signature, trace, and receipt hashes must not be ambiguous or interchangeable.

### 4. Pure replay environment

Replay must not depend on uncontrolled network, mutable environment variables, random state, wall-clock state, or hidden external services.

### 5. Execution signature

The receipt must bind the exact executable/dependency identity used for the run.

### 6. Execution trace consistency

The receipt must include a compact `execution_trace_hash` representing semantic execution path, including at minimum:

- ordered function/module calls relevant to the result
- branch decisions relevant to the result
- security/corridor/room admission steps relevant to the result

Do not store full debug traces as the canonical receipt. Store a canonical semantic trace representation and its hash.

```text
SAME OUTPUT
    +
DIFFERENT SEMANTIC TRACE
    =
DRIFT / DENY
```

### 7. Canonical feature structure

One feature must have exactly one canonical semantic structure.

```text
ONE FEATURE -> ONE CANONICAL STRUCTURE
```

Do not permit equivalent-but-differently-shaped structures to silently represent the same canonical feature.

Debug representation is not the semantic snapshot.

### 8. Output causality / anti-cheat

Output must be a function of the canonical input and declared execution context, not a hardcoded constant or bypass path.

At minimum, proof must include mutation/property scenarios showing that controlled input changes can affect the output when the underlying semantics require it, and that bypassed/hardcoded paths are detectable.

## VALID_EMPTY protection

`VALID_EMPTY` is a valid state, not an error.

But an empty result must carry a canonical reason:

```text
NO_SIGNAL
FILTERED_OUT
INSUFFICIENT_DATA
```

Two runs producing `[]` for different semantic reasons must not collapse to the same unexplained receipt state.

## Filesystem invariant

Canonical logic must not branch on uncontrolled filesystem state.

Forbidden pattern:

```text
if os.path.exists("cache.flag"):
    branch_A()
else:
    branch_B()
```

unless that filesystem artifact is explicitly declared as immutable canonical input and its raw bytes are included in the input identity.

## Byte-exact input identity

Canonical input identity is based on **raw bytes**, before parsing.

The hash boundary must distinguish:

- `LF` vs `CRLF`
- BOM vs no BOM
- encoding differences
- byte-order differences
- exact file contents

```text
RAW_BYTES -> INPUT_HASH -> PARSE
```

not:

```text
PARSED_OBJECT -> INPUT_HASH
```

## Dependency resolution lock

`dependency_hash` is insufficient unless it represents the complete resolved runtime dependency set.

The proof environment must capture a full resolved dependency snapshot, equivalent in authority to a complete `pip freeze`/lockfile resolution, including transitive dependencies and versions.

```text
RESOLVED_DEPENDENCY_TREE
        -> DEPENDENCY_HASH
```

## Anti-cheat doctrine

A system that can hardcode the expected output and still pass its own replay test is not forensically proven.

Proof must attempt to break the implementation.

Required attack classes include:

1. output hardcoding
2. branch bypass
3. function substitution
4. input mutation
5. feature-shape mutation
6. filesystem-state mutation
7. dependency-version mutation
8. serialization mutation
9. trace mutation
10. empty-result reason mutation

## Multi-scenario proof

Do not certify reproducibility from one fixture.

Run multiple **real** scenarios covering at least:

- different dates
- different missing-data patterns
- different data density
- valid non-empty outputs
- valid empty outputs
- filtered outputs
- insufficient-data outputs

For each scenario:

```text
FRESH_1
   =
REPLAY_1
   =
REPLAY_2
   =
FRESH_2
```

and additionally:

```text
execution_trace_hash(FRESH) == execution_trace_hash(REPLAY)
```

where semantic path equivalence is expected.

## Promotion rule

```text
FORENSIC PASS != PREDICTIVE EDGE
```

A perfectly reproducible system can still be useless as a predictive system.

Forensic certification proves reproducibility/integrity. It does **not** prove statistical edge, profitability, predictive power, or trading validity.

Therefore:

```text
FORENSIC_REPRODUCIBILITY = PROVEN
```

must never be rewritten as:

```text
PREDICTIVE_EDGE = PROVEN
```

## Final gate

Until the multi-scenario replay and anti-cheat proof succeeds:

```text
N003 = READY_FOR_PROOF
N004 = LOCKED
LAYER_2 = NOT_ALLOWED
PROMOTION = DENY
```
