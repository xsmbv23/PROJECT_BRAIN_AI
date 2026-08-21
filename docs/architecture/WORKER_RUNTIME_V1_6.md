# Worker Runtime V1.6 — Autonomous Recovery

## Objective

Prove that headless execution remains fail-closed across worker interruption and restart boundaries without browser execution authority and without inheriting a previous PASS.

## Recovery contract

```text
WORKER HEALTHY
  ↓
WORKER UNAVAILABLE / STALE
  ↓
HOLD
  ↓
RETRY / RECOVERY
  ↓
WORKER HEALTHY AGAIN
  ↓
NEW IMMUTABLE RECEIPT
  ↓
RECONCILIATION
  ↓
BOT1 LOCAL GATE
```

## Non-inheritance

A prior PASS is evidence about a prior execution observation. It is never a PASS for a recovered runtime. Recovery must emit a new receipt identity and preserve allocation/cycle lineage.

## Browser independence

`CHAT_SESSION_EXECUTION=CLOSED` and `execution_authority=HEADLESS_WORKER` remain required. Chat sessions cannot become fallback execution authority during recovery.

## Failure policy

- unavailable/stale worker → HOLD;
- missing receipt → HOLD;
- allocation identity mismatch → HOLD;
- conflicting worker observations → ESCALATE/HOLD;
- recovered worker → new receipt;
- promotion remains DENY until the canonical local forensic gate independently admits it.
