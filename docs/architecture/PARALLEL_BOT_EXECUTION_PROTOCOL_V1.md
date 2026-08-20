# Parallel Bot Execution Protocol V1

## Purpose

Allow independent AI bots to work concurrently without allowing one bot to silently alter the Forensic authority chain, promotion state, or immutable history.

## Authority order

```text
BRAIN / Project_Brain_AI
        = governance + persistent state + promotion authority

QUANT / Quant_Engine
        = Layer 1 execution/research plane

CHAT
        = communication interface only
```

## Parallelism rule

Bots MAY execute in parallel only when their work is explicitly classified as a **local prerequisite** or an isolated repository task.

Parallel work MUST NOT:

- promote Brain state;
- unlock a higher room/layer;
- reinterpret an UNKNOWN as PASS;
- rewrite immutable forensic history;
- fabricate external-runtime evidence;
- treat GitHub workflow self-attestation as external runtime truth;
- overwrite another bot's action receipt/state without a reconciliation step.

## Current frozen boundary

Brain's exact-current state may remain:

```text
ACTION_SPACE = 0
PROMOTION = DENY
LAYER_1 = LOCKED
STAIRCASE = LOCKED
```

while Quant Engine performs explicitly permitted local prerequisite work such as workflow verifier execution and bounded tests.

Quant evidence remains scoped to Quant repository execution. It cannot satisfy Brain's external-runtime observation gate unless Brain independently observes and records the required evidence.

## Handoff protocol

Every parallel task must leave:

1. action id;
2. repository and commit;
3. exact scope;
4. evidence type;
5. evidence freshness;
6. PASS/FAIL/UNKNOWN status;
7. limitations;
8. next action;
9. explicit statement of what the evidence is NOT allowed to prove.

## Forensic gate semantics

```text
PASS_IS_LOCAL
PASS_IS_PREREQUISITE_ONLY
NO_PASS_INHERITANCE
UNKNOWN_IS_NOT_PASS
DEFAULT_DENY
OWN_GATE_EVIDENCE_REQUIRED
FRESH_EVIDENCE_REQUIRED_FOR_PROMOTION
```

## Collision handling

If two bots modify the same state file or architectural authority file, the later bot MUST NOT blindly overwrite. It must reconcile against the latest canonical state, preserve both action histories, and advance the successor pointer only after the merged state is internally consistent.

## Objective

Parallelism increases throughput. It never increases authority.
