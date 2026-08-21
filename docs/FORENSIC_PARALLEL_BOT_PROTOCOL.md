# Forensic Parallel-Bot Protocol

## Purpose

Multiple AI bots may work concurrently on Fosennic/Forensic infrastructure. Concurrency must never create a second state machine, a hidden promotion path, or an implicit override of the canonical repository state.

## Authority

1. `state/current_state.json` is the current machine-readable state.
2. `state/next_action.json` is the successor handoff instruction.
3. Action logs are immutable historical evidence.
4. Chat is a communication interface, not persistent state authority.
5. One Forensic FSM governs the whole system.

## Parallel rule

A bot may execute work in parallel only when its work is explicitly marked as a safe local prerequisite or documentation/infrastructure task.

Parallel work MUST NOT:

- unlock a Brain gate;
- change promotion state;
- infer external runtime PASS from repository/workflow structure;
- overwrite canonical truth with derived data;
- bypass an UNKNOWN or UNREACHED gate;
- write credentials to GitHub;
- convert Brain into Data/Quant Engine;
- weaken the 320 MiB Render guard;
- unlock Layer 1 Room 02 or the staircase.

## Gate semantics

Every gate owns its own evidence.

```text
PASS at Gate A
      |
      v
permits evaluation of Gate B
      |
      +---- NOT ----> Gate B PASS
```

PASS never inherits.
FAIL or UNKNOWN stops reachability. Later gates are `UNREACHED`, not PASS.

## Database admission chain

```text
DB_EXISTENCE
    -> DB_BINDING
    -> SECRET_RESOLUTION
    -> DB_TLS_ADMISSION
    -> NETWORK_ORIGIN_PROOF
    -> DB_ROUND_TRIP
    -> PROMOTION
```

These are stages of ONE Forensic FSM, not independent Forensic systems.

- `DB_EXISTENCE`: resource existence only.
- `DB_BINDING`: service binding only.
- `DB_TLS_ADMISSION`: transport-security evidence only.
- `DB_ROUND_TRIP`: real write-read-hash evidence only.
- `PROMOTION`: governance decision only.

## Exact-current external observation

Repository CI execution is repository-execution evidence. It is not equivalent to independently observable production runtime truth.

Therefore:

```text
CI PASS
  !=
EXACT_CURRENT RUNTIME PASS
```

A successor must preserve `UNKNOWN` when the independent observation surface cannot prove the current runtime state.

## Parallel Quant Engine

`xsmbv23/Quant_Engine` may perform explicitly authorized Layer 1 Room 01 prerequisite work while Brain is waiting for independent external evidence.

Its evidence may be consumed by Brain only with its declared scope preserved. It cannot unlock Brain promotion.

## Successor rule

Before taking any action, the next bot MUST read:

1. `state/current_state.json`
2. `state/next_action.json`
3. the latest action log
4. this protocol

Then it must continue from the declared `next_action_id`, not from chat memory or assumptions.
