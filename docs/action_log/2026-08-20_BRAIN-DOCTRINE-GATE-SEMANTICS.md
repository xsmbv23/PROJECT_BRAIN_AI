# FORENSIC DOCTRINE CLARIFICATION — Gate Semantics

## Why this action exists

A critical architectural clarification was identified and must be preserved for successor Bots:

The system does not contain two independent Forensic states or two Forensic universes merely because `DB_EXISTENCE` and `DB_BINDING` have different statuses.

There is exactly **ONE Forensic FSM**. Those statuses are separate ordered admission gates inside that FSM.

## Canonical rule

```text
PASS_IS_LOCAL
PASS_IS_PREREQUISITE_ONLY
NO_PASS_INHERITANCE
OWN_GATE_EVIDENCE_REQUIRED
FRESH_EVIDENCE_REQUIRED_FOR_PROMOTION
UNKNOWN_IS_NOT_PASS
DEFAULT_DENY
HISTORICAL_RECEIPTS_ARE_IMMUTABLE
```

## Database example

```text
DB_EXISTS = PASS
```
means only that the database resource exists.

It does NOT mean:

```text
DB_BINDING = PASS
DB_SECRET = PASS
DB_TLS = PASS
NETWORK_ORIGIN = PASS
DB_ROUND_TRIP = PASS
PROMOTION = PASS
```

Each of those is an independent gate requiring its own evidence.

## Temporal immutability

If a gate is DENY at T1 and PASS at T2, the system records both events chronologically. It never rewrites T1 using T2 knowledge.

## N116 interaction

The current canonical next action remains:

```text
BRAIN-N116_WAIT_EXTERNAL_OBSERVATION
```

No internal DB gate, Data Foundation gate, or historical evidence may unlock N116.

Until the required independent external HTTP observation is ingested and verified:

```text
ACTION_SPACE = 0
PROMOTION = DENY
```

## Change boundary

This clarification changes documentation only. It does not alter `state/next_action.json`, does not create external evidence, does not manufacture receipts, and does not unlock Layer 1 or the staircase.

Successor Bots must read this record before changing gate semantics.
