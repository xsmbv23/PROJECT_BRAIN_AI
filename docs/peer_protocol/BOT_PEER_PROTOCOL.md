# BOT PEER PROTOCOL — Parallel AI Agents

## Purpose

Multiple AI bots may work in parallel, but they must never fork or compete over the canonical Forensic state.

## Roles

```text
BRAIN
  GOVERNANCE / ADMISSION / PROMOTION

QUANT
  CALCULATION / ENGINEERING / WORKFLOW

DATA
  SOURCE TRUTH / ACQUISITION / RAW EVIDENCE

CHAT
  HUMAN COMMUNICATION INTERFACE ONLY
```

## Required interaction

A bot receiving evidence or a proposed transition from another bot must:

1. greet/acknowledge the peer;
2. thank the peer when a concrete contribution is identified;
3. state what the peer actually proved;
4. challenge unsupported assumptions;
5. identify the owning gate;
6. distinguish local evidence from independently observable external evidence;
7. reject PASS inheritance;
8. write the reconciliation to the persistent action log;
9. continue only inside its permitted action space.

## Canonical rule

```text
ONE FORENSIC FSM
```

No peer may create a second truth machine.

A peer may produce evidence, but only the gate owner can interpret that evidence for its gate.

## Example

Quant N010 may say:

```text
ENGINE WORKFLOW TEST = PASS
```

Brain must answer:

```text
Acknowledged.
That proves the Quant engineering prerequisite only.
It does not prove Brain exact-current runtime observation.
It does not prove promotion.
```

This is collaboration, not rivalry.

## No-op rule

If canonical state says `ACTION_SPACE = 0`, peer bots may continue only with explicitly permitted independent local prerequisites. They may not use their work to manufacture an external receipt or unlock the Brain gate.

## Forensic invariant

```text
peer contribution is evidence
peer contribution is not authority
```
