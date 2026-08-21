# Current-State Authority for Successor Bots

## Mandatory reading order

A successor Bot AI MUST read these in order before acting:

1. `state/current_state.json`
2. `state/next_action.json`
3. the latest `docs/action_log/BRAIN-N*.md`
4. normative architecture documents

## Authority law

`state/current_state.json` and `state/next_action.json` are the authoritative current-state pointers.

Architecture documents may contain historical execution snapshots. A historical snapshot is **not** current runtime truth unless its commit/deploy/evidence is also referenced by the current state and independently verified as exact-current.

Therefore:

```text
CURRENT STATE FILE
    >
LATEST ACTION RECEIPT
    >
NORMATIVE ARCHITECTURE
    >
HISTORICAL SNAPSHOT
```

The `>` means authority for current execution state, not importance of the architecture itself.

## Why this exists

The Forensic Database Admission Chain document intentionally records the admission semantics, but older revisions can contain earlier runtime anchors. A successor must never take an old commit/deploy snapshot and treat it as today's runtime evidence.

The architecture remains normative:

```text
DB_EXISTENCE
 -> DB_BINDING
 -> SECRET_RESOLUTION
 -> DB_TLS_ADMISSION
 -> NETWORK_ORIGIN_PROOF
 -> DB_ROUND_TRIP
 -> PROMOTION
```

But the actual state of those gates MUST come from fresh exact-current evidence and the current state/action chain.

## Immutable history rule

Do not rewrite history merely to make an old document appear current.

If a document contains a historical runtime snapshot, preserve it as historical evidence and add a new action record explaining the supersession.

Never convert:

```text
historical PASS
```

into:

```text
current PASS
```

without fresh exact-current evidence.

## Forensic successor rule

A Bot is allowed to continue safe local preparation while `action_space = 0` only when that preparation is explicitly declared as non-dependent work. It may not use local preparation to unlock the blocked external gate, alter promotion, or inherit PASS.
