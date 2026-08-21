# Worker Allocation V1

BOT1 is the only canonical allocator. Deliberation produces recommendations; allocation converts the reconciled decision into department-owned executable work.

## Lifecycle

1. BOT1 issues allocation.
2. BOT2/BOT4 claim only their owner-scoped task.
3. Workers execute in parallel.
4. Each worker writes one append-only result to its exclusive inbox/result scope.
5. BOT1 reconciles results, preserving minority/conflict/stale findings.
6. BOT1 issues the next allocation or HOLD/ESCALATE.

## Authority boundaries

- Worker result is evidence/advisory output, never forensic promotion.
- Workers cannot mutate canonical `state/current_state.json` or `state/next_action.json`.
- Shared mutation is forbidden unless BOT1 explicitly assigns it.
- No worker inherits PASS from another worker or prior cycle.
- Missing or conflicting results produce HOLD/ESCALATE, not PASS.

## Future hierarchy

Departments may later receive child workers (e.g. BOT2.1, BOT3.1, BOT4.1). A child receives authority only through an explicit parent allocation and remains subject to BOT1 canonical gates.
