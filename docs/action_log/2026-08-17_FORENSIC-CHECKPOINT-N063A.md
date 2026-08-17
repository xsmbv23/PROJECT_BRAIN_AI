# FORENSIC CHECKPOINT — N063A

## Absolute operating state

```text
FOUNDATION = FROZEN
STATE      = WAIT_EXTERNAL_EVENT
ACTION     = NO-OP
FORENSIC   = INVARIANT
PROMOTION  = DENY
SEALED     = true
SYSTEM     = READY_BUT_NOT_AUTHORIZED
```

## Governing invariant

```text
CAPABILITY != AUTHORITY
```

Brain may possess code, FSM, workflow and implementation capability. That does not grant authority to change forensic state.

## One-way causal chain

```text
REALITY
  ↓
EVIDENCE
  ↓
STATE
  ↓
ACTION
```

Forbidden self-authorizing paths:

```text
INTENT  → ACTION   X
ACTION  → EVIDENCE X
STATE   → EVIDENCE X
BRAIN   → REALITY  X
```

## Database admission chain

The following are gates in ONE forensic admission chain, not independent forensic systems:

```text
DB_EXISTENCE
  ↓
DB_BINDING
  ↓
DB_TLS_ADMISSION
  ↓
DB_ROUND_TRIP
  ↓
PROMOTION
```

Critical invariant:

```text
PASS(Gn) NEVER IMPLIES PASS(Gn+1)
```

A gate's PASS is evidence only for that gate. The next gate requires its own evidence.

Therefore:

```text
DB_EXISTS = PASS
        !=
DB_ACCESS = PASS

DB_BINDING = PASS
        !=
DB_ROUND_TRIP = PASS

DB_ROUND_TRIP = PASS
        !=
PROMOTION unless the promotion policy explicitly accepts that exact evidence.
```

## Security interpretation

The database is a secured room:

```text
corridor_key + room_key
          ↓
       DB room
          ↓
  inner admission conditions
```

Knowing that a room exists is not possession of its key. Possessing a key is not proof that the inner latch opened. Opening the room is not proof that forensic evidence survived a write/read/hash round trip.

## Absolute rule at this checkpoint

NO REAL EVENT
→ NO NEW EVIDENCE
→ NO STATE CHANGE
→ NO ACTION
→ NO-OP IS THE ONLY CORRECT ACTION

Any successor Bot must preserve this checkpoint unless a new external reality event produces admissible evidence. It must not manufacture a transition merely because a next-action file exists.

## Layer state

```text
LAYER_1  = LOCKED
STAIRCASE = LOCKED
```

No capability may be promoted merely because implementation is complete.
