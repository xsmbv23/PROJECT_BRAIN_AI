# Forensic Admission Chain + Safe Parallel Work Protocol

## 1. One FSM, not multiple forensic state machines

The system has **ONE FORENSIC FSM**.

Database admission, source admission, research, backtest, edge, EV/P&L/ROI, robustness/risk/drift, and controlled action are not separate Forensic universes. They are ordered admission chains/segments inside the same governance model.

A gate PASS is always local evidence for that gate.

```text
PASS_IS_LOCAL
PASS_IS_PREREQUISITE_ONLY
NO_PASS_INHERITANCE
UNKNOWN_IS_NOT_PASS
DEFAULT_DENY
OWN_GATE_EVIDENCE_REQUIRED
FRESH_EVIDENCE_REQUIRED_FOR_PROMOTION
```

## 2. Database admission is an ordered chain

```text
DB_EXISTENCE
   -> DB_BINDING
   -> SECRET_RESOLUTION
   -> DB_TLS_ADMISSION
   -> NETWORK_ORIGIN_PROOF
   -> DB_ROUND_TRIP
   -> PROMOTION
```

Each gate has a different forensic meaning:

| Gate | Evidence meaning | What it does NOT prove |
|---|---|---|
| DB_EXISTENCE | the database resource exists | service has access |
| DB_BINDING | service has a database binding | secret is resolvable |
| SECRET_RESOLUTION | the secret is available to runtime | TLS is valid |
| DB_TLS_ADMISSION | transport security meets policy | network origin is trusted |
| NETWORK_ORIGIN_PROOF | connection originates from admitted runtime boundary | durable write/read integrity |
| DB_ROUND_TRIP | real compact write/read + SHA-256 match | governance authorization beyond this gate |
| PROMOTION | governance decision based on all required evidence | anything outside the declared authorization |

**Critical rule:** an earlier PASS never changes a later gate's state.

Example:

```text
DB_EXISTS = PASS
DB_BINDING = NOT_REACHED
```

must never be represented as `DB_ACCESS = PASS`.

Likewise:

```text
DB_BINDING = PASS
DB_ROUND_TRIP = NOT_REACHED
```

must never become `DURABLE_EVIDENCE = PASS`.

FAIL or UNKNOWN stops reachability. Later gates become `UNREACHED`, not PASS.

## 3. E2E chain

The global mission is:

```text
REAL_DATA
 -> VALID_RESEARCH
 -> VALID_BACKTEST
 -> EDGE
 -> EV_PNL_ROI
 -> ROBUSTNESS_RISK_DRIFT
 -> CONTROLLED_ACTION
```

Segments have their own owners and exit evidence. Downstream implementation may be prepared safely, but downstream status cannot inherit upstream PASS.

## 4. Safe parallel work

When the current Brain state has `action_space = 0` because an external exact-current evidence gate is waiting, a successor Bot may perform **only explicitly declared non-dependent local preparation**.

Allowed:

- documentation and architecture clarification;
- schema/contract validation;
- static tests that do not claim runtime truth;
- deterministic unit tests;
- bounded memory analysis;
- code preparation that cannot unlock or mutate the blocked gate;
- successor action receipts.

Forbidden:

- changing Brain current state to PASS;
- changing promotion from DENY;
- treating GitHub repository structure as CI execution evidence;
- self-attesting Render runtime evidence;
- fabricating or exposing credentials;
- using historical runtime evidence as current evidence;
- opening a locked downstream room;
- converting local test PASS into external runtime PASS.

Every parallel action must state:

```text
current E2E segment
immediate blocker
evidence required to exit blocker
downstream consequence
peer action required
safe parallel work
```

## 5. Successor Bot protocol

Before any mutation:

1. Read `state/current_state.json`.
2. Read `state/next_action.json`.
3. Read the latest `docs/action_log/BRAIN-N*.md`.
4. Read normative architecture documents.
5. Check exact-current commit/deploy/evidence references.
6. Decide whether the intended action is gate work or safe parallel work.
7. If safe parallel work, record that it cannot unlock the gate.
8. Never rewrite historical receipts.
9. Write a new action receipt before handing off.

## 6. Architectural invariant

The Brain remains the **Governance Control Plane**.

```text
DATA owns source truth.
QUANT ENGINE owns calculation.
SENSORS observe.
BRAIN governs admission, evidence, risk, authorization and controlled action.
CHAT is only a communication interface.
```

Brain must not become the data acquisition engine or Quant Engine.

## 7. Forensic immutability

A historical PASS remains historical PASS.

Only fresh exact-current evidence may promote the current state.

Never repair a contradiction by rewriting history. Repair it by creating a new action record that explicitly supersedes the earlier observation.
