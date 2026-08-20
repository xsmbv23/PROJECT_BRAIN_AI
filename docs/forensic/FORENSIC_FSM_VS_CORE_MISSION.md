# Forensic FSM vs Core Mission — Doctrine

## 1. One system, two roles

There is **ONE Forensic FSM**, not two independent forensic systems.

The distinction is between:

- **Core Mission** — the objective of the whole system.
- **Forensic FSM** — the admission/control mechanism that decides whether the system has enough evidence to move from one state to another.

### Core Mission

```text
REAL DATA
  -> VALID RESEARCH
  -> VALID BACKTEST
  -> EDGE
  -> EV / P&L / ROI
  -> ROBUSTNESS / RISK / DRIFT
  -> CONTROLLED ACTION
```

The Core Mission must remain the primary direction. The Forensic FSM must never become the product itself.

## 2. Forensic FSM semantics

The FSM answers only:

> "Do we have the exact evidence required to admit the next state?"

It does **not** answer:

> "What is the long-term purpose of the system?"

Therefore a runtime blocker may freeze the FSM while the Core Mission remains unchanged.

## 3. PASS semantics — critical invariant

Every gate owns its own evidence.

```text
PASS_IS_LOCAL
PASS_IS_PREREQUISITE_ONLY
NO_PASS_INHERITANCE
UNKNOWN_IS_NOT_PASS
DEFAULT_DENY
OWN_GATE_EVIDENCE_REQUIRED
FRESH_EVIDENCE_REQUIRED_FOR_PROMOTION
```

A PASS at one gate never becomes a PASS at another gate merely because the states are related.

Example:

```text
DB_EXISTENCE = PASS
        !=
DB_BINDING = PASS
        !=
DB_TLS_ADMISSION = PASS
        !=
DB_ROUND_TRIP = PASS
        !=
PROMOTION = PASS
```

These are sequential admission gates inside the **same** Forensic FSM.

## 4. Database admission chain

```text
DB_EXISTENCE
      |
      v
DB_BINDING
      |
      v
SECRET_RESOLUTION
      |
      v
DB_TLS_ADMISSION
      |
      v
NETWORK_ORIGIN_PROOF
      |
      v
DB_ROUND_TRIP
      |
      v
PROMOTION
```

A previous PASS only authorizes evaluation of the next gate. It never unlocks it by inheritance.

## 5. Current canonical runtime state

The canonical runtime is currently:

```text
BRAIN-N116_WAIT_EXTERNAL_OBSERVATION
```

Current action space:

```text
0
```

Mandatory action:

```text
NO-OP
```

Promotion:

```text
DENY
```

The current blocker is the absence of an independently observable, exact-current `/governance` receipt event.

## 6. Correct transition logic

```text
N116 WAIT
   |
   v
INDEPENDENT EXACT-CURRENT /governance OBSERVATION
   |
   +-- insufficient / stale / non-independent --> remain N116 + DENY
   |
   +-- sufficient evidence ---------------------> N117 admission
                                                   |
                                                   v
                                      verify identity / commit /
                                      action / nonce / freshness
                                                   |
                                                   v
                                           promotion decision
```

The Chat UI is not evidence. A human statement of PASS is not evidence. A startup log is not equivalent to an independently observed HTTP governance receipt.

## 7. NO-OP is a real FSM action

When `action_space = 0`, the system is not idle because it is broken. It is intentionally constrained by the FSM.

`MANDATORY_NO_OP` means:

- no mutation;
- no promotion;
- no Room 02 unlock;
- no staircase unlock;
- no synthetic evidence;
- no self-generated "independent" observation;
- only monitoring, immutable-history reading, integrity validation, and recording newly observed evidence.

## 8. Core Mission must not be frozen by an FSM blocker

A blocked forensic transition does **not** redefine the Core Mission.

The FSM may be waiting while the system architecture, documentation, and future research direction remain aligned with:

```text
REAL DATA -> RESEARCH -> BACKTEST -> EDGE -> EV/P&L/ROI -> ROBUSTNESS/RISK/DRIFT -> CONTROLLED ACTION
```

However, the blocked FSM must prevent the system from claiming that the blocked state has been admitted.

## 9. Successor rule

A successor Bot must read this doctrine before selecting a next action.

It must first determine:

1. Core Mission — what the system is ultimately trying to achieve.
2. Canonical FSM state — what has actually been admitted.
3. Action space — what actions are currently legal.
4. Evidence blocker — what exact evidence is missing.
5. Resume condition — what independently observable event can move the FSM.

If `action_space = 0` and `MANDATORY_NO_OP`, the successor must not invent a mutation simply because the user asks to "continue".

The successor may preserve the mission and monitor evidence, but the canonical FSM remains authoritative.
