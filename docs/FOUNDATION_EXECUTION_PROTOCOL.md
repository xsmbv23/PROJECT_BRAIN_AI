# Foundation Execution-Evidence Protocol

This document is the successor-Bot contract for proving foundation execution.

## 1. Authority rule

A GitHub workflow being configured is **not** evidence that it executed.
An absent connector-visible run/status is **UNKNOWN**, never PASS.

## 2. Canonical local execution

From repository root:

```bash
python tools/verify_foundation.py
python tools/verify_access_path.py
```

Equivalent shell entrypoint:

```bash
./tools/verify_foundation.sh
```

The canonical verifier is stdlib-only and must remain dataset-free.

## 3. Required evidence envelope

Every closure-readiness attempt must record:

```text
commit_sha
exact_commands
executor_identity
started_at_utc
finished_at_utc
exit_code
stdout_compact
stderr_compact
tracemalloc_peak_bytes
verifier_version/fingerprint
source_tree_fingerprint
```

Never record a PASS without the exit code and verifier output.

## 4. Memory gate

```text
peak < 320 MiB      => memory gate PASS
peak >= 320 MiB     => DENY / investigate
Render hard limit   => 512 MiB
```

The verifier itself must not load FULL_27, TAIL_27, spreadsheets, databases, or network clients.

## 5. GitHub Actions evidence

`.github/workflows/foundation.yml` is configured for `push` and `pull_request` on `main` and runs both deterministic verifiers. Its presence alone is not execution evidence.

## 6. Cross-plane proof

The same evidence run must cover:

```text
Brain governance
→ capability lease
→ security chain
→ corridor lock
→ room lock
→ protected-room inner latch
→ durable audit/state
→ source/adapter isolation
```

A PASS from one gate cannot authorize the next gate.

## 7. Failure semantics

Any verifier failure, missing output, missing commit fingerprint, missing memory evidence, or unobservable execution result is:

```text
UNKNOWN / FAIL
→ PROMOTION DENY
→ Layer 1 LOCKED
→ Staircase LOCKED
```

## 8. Success semantics

Only when all required evidence exists and every gate passes may the system enter closure-readiness audit. Closure-readiness is not Layer 1 activation; the staircase remains locked until the separate promotion gate passes.

## 9. Successor Bot rule

Before changing architecture, the next Bot must:

1. read `state/next_action.json`;
2. read the latest `docs/action_log/*` entry;
3. read this protocol;
4. reproduce the verifier;
5. preserve all DENY/LOCK invariants;
6. append its action/evidence/result/next-action record.
