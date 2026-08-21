# BRAIN-N164 — S1 Manifest Admission Audit

## Trigger

The exact-current Render runtime exposed a critical state-integrity defect: `state/current_state.json` and `state/next_action.json` had drifted away from the fail-closed `DATA_ADMISSION` verifier contract. The runtime correctly DENIED boot rather than trusting stale state.

## Observed failure

Render build succeeded, but the application boot gate returned `DENY` at `state_consistency` because required state fields were missing and DATA_ADMISSION semantics were not represented exactly.

This is a valid Forensic failure. The runtime was not permitted to silently repair its own persistent state at boot.

## Repair

Reconciled both direct JSON state artifacts:

```text
state_mode       = DATA_ADMISSION
state            = SOURCE_PROVENANCE_CAPTURE
action_space     = 1
action           = RUNTIME_PROVENANCE_EXECUTION
promotion        = PASS_TO_ROOM_01_ONLY;CANONICAL_QUORUM_DENY
layer_1          = ROOM_01_DATA_ADMISSION
room_02          = LOCKED
staircase        = LOCKED
pass_inheritance = false
unknown_is_not_pass = true
default_deny     = true
ci_status        = UNKNOWN_NO_OBSERVABLE_WORKFLOW_RUN
next_action_id   = BRAIN-N164_S1_MANIFEST-ADMISSION-AUDIT
```

## Architectural improvement

Added a machine-checkable S1 contract verifier:

```text
tools/verify_s1_manifest_contract.py
tests/test_s1_manifest_contract.py
```

and wired it into `tools/verify_foundation.py`.

The verifier intentionally distinguishes:

```text
PASS_CONTRACT
    !=
S1_ADMISSION
```

A contract can be internally coherent while no real canonical dataset has yet been admitted.

## Immutable Forensic rule

The old boot DENY event is not erased. N164 is a new corrective action and new commit. The state history therefore records:

```text
N163 -> observed external/data boundary
N164 -> state reconciliation + contract enforcement
```

## Current admission position

```text
DB_EXISTENCE          = PASS
DB_BINDING            = PASS
SECRET_RESOLUTION     = PASS
DB_TLS_ADMISSION      = PASS
NETWORK_ORIGIN_PROOF  = PASS
DB_ROUND_TRIP         = PASS
PROMOTION             = DENY

S1_CANONICAL_EVIDENCE = BLOCKED
S2+                   = LOCKED
```

The DB chain and S1 data chain are not collapsed. They are gates inside the same Forensic FSM with local evidence ownership and no PASS inheritance.

## Next

`BRAIN-N165` — run exact-current Render verification after state reconciliation and prove that the foundation gate can boot safely while keeping S1 promotion DENY. Then continue the S1 real-evidence admission chain only from observable evidence.
