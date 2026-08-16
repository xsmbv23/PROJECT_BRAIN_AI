# CHAT BOUNDARY AND PERSISTENT MEMORY

## Absolute rule

The conversation window is an interface, not the Brain.

```text
CHAT
  = communication only

BRAIN REPOSITORY + PERSISTENT SERVICES
  = memory + governance + continuity
```

The system must remain correct if the chat is closed, deleted, replaced, or continued by another Bot.

## What survives the chat

### 1. Current state

`state/current_state.json`

Defines the current governed state, verified gates, locked layers, and authoritative next action id.

### 2. Next action

`state/next_action.json`

Contains one concrete continuation action. It must be executable by a future Bot without guessing.

### 3. Action history

`docs/action_log/`

Append-only records capture what was actually done, what was only statically inspected, what runtime executed, what failed, and what remains blocked.

### 4. Architecture and policy

`docs/`

These files define the system independently of any chat transcript.

### 5. Evidence

Evidence is stored as compact, content-addressed records. Large XSMB data remains on the Data/Build plane. Brain does not ingest the full data lake merely to remember it.

## Chat responsibilities

Chat may:

- explain current state;
- translate user intent into a governed action;
- inspect persistent state;
- propose or execute the recorded next action;
- report evidence and failures.

Chat must NOT:

- invent missing state;
- become the sole memory;
- override the ledger;
- bypass corridors;
- mint capabilities;
- promote artifacts;
- rewrite source truth.

## Bot replacement test

A foundation is continuity-safe only if a fresh Bot with no conversation history can read the repository and answer:

1. What is the architecture?
2. What is the current state?
3. What was the last action?
4. What evidence exists?
5. What failed?
6. What is locked?
7. What is the exact next action?
8. What actions are forbidden?

If any answer depends on hidden chat context, the foundation is incomplete.
