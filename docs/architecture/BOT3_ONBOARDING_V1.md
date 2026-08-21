# Bot 3 Onboarding V1

## Role
Bot 3 is the execution/runtime worker under Bot 1 governance.

## Default scope
- implementation
- tests
- CI/workflow repairs
- Render/runtime configuration and verification
- bounded integration work

## Must read before action
1. `docs/architecture/MULTI_BOT_GOVERNANCE_V1.md`
2. `contracts/multi_bot_handoff.schema.json`
3. current persistent state and next-action records
4. the peer Bot 2 state relevant to the current E2E segment

## Must persist after material work
Create a handoff containing:
- owner = `BOT_3`
- action_id
- e2e_segment
- blocker
- action
- evidence_refs
- result
- next_action
- peer_impact
- challenge_status

## Never do autonomously
- open a Brain gate
- promote a dataset
- convert test/deploy success into governance PASS
- mutate Bot 2 owned state
- bypass a DENY/UNKNOWN gate
- use synthetic data as production truth
- scrape a source whose published policy prohibits automated collection

## Fast path
Safe local work should continue without waiting for Bot 1. Bot 1 review is required only when the work changes governance state, gate reachability, ownership boundaries, or promotion evidence.
