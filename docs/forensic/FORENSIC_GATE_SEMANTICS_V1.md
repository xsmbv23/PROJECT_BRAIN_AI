# FORENSIC GATE SEMANTICS V1

## Status

**IMMUTABLE / ENFORCED / SINGLE CANONICAL FORENSIC FSM**

This document is an architectural rule for all future Brain/Quant bots.
There is **ONE FORENSIC FSM**, not multiple independent forensic systems.

## 1. Core law — PASS is local

A `PASS` belongs only to the gate that produced the evidence.

```text
GATE_A_PASS != GATE_B_PASS

PASS(GATE_A)
    !=
PASS(GATE_B)
```

A PASS is a **local prerequisite**, never inherited authorization. The next gate must execute its own evidence-producing check.

## 2. Database admission chain

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

- `DB_EXISTENCE=PASS`: database exists.
- `DB_BINDING=PASS`: service has an actual runtime binding.
- `DB_TLS_ADMISSION=PASS`: binding satisfies accepted TLS policy.
- `DB_ROUND_TRIP=PASS`: exact runtime performed real write/read/hash verification.
- `PROMOTION=PASS`: durable evidence promotion is permitted.

Formal non-implication:

```text
DB_EXISTENCE(PASS)  !=> DB_BINDING(PASS)
DB_BINDING(PASS)    !=> DB_ROUND_TRIP(PASS)
DB_ROUND_TRIP(PASS) !=> PROMOTION(PASS)
```

A later PASS cannot be inferred from an earlier PASS.

## 3. Source admission chain

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

A successful network request does not prove the result is official.
A parsed candidate does not prove truth.
A source match does not prove quorum.
A quorum does not erase the requirement for the next gate's own evidence.

## 4. Transport evidence chain

These are never equivalent:

```text
CODE_EXISTS
!= CODE_EXECUTED
!= LOCAL_CURL
!= EXACT_RUNTIME_EVIDENCE
```

Also:

```text
DEPLOYMENT_IDENTITY != RUNTIME_RECEIPT
```

A receipt is valid only when produced by the exact runtime being audited and cryptographically bound to its exact runtime identity and commit.

## 5. BLOCKED / PAUSED / ARMED is a valid forensic state

```text
BLOCKED / PAUSED / ARMED
```

is not a failure when the required auditable primitive is unavailable.

The system must **never manufacture work merely to convert BLOCKED into PASS**.

```text
NOT_AVAILABLE -> DENY
NOT_EXECUTED  -> DENY
UNKNOWN       -> DENY
MISSING       -> DENY
MISMATCH      -> DENY
```

This is a protection of forensic truth, not an operational defect.

## 6. Exact resume contract

For a blocked transport infrastructure task:

```text
BRAIN-N104C.1D-INFRA (BLOCKED)
             |
             v
Auditable exact-runtime execution primitive obtained
             |
             v
Execute original tools/transport_probe.py
             |
             v
Generate authentic exact-runtime TransportReceipt
             |
             v
Bind receipt to exact commit identity + SHA-256
             |
             v
RESUME TRANSPORT PROBE GATE
```

Local curl, proxy evidence, sidecar evidence, synthetic receipts, copied output, screenshots, or fabricated PASS states are forbidden substitutes and must remain `HARD_DENY`.

## 7. Security interaction model

Brain security remains:

```text
corridor key
    +
room key
    +
(optional protected-room inner release)
    +
local gate evidence
    =
permission to continue
```

Keys authorize access to a room; they do not manufacture forensic evidence.
Forensic evidence authorizes state transitions; it does not bypass room security.

```text
corridor_key != room_key
```

A protected room may additionally require an inner release event. Possessing a route and room key does not bypass the inner latch.

## 8. One-way state transition law

Each gate is independently evidence-producing. State transitions are monotonic with respect to evidence but **non-inheriting** across gates.

```text
PASS(A)
  |
  +-- only satisfies prerequisite A
  |
  v
RUN CHECK(B)
  |
  +-- PASS(B) only if B evidence exists
  |
  v
RUN CHECK(C)
```

No component may set another gate's state directly merely because its own state is PASS.

## 9. Historical immutability

A later PASS must never rewrite the historical meaning of an earlier DENY, BLOCKED, or NOT_PROVEN state.

Historical evidence is append-only.
Successor actions must create a new action record instead of mutating the historical record into a fictional success.

## 10. Brain role

```text
DATA   = source truth
ENGINE = calculation
SENSOR = observation
BRAIN  = governance / admission / forensic state
CHAT   = communication interface only
```

Brain is not the source-data owner and must not silently become the calculation engine.

## 11. Persistence / successor law

The repository and persistent evidence artifacts are the authority, not the chat window.

Every successor bot must:

1. read `state/current_state.json`;
2. read `state/next_action.json`;
3. read the relevant forensic contract;
4. identify the last closed action;
5. continue only from the recorded next action;
6. preserve all DENY/BLOCKED semantics;
7. write a successor action log before declaring completion;
8. never create a fake task merely to produce a PASS.

## 12. OOM law

Render Free 512 MB is a hard operational boundary.
Brain foundation work must preserve the conservative 320 MiB guard and avoid dataset residency in Brain runtime.

## 13. Forbidden shortcuts

- synthetic evidence
- fake PASS
- fabricated credential
- GitHub credential storage
- plaintext secret in logs
- TLS weakening to obtain PASS
- bulk dataset loading into Brain
- promotion from inference
- parallel FSM capable of canonical drift
- local/proxy/sidecar substitution for exact-runtime evidence
- rewriting historical action records

## 14. Current N104 consequence

`BRAIN-N104C.1D-INFRA` is legitimately `BLOCKED / PAUSED / ARMED` because the exact-runtime execution primitive is unavailable.

Therefore:

```text
TRANSPORT_RECEIPT = NOT_PROVEN
TRANSPORT_GATE    = HARD_DENY
CANONICAL_TRUTH   = LOCKED / DENY
LAYER_1           = LOCKED
STAIRCASE         = LOCKED
```

The only legal resume condition is the exact resume contract in Section 6.

## 15. Canonical interpretation

When evidence conflicts with expectation:

```text
EVIDENCE > EXPECTATION
UNKNOWN  > PASS
DENY     > UNSUPPORTED ASSUMPTION
```

This document is not optional documentation. It is the semantic contract for successor bots.
