# Parallel Bot Coordination — Forensic Foundation

## Purpose

Project_Brain_AI may be worked on by multiple AI agents in parallel. Parallel work does **not** create parallel truth authorities and does **not** permit one agent to inherit another agent's PASS.

## Authority

`state/current_state.json` and `state/next_action.json` remain the successor hand-off authority. Historical action logs are immutable history. The active Forensic FSM remains singular.

## Parallelism rule

Safe parallel engineering is allowed only when it cannot mutate or bypass a locked admission gate. Examples:

- documentation and successor packaging;
- registry/collector drift repair in the Quant data plane;
- tests and static verification;
- memory/OOM instrumentation;
- non-secret contract validation.

Unsafe parallel actions are forbidden:

- fabricating an external observation;
- turning public-web agreement into a Render runtime receipt;
- promoting evidence because another agent says PASS;
- unlocking Room 02 or the staircase;
- exposing credentials;
- downloading or parsing protected source data from Brain;
- changing the canonical Forensic FSM without an explicit successor action and immutable receipt.

## Current frozen boundary

As of BRAIN-N116:

```text
Brain FSM             = ONE
Action space          = 0
Promotion             = DENY
Room 01               = DATA_ADMISSION
Room 02               = LOCKED
Staircase             = LOCKED
DB round-trip         = PASS (local gate evidence)
HTTP governance proof = NOT_YET_PROVEN_CURRENT
```

## Important distinction

A second Bot may continue **safe engineering** while this Bot is waiting for external observation. It must not be treated as an alternate Brain authority. Its output is a candidate engineering result until admitted by the same Forensic FSM.

## Resume rule

When an independently observable exact-current `/governance` receipt appears, the successor must create `BRAIN-N117` and verify:

1. runtime identity;
2. exact commit;
3. action ID;
4. nonce/request receipt;
5. freshness;
6. consistency with immutable state.

Only then may the FSM decide whether any gate can move. PASS never propagates automatically.
