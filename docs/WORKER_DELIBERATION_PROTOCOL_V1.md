# WORKER DELIBERATION PROTOCOL V1

## Purpose

This document preserves the failure/recovery lessons from the N175 multi-worker execution work before any new worker deliberation begins.

The goal is to prevent Worker N from repeating the same class of failure that affected BOT3: a component can appear operational, yet be unable to participate in the actual allocation/claim/execute/receipt chain. A later worker must therefore be verified as a **worker**, not merely as a live service or runnable script.

This document is normative for future worker onboarding and worker-to-worker deliberation.

---

## 1. Canonical worker model

The system has one orchestrator and multiple workers.

```text
ORCHESTRATOR
     |
     +---- WORKER 1
     +---- WORKER 2
     +---- WORKER 3
     +---- WORKER N
```

Workers may:

- receive an allocation;
- inspect their scoped evidence;
- execute their assigned work;
- publish durable receipts;
- challenge another worker's claims;
- rebut challenges with evidence;
- produce consensus and dissent;
- recommend the next action.

Workers may **not**:

- promote themselves;
- unlock a forensic gate;
- mutate canonical truth outside their owned scope;
- convert consensus into evidence;
- convert a local PASS into promotion permission;
- silently erase minority/conflict history;
- claim that another worker executed unless durable evidence exists.

The orchestrator decides the authoritative `NEXT_ACTION` after reviewing worker deliberation.

---

## 2. The BOT3 failure that must never repeat

### Initial failure mode

BOT3 appeared healthy because its HTTP/source-independence service was live. The service was backed by:

```text
SHA: c68242b4f59492fa53e0ae916e2ce039291e3bbf
```

The critical defect was not simple liveness. The running component was effectively an HTTP wrapper and did **not** provide the persistent allocation consumer / claim / execution / receipt loop required by the worker protocol.

Therefore:

```text
SERVICE_LIVE
     !=
WORKER_RUNTIME_READY
```

and specifically:

```text
ALLOCATION
     ↛
RUNTIME
```

There was no trustworthy proof that an allocated BOT3 task had been claimed, executed, and durably receipted.

### Why this caused HOLD

The system correctly held BOT3 because the following chain was incomplete:

```text
allocation issued
      ↓
worker claims allocation
      ↓
worker executes assigned process
      ↓
worker emits receipt
      ↓
receipt binds allocation + cycle + worker identity
      ↓
reconciliation observes receipt
```

A live HTTP endpoint could not substitute for this chain.

### Recovery direction

The solution was not to keep restarting the same service or to treat liveness as execution. The execution route was changed so BOT3 could run on an independent execution plane through the GitHub Actions E2E path.

The later canonical E2E contract bound the worker group to:

```text
ALLOC-N175-S1-E2E-TRIPLE-WORKER-002
BRAIN-N175-S1-CANONICAL-EVIDENCE-VERIFIER
```

The fresh E2E run then proved, for BOT2/BOT3/BOT4:

```text
process_executed = true
receipt_observed = true
allocation_bound = true
cycle_bound      = true
local_result_pass = true
promotion_denied = true
```

BOT3 additionally produced direct runtime evidence (`HTTP_READY`, port `18003`).

### Lesson

**Never onboard a new Worker N from service liveness alone.**

The minimum proof is an end-to-end worker execution receipt bound to the current allocation and current cycle.

---

## 3. Worker N onboarding gate

Before Worker N is allowed into deliberation, verify all of the following independently:

```text
IDENTITY
  ↓
SESSION_START_SYNC
  ↓
ALLOCATION_RECEIVED
  ↓
ALLOCATION_CLAIMED
  ↓
PROCESS_EXECUTED
  ↓
RECEIPT_EMITTED
  ↓
RECEIPT_PERSISTED
  ↓
RECEIPT_BOUND_TO_CURRENT_ALLOCATION
  ↓
RECEIPT_BOUND_TO_CURRENT_CYCLE
  ↓
RECONCILIATION_OBSERVED
  ↓
LOCAL_GATE_PASS / DENY
```

A Worker is not considered active merely because:

- a process is listening on a port;
- a health endpoint returns 200;
- a Python module imports successfully;
- a container is running;
- a workflow is present;
- a historical receipt exists;
- another worker says it is running.

Those are supporting signals only.

---

## 4. No historical receipt inheritance

Historical worker evidence must never satisfy a fresh execution predicate.

```text
OLD_RECEIPT
   !=
CURRENT_EXECUTION
```

A receipt from Worker N on allocation `A-001` cannot satisfy a new allocation `A-002`.

A receipt from a previous cycle cannot satisfy a new cycle.

A receipt from a previous execution boundary cannot prove execution on a new execution boundary.

This is especially important after a worker recovery or routing change.

---

## 5. Execution-plane routing rule

If the current execution plane can prove only liveness but cannot prove the complete worker lifecycle, do **not** repeatedly restart the same route.

Use this decision rule:

```text
Can current plane prove
allocation → claim → execute → receipt?
             |
       +-----+-----+
       |           |
      YES          NO
       |           |
    continue     HOLD
                   |
            inspect routing
                   |
       choose independent permitted
          execution plane if available
```

A routing change must itself be recorded as an action with evidence. It must not be hidden as an implementation detail.

---

## 6. Deliberation is itself an executable protocol

Future worker discussion must not be simulated by the orchestrator's prose.

The actual worker group must execute a deliberation cycle:

```text
TASK ALLOCATION
      ↓
WORKER 1 INITIAL POSITION
WORKER 2 INITIAL POSITION
WORKER 3 INITIAL POSITION
      ↓
CROSS-READ
      ↓
CHALLENGE / COUNTERARGUMENT
      ↓
REBUTTAL
      ↓
EVIDENCE CHECK
      ↓
CONSENSUS + DISSENT
      ↓
RECOMMENDATION
```

A worker may disagree with the majority. Minority reasoning must be preserved.

```text
CONSENSUS != TRUTH
DISSENT != FAILURE
```

The value of deliberation is that independent workers expose assumptions that a single worker or orchestrator might miss.

---

## 7. Required deliberation output

Every completed worker deliberation must persist:

```text
session_id
allocation_id
cycle_id
worker identities
execution boundary
initial positions
peer challenges
peer rebuttals
evidence references
agreements
disagreements
minority position
consensus
recommended_next_action
unresolved_risks
promotion = DENY unless independently gated
```

No prose-only consensus is authoritative.

The durable record is authoritative.

This follows the existing session-start rule that a peer-Bot claim is not evidence of peer synchronization; only a durable peer record is evidence.

---

## 8. Communication security for worker exchange

Worker-to-worker communication must use registered, capability-authorized corridors. The existing communication security contract requires identity, project, layer, corridor, capability, nonce/freshness, lineage, payload hash, policy, post-verification and audit append before acceptance.

Failure at any communication gate is `DENY`.

Worker messages must not contain:

- credentials;
- database URLs;
- cookies;
- tokens;
- private capability material;
- secrets.

Replay protection and lineage remain mandatory.

---

## 9. Worker deliberation must not mutate canonical truth

The worker group may produce recommendations and scoped artifacts, but deliberation must not silently modify canonical state.

The safe boundary is:

```text
WORKER EVIDENCE
      ↓
WORKER DELIBERATION
      ↓
RECOMMENDATION
      ↓
ORCHESTRATOR REVIEW
      ↓
AUTHORITATIVE NEXT_ACTION
```

Not:

```text
WORKER CONSENSUS
      ↓
CANONICAL PROMOTION
```

`PROMOTION=DENY` remains the default until the specific gate's own evidence proves otherwise.

---

## 10. Failure taxonomy for future Worker N

### A. Liveness-only failure

```text
HTTP 200 / process alive
but no allocation claim
```

Result: `HOLD`.

### B. Allocation-to-runtime disconnect

```text
allocation exists
but worker never executes it
```

Result: `HOLD` and inspect routing.

### C. Runtime-to-receipt disconnect

```text
process executes
but durable receipt missing
```

Result: `HOLD`.

### D. Receipt identity mismatch

```text
receipt worker != allocated worker
```

Result: `DENY`.

### E. Allocation mismatch

```text
receipt allocation != current allocation
```

Result: `DENY`.

### F. Cycle mismatch

```text
receipt cycle != current cycle
```

Result: `DENY`.

### G. Stale execution boundary

```text
old GitHub/Render/process evidence
used as current proof
```

Result: `HOLD`; require fresh execution.

### H. Consensus-without-evidence

```text
all workers agree
but no durable execution/evidence
```

Result: `UNKNOWN/HOLD`, never PASS.

### I. Worker isolation failure

```text
worker cannot read required peer handoff
or cannot publish durable handoff
```

Result: deliberation cannot be considered complete.

### J. Promotion leakage

```text
worker PASS
     ↓
worker assumes promotion allowed
```

Result: `DENY`.

---

## 11. Recovery playbook

When a Worker N becomes `HOLD`:

1. Do not redefine `HOLD` as PASS.
2. Do not delete the failed history.
3. Identify the exact broken edge in the lifecycle chain.
4. Determine whether the failure is worker logic, execution routing, allocation binding, receipt persistence, or communication.
5. If the current execution plane cannot prove the required edge, evaluate a permitted independent execution plane.
6. Record the routing change and reason.
7. Issue a **fresh allocation** for the recovered route.
8. Run the worker end-to-end.
9. Require a fresh receipt bound to the new allocation and cycle.
10. Reconcile the receipt independently.
11. Only then allow the worker back into deliberation.

The recovery target is:

```text
WORKER N = RUNTIME-VERIFIED
```

not merely:

```text
WORKER N = SERVICE-LIVE
```

---

## 12. Pre-deliberation checklist

Before assigning the first real multi-worker discussion task:

- [ ] every worker passed `SESSION_START_SYNC`;
- [ ] every worker identity is explicit;
- [ ] every worker has a current allocation;
- [ ] every allocation has a claim record;
- [ ] every worker has fresh runtime execution evidence;
- [ ] every worker has a durable receipt;
- [ ] receipts bind current allocation and current cycle;
- [ ] worker-to-worker communication corridor is registered;
- [ ] nonce/freshness/replay protection is active;
- [ ] peer handoffs are durable;
- [ ] dissent/minority history is preserved;
- [ ] deliberation output has a durable evidence artifact;
- [ ] consensus is treated as recommendation, not proof;
- [ ] promotion remains `DENY` unless separately gated.

---

## 13. Permanent rule

The N175/BOT3 incident establishes the permanent rule for every future worker:

> **Do not ask whether the worker is alive. Ask whether the worker can complete the entire allocation → claim → execute → receipt → reconcile chain on the current execution boundary.**

Only after that chain is proven may the worker participate in autonomous multi-worker deliberation.

The repository's existing continuity, communication-security and action-ledger contracts remain authoritative; this document adds the worker-specific failure/recovery lessons that those generic contracts cannot infer from liveness alone.
