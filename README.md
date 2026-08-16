# Project_Brain_AI

## Fosennic Governance Plane — Foundation

This repository is the **governance/control plane** for the XSMB forensic system.

It is deliberately separate from `xsmb-quant`.

### Brain is NOT

- a crawler;
- a canonical XSMB database;
- a data editor;
- a truth oracle;
- a replacement for the Build Plane;
- a promotion shortcut.

### Brain IS

- project-state authority;
- governance/policy gate;
- corridor/capability authority;
- verification gate;
- evidence registry/index;
- action/progress ledger;
- continuity memory for future Bots;
- promotion DENY gate.

## Fosennic invariant

```text
DEFAULT DENY
  + explicit layer
  + registered corridor
  + capability
  + lineage
  + nonce/freshness
  + post-verification
  + append-only audit
  = authorized communication
```

No project may become `PROMOTED` from static inspection alone.

## Data-plane boundary

`xsmb-quant` owns canonical data and runtime data access.

`Project_Brain_AI` receives compact evidence envelopes only. Brain must never silently mutate canonical truth.

## Foundation status

```text
BRAIN REPOSITORY                 🟢 CREATED
GOVERNANCE CONTRACTS             🟢 FOUNDATION
CORRIDOR/CAPABILITY MODEL        🟢 FOUNDATION
ACTION LEDGER                    🟢 FOUNDATION
EVIDENCE ENVELOPE                🟢 FOUNDATION
PROMOTION GATE                   🔒 DENY
RENDER                           ⚪ NOT CONNECTED YET
LAYER 1                          🔒 LOCKED
```

## Mandatory Bot continuation

Before any future Bot acts, it MUST read:

1. `docs/AI_START_HERE.md`
2. `docs/FOSENNIC_FOUNDATION.md`
3. `docs/COMMUNICATION_SECURITY.md`
4. `docs/EVIDENCE_PROTOCOL.md`
5. `docs/ACTION_LEDGER_PROTOCOL.md`
6. `state/current_state.json`
7. `state/next_action.json`
8. the newest files under `action_log/`

After every action it MUST update the ledger and next action.

## Layer 1 is forbidden until foundation completion

The repository is intentionally initialized as a foundation only. Business/AI intelligence features must not be added until all foundation gates are runtime verified.
