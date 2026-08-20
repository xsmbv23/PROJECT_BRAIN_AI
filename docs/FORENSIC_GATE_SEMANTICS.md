# FORENSIC GATE SEMANTICS — Permanent Doctrine

## 1. One Forensic FSM

There is exactly **one** Forensic finite-state machine across Brain and downstream rooms.

The states below are not independent Forensic systems. They are local gate states inside one admission chain.

## 2. Gate hierarchy

```text
RESOURCE EXISTENCE
      │
      ▼
AUTHORIZATION / BINDING
      │
      ▼
SECURITY ADMISSION
      │
      ▼
NETWORK / ORIGIN PROOF
      │
      ▼
REAL OPERATION / ROUND-TRIP
      │
      ▼
PROMOTION
```

A prior gate does not become a later gate.

`DB_EXISTS=PASS` does NOT imply `DB_BOUND=PASS`.
`DB_BOUND=PASS` does NOT imply `TLS_ADMISSION=PASS`.
`TLS_ADMISSION=PASS` does NOT imply `ROUND_TRIP=PASS`.
`ROUND_TRIP=PASS` is required before durable promotion can occur.

## 3. Permanent gate semantics

Every gate obeys:

- `PASS_IS_LOCAL`
- `PASS_IS_PREREQUISITE_ONLY`
- `NO_PASS_INHERITANCE`
- `UNKNOWN_IS_NOT_PASS`
- `DEFAULT_DENY`
- `OWN_GATE_EVIDENCE_REQUIRED`
- `FRESH_EVIDENCE_REQUIRED_FOR_PROMOTION`

## 4. Evidence meaning

Evidence types are also distinct and must not be conflated:

- **Existence evidence** proves that a resource exists.
- **Binding evidence** proves that a runtime has an explicit authorized binding.
- **Security evidence** proves the binding satisfies the required security policy.
- **Origin evidence** proves the observed endpoint/source is the intended origin.
- **Round-trip evidence** proves the actual operation succeeded and its returned evidence matched the expected digest.
- **Promotion evidence** proves the complete admission chain is satisfied.

Evidence from one gate cannot be silently reused as evidence for another gate.

## 5. Raw hash vs semantic hash

`raw_sha256` means exact byte identity of an artifact **within its source**.

`semantic_sha256` means equality of the validated canonical semantic domain.

They have different meanings and cannot substitute for each other.

Example:

```text
ketqua16 page A raw hash != ketqua16 page B raw hash
```

may be normal when advertisements change while the official result remains identical.

Therefore raw byte hash mismatch does not automatically mean semantic disagreement.

Conversely:

```text
same semantic hash
```

does not prove the two sources are independent. Source identity and runtime identity remain separate evidence fields.

## 6. Source page chrome and advertising

Advertising, navigation, headers, footers, page counters, tracking markup, and unrelated numeric content are **NON_TRUTH_CONTENT**.

A generic numeric regex is never sufficient evidence of a canonical result.

Semantic extraction must identify the official result-bearing panel before a candidate can enter the canonical domain.

## 7. State transition rule

A transition is valid only when its own gate evidence is fresh and observable.

```text
DEFINED != IMPLEMENTED
IMPLEMENTED != TESTED
TESTED != RUNTIME_VERIFIED
RUNTIME_VERIFIED != CROSS_REPO_VERIFIED
CROSS_REPO_VERIFIED != FORENSIC_ADMITTED
FORENSIC_ADMITTED != PROMOTED
```

`FIXED` is not a PASS state.

`UNKNOWN` remains UNKNOWN until independent evidence changes it.

## 8. Successor rule

A successor Bot must read this document together with:

- `state/current_state.json`
- `state/next_action.json`
- `docs/action_log/`

The chat transcript is not the authority.

The successor must continue from the durable state and must never infer completion merely from the number of prior actions.

## 9. Core mission rule

Progress is measured by removal of verified blockers on:

```text
REAL DATA
  → VALID RESEARCH
  → VALID BACKTEST
  → EDGE
  → EV / PNL / ROI
  → ROBUSTNESS / RISK / DRIFT
  → CONTROLLED ACTION
```

Not by action-count, contract-count, or document-count.
