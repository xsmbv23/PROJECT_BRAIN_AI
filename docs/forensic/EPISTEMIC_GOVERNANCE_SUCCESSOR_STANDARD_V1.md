# EPISTEMIC GOVERNANCE SUCCESSOR STANDARD V1

## Status

NORMATIVE. This document is part of the Project_Brain_AI foundation custody chain.

## Supreme rule

Every statement originating outside the independent evidence/verifier path is a **HYPOTHESIS** until an admissible evidence receipt proves the exact claim.

This includes, without limitation:

- external AI conclusions;
- ChatGPT/DeepSeek/GPT or any other model statements;
- human conversation claims;
- old documentation;
- copied logs;
- screenshots or HTML claims;
- source-code existence claims;
- historical PASS states;
- tool output that does not itself constitute an admissible receipt.

An external statement may describe what should be checked. It cannot by itself mutate canonical state.

## Chain of truth

```text
EXTERNAL STATEMENT
        |
        v
     HYPOTHESIS
        |
        | independent verifier
        v
 PROOF DETERMINATION
        |
        | admissibility rules satisfied
        v
 ADMISSIBLE EVIDENCE RECEIPT
        |
        | exact claim + exact runtime/source identity bound
        v
 CANONICAL FSM MUTATION
```

The implication is strictly one-way:

```text
HYPOTHESIS -> may request verification
HYPOTHESIS -/-> PASS
HYPOTHESIS -/-> STATE MUTATION
```

## Evidence receipt requirement

No admissible receipt means:

```text
NOT_PROVEN
DENY
NO_STATE_MUTATION
```

The receipt must be independently recoverable from the authoritative evidence surface and cryptographically checkable. A hash printed by a model or copied into a conversation is not a receipt.

## Gate non-inheritance

The project has **ONE Forensic FSM**, not multiple competing Forensic state machines.

Each gate owns a local evidence condition.

```text
PASS(G_i)
    !=
PASS(G_i+1)
```

A PASS only establishes that the exact gate was proven. It merely authorizes evaluation of the next gate.

## Database example

```text
DB_EXISTENCE
    -> DB_BINDING
    -> DB_TLS_ADMISSION
    -> DB_ROUND_TRIP
    -> PROMOTION
```

Therefore:

```text
DB_EXISTS = PASS
```

means only that the database resource exists.

It does **not** mean:

```text
SERVICE_BOUND = PASS
TLS_ADMITTED = PASS
ROUND_TRIP = PASS
PROMOTION = PASS
```

Likewise:

```text
DB_ROUND_TRIP = PASS
```

is local evidence for that gate and does not unlock unrelated rooms, Layer 1, or the staircase.

## Source example

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

A transport PASS cannot be inherited by official-panel validation. An official-panel PASS cannot be inherited by quorum. Quorum cannot be inferred from one source's confidence.

## Canonical state discipline

`state/current_state.json` is the mutable projection of exact current admissible evidence.

`docs/action_log/` is immutable append-only custody history.

A successor Bot MUST:

1. read the successor read-order from `current_state.json`;
2. read the current `next_action.json`;
3. read the relevant normative standards;
4. treat all conversation/model claims as hypotheses;
5. locate the gate-specific admissible receipt;
6. independently verify the receipt;
7. mutate canonical state only after admissibility passes;
8. append the action record before claiming completion.

## Current N109 boundary

The current state explicitly records `N109` as the sole admitted next action and states that exact-live runtime execution remains externally blocked. A successor must not convert any local/source PASS into N109 completion.

The exact current state is authoritative over prose.

## Forbidden state laundering

The following are never acceptable substitutions for an admissible receipt:

```text
"I ran it"                 -> NO
"The deploy is live"       -> NO
"HTTP returned 202"        -> NO
"Source code is correct"   -> NO
"Local test passed"        -> NO
"Old receipt says PASS"    -> NO
"Another AI confirmed it"  -> NO
"The database exists"      -> NO
```

Only the exact evidence chain may mutate the FSM.

## Succession oath

> Preserve the one FSM. Preserve gate ownership. Preserve non-inheritance. Preserve append-only history. Never upgrade state from prose. Never substitute a proxy for exact evidence. When evidence is missing, stop at DENY and record why.
