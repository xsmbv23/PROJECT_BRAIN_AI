# Reality Gate Semantics — Successor Record

This record preserves the semantic decision confirmed in the preceding review.

## Frozen doctrine

The system contains one Forensic FSM. Database existence, binding, TLS admission, round-trip verification, and promotion are sequential gates inside that FSM.

`PASS(N)` is local to gate N. It is a prerequisite, never inherited permission.

## Required invariants

- `DB_EXISTENCE != DB_AUTHORIZATION`
- `DB_AUTHORIZATION != DB_TLS_ADMISSION`
- `DB_TLS_ADMISSION != DB_ROUND_TRIP`
- `DB_ROUND_TRIP != DOMAIN_TRUTH`
- `STRUCTURALLY_VALID != DOMAIN_TRUE`
- `ROUNDTRIP_VALID != DOMAIN_UNDERSTANDING`
- `READINESS != AUTHORITY`
- `LOG != EVIDENCE`
- `RULE != AUTHORITY`
- `ARTIFACT != PROGRESS`
- `SIMULATION != EVIDENCE`
- `PASS != INHERITED_PERMISSION`

## Transition law

```text
NO EXTERNAL EVENT -> NO TRANSITION -> NO ACTION
```

The system must not self-create an external event merely to escape a waiting state.

## Current handoff

`REALITY-N011-STABILITY-QUORUM` is `WAIT_EXTERNAL_EVENT`.

Until a real GitHub Actions workflow-dispatch event produces an independent runtime receipt, the correct action is NO-OP.

## Anti-drift requirement

Future Bots must treat this file, `state/current_state.json`, and `state/next_action.json` as persistent successor authority. The chat transcript is only the communication interface.
