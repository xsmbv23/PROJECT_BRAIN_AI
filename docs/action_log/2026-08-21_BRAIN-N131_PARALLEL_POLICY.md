# BRAIN-N131 — Parallel Bot Policy Handoff

## Decision

Parallel work is permitted, but only as scoped local prerequisite work. The Brain Forensic FSM remains singular and authoritative.

## Current inherited state

Read from `state/current_state.json` and `state/next_action.json`:

- action space = 0
- promotion = DENY
- Brain next action = `BRAIN-N125_WAIT_EXTERNAL`
- Quant parallel work = explicitly allowed as local prerequisite only

## Rule

A second Bot may work continuously on Quant/local prerequisites without waiting for the Brain gate. It must not:

- claim external runtime verification;
- claim independent Render observation;
- claim durable DB promotion;
- unlock Layer 1;
- unlock the staircase;
- overwrite source truth with derived data;
- convert its own repository-local PASS into Brain external PASS.

## Evidence relation

```text
ONE FORENSIC FSM
        |
        +--> Brain gate evidence
        |
        +--> Quant local evidence
                 |
                 +--> may support future gate
                 +--> may NOT unlock gate by inheritance
```

## Next action

No Brain gate mutation is authorized until fresh independently observable exact-current CI or governance evidence arrives. The repository may continue receiving safe local prerequisite work and successor documentation in parallel.
