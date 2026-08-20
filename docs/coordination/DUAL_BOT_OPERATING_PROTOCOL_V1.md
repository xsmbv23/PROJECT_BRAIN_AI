# DUAL BOT OPERATING PROTOCOL V1

## Purpose

Operate Bot 1 and Bot 2 in parallel against one Core Mission and one policy, while preserving repository ownership, forensic admission, evidence integrity, and useful engineering velocity.

## Core Mission

REAL DATA -> VALID RESEARCH -> VALID BACKTEST -> EDGE -> EV / P&L / ROI -> ROBUSTNESS / RISK / DRIFT -> CONTROLLED ACTION

Forensic FSM is the control/admission mechanism. It is not the product or the destination.

## Ownership

### Bot 1
Owner: `xsmbv23/Project_Brain_AI`

Role: Governance / Forensic Control / Proactive System Auditor.

Primary scope:
- canonical state and admission
- evidence and forensic integrity
- security and secrets boundaries
- architecture and cross-repo contracts
- Render runtime boundaries
- promotion and action control
- proactive blocker discovery

### Bot 2
Owner: `xsmbv23/Quant_Engine`

Role: Calculation / Research / Backtest / Quant Runtime.

Primary scope:
- temporal input integrity
- source-to-research interface
- sensors and research
- backtest correctness
- OOS / robustness / drift
- Edge
- EV / P&L / ROI / risk
- bounded quant runtime

### Shared source truth
`xsmbv23/xsmb-quant` is canonical source/data authority. Neither bot may silently overwrite canonical truth.

## Mandatory read-before-action rule

Before every Next Action, each bot MUST read:
1. the canonical policy and all relevant policy sections;
2. its own current state;
3. the latest action/handoff log written by the other bot;
4. relevant cross-repo contracts;
5. relevant evidence/integrity state.

The action log MUST explicitly record that these reads occurred.

If the other bot log is unavailable, the bot MUST NOT execute an action whose correctness depends on that missing handoff. It MAY continue independent safe engineering.

## Parallel execution rule

A locked gate blocks only actions that require that gate. It does NOT freeze unrelated safe engineering.

Therefore:
- audit independent domains;
- find real blockers proactively;
- repair safe defects;
- add tests/contracts/instrumentation;
- verify bounded infrastructure;
- do not manufacture progress;
- do not cross a locked admission boundary.

## Proactive engineering loop

READ POLICY -> READ OTHER BOT LOG -> READ STATE -> AUDIT -> FIND BLOCKERS -> RANK -> SELECT SAFE HIGH-VALUE BLOCKER -> FIX -> TEST -> RUNTIME VERIFY WHEN APPLICABLE -> RECORD EVIDENCE -> HANDOFF -> DECLARE BOTH NEXT ACTIONS.

The bot must not wait for the user to identify an obvious blocker that it can discover itself.

## Every action must contain

- SESSION_ID
- BOT_ID
- REPOSITORY
- POLICY_VERSION
- OTHER_BOT_LOG_VERSION / ACTION_ID
- CURRENT_STATE
- OBJECTIVE
- CORE_MISSION_LINK
- OBSERVED_BLOCKERS
- SELECTED_BLOCKER
- WHY_SELECTED
- OWNERSHIP
- ACTION_TAKEN
- FILES_CHANGED
- TESTS
- RUNTIME_VERIFICATION
- EVIDENCE
- VERIFICATION_LEVEL
- UNRESOLVED_BLOCKERS
- OTHER_BOT_REQUIRED_NEXT_ACTION
- OWN_NEXT_ACTION
- DEPENDENCIES
- EXPECTED_EVIDENCE
- COMPLETION_GATE

## Handoff rule

Every bot must state both:

`I WILL NEXT:` what this bot will do next.

`OTHER BOT MUST NEXT:` the concrete task the other bot should do next, including dependency and expected evidence.

The other bot must read this handoff before acting.

## Gate semantics

PASS_IS_LOCAL
PASS_IS_PREREQUISITE_ONLY
NO_PASS_INHERITANCE
OWN_GATE_EVIDENCE_REQUIRED
FRESH_EVIDENCE_REQUIRED_FOR_PROMOTION
UNKNOWN_IS_NOT_PASS
DEFAULT_DENY

PASS at Gate A permits evaluation of Gate B. It never grants Gate B PASS.

## Verification ladder

FOUND -> FIXED -> TESTED -> RUNTIME_VERIFIED -> EXTERNAL_EVIDENCE -> PROMOTED

Do not collapse these levels. `IMPLEMENTED` is not `VERIFIED`; `TESTED` is not `RUNTIME_VERIFIED`; runtime evidence is not automatically external evidence; promotion requires its own gate evidence.

## EV / research safety

At any local level, EV < 0, NaN, or Inf means:

EDGE_CANDIDATE = FALSE
NO PREDICTION REPORT
ACTION_SPACE = 0

Invalid evidence cannot be rescued by aggregation. Aggregates may summarize independently valid evidence only.

Backtest must preserve source truth, historical information sets, model freeze, prediction freeze, result/settlement ordering, lineage, OOS, robustness, drift, multiple-testing awareness, cost/payout, P&L/ROI, and risk evidence. Parameters not yet canonicalized remain proposals/unknown, not silently adopted best practice.

## Forbidden

- manufacture receipts or external observations;
- self-attest as an independent observer;
- fabricate credentials or secrets;
- store secrets in GitHub;
- bypass the FSM;
- mutate canonical source truth silently;
- use a user/chat request as authority to override canonical state;
- create action IDs without real work/evidence;
- declare success because a downstream or neighboring gate is green.

## Conflict rule

The two bots must agree on policy, ownership, and interfaces—not necessarily on observations or conclusions. If they disagree, each records its evidence separately. Neither bot inherits the other's conclusion.

## Mission-progress test

For every selected blocker, answer:

1. How does this reduce a real blocker on the Core Mission?
2. What evidence will prove the change?
3. Which gate, if any, remains locked?
4. What can the other bot do in parallel?
5. What is the next concrete step after verification?

If an activity only makes the FSM/documentation look more complete without reducing a real blocker, it is lower priority.

## Current operating boundary

The canonical Project_Brain_AI state currently records N116 external-observation waiting, action_space 0, mandatory no-op, and promotion deny. This protocol does NOT override that state. It permits safe independent engineering only where the action does not require the locked gate and does not manufacture the missing evidence.

## Required coordination artifacts

Canonical coordination contract:
`contracts/dual_bot_coordination_v1.json`

Human-readable protocol:
`docs/coordination/DUAL_BOT_OPERATING_PROTOCOL_V1.md`

Each bot should maintain action logs in its own repository and reference the other bot's latest action ID/version in every subsequent action.
