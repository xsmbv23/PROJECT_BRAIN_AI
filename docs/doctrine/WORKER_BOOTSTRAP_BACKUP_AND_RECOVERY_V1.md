# Worker Bootstrap Backup & Recovery V1

Status: CANONICAL OPERATING DOCTRINE
Owner: BOT1_LEAD
Scope: BOT2 / BOT3 / BOT4 successor recovery

## Principle

Every worker must have recoverable persistent bootstrap state. A worker is disposable; its identity, role, contracts, allocation history, and recovery metadata are not.

The repository is the canonical backup of worker bootstrap doctrine and recovery metadata. A live worker filesystem is an execution cache, not the sole source of truth.

## Per-worker bootstrap

Each worker has a versioned bootstrap manifest:

```text
workers/bootstrap/BOT2_QUANT.md
workers/bootstrap/BOT3_REALITY.md
workers/bootstrap/BOT4_EXECUTION.md
```

Each manifest must contain:

- role and scope
- authority boundaries
- canonical doctrine references
- worker-specific execution contract
- current deployment identity/reference
- current allocation/lease expectations
- receipt format
- recovery procedure
- known blockers
- last verified bootstrap checkpoint

Worker manifests must never contain secrets, credentials, tokens, or private keys.

## Recovery model

```text
WORKER DIES
   -> detect stale/missing heartbeat or receipt
   -> mark worker runtime unavailable
   -> preserve last known receipt/history
   -> create replacement worker identity/runtime
   -> load canonical worker bootstrap
   -> verify role/contract/authority
   -> issue fresh allocation/lease
   -> execute
   -> produce fresh receipt
   -> reconcile
```

A replacement worker does not inherit an old PASS merely because it loads the old bootstrap. It must produce fresh execution evidence.

## Backup layers

### Layer 1 — Git repository

Canonical worker bootstrap, contracts, orchestration code, allocation schemas, and recovery doctrine.

### Layer 2 — Persistent coordination state

Allocations, claims, receipts, reconciliations, conflicts, holds, and recovery records.

### Layer 3 — Deployment metadata

Worker deployment identity, artifact/version/hash, runtime version, health state, and deployment receipts.

### Layer 4 — Worker local state

Ephemeral cache only. It may accelerate recovery but must never be required for reconstructing authority or forensic history.

## Failure classes

### Worker process dies

Restart/replacement may reuse the same logical worker role but must create a fresh execution attempt/lease.

### Worker server dies

Rehydrate from repository + persistent coordination. Do not trust local disk as the only copy.

### Worker deployment is stale

Deployment is `UNKNOWN` until a fresh deployment/runtime receipt proves the requested artifact is active.

### Worker returns conflicting evidence

Preserve the conflict and route to BOT1 reconciliation. Never overwrite the minority record.

### Worker is permanently unavailable

BOT1 may allocate a replacement worker for the same department. The replacement must bootstrap from the canonical worker manifest and receive a new lease.

## Bootstrap checkpoint

A worker successor may declare bootstrap complete only after:

```text
ROLE_VERIFIED
CONTRACT_VERIFIED
AUTHORITY_VERIFIED
CANONICAL_ALLOCATION_VERIFIED
RUNTIME_IDENTITY_VERIFIED
RECEIPT_PATH_VERIFIED
RECOVERY_PATH_VERIFIED
```

Reading documentation alone is not sufficient.

## Security boundary

Credentials and deployment secrets remain outside Git/bootstrap documents. Recovery automation must reference secret names or secret-store bindings, never persist secret values in repository state or receipts.

## BOT1 responsibility

BOT1 owns the canonical worker registry, allocation, recovery decision, and reconciliation. BOT1 does not depend on a live ChatGPT session for worker continuity.

## Successor rule

If BOT2/BOT3/BOT4 disappears, the replacement must be able to reconstruct its operating role from persistent repository doctrine + coordination state without relying on copied chat history.

This doctrine is versioned and may only be superseded by a later versioned worker-recovery doctrine.
