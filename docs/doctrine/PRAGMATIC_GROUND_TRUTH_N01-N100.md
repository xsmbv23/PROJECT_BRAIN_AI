# Pragmatic Ground-Truth — N01-N100 Role

## Canonical rule

`Pragmatic Ground-Truth` does NOT replace N01-N100.

N01-N100 remain mandatory foundation controls. They do not become numeric-data analyzers; they analyze the **trust conditions, authority, identity, execution environment, and admission process** under which Excel may act as a ground-truth anchor.

## N01-N100 participation

### N01-N040 — Doctrine

Purpose: prevent Ground-Truth from becoming circular self-validation.

Mandatory principles:

- `DEFAULT_DENY`
- `UNKNOWN_IS_NOT_PASS`
- `PASS_IS_LOCAL_TO_GATE`
- `NO_PASS_INHERITANCE`

`EXCEL_VS_WEB_MATCH = PASS` may only satisfy that local gate. It MUST NOT automatically imply `CANONICAL_QUORUM = PASS`.

### N041-N070 — Forensic FSM / State Authority

Purpose: define who may admit the Excel anchor and who owns persistent state.

Rules:

- Brain is the governance control plane.
- Chat is only a communication interface.
- Persistent repository/evidence state is authoritative.
- Excel is not Ground-Truth merely because the file exists.
- The admission state must explicitly declare `DATA_ADMISSION_MODE = EXCEL_GROUND_TRUTH` before downstream comparison may rely on it.

### N071-N090 — Infrastructure / State Drift

Purpose: establish that the runtime performing the comparison is sufficiently trustworthy.

Controls include:

- runtime identity
- state consistency
- deployment/runtime evidence
- network-origin evidence where required
- state-drift detection

`NETWORK_ORIGIN_PROOF = NOT_PROVEN` remains a real state and cannot be silently converted to PASS.

### N091-N100 — Source Identity / Data Shape

Purpose: establish the identity and minimum completeness of the Excel anchor.

Rules:

- `FULL27` is source truth.
- `TAIL27` is derived data only.
- A TAIL27-only artifact cannot be promoted as source truth.
- The Excel anchor must satisfy the required source-shape gate before it can participate in Ground-Truth admission.

## Ground-Truth admission chain

```text
N01-N040 doctrine
      |
      v
N041-N070 state authority
      |
      v
N071-N090 runtime trust
      |
      v
N091-N100 source identity / FULL27 shape
      |
      v
EXCEL_GROUND_TRUTH_ADMISSION
      |
      +----> WEB FETCH
      |
      +----> EXCEL vs WEB COMPARISON
      |
      v
EXCEL_VS_WEB_MATCH
      |
      v
CANONICAL_QUORUM
```

Each arrow is a **gate transition**, not inherited permission.

## Important distinction

N01-N100 do not answer:

> "What are the lottery numbers?"

They answer:

> "Under what verified conditions are we allowed to trust this artifact, compare it, and admit the resulting evidence?"

Therefore Ground-Truth is a **data-admission strategy**, while N01-N100 are the **forensic trust infrastructure** that makes the strategy legitimate.

## Replacement rule

A future successor MUST NOT describe Pragmatic Ground-Truth as "replacing N103" without qualification.

Correct statement:

> Pragmatic Ground-Truth replaces the original *network-origin independence proof strategy* at the specific canonical-quorum gate, while preserving the underlying N01-N100 doctrine and all gates whose purposes are independent of that strategy.

## Promotion rule

`EXCEL_VS_WEB_MATCH` is necessary but not sufficient for promotion.

Promotion requires all upstream gates to be PASS according to their own local evidence.

No gate may inherit PASS from another gate.

## Successor instruction

When continuing from this doctrine, read this document together with:

- `state/current_state.json`
- `state/next_action.json`
- `docs/action_log/*`
- the canonical source-data contract

Never reconstruct the architecture from chat history alone.
