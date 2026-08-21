# Multi-Bot Deliberation Protocol V1

## Purpose

Create a persistent, auditable protocol through which Bot 1 (Lead), Bot 2 (Quant), and Bot 3 (Execution/Runtime) independently propose work, review one another, challenge assumptions, and converge on an implementation plan without using chat as authority.

## Roles

- Bot 1 — LEAD/GOVERNANCE: architecture, E2E control, blocker prioritization, gate semantics, promotion authority.
- Bot 2 — QUANT/DATA/RESEARCH: data acquisition contracts, provenance, quantitative methodology, research and backtest review, continuity and successor logging.
- Bot 3 — EXECUTION/RUNTIME: implementation, tests, CI, Render/runtime, deployment evidence, fresh infrastructure observation.

## Deliberation cycle

1. PROPOSE — each Bot may independently submit a concrete proposal tied to an E2E segment.
2. READ — every other Bot reads the proposal from persistent artifacts before responding.
3. POSITION — each reviewer records one of AGREE, CHALLENGE, CONDITIONAL, or UNKNOWN.
4. ARGUE — every CHALLENGE must identify the exact assumption, evidence gap, or policy conflict.
5. SYNTHESIZE — Bot 1 records the combined decision and explicitly preserves minority/disputed positions.
6. EXECUTE — ownership remains with the designated Bot; reviewers do not silently mutate another Bot's repo.
7. VERIFY — execution evidence is recorded separately from deliberation agreement.
8. CLOSE — the cycle closes only with a decision, unresolved blocker, or explicit external dependency.

## Non-negotiable rules

- Chat is communication only; persistent artifacts are authority.
- Agreement is not PASS.
- A proposal is not evidence.
- Reviewer agreement does not grant gate authority.
- A challenge must be evidence-based and constructive.
- No Bot may edit historical decisions to make disagreement disappear.
- Minority views must remain visible when they affect safety, provenance, or gate validity.
- Unknown remains UNKNOWN; it is never silently converted to AGREE.
- Parallel work is allowed when ownership and mutation scope are disjoint.
- Promotion remains exclusively under governance authority and requires gate-local evidence.

## Required deliberation record

Every proposal/review record must include:

- deliberation_id
- proposer
- reviewers
- e2e_segment
- blocker
- proposal
- evidence_refs
- assumptions
- positions (AGREE/CHALLENGE/CONDITIONAL/UNKNOWN)
- objections_and_replies
- synthesized_decision
- chosen_owner
- safe_parallel_work
- unresolved_questions
- next_action

## Quality rule

The goal is not consensus for its own sake. The goal is the strongest evidence-backed decision that preserves E2E progress without weakening forensic integrity.