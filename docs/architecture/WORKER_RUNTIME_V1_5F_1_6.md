# Worker Runtime V1.5F → V1.5G → V1.6

## V1.5F — Execution safety
Headless workers may execute only owner-scoped allocations. BOT1 remains the sole canonical allocator and canonical-state authority. Promotion is always denied at worker level.

## V1.5G — Receipt and recovery
Execution is considered durable only when a persistent receipt can be independently re-read and its integrity verified. Missing, stale, duplicated, or conflicting receipts produce HOLD/ESCALATE rather than PASS.

## V1.6 — Interface independence
ChatGPT sessions are interfaces, not execution authorities. Headless workers must continue from persistent coordination state after browser/session closure. The forensic FSM remains unchanged: deliberation, worker output, and consensus cannot promote a gate.

## Next-generation hierarchy
BOT2 Quant/Data owns archival/lineage duties for worker results and doctrine transmission. BOT4 owns execution/reality checks. Future child workers may be attached under each department only through explicit BOT1 allocation.
