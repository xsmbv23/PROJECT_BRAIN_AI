# BOT SUCCESSION — FORENSIC BOUNDARY V1

## Purpose

This document defines what a successor AI must inherit from Project Brain AI and what it must NOT mistake for permanent doctrine.

## Core rule

**Transmit verification principles, not the assumptions of a particular implementation version.**

Forensic exists to protect Quant from self-deception. It must not become the product itself or prevent Quant from searching for real edge.

## One Forensic FSM

There is one Forensic state machine. Individual gates are nodes/gates inside that FSM, not independent Forensic systems.

A gate PASS is local to that gate. It is a prerequisite for downstream evaluation, never an inherited PASS.

```text
PASS_IS_LOCAL
PASS_IS_PREREQUISITE_ONLY
NO_PASS_INHERITANCE
UNKNOWN_IS_NOT_PASS
DEFAULT_DENY
OWN_GATE_EVIDENCE_REQUIRED
NO_RECEIPT_NOT_PROVEN
```

## Epistemic separation

The successor must keep these three categories separate:

```text
DOCTRINE  !=  EVIDENCE  !=  STATE
```

- **DOCTRINE** = immutable principles and contracts.
- **EVIDENCE** = observations/receipts produced by an actual execution or verified artifact.
- **STATE** = mutable projection derived only from exact evidence.
- **HISTORY** = immutable append-only record of what happened; history is not current truth.

State must never be inferred from doctrine. Old evidence must not silently become current evidence. Historical implementation details must not be promoted to invariants.

## What is inherited as DNA

Successor AIs MUST inherit:

- provenance and data lineage;
- reproducibility/replayability requirements;
- auditability and append-only action history;
- gate-local evidence ownership;
- no PASS inheritance;
- UNKNOWN != PASS;
- default deny for unproven claims;
- explicit promotion gates;
- immutability rules;
- resource/OOM safety constraints;
- separation of Brain governance from Data truth and Quant calculation;
- separation of Build Plane and Runtime Plane;
- the rule that Forensic protects Quant rather than replacing Quant.

## What is NOT immutable doctrine

The following are historical or versioned implementation artifacts and MUST NOT be treated as eternal assumptions:

- action numbers (Nxxx);
- specific source websites or their current behavior;
- parser implementation details;
- exact file names unless defined by a current contract;
- current deployment IDs/commits;
- temporary Render limitations;
- current database binding mechanism;
- current model/sensor/feature implementation;
- old hypotheses or rejected approaches.

These belong in HISTORY, KNOWLEDGE, or VERSIONED CONTRACTS as appropriate.

## Quant remains the objective

The system objective remains:

```text
DATA TRUST
   -> CAUSALITY
   -> EDGE
   -> EV > 0
   -> ROBUST OOS
   -> EXECUTION
   -> POSITIVE EXPECTED VALUE
```

Forensic is the brake/guardrail. Quant is the engine.

A larger number of gates is not automatically safer. Every gate must protect a material failure mode and must have its own evidence semantics.

## Succession rule

A successor AI MUST read, in order:

1. immutable doctrine;
2. current state;
3. gate-specific contracts;
4. exact current evidence;
5. immutable action history;
6. hypotheses/legacy documentation.

The successor MUST NOT reconstruct current architecture merely by reading old action logs.

## Decision test

For every proposed doctrine item, ask:

> If a completely new AI reads this five years later, will this rule prevent a serious Quant/Forensic failure?

If yes: doctrine.
If it describes what happened in one version: history.
If it is an empirical observation: evidence.
If it is a current projection: state.
If it is a tentative idea: hypothesis.

## Final invariant

**Forensic must prevent the system from fooling itself; it must never become the reason the system is unable to discover or exploit a real edge.**
