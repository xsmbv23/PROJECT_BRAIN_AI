# XSMB DATA → BRAIN EVIDENCE CORRIDOR V1

## Authority

Canonical data authority remains `xsmbv23/xsmb-quant`.

Brain is a governance/evidence consumer. It is **not** the canonical data writer.

The current XSMB data contract states:

- raw source bytes are preserved and hashed before parsing;
- canonical truth is FULL_27;
- prize structure is `1,1,2,6,4,6,3,4`;
- TAIL_27 is derived only after FULL_27 validation;
- canonical acceptance requires quorum >= 2 independent domains;
- conflicts are recorded and never silently overwritten;
- legacy `Ket_Qua_Loto27.xlsx` is reconciliation reference only.

## Corridor

```text
XSMB DATA PLANE

raw source
   │
   ▼
source SHA
   │
   ▼
FULL_27 structural validation
   │
   ▼
provenance + source identity
   │
   ▼
quorum / conflict decision
   │
   ▼
canonical record
   │
   ├── FULL_27 SHA
   ├── TAIL_27 derived SHA
   ├── day shard SHA
   └── manifest/root SHA
          │
          ▼
   COMPACT EVIDENCE ENVELOPE
          │
          │ corridor: XSMB_DATA_EVIDENCE_EXPORT_V1
          │ capability: EVIDENCE_WRITE
          │ source layer: L0_DATA
          │ destination layer: L0_GOVERNANCE
          │
          ▼
PROJECT_BRAIN_AI
          │
          ├── verify envelope
          ├── verify lineage
          ├── verify hashes
          ├── append evidence index
          └── governance decision
```

## Forbidden paths

```text
Brain → canonical DB mutation       DENY
Brain → source rewrite              DENY
Brain → FULL_27 fabrication         DENY
TAIL_27 → FULL_27 reconstruction    DENY
legacy Tail27 → FULL_27 relabel     DENY
Brain → promotion                   DENY
Chat → direct data mutation         DENY
```

## Evidence envelope

Minimum fields:

```json
{
  "schema": "EVIDENCE_ENVELOPE_V1",
  "project_id": "XSMB_FORENSIC",
  "corridor_id": "XSMB_DATA_EVIDENCE_EXPORT_V1",
  "source_artifact_id": "...",
  "source_sha256": "...",
  "canonical_record_id": "...",
  "full27_sha256": "...",
  "tail27_sha256": "...",
  "shard_sha256": "...",
  "manifest_sha256": "...",
  "provenance_id": "...",
  "verification_state": "...",
  "promotion": "DENY"
}
```

No database password, `DATABASE_URL`, API key, cookie, credential, or secret may appear in the envelope.

## OOM boundary

Brain receives compact envelopes only.

```text
4,000+ days
    ↓
DATA PLANE / DB / SHARDS
    ↓
small evidence envelope
    ↓
BRAIN RAM
```

Brain must never query and materialize the entire historical dataset merely to render governance status.

## Next gate

Before this corridor is marked ACTIVE:

1. validate against the real XSMB foundation contract;
2. execute one bounded fixture end-to-end;
3. verify source→canonical→shard→manifest lineage;
4. verify compact evidence acceptance by Brain security gate;
5. record runtime evidence;
6. keep promotion DENY.
