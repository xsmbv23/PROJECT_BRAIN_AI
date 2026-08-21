# Worker Delegation V1

Status: CANONICAL PROPOSAL IMPLEMENTED AS CONTRACT BASELINE
Owner: BOT1_LEAD

## Hierarchy

```text
BOT1_LEAD
  -> BOT2 / BOT3 / BOT4
       -> optional child workers BOTn.m
```

A child worker inherits only a subset of its parent's delegated authority. No child may delegate authority it does not possess.

## Rules

1. BOT1 remains the canonical allocator and final reconciler.
2. BOT2/BOT3/BOT4 may request or receive child-worker allocations only within their delegated scope.
3. Child workers cannot mutate `state/current_state.json` or `state/next_action.json`.
4. Child workers cannot perform forensic promotion.
5. Every child has `worker_id`, `parent_worker_id`, `generation`, capabilities, delegated scope, bootstrap reference, receipt path, runtime identity, allocation and lease state.
6. A replacement worker requires fresh execution evidence; no PASS inheritance.
7. Child worker write scopes must be disjoint where practical.
8. Every execution is bound to allocation/cycle/task identity and a lease.
9. Worker results are advisory/evidence outputs, not canonical-state mutations.
10. Persistent coordination is the authority for active allocations; browser/chat sessions are not execution dependencies.

## Spawn flow

```text
PARENT WORKER
  -> SPAWN/DELEGATION REQUEST
  -> authority/scope validation
  -> CHILD ALLOCATION
  -> CHILD BOOTSTRAP
  -> CLAIM / LEASE
  -> EXECUTE
  -> RECEIPT
  -> PARENT RECONCILE
  -> BOT1 RECONCILE
```

A parent must not silently create unlimited workers. Resource/quota policy, scope, and lease must be validated before activation.

## Recovery

If a child dies, preserve its last receipt and history, mark its runtime unavailable/stale, and create a fresh replacement attempt. The replacement reads its bootstrap from the repository and produces fresh evidence.

## Forensic boundary

Hierarchy is an execution organization, not a forensic authority hierarchy. More workers do not create more promotion authority.

```text
MORE WORKERS != MORE FORENSIC AUTHORITY
```
