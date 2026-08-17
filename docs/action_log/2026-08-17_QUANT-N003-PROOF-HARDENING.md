# QUANT-N003-PROOF-HARDENING — Successor Execution Protocol

## Why this exists

A successor Bot must not treat a test specification as proof. N003-PROOF is a controlled break-and-prove protocol for Layer 1 Room 01.

## Critical failure class

A system can be perfectly reproducible and still be useless:

```text
CONSISTENTLY_WRONG_PIPELINE
```

Therefore:

```text
FORENSIC INTEGRITY != CAUSAL RESPONSIVENESS != MODEL CORRECTNESS
```

A green replay/hash receipt never licenses a correctness claim.

## Mandatory doctrine

```text
BUILD -> HARDEN -> BREAK -> PROVE
```

The objective is not to make the test suite green. The objective is to discover whether the system can be cheated, whether evidence is causally tied to the actual execution path, and whether exact replay is truly identical.

## Proof layers

### Layer 1 — Identity baseline

Run the real bounded source scenario repeatedly. Target at least 10 executions when the runtime permits.

Required identity relation:

```text
FRESH_1 = REPLAY_1 = REPLAY_2 = FRESH_2
```

Identity means complete canonical evidence, not merely final candidates.

### Layer 2 — Mutation matrix

Run real mutations:

- reorder keys -> expected same canonical semantic evidence when order is non-semantic
- add null/unknown field -> expected explicit deny or defined canonical behavior
- change one semantic value -> expected evidence/output change
- truncate input -> expected deny
- remove/change/retype a feature -> expected hash/trace/output change or explicit deny
- drop/reorder a trace step -> expected trace mismatch/deny
- change dependency/runtime signature -> expected signature mismatch or explicit non-comparability

### Layer 3 — Adversarial break tests

1. Trace collision: different semantic paths must not share the same semantic trace hash.
2. Hash-preserving attack: semantic changes cannot hide behind canonicalization.
3. Fake-empty attack: distinct empty causes must remain distinguishable.
4. Input sensitivity: meaningful perturbations must not disappear silently.
5. Partial corruption: one-byte corruption must be detected.
6. Cross-environment replay: output differences require execution-signature explanation.
7. Filesystem branch attack: uncontrolled external state must not alter the path invisibly.
8. Dead pipeline: meaningful inputs must not collapse to unexplained constants.
9. Anti-hardcode: prove the input is causally consumed.
10. Feature information: accepted meaningful variation must not collapse into a fabricated constant feature vector; use variance/unique semantic states as evidence, not as a claim of statistical quality.
11. Execution graph: semantic trace hash is not assumed to fully represent topology; future evidence should include ordered semantic operations, branch decisions, feature usage map and dependency identities.

## Failure semantics

Any unexpected mutation result is a finding, not a reason to loosen the invariant.

```text
TEST FAIL -> FINDING -> FIX SYSTEM -> RE-RUN PROOF
TEST PASS -> EVIDENCE RECORDED
ALL PROOF PASS -> REPRODUCIBILITY/EXECUTION INTEGRITY PROVEN
```

Even after all proof passes:

```text
REPRODUCIBLE != CORRECT
```

Correctness remains a separate empirical/model-validation question.

## State handoff

- Brain remains Governance Control Plane.
- Chat remains communication interface only.
- Data owns source truth.
- Quant Engine owns calculation.
- Sensors are observation-only.
- No implicit graph edges.
- No hidden state.
- No global cache.
- Layer 1 remains isolated.
- N004 remains locked until N003-PROOF completion gate is met.
