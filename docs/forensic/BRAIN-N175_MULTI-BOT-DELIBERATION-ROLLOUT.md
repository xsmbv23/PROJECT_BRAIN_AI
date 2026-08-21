# BRAIN-N175 — Multi-Bot Deliberation Rollout

## Decision

Adopt `MULTI_BOT_DELIBERATION_V1` as the persistent communication/review protocol for Bot 1, Bot 2, and Bot 3.

## Why

The three-Bot topology is intentionally heterogeneous:

- Bot 1: system-wide governance, architecture, forensic integrity, E2E control.
- Bot 2: quantitative/data continuity, provenance, research/backtest, successor/logging discipline.
- Bot 3: independent execution/runtime perspective, implementation, deployment, and fresh-observation bias.

The purpose of deliberation is to exploit those differences rather than force artificial consensus.

## Required cycle

PROPOSE → READ → POSITION → CHALLENGE/REPLY → SYNTHESIZE → EXECUTE → VERIFY → CLOSE

## Position semantics

- AGREE: evidence/policy supports the proposal.
- CHALLENGE: identify a concrete assumption, missing evidence, or policy conflict.
- CONDITIONAL: support only if named conditions are satisfied.
- UNKNOWN: insufficient evidence to agree or challenge.

## Authority

Deliberation never grants PASS or promotion. Gate-local evidence and governance rules remain authoritative.

## Current gate state

This rollout does not change S1/S2/S3+ state. Existing promotion DENY and locked downstream gates remain unchanged.

## Next

Future substantive actions should carry a deliberation record when they affect architecture, E2E sequencing, gate semantics, forensic integrity, or cross-Bot ownership.