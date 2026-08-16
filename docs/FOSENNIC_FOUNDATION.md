# FOSENNIC FOUNDATION

## 1. Three planes

```text
DATA / BUILD PLANE
  canonical truth
  raw capture
  shard creation
  heavy audit

GOVERNANCE PLANE — Project_Brain_AI
  state
  policy
  corridor
  capability
  evidence
  verification
  promotion gate

RUNTIME / UI PLANE — xsmb-quant
  lightweight reads
  audit projections
  preserved app.py interface
```

No plane may silently absorb another plane's authority.

## 2. Authority hierarchy

```text
FOUNDATION / GOVERNANCE
        ↓
BUILD / DATA
        ↓
RUNTIME / UI
```

A lower layer cannot mint authority belonging to a higher layer.

UI cannot mutate canonical truth.

Data builders cannot promote themselves.

Brain cannot rewrite source truth.

## 3. Evidence hierarchy

```text
RAW_CAPTURE
  ↓
CANONICAL_RECORD
  ↓
DAY_SHARD
  ↓
MANIFEST
  ↓
AUDIT_PROJECTION
  ↓
EVIDENCE_ENVELOPE
```

Every step must preserve lineage.

## 4. Fosennic closure

A path is closed only when all required gates pass:

```text
identity
→ layer
→ corridor
→ capability
→ lineage
→ freshness
→ schema
→ verification
→ audit
→ governance
→ promotion
```

Any failure closes the path.

## 5. No circular authority

Brain may receive evidence from XSMB through an explicit corridor and return governance decisions through another explicit corridor.

It must never obtain an implicit direct mutation path to canonical data.

## 6. Foundation completion

Foundation is complete only when communication security and state continuity are runtime verified, evidence contracts are executable, and the Brain service can safely operate with `PROMOTION=DENY`.

Until then Layer 1 remains locked.
