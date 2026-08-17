# N003-PROOF — Execution Protocol and Cross-Domain Boundary

## Status

N003-PROOF is a **destruction/proof protocol**, not a business strategy and not a data-source-specific algorithm.

Core rule:

> TEST SPEC != EVIDENCE
> REPRODUCIBLE != CORRECT
> UNBREAKABLE != USEFUL

The protocol exists to attack a system systematically after BUILD/HARDEN and before promotion.

## Required execution layers

### Layer 1 — Identity / Baseline

Run fresh/replay identity checks and multi-run identity (>=10 runs where practical).

Expected:

`FRESH1 = REPLAY1 = REPLAY2 = FRESH2`

Non-determinism without an explicitly documented acceptable cause => DENY.

### Layer 2 — Mutation Matrix

Input mutations:

- reorder keys => same semantic result
- add null field => DENY when schema forbids it
- change one value => output/evidence must change or the mutation must be explicitly proven irrelevant
- truncate input => DENY

Feature mutations:

- remove feature
- reorder structure
- change type

Expected: evidence/trace changes or explicit DENY.

Trace mutations:

- drop step
- reorder steps

Expected: trace hash mismatch => DENY.

Dependency mutations:

- Python patch/minor version
- numerical dependency changes

Expected: execution signature changes or explicit cross-environment comparability contract.

### Layer 3 — Adversarial Break Tests

1. TRACE COLLISION TEST
   - different semantic paths producing same output must retain different trace identities.
   - trace collision => FAIL.

2. HASH-PRESERVING ATTACK
   - ignored fields, nested reordering, equivalent encodings.
   - must produce a semantic-equivalence proof, hash change, or explicit DENY.
   - same hash + different semantic meaning => FAIL.

3. FAKE EMPTY ATTACK
   - forced empty filter
   - missing data
   - bypassed logic
   - empty results require distinct, auditable reasons.

4. INPUT SENSITIVITY TEST
   - one-value change
   - small perturbation
   - materially different input
   - output may remain stable only when stability is explainable and evidenced.

5. PARTIAL CORRUPTION TEST
   - flip one byte in input, feature, or trace.
   - expected: hash mismatch => DENY.

6. CROSS-ENVIRONMENT REPLAY
   - Windows/Linux or Python variants.
   - expected: identical output only with identical execution contract; otherwise signature mismatch => NOT_COMPARABLE.
   - different output + same signature => FAIL.

7. FILESYSTEM BRANCH ATTACK
   - environment-dependent branch injection.
   - expected: execution/trace identity detects branch change.

8. DEAD PIPELINE TEST
   - random, repeated, and edge-case inputs.
   - constant output distribution without an explicit reason => FAIL.

9. ANTI-HARDCODE TEST
   - inject controlled input noise and semantic-preserving reorderings.
   - verify the pipeline actually consumes the mutated input.

## Interpretation rule

Passing tests never automatically establishes correctness. N003-PROOF establishes that the system survived the defined attacks under the defined evidence contract.

A proof protocol is therefore **orthogonal to domain logic**.

## Cross-domain applicability

The same N003-PROOF protocol can govern multiple downstream engines without turning Brain into those engines.

### Lottery / XSMB engine

Possible domain-specific evidence:

- source identity
- source timestamp
- full27 source truth
- tail27 derivation lineage
- scraper/path identity
- transformation hashes
- result provenance

N003 tests the integrity of the pipeline; it does **not** claim lottery outcomes are predictable or profitable.

### Securities / Quant engine

The same protocol applies to:

- EOD source provenance
- market calendar correctness
- feature lineage
- no-lookahead enforcement
- model/version identity
- backtest replay identity
- order/signal trace
- risk-engine mutation tests
- portfolio-state mutation tests
- execution-feasibility evidence

Domain-specific quant correctness remains a separate gate. N003 cannot turn a reproducible backtest into a profitable strategy.

### Other possible domains

The proof layer can also govern:

- ETL/data pipelines
- fraud/risk scoring
- anomaly detection
- forecasting
- document processing
- compliance/audit pipelines
- research reproducibility

## Architectural boundary

```text
BRAIN / FORENSIC CONTROL PLANE
        |
        +--> N003-PROOF (domain-agnostic attack/proof protocol)
        |
        +--> domain engine A (lottery)
        |
        +--> domain engine B (securities)
        |
        +--> future domain engines
```

N003 is a **gate and verifier**, not an alpha generator.

It must never silently inherit domain assumptions from XSMB merely because XSMB was the first application.

## Promotion rule

`N003_PASS` means only that the defined proof campaign passed.

It does not mean:

- profitable
- statistically valid for every domain
- economically useful
- predictive
- production-safe without domain-specific gates

Every downstream engine retains its own domain admission contract.
