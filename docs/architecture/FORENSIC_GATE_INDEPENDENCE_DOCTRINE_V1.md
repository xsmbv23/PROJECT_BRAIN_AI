# FORENSIC GATE INDEPENDENCE DOCTRINE V1

## Purpose

This document is normative for all successor Bots and all future code changes in `Project_Brain_AI`.

There is **ONE Forensic FSM**, not multiple independent Forensic systems.

The FSM contains multiple admission chains/domains. A gate result is evidence about one local proposition only.

## Core invariant

> PASS IS LOCAL TO THE GATE.
> PASS IS A PREREQUISITE FOR THE NEXT GATE, NEVER A GLOBAL AUTHORIZATION.
> NO PASS INHERITANCE ACROSS GATES OR DOMAINS.

Therefore:

```text
PASS(DB_EXISTENCE)
        != PASS(DB_BINDING)
        != PASS(DB_TLS_ADMISSION)
        != PASS(DB_ROUND_TRIP)
        != PASS(PROMOTION)
```

and:

```text
PASS(SOURCE_INDEPENDENCE)
        != PASS(NETWORK_ORIGIN_PROOF)
        != PASS(EXCEL_VS_WEB_MATCH)
        != PASS(CANONICAL_QUORUM)
        != PASS(TRUTH_ADMISSION)
```

A PASS in the database chain cannot satisfy a source-chain prerequisite.
A PASS in the source chain cannot satisfy a database-chain prerequisite.

## Database admission chain

```text
DB_EXISTENCE
     |
     v
DB_BINDING
     |
     v
DB_TLS_ADMISSION
     |
     v
DB_ROUND_TRIP
     |
     v
PROMOTION
```

Meaning:

- `DB_EXISTENCE`: the database resource is confirmed to exist.
- `DB_BINDING`: the service has an explicit runtime binding.
- `DB_TLS_ADMISSION`: that binding satisfies the allowed TLS policy.
- `DB_ROUND_TRIP`: a real compact metadata envelope was written, read back, and its hash matched.
- `PROMOTION`: durable evidence use is authorized only after every prior DB proposition is independently proven.

`DB_EXISTENCE=PASS` never grants access.
`DB_BINDING=PASS` never proves the round trip.
`DB_TLS_ADMISSION=PASS` never proves data persistence.

## Source admission chain

```text
SOURCE_INDEPENDENCE
        |
        v
NETWORK_ORIGIN_PROOF
        |
        v
EXCEL_VS_WEB_MATCH
        |
        v
CANONICAL_QUORUM
        |
        v
TRUTH_ADMISSION
```

Meaning:

- `SOURCE_INDEPENDENCE`: the proposition that the selected sources are independent is proven under the current source-independence policy.
- `NETWORK_ORIGIN_PROOF`: the network response is proven to originate from the declared source boundary.
- `EXCEL_VS_WEB_MATCH`: source content reconciles against the Excel ground-truth admission policy. This is a local gate only.
- `CANONICAL_QUORUM`: the configured quorum rule is independently satisfied.
- `TRUTH_ADMISSION`: only the final source-domain chain may admit content as source truth.

`EXCEL_VS_WEB_MATCH=PASS` does **not** grant canonical quorum.
`NETWORK_ORIGIN_PROOF=PASS` does **not** grant truth admission.

## Database/source separation

```text
DATABASE DOMAIN                         SOURCE DOMAIN
---------------                         ------------
DB_EXISTENCE                            SOURCE_INDEPENDENCE
DB_BINDING                              NETWORK_ORIGIN_PROOF
DB_TLS_ADMISSION                        EXCEL_VS_WEB_MATCH
DB_ROUND_TRIP                            CANONICAL_QUORUM
PROMOTION                               TRUTH_ADMISSION
```

The domains share the same Forensic FSM and the same default-deny doctrine, but they do not share PASS state.

## Security corridor relation

The physical security metaphor maps to admission control:

```text
CORRIDOR_KEY -> ROOM_KEY -> INNER_RELEASE_WHEN_PROTECTED
```

A correct corridor key does not imply a correct room key.
A correct room key does not bypass an inner latch on protected rooms.
The same principle applies to evidence gates.

## Unknown and failure

```text
UNKNOWN -> NOT PASS
MISSING EVIDENCE -> DENY
INVALID EVIDENCE -> DENY
CROSS-DOMAIN EVIDENCE -> DENY FOR THAT PROPOSITION
```

No gate may convert another gate's PASS into its own PASS without its own receipt.

## Evidence receipt rule

Every PASS that can affect promotion must have its own immutable evidence receipt.
A receipt is a reference to evidence; it is not itself permission.

## Successor rule

A successor Bot must read this doctrine before modifying:

- `core/forensic_gate.py`
- source adapters
- database adapters
- promotion gates
- state artifacts
- action logs

If a proposed change causes PASS to become global, inherited, implicit, or cross-domain, the change is **FORBIDDEN**.

## Current implementation authority

The executable implementation is `core/forensic_gate.py`.
The durable successor state is `state/current_state.json` and `state/next_action.json`.
The immutable action history is under `docs/action_log/`.

This document explains the invariant; executable code remains the enforcement authority.
