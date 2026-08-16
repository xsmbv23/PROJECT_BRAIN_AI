# EXECUTION ROUTING AND OOM GUARD V1

## Purpose

Prevent the Render Free 512 MB / 1 CPU services from becoming execution hosts for unbounded workloads.

This is a pre-execution governance rule. The system must classify a task before opening/loading its data.

## Runtime boundaries

```text
                     USER / BOT
                         |
                         v
                +------------------+
                | PROJECT_BRAIN_AI |
                | 512MB SAFE ZONE  |
                +---------+--------+
                          |
              +-----------+-----------+
              |                       |
              v                       v
        BOUNDED EXECUTION       EXTERNAL EXECUTION
        <= declared budget      build/worker/local
              |                       |
              +-----------+-----------+
                          v
                    COMPACT EVIDENCE
                          |
                          v
                     BRAIN INDEX
```

## Preflight decision

Every job gets a `WORKLOAD_CLASS_V1` envelope before data access:

- `P0`: metadata/state/evidence/index/health only.
- `P1`: bounded fixture or bounded shard operation with explicit row/date/byte limits.
- `P2`: historical, bulk, workbook-scale, batch Quant, training, optimization, or unknown footprint.

`P2` MUST NOT execute in Brain/UI.

Unknown footprint is treated as `P2`.

## Required preflight fields

```text
job_id
input_artifact_id
input_sha256
estimated_input_bytes
estimated_rows
estimated_history_days
estimated_peak_memory_bytes
estimated_cpu_cost
output_mode
resume_token
workload_class
execution_boundary
```

## Safety budget

The 512 MB limit is not treated as a target.

Brain/UI should retain a large safety margin and reject jobs whose estimated peak memory is not demonstrably bounded. No code may use the theoretical remaining RAM as an execution budget.

## Forbidden patterns on Brain/UI

- full historical pandas DataFrame;
- reading all Excel workbooks into one process;
- concatenating all daily shards;
- loading raw source and all derived projections simultaneously;
- unbounded JSON responses;
- batch Quant across the full history;
- model training/optimization;
- retry loops that repeat memory growth;
- in-process multiprocessing that multiplies memory;
- caching large source payloads in process memory.

## Allowed patterns

- SQL projection with explicit `LIMIT` and date range;
- streaming/chunked reads;
- one shard at a time;
- one bounded fixture at a time;
- compact hashes and metadata;
- artifact-by-ID access;
- restartable stages;
- evidence envelopes that reference artifacts rather than copying them.

## OOM / crash protocol

If a worker exits unexpectedly:

```text
WORKER_FAILED
    |
    +--> source artifact remains immutable
    +--> manifest remains unchanged
    +--> evidence = PENDING/FAIL
    +--> promotion = DENY
    +--> next_action = RESUME_FROM_ARTIFACT_ID
```

A restart never authorizes historical rewriting.

## Scaling rule

If a workload grows beyond the current boundary, do not increase in-process complexity first.

First consider:

1. split by day;
2. split by shard;
3. split by stage;
4. move execution to external worker/build plane;
5. return compact evidence.

Only then consider a higher resource plan.

## Fosennic invariant

Performance decisions are subordinate to forensic integrity.

```text
OOM protection != data deletion
OOM protection != provenance loss
OOM protection != silent rewrite
OOM protection != promotion bypass
```
