# BRAIN-N111 — Epistemic Governance Rule Preservation

## Purpose

Preserve the rule that prevents successor AI agents from laundering hypotheses into canonical state.

## Normative rule

Every external statement is HYPOTHESIS until independently verified and backed by an admissible evidence receipt.

```text
External statement
      -> HYPOTHESIS
      -> independent verifier
      -> proof determination
      -> admissible receipt
      -> canonical FSM mutation
```

No receipt means no mutation.

## Single FSM rule

There is ONE Forensic FSM. Database admission gates are sequential local gates, not independent state machines.

```text
DB_EXISTENCE
 -> DB_BINDING
 -> DB_TLS_ADMISSION
 -> DB_ROUND_TRIP
 -> PROMOTION
```

`PASS(G_i)` is only a prerequisite to evaluate `G_i+1`; it is never inherited.

## Source chain

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

## Canonical custody

- `state/current_state.json` = mutable projection of exact admissible current evidence.
- `state/next_action.json` = single successor action authority.
- `docs/action_log/` = append-only historical custody.
- Model/chat prose = hypothesis only.

## Important anti-drift rule

A historical PASS, source PASS, local PASS, HTTP acknowledgement, database existence, screenshot, copied receipt, or another AI's conclusion cannot replace exact-current evidence.

## Current handoff

Canonical state currently reports:

```text
last_action = BRAIN-N110
next_action = BRAIN-N109
N109 = READY_BUT_EXTERNAL_CAPABILITY_BLOCKED
current deployment = LIVE_BUT_UNVERIFIED
source promotion = DENY
staircase = LOCKED
```

This action deliberately does **not** mutate those canonical values because this document itself is not an admissible runtime evidence receipt. It is normative governance documentation only.

## Next action remains

`BRAIN-N109`.

The successor must solve the exact-live execution/evidence boundary without proxies, local substitution, source modification, receipt fabrication, or state laundering.
