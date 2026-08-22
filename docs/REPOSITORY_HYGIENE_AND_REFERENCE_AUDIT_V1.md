# REPOSITORY HYGIENE AND REFERENCE AUDIT V1

## Purpose

Prevent future workers from treating every file in the repository as equally authoritative. The repository contains live contracts, current state, runtime code, evidence receipts, immutable history, derived artifacts, experiments and possible scrap. These categories must not be mixed.

## Classification model

```text
                         REPOSITORY FILE
                               |
              +----------------+----------------+
              |                                 |
       referenced by live               not referenced by
       contract/state/code?              live system?
              |                                 |
        +-----+-----+                     +-----+-----+
        |           |                     |           |
       YES          NO                    YES         NO
        |           |                     |           |
      LIVE       inspect              HISTORY?    SCRAP?
        |                                 |           |
        v                                 v           v
  authoritative /                 immutable evidence  candidate
  runtime source                  / historical only   for removal
```

## Current high-priority roots

The following roots are the first reference anchors for future audits:

- `state/current_state.json`
- `state/next_action.json`
- `contracts/`
- `.github/workflows/`
- `docs/AI_START_HERE.md`
- `docs/architecture/`
- `docs/forensic/`
- `docs/coordination/`
- `docs/evidence/`
- `docs/*ACTION*`
- `orchestration/`
- `workers/`
- `Quant_Engine/`
- `coordination/receipts/`
- `coordination/reconciliation/`

## Important distinction

A file being old does not make it scrap.

A file being generated does not make it disposable.

A file being green in a test does not make it authoritative.

A file not linked from the README does not make it unused.

Deletion requires a reference-graph check plus confirmation that the artifact is neither:

- current implementation;
- current contract;
- state authority;
- workflow input;
- runtime dependency;
- durable evidence;
- immutable history;
- required fixture;
- reproducible test fixture;
- peer handoff / continuity artifact.

## Cleanup workflow

```text
INVENTORY
   ↓
REFERENCE SEARCH
   ↓
IMPORT / WORKFLOW / STATE LINK CHECK
   ↓
EVIDENCE / LEDGER LINK CHECK
   ↓
CLASSIFY
   ↓
LIVE / HISTORICAL / DERIVED / SCRAP CANDIDATE
   ↓
ONLY THEN propose deletion
```

No mass deletion is permitted as a cleanup shortcut.

## Future output

A future cleanup action should produce a machine-readable inventory with:

```text
path
classification
referenced_by
runtime_relevance
evidence_relevance
last_known_role
replacement_if_any
delete_safe = true/false/unknown
reason
```

Until that inventory exists, unknown files remain **UNKNOWN**, not SCRAP.
