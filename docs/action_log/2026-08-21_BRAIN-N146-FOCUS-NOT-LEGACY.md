# BRAIN-N146 — Focus policy: active engineering over bot legacy handoff

## Purpose

Peer handoff / continuity is a coordination mechanism, not the Core Mission.

Do not over-produce “future bot” / “transmission” artifacts when the active blocker can be investigated, implemented, tested, or independently verified now.

## Priority

1. Core Mission / forensic integrity
2. Active gate blocker and highest-value safe engineering
3. Evidence generation and verification
4. Cross-repo synchronization required for the active dependency
5. State/action log continuity
6. Legacy/future-bot handoff only when it materially prevents loss of required context

## Anti-pattern

`next action -> write another bot-handoff document -> write another bot-handoff document`

This is not progress if the active system blocker remains untouched.

## Required behavior

At each next action, the Bot must first ask:

- What is the highest-value unresolved blocker?
- Can it be safely fixed within the repo owned by this Bot?
- What evidence can be produced now?
- Is peer synchronization actually required for this action?

Only if the answer is yes should an additional peer handoff artifact be created.

## Current peer coordination

Bot 2 owns Quant_Engine and is executing QUANT-N010. Bot 1 owns Project_Brain_AI. Bot 1 must continue Brain-side hardening without waiting for or repeatedly generating legacy handoff documents. Bot 2 remains responsible for its own N010 implementation/evidence.

## Gate discipline

This policy does not relax any gate. UNKNOWN remains UNKNOWN. PASS remains local. Promotion remains DENY until its own evidence exists.
