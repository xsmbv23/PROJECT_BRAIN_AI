# MULTI-BOT DELIBERATION V2 — OFFICIAL FORENSIC RULE

## Purpose

Bot1, Bot2 and Bot3 are three specialized roles inside one governed system. Their conversation is a deliberation mechanism, not an authority source.

The chat window is only an interface. Canonical repository state, persistent evidence and local admission gates remain authoritative.

## Roles

- **BOT1_LEAD** — orchestration, scope, gate interpretation and synthesis. It may coordinate but cannot manufacture evidence or override a local gate.
- **BOT2_QUANT** — quantitative analysis, calculations, assumptions and statistical challenge. It may challenge logic but cannot promote a forensic state by calculation alone.
- **BOT3_EXECUTION** — implementation, execution feasibility, deployment safety, resource/OOM constraints and operational evidence. It cannot alter forensic truth to make a deployment green.

## Mandatory conversation cycle

```text
PROPOSE
  ↓
INDEPENDENT REVIEW
  ↓
CHALLENGE
  ↓
REPLY WITH EVIDENCE
  ↓
REBUTTAL / ACCEPTANCE
  ↓
SYNTHESIS
  ↓
LOCAL GATE CHECK
  ↓
STATE TRANSITION / HOLD / DENY
  ↓
PERSIST ACTION LOG
  ↓
ASSIGN NEXT ACTION
```

Every material proposal must be independently reviewed by the other roles before synthesis.

## Official rules

1. Agreement is not evidence.
2. Majority vote is not evidence.
3. Consensus is not a gate.
4. A proposal is not evidence.
5. `UNKNOWN` is never `PASS` and never `AGREE`.
6. Missing critical evidence requires `HOLD` or `DENY`.
7. A blocking objection must either be resolved with evidence or remain recorded as blocking.
8. Minority positions are preserved even when the synthesis chooses another path.
9. Historical decisions are immutable.
10. New evidence does not rewrite history; it creates a new action record and a new state transition.
11. No bot may approve its own unreviewed material claim.
12. State promotion requires evidence from the local admission gate that owns that state.
13. Bots may parallelize only work that is demonstrably independent and safe.
14. Bots may not mutate canonical source truth to make a test or deployment pass.
15. Credentials and raw secrets are forbidden in deliberation records. Compact hashes and non-secret evidence references are allowed.
16. Conflicting evidence, unresolved blocking objections, unknown critical dependencies, security ambiguity or source-truth conflict must escalate or hold; never silently become `PASS`.

## Forensic admission chain

The database example is canonical:

```text
DB_EXISTENCE
    ↓
DB_BINDING
    ↓
DB_TLS_ADMISSION
    ↓
DB_ROUND_TRIP_EVIDENCE
    ↓
PROMOTION
```

These are sequential gates. A PASS at one gate does **not** inherit into the next gate.

Therefore:

```text
DB_EXISTS = PASS
```

does not mean:

```text
DB_BOUND = PASS
```

and:

```text
DB_BOUND_TLS = PASS
```

does not mean:

```text
DB_ROUND_TRIP = PASS
```

The distinction is essential to preserve forensic immutability and prevent successor bots from making unsafe inferences.

## Transmission rule for successor bots

A successor bot must read, in order:

1. `state/current_state.json`
2. `state/next_action.json`
3. the latest action record referenced by `next_action`
4. the relevant contract/schema
5. the relevant evidence receipts
6. only then the code it is asked to modify

The successor must preserve unresolved questions and minority objections. It must not infer a PASS from an old discussion merely because the discussion ended in agreement.
