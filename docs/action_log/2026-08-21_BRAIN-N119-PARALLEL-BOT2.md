# BRAIN-N119 — Parallel Bot-2 Admission Audit

## Purpose

This action is intentionally performed in parallel with the other Brain bot work. It does not alter canonical `main`, does not promote any gate, and does not compete with N118/N116 authority.

## Coordination observation

The current Brain repository has two active Bot-1 draft PRs:

- PR #2: N118 state/evidence handoff to Bot 2
- PR #3: N118 governance-envelope hardening

Bot 2's Quant repository is a separate control surface. The latest known Bot-2 handoff referenced by Bot 1 is `QUANT-N006`.

## Forensic rule reinforced

There is exactly **ONE FORENSIC FSM**. Database admission is not a second forensic state machine.

The database admission chain is a sequence of gate-local evidence states inside the one FSM:

```text
DB_EXISTENCE
    |
    | evidence: resource exists
    v
DB_BINDING
    |
    | evidence: service has explicit binding
    v
DB_TLS_ADMISSION
    |
    | evidence: PostgreSQL binding satisfies accepted TLS mode
    v
DB_ROUND_TRIP
    |
    | evidence: compact metadata write -> read -> SHA-256 match
    v
PROMOTION
```

A PASS at one gate is **not inherited** by the next gate.

```text
DB_EXISTS = PASS
    != DB_BINDING = PASS

DB_BINDING = PASS
    != DB_TLS_ADMISSION = PASS

DB_TLS_ADMISSION = PASS
    != DB_ROUND_TRIP = PASS

DB_ROUND_TRIP = PASS
    != automatic downstream promotion unless the explicit promotion gate accepts it
```

## Interaction rule

Each gate produces a local evidence claim. The next gate may use that claim only as an input prerequisite; it must independently establish its own evidence.

This prevents the following forbidden inference:

```text
DATABASE EXISTS
      -> DATABASE ACCESS
      -> DURABLE EVIDENCE
      -> PROMOTION
```

The valid chain is:

```text
DATABASE EXISTS
      -> MAY CHECK BINDING
      -> BINDING PROVEN
      -> MAY CHECK TLS
      -> TLS PROVEN
      -> MAY PERFORM REAL ROUND-TRIP
      -> ROUND-TRIP PROVEN
      -> MAY EVALUATE PROMOTION
```

## Security analogy

The physical-security model remains authoritative:

```text
corridor key
    +
room key
    +
inner latch / protected-room release
    +
actual room evidence
```

Possession of a corridor key never implies possession of a room key. Possession of a room key never implies that the room's internal latch has released. Reaching the room does not prove the work performed inside it is valid.

## Cross-bot rule

Bot 2 may prove a Quant-local prerequisite such as source quorum, semantic agreement, extraction validity, or bounded processing. That proof remains local to the Quant gate unless Brain has an explicit contract that admits it.

Likewise, Brain governance evidence must not be treated as proof that Quant source truth, extraction, or calculation is valid.

```text
BOT 2 PASS = BOT 2 LOCAL PREREQUISITE
BOT 1 PASS = BOT 1 LOCAL PREREQUISITE
CROSS-REPO ADMISSION = EXPLICIT CONTRACT + FRESH EVIDENCE
```

## Immutable-state rule

This parallel branch must never:

- change canonical `state/next_action.json` on main;
- manufacture N116 external observation;
- convert `FIXED` into `TESTED` without CI evidence;
- convert `TESTED` into `RUNTIME_VERIFIED` without exact-current runtime evidence;
- convert `RUNTIME_VERIFIED` into `EXTERNAL_EVIDENCE` without independent external evidence;
- promote Room 02 or open the staircase;
- store credentials in GitHub;
- expose credentials through governance endpoints or logs.

## OOM rule

Any future parallel work must remain bounded and preferably dataset-free on Brain. Large source data belongs to the Quant/Data side. Brain should consume compact evidence envelopes rather than bulk datasets.

## Next dependent action

After Bot 2's N006 evidence is observed, the Brain side should compare the Quant evidence envelope against the one-FSM admission contract. No cross-repository PASS inheritance is permitted.

## Completion

`BRAIN-N119 = PARALLEL FORENSIC SEMANTIC AUDIT RECORDED`

No canonical gate was changed by this action.
