# BRAIN-N119 — FORENSIC ADMISSION CHAIN INVARIANT

## Context

A prior discussion exposed a dangerous ambiguity: describing `DB_EXISTS` and `DB_BINDING` as "two forensic states" could cause a successor bot to model them as separate forensic systems.

That interpretation is explicitly rejected.

## Canonical correction

There is exactly **ONE Forensic FSM**.

`DB_EXISTENCE`, `DB_BINDING`, `DB_TLS_ADMISSION`, `DB_ROUND_TRIP`, and `PROMOTION` are gates inside one admission chain.

Canonical rule:

```text
PASS(GATE_N) != PASS(GATE_N+1)
```

PASS is local to the gate that produced it. It is never inherited.

## Why this matters

Examples:

```text
DB_EXISTS = PASS
```

means only that the database resource exists.

It does not mean:

```text
DB_BINDING = PASS
DB_TLS_ADMISSION = PASS
DB_ROUND_TRIP = PASS
PROMOTION = PASS
```

Likewise:

```text
BOUND_TLS = PASS
```

means the runtime binding satisfies the credential-free TLS admission contract. It does not prove that a real database write/read/hash round-trip succeeded.

## Cross-repository consequence

Bot 2's Quant Engine evidence is a local prerequisite only.

Bot 1 must evaluate its own Brain gate using its own evidence.

No cross-repository PASS inheritance is allowed.

## Protected-room consequence

The same logic applies to the physical-room security metaphor:

```text
corridor key + room key
```

does not override:

```text
inner latch / owner release
```

Each security boundary is independently satisfied.

## Current canonical locks

The current dual-bot handoff observed in open work records keeps:

```text
ACTION_SPACE = 0
MANDATORY_NO_OP = TRUE
PROMOTION = DENY
ROOM_02 = LOCKED
STAIRCASE = LOCKED
```

N119 does not alter those values and does not perform a promotion or unlock.

## Work performed

Added:

```text
`docs/architecture/FORENSIC_ADMISSION_CHAIN_V1.md`
```

Commit:

```text
3ea35b66f00f622cd7394c3991b5119924472907
```

No source data, credential, or gated state was changed.

## Verification level

```text
FOUND = PASS
FIXED = PASS
TESTED = NOT CLAIMED
RUNTIME_VERIFIED = NOT CLAIMED
EXTERNAL_EVIDENCE = NOT CLAIMED
PROMOTED = NO
```

This is an architectural invariant/documentation action, not a runtime admission.

## Successor instruction

Before any dependent action, successor bots must read this document and preserve the invariant:

> **One Forensic FSM; many gates. No PASS inheritance. Every transition requires its own evidence.**

## Next action

Continue the current canonical action selected by the active state contract. Do not replace the canonical `NEXT_ACTION` merely because N119 is complete.
