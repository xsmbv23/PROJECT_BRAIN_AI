# FORENSIC FOUNDATION — FROZEN INVARIANTS

## Purpose

This document is normative for successor AI bots. It prevents later agents from collapsing distinct forensic evidence into a single convenient boolean.

## One database admission FSM

There is **one** Forensic database admission chain, not multiple independent Forensic systems:

```text
DB_EXISTENCE
    ↓
DB_BINDING
    ↓
SECRET_RESOLUTION
    ↓
DB_TLS_ADMISSION
    ↓
NETWORK_ORIGIN_PROOF
    ↓
DB_ROUND_TRIP
    ↓
PROMOTION
```

Each gate answers a different factual question.

- `DB_EXISTENCE`: does the database resource exist?
- `DB_BINDING`: is the exact service bound to the database?
- `SECRET_RESOLUTION`: was the required credential reference resolved from the authorized secret store?
- `DB_TLS_ADMISSION`: does the resolved binding satisfy the explicit TLS policy?
- `NETWORK_ORIGIN_PROOF`: is the connection origin proven to be the exact authorized runtime/database path?
- `DB_ROUND_TRIP`: did the exact runtime perform a real compact metadata write, read it back, and obtain the expected SHA-256 match?
- `PROMOTION`: may durable evidence be promoted to the authoritative sink?

## State is not capability

The following distinction is immutable:

```text
STATE ≠ CAPABILITY ≠ VALIDATION ≠ EXECUTION
```

`DB_EXISTENCE = PASS` never grants DB access.

`DB_BINDING = PASS` never implies secret resolution.

`SECRET_RESOLUTION = PASS` never implies TLS admission.

`DB_TLS_ADMISSION = PASS` never implies network-origin proof.

`NETWORK_ORIGIN_PROOF = PASS` never implies successful round-trip.

Only the real temporal round-trip evidence may satisfy the final execution gate.

## No pass inheritance

```text
PASS_IS_PREREQUISITE_ONLY
NO_PASS_INHERITANCE
UNKNOWN_IS_NOT_PASS
DEFAULT_DENY
```

A later gate may execute only when every preceding gate has an explicit PASS evidence event.

## First-failure reachability

The FSM is strictly sequential.

```text
FIRST FAIL OR UNKNOWN
        ↓
       DENY
        ↓
LATER GATES = UNREACHED
```

Do not manufacture `false` for an unreached gate. `UNREACHED` has forensic meaning and must remain distinguishable from `FAIL`.

## No derived state

Do not introduce convenience states such as:

- `DATABASE_PASS`
- `DB_READY`
- `DB_OK`
- `DB_AVAILABLE`
- `DB_CONNECTED`

unless each is explicitly defined as an independent evidence-bearing gate. Never use a derived aggregate boolean as a substitute for the admission FSM.

## Failure history is immutable

A later retry may append a new event but must not erase, overwrite, or reinterpret the earlier failure.

```text
attempt A → DENY(reason X)
attempt B → PASS(reason Y)
```

Both events remain part of the audit history.

## Temporal round-trip requirement

A valid round-trip requires two distinct temporal evidence points:

```text
nonce/event A → WRITE
nonce/event B → READ
SHA256(expected) == SHA256(observed)
```

A local mock, static fixture, cache, tunnel, proxy, synthetic response, or precomputed hash is not evidence of the Render runtime round-trip.

## Environment and origin rules

```text
LOCAL_PASS ≠ RENDER_PASS
```

Only the exact runtime anchor may establish runtime-specific evidence.

Local tunnels, developer caches, ambiguous proxies, or copied environment values are DENY conditions for origin proof.

## Secret rule

Credentials may exist only in the authorized runtime secret store.

Never:

- commit credentials to GitHub;
- print raw credentials;
- return raw credentials through health endpoints;
- hash raw credentials as evidence;
- place credentials into forensic envelopes;
- fabricate a credential to make a gate pass.

## Current frozen terminal state

```text
DB_EXISTENCE            = PASS
DB_BINDING              = NOT_BOUND
SECRET_RESOLUTION       = UNREACHED
DB_TLS_ADMISSION        = UNREACHED
NETWORK_ORIGIN_PROOF    = UNREACHED
DB_ROUND_TRIP            = UNREACHED
PROMOTION               = DENY
```

This is a truthful terminal state, not a defect.

## Boundary

The foundation is frozen. Future Quant work belongs in `xsmbv23/Quant_Engine`.

Infrastructure gates must not be reopened unless an authorized external binding condition changes and new evidence is available.
