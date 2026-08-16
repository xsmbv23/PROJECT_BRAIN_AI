# RENDER FREE 512MB / 1 CPU — OOM PROTECTION POLICY V1

## Non-negotiable constraint

The Render Free runtime has approximately 512 MB RAM and 1 CPU. OOM/reset is treated as an architectural failure, not as a performance inconvenience.

The system must route work by memory/CPU profile instead of allowing every task to execute inside one Render process.

## Workload classes

### P0 — lightweight / allowed on Brain/UI

- health checks;
- governance checks;
- state reads;
- next-action reads;
- compact evidence reads;
- hash verification of bounded payloads;
- small manifest/index reads;
- small UI projections.

### P1 — bounded / allowed only with explicit limits

- single-day fixture validation;
- bounded reconciliation;
- compact evidence generation;
- shard-level validation;
- small database queries with strict LIMIT/date bounds.

Rules: streaming/chunking, bounded rows, no full-history materialization, no unbounded pandas DataFrame, no giant JSON object.

### P2 — heavy / must leave the Brain/UI process

- multi-year historical crawling;
- Excel workbook parsing at scale;
- full historical reconciliation;
- bulk canonicalization;
- shard generation over thousands of days;
- large statistical calculations;
- Quant Engine batch calculations;
- model training/optimization;
- large exports.

These workloads must execute on a separate build/worker/local execution boundary and emit compact, content-addressed evidence back to Brain.

## Routing rule

```text
TASK
  ↓
CLASSIFY MEMORY / CPU / DATA VOLUME
  ↓
P0 ─────────→ Brain/UI
P1 ─────────→ bounded execution
P2 ─────────→ external worker/build plane
```

A task must be routed BEFORE loading its input data.

## Repository routing

```text
Project_Brain_AI
  = governance + memory + compact evidence

xsmb-quant
  = data/build/source-truth plane

Quant_Engine
  = Layer 1 intelligence rooms

future worker/build repo or execution boundary
  = heavy computation when required
```

Creating another repository is permitted when it prevents an unsafe workload from entering the 512 MB Brain/UI boundary. The repository itself is not the execution guarantee; an actual execution boundary must exist.

## Memory safety rules

1. Never load the full historical XSMB dataset into Brain.
2. Never concatenate all daily shards merely for display.
3. Never parse a large Excel history inside the lightweight UI request process.
4. Prefer streaming readers and chunked processing.
5. Prefer SQL aggregation/projection over Python-side materialization.
6. Use explicit row/date limits.
7. Keep evidence compact and content-addressed.
8. Do not duplicate raw payloads in evidence.
9. Do not retain large intermediate objects after a stage completes.
10. Heavy jobs must be independently restartable from immutable input IDs/hashes.

## Anti-OOM decision tree

```text
START
 │
 ├─ Is input > bounded fixture? ── YES → external execution
 │
 ├─ Is historical range multi-day? ─ YES → shard/worker
 │
 ├─ Does task require full workbook? ─ YES → build/data plane
 │
 ├─ Does task require batch Quant? ─ YES → Quant_Engine worker
 │
 ├─ Is output larger than compact evidence? ─ YES → artifact store + index
 │
 └─ Otherwise → Brain/UI bounded path
```

## Failure policy

If a task cannot prove that its memory footprint is bounded, it is **DENIED** on the Render Free Brain/UI service.

```text
OOM_RISK_UNKNOWN = DENY
UNBOUNDED_INPUT   = DENY
UNBOUNDED_OUTPUT  = DENY
```

## Fosennic requirement

OOM protection must never cause silent data loss or mutation.

If a worker dies:

```text
source truth remains intact
manifest remains intact
evidence remains DENY/PENDING
next_action remains resumable
```

A restart is not permission to rewrite history.
