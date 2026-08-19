# Action Receipt Validator — Immutable Admission Law

## Purpose

`ACTION_RECEIPT_VALIDATOR` closes the evidence gap between repository state and the runtime/process that claims to have completed an action.

The system MUST NOT treat these as equivalent:

```text
STATE.last_action == X
```

and

```text
runtime actually emitted a valid receipt for X
```

Both are required.

## Mandatory boot evidence chain

```text
REPOSITORY STATE
      +
NEXT_ACTION POINTER
      +
ACTION_RECEIPT
      +
RUNTIME EVIDENCE
      ↓
RECONCILIATION
      ↓
PASS / DENY
```

## Invariants

### 1. PASS does not inherit

```text
PASS(A)
≠ PASS(B)
```

No gate may promote another gate merely because it passed earlier.

### 2. Receipt must support the exact last action

```text
receipt.action_id == state.last_action
```

### 3. Receipt must be self-integrity-valid

`receipt_sha256` is recomputed from the receipt body with the hash field removed. A mismatch is DENY.

### 4. Receipt must belong to the exact runtime commit

```text
receipt.commit_sha == runtime.commit_sha
```

A valid receipt from an older deployment cannot certify the current deployment.

### 5. Chat has zero runtime authority

Chat intent, confirmation, explanation, or model confidence is never an evidence receipt.

### 6. No self-acting FSM

The Bot MUST NOT perform:

```text
decide → fabricate receipt → validate itself → promote
```

The permitted direction is:

```text
runtime/process executes
        ↓
real evidence emitted
        ↓
validator verifies
        ↓
authority updates state
```

### 7. Validator never advances state

The validator is a read/verify component only. It cannot modify `current_state`, `next_action`, or receipts.

## N104C.1R reconciliation gate

N104C.1R is the exact-current reconciliation step between the persisted state and the runtime evidence.

It MUST verify:

1. exact current commit
2. exact current state snapshot
3. exact next-action pointer
4. exact action-receipt existence
5. receipt SHA integrity
6. receipt action identity
7. receipt commit identity
8. runtime evidence availability

The output is a `RECONCILIATION_RECEIPT`.

No forward action may be promoted from reconciliation intent alone.

## Failure semantics

```text
UNKNOWN              → DENY
MISSING_RECEIPT      → DENY
SHA_MISMATCH         → DENY
ACTION_MISMATCH      → DENY
COMMIT_MISMATCH      → DENY
RUNTIME_UNOBSERVABLE → DENY
```

This law is permanent and applies to successor Bots.
