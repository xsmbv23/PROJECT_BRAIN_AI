# BOT COORDINATION BUS V1

## Purpose
Shared persistent coordination layer for BOT1_LEAD, BOT2_QUANT, and BOT3_EXECUTION.

This bus is a coordination mechanism only. It is not a forensic gate, not an evidence source, and not an authority to promote state.

## Authority separation
- `coordination/` records proposals, acknowledgements, challenges, deliberations, and next-action handoffs.
- `state/current_state.json` remains canonical governance state.
- Evidence receipts and artifacts remain the authority for factual claims.
- Local gate evaluators alone determine PASS/DENY/HOLD/ESCALATE.

## Required read order for every Bot cycle
1. `state/current_state.json`
2. `state/next_action.json`
3. latest action record relevant to the Bot
4. latest coordination cycle / inbox message
5. `contracts/multi_bot_deliberation.schema.json`
6. evidence receipts needed for the claim
7. code/runtime only after the above

## Shared-cycle files
- `coordination/current_cycle.json` — current deliberation cycle and requested actions
- `coordination/inbox/BOT1_LEAD.jsonl` — messages addressed to Bot 1
- `coordination/inbox/BOT2_QUANT.jsonl` — messages addressed to Bot 2
- `coordination/inbox/BOT3_EXECUTION.jsonl` — messages addressed to Bot 3
- `coordination/deliberations/` — immutable deliberation records
- `coordination/acks/` — append-only acknowledgements
- `coordination/recommendations/` — recommendations only; never gate outcomes

## Message semantics
Each message must carry:
- `message_id`
- `cycle_id`
- `from_bot`
- `to_bots`
- `created_at`
- `content_sha256`
- `message_type` (`PROPOSAL`, `CHALLENGE`, `REPLY`, `ACK`, `EVIDENCE_REQUEST`, `RECOMMENDATION`, `NEXT_ACTION`)
- `epistemic_status` (`REPORTED`, `OBSERVED`, `VERIFIED`, `UNKNOWN`)
- `e2e_segment`
- `blocker`

## Human relay rule
A message manually relayed by the user is a transport event, not evidence. The Bot receiving it must:
1. ACK receipt.
2. Preserve the exact relayed content hash.
3. Independently verify claims where possible.
4. Convert substantive disagreement/agreement into a deliberation record.
5. Write its own next-action recommendation to the bus.

The Bot must never treat "the user said another Bot said X" as proof that X is true.

## Parallel-write rule
Bots may append to their own inbox and coordination records. They must not concurrently overwrite canonical `state/current_state.json` or `state/next_action.json` without an explicit reconciliation record.

## End-to-end rule
Every cycle must connect:
`CURRENT_STATE -> BLOCKER -> DELIBERATION -> SAFE PARALLEL WORK -> EVIDENCE -> LOCAL GATE -> NEXT ACTION`.

## Successor rule
Future Bots inherit rationale and history from the bus. They do not inherit truth, PASS, promotion, or gate outcome from deliberation consensus.
