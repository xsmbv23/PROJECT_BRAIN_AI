# BRAIN-N140 — Peer QUANT-N010 Temporal Evidence Block

## Trigger

Mandatory peer-first review of Quant_Engine before taking the next parallel action.

## Observed peer state

Quant_Engine remains at QUANT-N010. Its research_dataset_admission.py derives start/end, actual_days, contiguity, and missing dates from DayRecord values, and computes required_days as train + test + 1. This is implementation evidence only; it is not an independent admission receipt.

## Cross-repo contract comparison

Project_Brain_AI research admission consumer requires:

- temporal_evidence_reference
- date_manifest_sha256
- source provenance reference
- canonical input reference
- date span and counts
- temporal policy

Quant_Engine's current ResearchDatasetAdmission object does NOT yet carry temporal_evidence_reference or date_manifest_sha256.

## Decision

This is a real cross-repo contract blocker. Brain MUST NOT weaken its consumer contract to accept the missing evidence. Quant Engine must emit independently traceable temporal evidence before Brain can consume a research-admission receipt.

Required evidence shape:

DayRecord.date
→ canonical ordered date manifest
→ deterministic serialization
→ SHA-256(date manifest)
→ temporal evidence artifact/reference
→ research admission receipt

The manifest hash is a temporal/date-manifest integrity identifier, NOT a raw-source byte hash and NOT source truth.

## Gate semantics

This does NOT open Brain's external gate and does NOT promote data.

BRAIN-N125_WAIT_EXTERNAL remains unchanged.
ACTION_SPACE remains 0.
PROMOTION remains DENY.

## Peer next action

Quant Engine: extend ResearchDatasetAdmission/evidence emission so the research admission receipt contains the required temporal evidence reference and date manifest SHA-256, with deterministic manifest semantics and tests.

## Brain next action

Brain: keep the consumer strict, add/maintain regression tests for missing temporal evidence, and on receipt arrival independently recompute/validate the manifest binding before admitting research eligibility.

## Status

IMPLEMENTED: NO (peer evidence requirement identified)
TESTED: UNKNOWN
RUNTIME_VERIFIED: UNKNOWN
PROMOTED: NO
