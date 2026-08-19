# BRAIN-DOCTRINE-GATE-SEMANTICS

## Action

Persist the architectural clarification that was identified during review of the N103 admission state.

## Locked conclusion

There are not two independent Forensic systems. There is **one Forensic FSM** containing multiple independently evidenced gates.

A gate PASS is local to the proposition it proves.

```text
DB_EXISTENCE PASS
    !=
DB_BINDING PASS
    !=
DB_TLS_ADMISSION PASS
    !=
DB_ROUND_TRIP PASS
    !=
PROMOTION PASS
```

The same rule applies to source admission:

```text
SOURCE_INDEPENDENCE PASS
    !=
CANONICAL_QUORUM PASS
    !=
TRUTH_ADMISSION PASS
```

## Why this was added

Without this explicit doctrine, a future Bot could see a valid upstream observation and accidentally inherit it as downstream authority.

That would violate Forensic immutability because the proposition being asserted would have changed without a new evidence receipt.

## Required interaction model

```text
UPSTREAM PASS
     |
     v
DOWNSTREAM GATE MAY OPEN FOR EVALUATION
     |
     +--> downstream evidence required
     |
     +--> downstream PASS/FAIL/UNKNOWN produced locally
```

Upstream PASS is therefore a **prerequisite**, never a transferable permission.

## Current N103 implication

N103 has no DNS/RDAP evidence. Therefore:

```text
independence_proven = false
status = DENY_INDEPENDENCE
canonical_quorum = LOCKED
N104 = NOT OPEN
```

This does not assert that the sources share infrastructure. It asserts only that the current evidence is insufficient to prove independence.

## Successor requirement

A later Bot must not weaken this state by inference, stale evidence, hostname comparison, HTML comparison, or assumption. The retry must obtain fresh evidence and persist the resulting receipt before any downstream gate is opened.
