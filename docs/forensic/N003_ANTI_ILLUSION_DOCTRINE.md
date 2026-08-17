# N003 Anti-Illusion Doctrine — Brain Authority

This document is part of the persistent Forensic handoff and is binding guidance for successor Bots.

## Core distinction

```text
FORENSIC INTEGRITY
        !=
CAUSAL RESPONSIVENESS
        !=
MODEL CORRECTNESS
```

A pipeline may be deterministic, replayable, hash-consistent and forensically intact while still being consistently wrong. This failure class is named `CONSISTENTLY_WRONG_PIPELINE`.

Therefore a green forensic replay receipt is never permission to claim model correctness.

## N003 proof requirements

1. Multi-run identity: fresh/replay executions agree on all required evidence domains.
2. Input sensitivity: meaningful semantic input changes must change evidence/output/trace or be explicitly denied.
3. Feature information: accepted meaningful variation must not silently collapse into a fabricated constant feature vector.
4. Causal dependency: canonical input must demonstrably participate in the feature/evidence/output chain.
5. Anti-hardcode: materially different accepted inputs must not be mapped to a fixed output by hidden hardcoding.
6. Execution graph: semantic trace must not be treated as a substitute for proving branch/path identity; future evidence should include a compact execution-graph fingerprint.
7. Adversarial mutation: corrupted input, feature evidence, trace and hash-domain attacks must fail closed.

## Gate semantics

```text
PROOF_FAIL -> FINDING -> FIX -> RE-RUN
PROOF_PASS -> EVIDENCE RECORDED
```

Even complete N003 proof does not establish economic, statistical, or predictive correctness.

## Architectural lock

N004 and higher semantic layers remain locked until the N003 completion gate is satisfied on the actual replay path and the compact forensic receipt is persisted.

Successor Bots must not convert documentation, local unit-test success, or reproducibility into a correctness claim.
