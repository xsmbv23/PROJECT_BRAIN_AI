# N106 HANDOFF

N106 is a semantic clarification only. It does not change the execution gate.

ONE FORENSIC FSM.

Current state is mutable evidence projection; history is immutable append-only.

PASS is local to its gate, prerequisite-only, never inherited. Every gate owns its own evidence.

DB chain:
`DB_EXISTENCE -> DB_BINDING -> DB_TLS_ADMISSION -> DB_ROUND_TRIP -> PROMOTION`

Runtime chain:
`Container Exists -> Container Running -> Shell Active -> Probe Executed -> Receipt Proven`

For both chains:
`NO RECEIPT -> NOT_PROVEN -> HARD_DENY`

The current next action remains the exact-runtime execution primitive for the live deployment. Do not modify source merely to create a probe endpoint. Do not substitute local/proxy evidence.

Layer 1 and staircase remain locked.
