# Forensic Evidence Lineage

## Canonical purpose

This is a lineage contract for successor Bots. It defines how evidence moves from real observation to derived computation and finally to Brain admission.

The chain is one Forensic FSM, but evidence domains remain distinct.

```text
REAL SOURCE OBSERVATION
        |
        v
RAW EVIDENCE
        |
        +--> raw-byte hash
        |
        v
SEMANTIC EXTRACTION
        |
        +--> semantic hash
        |
        v
DERIVED / QUANT EVIDENCE
        |
        v
BRAIN ADMISSION ENVELOPE
        |
        v
FORENSIC GATE
```

## Non-negotiable distinctions

### Raw-byte hash

Answers:

> Are these exact bytes identical?

It does **not** prove semantic equivalence.

### Semantic hash

Answers:

> Is the canonical extracted meaning identical under the declared normalization rules?

It does **not** prove the original bytes were identical.

Therefore:

```text
RAW_HASH != SEMANTIC_HASH
```

They are complementary evidence, never interchangeable.

## Source truth cannot be replaced by derived truth

```text
SOURCE_TRUTH
    |
    +--> DERIVED_VALUE
    |
    +--> SCORE
    |
    +--> SENSOR
    |
    +--> QUANT_RESULT
```

A derived artifact may reference source evidence, but it may never become the source of truth merely because it is newer, faster, or more convenient.

Forbidden:

```text
Derived result -> overwrite source truth
Derived hash   -> masquerade as source hash
Local receipt  -> masquerade as external observation
```

## External observation versus local receipt

A local process can attest:

```text
I executed X.
```

It cannot thereby prove:

```text
An external system observed X.
```

An external Render/network observation requires an independently observable runtime receipt.

Therefore:

```text
LOCAL_RECEIPT != EXTERNAL_OBSERVATION
```

and:

```text
PUBLIC_WEB_AGREEMENT != RENDER_RUNTIME_RECEIPT
```

## Admission chain

The evidence lineage feeds separate gates:

```text
SOURCE DOMAIN
  source observation
       |
       v
network/source identity
       |
       v
result transport
       |
       v
official result panel
       |
       v
candidate
       |
       v
Excel-vs-Web match
       |
       v
canonical quorum
       |
       v
TRUTH ADMISSION

INFRASTRUCTURE DOMAIN
  DB existence
       |
       v
DB binding
       |
       v
secret resolution
       |
       v
TLS admission
       |
       v
network origin proof
       |
       v
DB round-trip
       |
       v
PROMOTION
```

These domains are related but cannot substitute for one another.

```text
TRUTH_ADMISSION != DATABASE_PROMOTION
```

A trustworthy source does not grant database authority, and a successfully bound database does not make source data truthful.

## Gate-state discipline

Every gate owns its own evidence.

```text
PASS_IS_LOCAL
PASS_IS_PREREQUISITE_ONLY
NO_PASS_INHERITANCE
UNKNOWN_IS_NOT_PASS
DEFAULT_DENY
OWN_GATE_EVIDENCE_REQUIRED
FRESH_EVIDENCE_REQUIRED_FOR_PROMOTION
```

Valid example:

```text
DB_EXISTENCE = PASS
DB_BINDING = BOUND_TLS
NETWORK_ORIGIN_PROOF = NOT_PROVEN
DB_ROUND_TRIP = NOT_PROVEN
PROMOTION = DENY
```

This is not contradictory. It is a partially admitted chain.

## Brain role

Brain is the governance control plane.

It may:

- classify evidence
- enforce gates
- reject invalid transitions
- preserve immutable history
- expose compact forensic envelopes
- coordinate admission

Brain may not:

- become the Data Engine
- become the Quant Engine
- manufacture source evidence
- convert a derived artifact into source truth
- self-attest an independent external observation

## Successor rule

Before changing any evidence/admission code, the next Bot must read:

1. `state/current_state.json`
2. `state/next_action.json`
3. `docs/FORENSIC_DATABASE_ADMISSION_CHAIN.md`
4. this document
5. the latest action log

The successor must preserve the existing state machine and append a new action receipt. It must never rewrite history to make a failed gate appear to have passed.
