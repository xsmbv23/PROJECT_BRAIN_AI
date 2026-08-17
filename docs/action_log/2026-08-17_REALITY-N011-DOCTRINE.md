# REALITY-N011 — Successor Doctrine Lock

## Why this record exists

The system is currently armed for an external runtime event. This record preserves the rule that a waiting forensic state is valid and must not be converted into artificial internal activity.

## Exact state

```text
IMPLEMENTATION = DONE
CONDITION      = FIXED
TRIGGER        = EXTERNAL
STATE          = WAITING_FOR_EXTERNAL_EVENT
PROMOTION      = DENY
```

## Non-negotiable law

```text
PROGRESS != ACTIVITY
PROGRESS = NEW EVIDENCE
```

A commit is not automatically progress. A refactor is not automatically progress. A passing local test is not automatically progress toward a real-world experiment. Progress exists only when a named uncertainty is reduced by admissible evidence or when the declared external event is captured and consumed by the FSM.

## Current experiment boundary

N011 is a GitHub Actions transport probe. It is independent from truth, parsing, normalization, admission, and promotion.

The workflow has been implemented but must not be treated as executed until a real workflow-run observation exists.

The current state therefore remains:

```text
N011_IMPLEMENTATION = DONE
N011_EXECUTION      = UNREACHED_UNTIL_WORKFLOW_RUN
N011_RUNTIME        = github_actions
N011_PARSE          = FORBIDDEN
N011_DOMAIN_TRUTH   = UNREACHED
N011_PROMOTION      = DENY
```

## Valid next events

### A. Workflow run occurs

Capture the actual receipt and then classify it. Do not modify the experiment condition before comparison.

### B. Workflow run does not occur

Keep the FSM unchanged.

Do not manufacture a substitute receipt.

## Successor instructions

A future Bot reading this record must not interpret the absence of a workflow run as a coding defect. It is an external-event wait state.

Do not add a second FSM to handle the wait. Do not create a synthetic GitHub Actions receipt. Do not turn readiness into execution authority.

## Forensic principle

> A correct Forensic system must be able to remain unchanged while waiting for evidence.

This record is durable memory for successor Bots and does not itself change experiment authority.
