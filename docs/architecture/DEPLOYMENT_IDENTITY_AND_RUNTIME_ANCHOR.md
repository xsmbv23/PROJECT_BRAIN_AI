# Deployment Identity and Runtime Anchor

## Critical correction

`GitHub main HEAD` and `Render runtime commit` are not automatically the same object.

Render may serve the last deployed commit while GitHub `main` receives documentation, action-log, or state commits. Therefore repository HEAD drift must not automatically be classified as runtime drift.

## Canonical model

```text
GitHub main HEAD
      |
      | repository history / successor memory
      v
Runtime Anchor Commit  <------------------+
      |                                    |
      | deploy                             | compare
      v                                    |
Render Runtime Commit ---------------------+
```

The **runtime anchor** is the explicit commit selected as the runtime-bearing forensic release point and recorded in the action evidence before deployment.

## Admission rules

```text
runtime_commit == runtime_anchor_commit
        |
      PASS
        |
 runtime admission may proceed
```

If they differ:

```text
DEPLOYMENT_RUNTIME_DRIFT = DENY
```

Repository `main` HEAD is separately observable. A HEAD change is classified as runtime-affecting only when the change policy declares it runtime-bearing or when the resulting release anchor is advanced.

## Why this exists

Without this distinction, writing the successor's state file after a successful deploy would create a new Git commit and falsely make the live service look stale even though the service itself had not changed.

That is a bookkeeping artifact, not runtime drift.

## Forensic law

- Runtime evidence is anchored to a specific deployed release commit.
- Repository history may advance independently for successor documentation.
- A documentation-only HEAD advance does not revoke an otherwise valid runtime anchor.
- A runtime-affecting change must create a new anchor and receive a new deployment identity receipt.
- No credential is ever required to evaluate this gate.
- Functional PASS never overrides runtime-anchor mismatch.

## Successor-Bot law

Never use `DATABASE_PASS`, `RUNTIME_PASS`, or `MAIN_PASS` as a single umbrella flag.
Keep repository history, runtime identity, database admission, and promotion as separate ordered evidence gates.
