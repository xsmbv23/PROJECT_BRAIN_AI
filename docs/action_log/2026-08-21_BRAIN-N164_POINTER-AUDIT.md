# BRAIN-N164 — Successor Pointer Integrity Audit

## Finding

A fresh audit found a persistent-state pointer mismatch:

```text
state/current_state.json
    next_action_id = BRAIN-N164

state/next_action.json
    action_id = BRAIN-N162
```

The current-state file also records:

```text
last_action_id = BRAIN-N163_E2E-PEER-N011-N012-S1-EVIDENCE
next_action_id = BRAIN-N164_S1_MANIFEST-ADMISSION-AUDIT
```

This is a **state-pointer integrity issue**, not evidence that either N162 or N164 is PASS.

## Forensic response

No file was silently overwritten to make the pointers agree.

The system now has:

`tools/verify_successor_pointer_consistency.py`

which returns `DENY` on pointer disagreement and explicitly applies:

```text
DO_NOT_GUESS_ON_POINTER_DRIFT
```

Unit tests cover both matching and mismatching pointers.

## Why this matters

The successor handoff architecture states that `current_state.json` and
`next_action.json` are both authoritative current-state pointers. A mismatch
means a successor Bot cannot safely infer which action is current without a
new reconciliation event.

This protects the transmission chain from a race between parallel Bots.

## S1 remains unchanged

```text
S1_CANONICAL_EVIDENCE = BLOCKED
S2 = UNKNOWN_LOCKED
S3-S7 = UNREACHED_LOCKED
PROMOTION = DENY
```

The S1 verifier/bridge from the parallel N162 work is available, but no real
canonical artifact has been admitted.

## Parallel Bot rule

Because another Bot is actively progressing the repository, this action did
not mutate `state/current_state.json` or `state/next_action.json`.

A future reconciliation action must resolve the pointer mismatch using fresh
Git history/evidence rather than timestamp guessing or chat context.
