# Evidence Lineage V1 — Forensic Admission Doctrine

## Purpose

This document defines how evidence travels from a real external source to Brain admission.
It is part of the foundation and must be read by every successor Bot before changing the admission chain.

## One lineage, distinct evidence classes

```text
REAL SOURCE OBSERVATION
        |
        v
SOURCE EVIDENCE
(raw bytes + source identity + observation metadata)
        |
        v
TRANSPORT / ORIGIN EVIDENCE
(request/response provenance, freshness, origin checks)
        |
        v
SEMANTIC EXTRACTION
(structured fields derived from source evidence)
        |
        v
QUANT DERIVED EVIDENCE
(indicators, calculations, models, scores, risk metrics)
        |
        v
BRAIN EVIDENCE ENVELOPE
(compact admission artifact referencing its parents)
        |
        v
FORENSIC GATE
(local gate evidence only)
        |
        v
NEXT STATE / PROMOTION
```

## Raw hash vs semantic hash

These hashes are not interchangeable.

- `raw_sha256`: integrity identity of the exact source payload/bytes.
- `semantic_sha256`: integrity identity of the normalized structured representation produced by an explicit parser.

A semantic hash MUST NOT replace the raw hash as proof of source truth.
A parser change can legitimately change the semantic representation while the raw source remains identical.

## Provenance rules

Every derived artifact must identify its parent evidence by stable IDs/hashes.
Derived artifacts cannot overwrite, replace, or impersonate source evidence.

Required conceptual fields:

```text
source_id
source_observation_id
raw_sha256
semantic_sha256 (only when semantic extraction exists)
parser_version (when semantic extraction exists)
collector_version (when acquisition exists)
observed_at
source_date
freshness_class
parent_evidence_ids
producer_component
```

## No masquerading

The following are explicitly forbidden:

```text
QUANT_RESULT -> treated as SOURCE_TRUTH
LOCAL_RECEIPT -> treated as INDEPENDENT_EXTERNAL_OBSERVATION
SEMANTIC_HASH -> treated as RAW_HASH
OLD_RUNTIME_LOG -> treated as FRESH_CURRENT_EVIDENCE
CHAT_ASSERTION -> treated as RUNTIME_EVIDENCE
```

## Brain admission

Brain may admit a state only when the gate's own evidence exists and is fresh enough for that gate.

```text
PASS_IS_LOCAL
PASS_IS_PREREQUISITE_ONLY
NO_PASS_INHERITANCE
UNKNOWN_IS_NOT_PASS
DEFAULT_DENY
OWN_GATE_EVIDENCE_REQUIRED
FRESH_EVIDENCE_REQUIRED_FOR_PROMOTION
```

Therefore:

```text
SOURCE_TRUTH_PASS
      !=
TRANSPORT_PASS
      !=
SEMANTIC_EXTRACTION_PASS
      !=
QUANT_DERIVATION_PASS
      !=
BRAIN_ADMISSION_PASS
      !=
PROMOTION_PASS
```

These are evidence classes/gates in one Forensic FSM, not separate forensic systems.

## External observation rule

An external observation must be independently observable through a safe control surface.
A service cannot self-attest an event as independent merely by writing a log that says it happened.

A human message in ChatGPT is an evidence carrier, not the state authority.

## Current safety posture

```text
action_space = 0
promotion = DENY
Room 02 = LOCKED
staircase = LOCKED
```

Safe engineering may improve lineage, schemas, parsers, tests, documentation, and deterministic validation.
Safe engineering may not manufacture the missing external observation or promote a blocked state.
