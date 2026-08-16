# EVIDENCE PROTOCOL V1

Brain consumes evidence references, not the complete data lake.

## Evidence envelope

Required fields:

- project_id
- artifact_id
- source_ids
- canonical_sha256
- shard_sha256
- manifest/root hash where available
- calendar_state
- verification_state
- promotion_state
- lineage
- builder_version
- state_version
- evidence_schema_version

## State machine

```text
PLANNED
  ↓
IMPLEMENTED
  ↓
STATIC_VERIFIED
  ↓
RUNTIME_VERIFIED
  ↓
EVIDENCE_BOUND
  ↓
PROMOTED
```

Any failed gate produces `DENIED` and never skips forward.

## Promotion rule

The evidence consumer cannot infer promotion merely because hashes match.

Hash match proves integrity, not correctness.

Promotion requires independent governance and verification gates.

Foundation defaults to:

```text
promotion = DENY
```

## Sharded data rule

Canonical XSMB data is represented as immutable day shards. TAIL_27 is a derived view and cannot replace FULL_27.

## Fast UI rule

The UI consumes `AUDIT_PROJECTION_V1`, which is a compact derived read model. It never recomputes full forensic history.
