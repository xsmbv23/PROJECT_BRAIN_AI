# Forensic Admission FSM V1

## Purpose

This document is a permanent architectural contract for successor Bots. It resolves a critical ambiguity: the system has **ONE Forensic FSM**, not multiple independent Forensic state machines.

Every gate below is one state transition/evidence boundary inside the same FSM.

## Core invariant

> PASS is local. PASS is a prerequisite, never an inherited permission.

A gate may only change its own state when its own evidence is present and fresh enough for the gate's purpose.

A previous gate PASS does **not** set the next gate to PASS.

If a gate is FAIL or UNKNOWN, downstream gates are **UNREACHED**, not PASS.

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

### Gate meanings

| Gate | Evidence owned by gate | Does PASS unlock next evaluation? | Does PASS grant next PASS? |
|---|---|---:|---:|
| DB_EXISTENCE | Resource exists and is identifiable | YES | NO |
| DB_BINDING | Service has the required runtime binding | YES | NO |
| SECRET_RESOLUTION | Binding resolves from an approved secret boundary | YES | NO |
| DB_TLS_ADMISSION | PostgreSQL transport satisfies explicit TLS policy | YES | NO |
| NETWORK_ORIGIN_PROOF | Connection originates from the admitted runtime boundary | YES | NO |
| DB_ROUND_TRIP | Real compact write -> read -> SHA-256 match | YES | NO |
| PROMOTION | Governance decision based on all required evidence | N/A | N/A |

## Example

This sequence is valid:

```text
DB_EXISTS = PASS
DB_BINDING = NOT_BOUND
SECRET_RESOLUTION = UNREACHED
DB_TLS_ADMISSION = UNREACHED
NETWORK_ORIGIN_PROOF = UNREACHED
DB_ROUND_TRIP = UNREACHED
PROMOTION = DENY
```

This sequence is **invalid**:

```text
DB_EXISTS = PASS
DB_BINDING = NOT_BOUND
DB_TLS_ADMISSION = PASS       # INVALID: no own evidence and gate unreachable
DB_ROUND_TRIP = PASS          # INVALID
PROMOTION = PASS               # INVALID
```

## Why existence and authorization are different

`DB_EXISTENCE` answers:

> Does the database resource exist?

`DB_BINDING` answers:

> Has this service been given the runtime key/binding needed to attempt access?

`DB_TLS_ADMISSION` answers:

> Does that binding produce an explicitly accepted TLS transport?

`DB_ROUND_TRIP` answers:

> Did the exact runtime actually perform the real write/read/hash verification?

These are different evidence classes and must never be collapsed into one `DATABASE_PASS` flag.

## Evidence lineage

The FSM distinguishes:

```text
RAW BYTE IDENTITY
        !=
SEMANTIC MEANING
```

Raw byte hashes prove byte identity.
Semantic hashes prove canonicalized meaning.
Neither may silently substitute for the other.

Canonical fields are authoritative. Legacy aliases are denied unless an explicit historical fixture marks them as allowed.

## Source admission chain

The same ONE FSM principle applies to source acquisition:

```text
SOURCE_INDEPENDENCE
        |
        v
NETWORK_ORIGIN_PROOF
        |
        v
RESULT_TRANSPORT
        |
        v
OFFICIAL_RESULT_PANEL
        |
        v
CANDIDATE
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

Advertising, navigation elements, banners, unrelated links, and page chrome are **non-truth content**. They cannot satisfy result evidence.

## Action receipts

An action receipt is evidence that an action occurred. It is **not** itself permission to perform the action.

Required conceptual sequence:

```text
ACTION INTENT
   |
   v
AUTHORIZATION / ADMISSION
   |
   v
ACTION EXECUTION
   |
   v
ACTION RECEIPT
   |
   v
INDEPENDENT OBSERVATION
```

A Bot must never manufacture an action receipt from an intended command, a repository commit, a deployment request, or a human statement that the action happened.

## Human/chat boundary

The chat window is only a communication interface.

Human messages may carry evidence, instructions, or context, but they do not mutate Forensic state by assertion alone.

Persistent state authority remains the repository/evidence system and independently observable runtime evidence.

## Promotion rule

Promotion requires every required upstream gate to have valid evidence. No downstream PASS may be inherited.

If the external evidence surface cannot independently observe a required gate:

```text
UNKNOWN != PASS
PROMOTION = DENY
```

## OOM rule

The FSM must remain safe on Render Free:

```text
HARD BOUNDARY = 512 MB
CONSERVATIVE GUARD = 320 MiB
```

Brain must not load large datasets into memory merely to prove a gate. Evidence should remain compact and immutable.

## Successor instruction

A successor Bot must read this file before changing admission logic. If a proposed change introduces:

- inherited PASS;
- hidden state transition;
- evidence generated without execution;
- credential exposure;
- source-truth overwrite by derived data;
- bulk dataset loading in Brain;
- or a second competing Forensic FSM;

then the change is architecturally invalid and must be DENIED.
