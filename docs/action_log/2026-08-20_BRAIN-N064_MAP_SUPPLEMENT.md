# N064 MAP SUPPLEMENT — N116 COMPATIBILITY NOTICE

This is a documentation-only foundation supplement created while the canonical Forensic FSM is frozen at `BRAIN-N116_WAIT_EXTERNAL_OBSERVATION`.

## Authority rule

`state/current_state.json` and `state/next_action.json` remain authoritative. This supplement MUST NOT change the current action, action_space, promotion state, Layer 1, or staircase.

## Repository map

```text
                    ONE FORENSIC FSM
                          │
                          ▼
               Project_Brain_AI
          Governance / Admission / Forensic
                    │           │
              control │           │ deny/permit
                    ▼           ▼
             xsmb-quant ←──→ Quant_Engine
          Source/Data Truth     Calculation/Research
```

The arrows above are conceptual authority/evidence relationships, not a permission to create an automatic closed execution loop.

### `xsmbv23/xsmb-quant`

Owns source truth, ingestion, raw artifacts, reconciliation, calendar/state, data contracts, and data-foundation security. Existing repository evidence includes `docs/STATE_AUTHORITY_HANDOFF.md`, `docs/AI_ACTION_LOG_V1.md`, `docs/AI_PROGRESS_LEDGER_V1.md`, `data/contracts/README.md`, `storage/raw_artifacts.py`, `data/reconciliation/legacy_reconcile.py`, `security/corridor.py`, and `security/capability.py`.

### `xsmbv23/Quant_Engine`

Owns calculation/research. It consumes explicit admissible data and produces derived results. It must not mutate source truth and must not become a substitute for Brain governance.

### `xsmbv23/Project_Brain_AI`

Owns governance, Forensic FSM semantics, admission, capability/room/corridor security, immutable state, promotion gates, successor action handoff, and compact evidence. It must not become the data-ingestion or quant-calculation authority.

## Critical gate doctrine

There is exactly **ONE Forensic FSM**. The following are gates in one chain, not separate Forensic universes:

```text
DB_EXISTENCE
 -> DB_BINDING
 -> SECRET_RESOLUTION
 -> DB_TLS_ADMISSION
 -> NETWORK_ORIGIN_PROOF
 -> DB_ROUND_TRIP
 -> PROMOTION
```

```text
PASS_IS_LOCAL
PASS_IS_PREREQUISITE_ONLY
NO_PASS_INHERITANCE
OWN_GATE_EVIDENCE_REQUIRED
FRESH_EVIDENCE_REQUIRED_FOR_PROMOTION
UNKNOWN_IS_NOT_PASS
DEFAULT_DENY
```

The same rule applies to source admission and runtime action admission.

## Current runtime doctrine

As of this supplement:

```text
current action = BRAIN-N116_WAIT_EXTERNAL_OBSERVATION
action_space  = 0
mandatory_no_op = true
promotion = DENY
```

Track B data-foundation preparation may continue only within the frozen doctrine's allowed scope. It cannot unlock Track A and cannot alter `NEXT_ACTION`.

## Successor instruction

Read this supplement together with:

- `docs/forensic/FORENSIC_FSM_GATE_SEMANTICS.md`
- `docs/SYSTEM_REPOSITORY_MAP_V1.md`
- `state/current_state.json`
- `state/next_action.json`

Never infer runtime permission from repository correctness alone. Every cross-repository edge requires its own admission evidence.
