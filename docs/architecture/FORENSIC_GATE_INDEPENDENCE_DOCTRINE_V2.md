# FORENSIC GATE INDEPENDENCE DOCTRINE V2

## Purpose

This document formalizes a critical invariant discovered during the Brain foundation work and confirmed during the N104C comparison review.

There is **ONE Forensic FSM**. Individual forensic states/gates are not independent FSMs. A gate is a local proposition inside the single FSM.

## Core invariant

> **PASS belongs only to the gate that produced the evidence. PASS is a prerequisite for downstream evaluation, never inherited as downstream PASS.**

Therefore:

```text
GATE_A = PASS
        !=
GATE_B = PASS
```

unless GATE_B has its own explicit evidence and admission decision.

## Database admission chain

```text
DB_EXISTENCE
    -> DB_BINDING
        -> DB_TLS_ADMISSION
            -> DB_ROUND_TRIP
                -> PROMOTION
```

Meaning:

- `DB_EXISTENCE=PASS`: the database resource exists.
- `DB_BINDING=PASS`: the service has an explicit binding to that database.
- `DB_TLS_ADMISSION=PASS`: that binding satisfies TLS policy.
- `DB_ROUND_TRIP=PASS`: a real compact evidence write/read/hash-match was observed.
- `PROMOTION=PASS`: only now may durable evidence promotion occur.

No earlier PASS grants a later PASS.

## Source admission chain

```text
SOURCE_INDEPENDENCE
    -> NETWORK_ORIGIN_PROOF
        -> RESULT_TRANSPORT
            -> OFFICIAL_RESULT_PANEL
                -> CANDIDATE
                    -> EXCEL_VS_WEB_MATCH
                        -> CANONICAL_QUORUM
                            -> TRUTH_ADMISSION
```

Each arrow is a prerequisite relationship, not PASS inheritance.

Examples:

```text
NETWORK_ORIGIN_PROOF = PASS
        != RESULT_TRANSPORT = PASS

RESULT_TRANSPORT = PASS
        != CANDIDATE = PASS

CANDIDATE = PASS
        != EXCEL_VS_WEB_MATCH = PASS

EXCEL_VS_WEB_MATCH = PASS
        != CANONICAL_QUORUM = PASS
```

## Runtime evidence outranks repository projection

The authority order is:

```text
EXACT_CURRENT_RUNTIME_EVIDENCE
        >
BRAIN_PERSISTED_STATE
        >
IMMUTABLE_ACTION_HISTORY
        >
OLD_DOCUMENTATION
        >
HYPOTHESIS
```

Therefore a repository state claiming PASS cannot override a running deployment that emits DENY.

Conversely, a GitHub file that looks correct cannot be called runtime proof until the exact deployment executes that file and emits the expected evidence.

## Forensic progress accounting

Progress percentages must be based on **proven capability**, not merely code presence.

For any room/engine/gate:

```text
CODE_WRITTEN_ONLY          = NOT_RUNTIME_PROVEN
RUNTIME_EXECUTED           = NOT_CONTENT_PROVEN
CONTENT_PROVEN             = NOT_CANDIDATE_PROVEN
CANDIDATE_PROVEN           = NOT_EXCEL_MATCH
EXCEL_MATCH_PROVEN         = NOT_CANONICAL_QUORUM
CANONICAL_QUORUM_PROVEN    = NOT_TRUTH_ADMISSION
```

A successor Bot must never inflate completion by counting locked-but-written code as operational capability.

## Security interaction

The communication path remains:

```text
CORRIDOR_KEY
    +
ROOM_KEY
    +
INNER_RELEASE (protected rooms only)
```

These security credentials authorize access to the room. They do not create forensic evidence and do not grant domain truth.

## Ads and non-truth DOM

Advertisements, trackers, forum links, promotional blocks, and unrelated DOM are explicitly non-truth content. Presence in the fetched HTML does not make such content eligible evidence.

A source adapter may ignore these regions only through an allowlisted official-result selector. It may not infer truth merely because numeric strings appear in an advertisement or unrelated panel.

## N104C.1 consequence

N104C.1 may prove only:

```text
exact source response
    -> transport classification
    -> official result panel identification
```

It may not admit numeric candidates automatically and may not advance Excel-vs-web, canonical quorum, or truth admission.

## Default-deny rule

```text
UNKNOWN = NOT PASS
MISSING EVIDENCE = DENY
RUNTIME/REPOSITORY MISMATCH = DENY
TRANSPORT HINT = NOT TRANSPORT PROVEN
```

## Successor instruction

Read this document before modifying any admission gate. If a proposed change causes one gate's PASS to imply another gate's PASS without fresh evidence, the change is architecturally invalid and must be rejected.
