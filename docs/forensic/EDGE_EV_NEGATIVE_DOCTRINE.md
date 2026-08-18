# Edge & EV<0 — Forensic Admission Doctrine

## Purpose

This document is a successor-safe rule for the Quant/Brain boundary. It does not calculate Edge or Expected Value. Calculation belongs to Quant Engine / Layer 1 when that layer is legitimately unlocked.

Brain only governs admission, evidence, and state transitions.

## Definitions

- `EDGE` = an explicitly produced, source-backed advantage estimate from the calculation layer.
- `EV` = an explicitly produced Expected Value estimate from the calculation layer.
- `EV < 0` = negative expected value; it is a **deny signal**, not a reason to alter the calculation until it becomes positive.
- `EDGE_UNKNOWN` = no fresh, admissible Edge evidence.
- `EV_UNKNOWN` = no fresh, admissible EV evidence.

## Immutable rules

1. Brain never manufactures Edge.
2. Brain never manufactures EV.
3. Brain never infers positive Edge from a successful test, successful scrape, successful deployment, or historical PASS.
4. `EDGE_UNKNOWN` is not `EDGE_PASS`.
5. `EV_UNKNOWN` is not `EV>=0`.
6. `EV < 0` is an explicit **DENY** for the governed action under evaluation.
7. A negative EV result must remain preserved as evidence; it must not be overwritten by a later PASS from another gate.
8. PASS is local to the gate that produced it. There is no PASS inheritance.
9. Every Edge/EV decision requires fresh evidence tied to an exact source/input/version/commit where applicable.
10. Brain may route an EV<0 result to a safe alternative branch (observe, reject, quarantine, request fresh evidence), but may not silently mutate the underlying calculation.

## Admission chain

```text
SOURCE TRUTH
    |
    v
CALCULATION LAYER
    |
    +--> EDGE_UNKNOWN --------> DENY / REQUEST_FRESH_EVIDENCE
    |
    +--> EDGE_PRESENT
    |       |
    |       v
    |    EV_UNKNOWN ---------> DENY / REQUEST_FRESH_EVIDENCE
    |       |
    |       v
    |    EV < 0 -------------> DENY / QUARANTINE
    |       |
    |       v
    |    EV >= 0 ------------> proceed to next independent gate
    |
    v
INDEPENDENT FORENSIC GATES
    |
    v
PROMOTION (only after every required gate has fresh evidence)
```

## Important distinction

`EV < 0` is not equivalent to `UNKNOWN`.

```text
EV_UNKNOWN = insufficient evidence
EV < 0     = sufficient evidence of negative expected value
```

Both deny the governed action, but their forensic meanings differ and must remain distinguishable in receipts.

## Receipt requirements

A future admissible Edge/EV receipt should contain only compact metadata:

- action id
- source id / source hash
- calculation version / commit
- observation timestamp
- Edge status
- EV status
- EV sign classification
- input envelope hash
- output envelope hash
- decision

Never store credentials or bulk source payloads in Brain receipts.

## Successor rule

If a future Bot sees `EV < 0`, it must not attempt to “fix” the result by changing thresholds, inventing data, selecting a different source, or weakening a gate. It must preserve the negative result and move to the explicitly documented safe branch.
