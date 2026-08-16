# BRAIN CORE HARDENING V1

## Decision

Do NOT replace the Brain core. The current architecture is directionally correct: Brain is the governance/control plane, not the data plane or intelligence engine. The core should be hardened with explicit controls before Layer 1 opens.

## Additions required

### 1. Policy/version pinning
Every decision must carry `policy_version`, `schema_version`, `brain_state_version`, and `decision_id`. A future Bot cannot silently reinterpret an old decision under a new policy.

### 2. Capability leases
A capability is not permanent authority. Every corridor capability gets a short-lived lease with:
- capability ID;
- source/destination layer;
- corridor ID;
- issued_at;
- expires_at;
- nonce;
- policy version;
- maximum operation count.

Expired or over-used leases DENY.

### 3. Two-phase governance decisions
Separate:

```text
PROPOSED → VERIFIED → EFFECTIVE
```

A Brain proposal is not an executable command. The effective state requires post-verification and audit append.

### 4. Quarantine state
Add a terminal containment state:

```text
QUARANTINED
```

for malformed evidence, lineage breaks, replay, schema drift, suspicious corridor traffic, or repeated resource guard violations. Quarantine prevents automatic retry loops.

### 5. Circuit breakers
Per corridor and per capability:
- consecutive failure counter;
- rate limit;
- replay counter;
- resource guard counter;
- cooldown window.

A breaker opening produces DENY and requires an explicit new action ledger entry before recovery.

### 6. Clock/freshness authority
Freshness must use one declared time authority. Never trust arbitrary client timestamps alone. Store received_at and evaluated_at separately from issued_at.

### 7. Schema registry
Evidence and communication envelopes require registered schema versions. Unknown major versions DENY. Compatible minor versions require explicit compatibility rules.

### 8. Append-only decision ledger
Every ACCEPT, DENY, QUARANTINE, breaker-open and recovery event gets a deterministic event hash and previous-event hash:

```text
H(n) = SHA256(H(n-1) + canonical_event(n))
```

This creates a tamper-evident chain without storing bulk data.

### 9. Recovery is a state transition
Restart/redeploy must restore state from durable evidence/ledger. It must never infer state from process memory. Recovery itself must create an auditable event.

### 10. Resource governor
The 512 MB Render Free ceiling and 320 MB conservative guard become Brain policy, not merely runner configuration. Heavy operations must be classified and routed away from the Render UI/control process.

## Keep unchanged

- FULL_27 remains canonical source truth.
- TAIL_27 remains derived.
- Brain never mutates canonical truth directly.
- UI never mutates canonical truth.
- No implicit corridor.
- No permanent capability.
- Promotion remains DENY by default.
- Layer 1 remains LOCKED until foundation runtime gates pass.
- Chat remains communication only.

## Why this is the correct modification

These controls strengthen the existing Fosennic closure instead of adding intelligence prematurely. They make future Bots less likely to bypass a corridor, reuse stale authority, replay evidence, retry a failed path forever, or mistake integrity for correctness.
