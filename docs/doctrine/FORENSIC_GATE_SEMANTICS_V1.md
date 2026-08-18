# FORENSIC GATE SEMANTICS V1

## Status

FROZEN doctrine. This document clarifies the meaning of the existing immutable database-admission FSM; it does not change the FSM.

## One Forensic FSM, not multiple forensic states

The database admission chain is ONE chain:

`DB_EXISTENCE -> DB_BINDING -> SECRET_RESOLUTION -> DB_TLS_ADMISSION -> NETWORK_ORIGIN_PROOF -> DB_ROUND_TRIP -> PROMOTION`

Each gate produces a local evidence state. A PASS belongs only to that gate.

## Non-inheritance rule

`PASS_AT_GATE_IS_PREREQUISITE_ONLY`.

A PASS at gate N:

- does not imply PASS at gate N+1;
- does not grant privilege at gate N+1;
- does not convert UNKNOWN or NOT_PROVEN at another gate into PASS;
- cannot be copied into another gate's state field;
- cannot be inferred from existence of the resource or availability of a connector.

Therefore:

`DB_EXISTENCE=PASS` does not mean `DB_BINDING=PASS`.

`DB_BINDING=PASS` does not mean `SECRET_RESOLUTION=PASS`.

`DB_TLS_ADMISSION=PASS` does not mean `NETWORK_ORIGIN_PROOF=PASS`.

`NETWORK_ORIGIN_PROOF=PASS` does not mean `DB_ROUND_TRIP=PASS`.

Only the evidence required by the specific gate can change that gate's state.

## Admission semantics

The chain behaves like secured rooms:

1. resource existence confirms the room exists;
2. binding confirms the service has an authorized binding;
3. secret resolution confirms the secret can be resolved without exposing it;
4. TLS admission confirms the connection policy is acceptable;
5. network-origin proof confirms the actual runtime origin can reach the intended endpoint;
6. round-trip proves a real compact durable write/read and SHA-256 match;
7. promotion is the final authorization state.

Having a key to one door is never a key to the next door.

## State meanings

- `PASS`: this exact gate has its required evidence.
- `DENY`: this exact gate has evidence of a prohibited/failed condition.
- `NOT_PROVEN`: the required evidence does not exist.
- `UNREACHED`: the gate has not been legitimately evaluated because an earlier prerequisite is unresolved.
- `WAIT_EXTERNAL_EVENT`: the next required transition depends on an external infrastructure change; the Brain must not fabricate an internal workaround.

## Forensic invariants

- Unknown is not pass.
- Default deny.
- No synthetic durable mutation.
- No credentials in GitHub.
- No credentials in logs/evidence.
- Local/in-memory audit success is never durable PostgreSQL proof.
- Adapter code cannot escalate privilege.
- Deterministic replayability remains mandatory.
- Layer 1 and staircase remain locked until the immutable promotion chain authorizes them.

## Current canonical interpretation

The current canonical state reports:

`DB_EXISTENCE -> DB_BINDING -> SECRET_RESOLUTION -> DB_TLS_ADMISSION = PASS`

but:

`NETWORK_ORIGIN_PROOF = NOT_PROVEN`

and therefore:

`DB_ROUND_TRIP = NOT_PROVEN`

and:

`PROMOTION = DENY`.

This is a coherent single FSM state, not contradictory forensic states.
