# Forensic Gate Interaction — One FSM, No Pass Inheritance

## Core rule

There is exactly **one Forensic FSM**. A gate is not an independent Forensic universe. Each gate is one ordered state transition inside the same admission chain.

A PASS is always **local evidence**. It is only a prerequisite that makes the next gate reachable. It never grants the next gate PASS.

```text
PASS(G_n) != PASS(G_n+1)
PASS(G_n) -> reachability(G_n+1)
```

FAIL or UNKNOWN stops reachability. Later gates are `UNREACHED`, not PASS.

## Database admission chain

```text
DB_EXISTENCE
     |
     v
DB_BINDING
     |
     v
SECRET_RESOLUTION
     |
     v
DB_TLS_ADMISSION
     |
     v
NETWORK_ORIGIN_PROOF
     |
     v
DB_ROUND_TRIP
     |
     v
PROMOTION
```

### Meaning of each gate

| Gate | Evidence owned by gate | Does PASS grant next PASS? |
|---|---|---|
| DB_EXISTENCE | database resource exists and is the intended resource | No |
| DB_BINDING | service has the required runtime binding | No |
| SECRET_RESOLUTION | required secret resolves without exposing it | No |
| DB_TLS_ADMISSION | transport satisfies explicit TLS policy | No |
| NETWORK_ORIGIN_PROOF | connection originates from the authorized runtime boundary | No |
| DB_ROUND_TRIP | real compact write/read/hash-match evidence | No |
| PROMOTION | governance decision using fresh evidence | Final decision only |

## Why this distinction exists

`DB_EXISTS = PASS` means only:

> the room exists.

It does **not** mean:

> the service has the key.

Likewise `DB_BINDING = PASS` does not mean the secret resolved, TLS passed, network origin was authorized, or a real round-trip occurred.

The chain therefore behaves like a secured building:

```text
corridor key
   +
room key
   +
secret release
   +
TLS admission
   +
network-origin proof
   +
actual room interaction
   =
promotion candidate
```

A special/protected room may additionally require an inner release from the room owner. This is a distinct gate, not an inherited permission.

## Forensic invariants

- UNKNOWN is not PASS.
- Default is DENY.
- Every gate owns its own evidence.
- Fresh evidence is required for promotion.
- Historical evidence cannot be silently reused as current evidence.
- Raw-byte identity and semantic meaning are different hash domains.
- Derived data cannot overwrite source truth.
- Brain is governance control plane, not Data Engine or Quant Engine.
- Chat is communication interface only; persistent repository state is authority.
- No credential may be stored in GitHub, logs, receipts, or Brain state.
- Render Free 512 MB is a hard boundary; 320 MiB is the conservative guard.

## Successor rule

A future Bot must read this document before modifying any gate. It must not collapse gates merely because several currently appear to PASS. The exact evidence belonging to each gate is the only authority for that gate.
