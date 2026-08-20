# FORENSIC SUCCESSOR READING ORDER

A successor Bot must not infer architecture from chat history.

Read these files in this order:

1. `state/current_state.json` — exact current canonical state.
2. `state/next_action.json` — exact next action; do not invent a different one.
3. `docs/forensic/FORENSIC_FSM_GATE_SEMANTICS.md` — permanent one-FSM doctrine.
4. `docs/forensic/FORENSIC_GATE_ADMISSION_MODEL.md` — formal gate/admission model; especially PASS locality and no inheritance.
5. Latest `docs/action_log/` record — chronology of the most recent completed action.

## Immutable rule

A PASS belongs only to the gate that earned it.

A PASS may unlock evaluation of the next gate, but it never grants the next gate's PASS.

## Current N116 rule

`BRAIN-N116_WAIT_EXTERNAL_OBSERVATION` is the canonical next action until an independently supplied exact-current external `/governance` observation is received through Evidence Ingress and verified.

While waiting:

```text
ACTION_SPACE = 0
PROMOTION = DENY
```

Do not manufacture the observation, do not self-verify an internally manufactured receipt, do not rewrite historical evidence, and do not unlock Layer 1 or the staircase.
