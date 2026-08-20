# FORENSIC TERMINOLOGY HARDENING — 2026-08-20

## Purpose

Preserve the canonical interpretation for successor AI agents.

## Canonical model

```text
ONE FORENSIC FSM
```

Database admission is not a second FSM. Its gates are one ordered chain inside the single FSM.

```text
DB_EXISTENCE
→ DB_BINDING
→ DB_TLS_ADMITTED
→ DB_ROUND_TRIP_PROVEN
→ PROMOTION_AUTHORIZED
```

## Mandatory separation

```text
DOCTRINE != EVIDENCE != STATE
```

- Doctrine defines rules.
- Evidence proves a specific gate.
- State projects valid current evidence through legal transitions.

Never infer state from doctrine.
Never use historical state as current evidence.
Never use one gate's PASS as another gate's evidence.

## Gate-local PASS

```text
PASS(A) = evidence for A only
PASS(A) ≠ PASS(B)
PASS(A) ≠ evidence(B)
```

A PASS can only make the next gate eligible for evaluation.

## Epistemic safety

```text
UNKNOWN != PASS
NO RECEIPT -> NOT_PROVEN -> HARD_DENY
```

`BLOCKED_BY_CAPABILITY_BOUNDARY` is a legitimate forensic condition. It is not a progress failure and must not be converted into PASS merely because source code exists.

## Exact-runtime rule

Source inspection proves implementation properties only.

It does not prove exact-current runtime execution.

Forbidden substitutions include:

- local execution for Render execution;
- proxy execution;
- replayed receipts;
- fabricated receipts;
- HTTP acknowledgement as forensic PASS;
- HTML hashing as TransportReceipt proof;
- source modification to force a probe result.

## Current N109 boundary

Canonical `state/next_action.json` remains the authority and names `BRAIN-N109` as the sole admitted action.

N109 requires exact-current execution of the unchanged N108 bridge and independent cryptographic runtime binding of the resulting TransportReceipt.

The available Render control surface currently exposes service configuration, deployment, logs, metrics, and environment-variable mutation, but does not expose a direct exact-live HTTP invocation primitive to this agent. Therefore this action boundary must remain external rather than being simulated.

## Promotion safety

Until N109 exact-live evidence exists:

```text
ROOM_01       = LOCKED
LAYER_1       = LOCKED
STAIRCASE     = LOCKED
CANONICAL     = DENY
```

This is a successful Forensic outcome because the system refuses an unsupported transition.

## Successor instruction

Read this file before interpreting any PASS/NOT_PROVEN state. If a later AI cannot locate gate-specific current evidence, it must preserve the existing state and emit `NOT_PROVEN`, not invent a transition.
