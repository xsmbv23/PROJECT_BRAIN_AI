# ACTION LEDGER PROTOCOL V1

This ledger is the continuity mechanism for future Bots.

## Every action record must contain

```text
DATE/TIME
BOT/ACTOR
ACTION_ID
OBJECTIVE
SCOPE
SOURCE_STATE
FILES_CHANGED
COMMIT_SHA
STATIC_VERIFICATION
RUNTIME_VERIFICATION
EVIDENCE_ARTIFACTS
FAILURES / UNKNOWNS
GOVERNANCE_DECISION
CURRENT_STATE
NEXT_ACTION
```

## Rules

1. Append; never erase history.
2. Never replace a failure with a synthetic PASS.
3. Never claim runtime execution from static inspection.
4. Every mutation must have a commit SHA.
5. Every runtime result must identify the execution boundary.
6. Secrets are forbidden.
7. The exact next action must be concrete enough for a new Bot to execute without conversation history.
8. If the next action is blocked, record the blocker rather than inventing a workaround.
