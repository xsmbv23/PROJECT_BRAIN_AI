# BRAIN-N110 — One Forensic FSM / Gate Non-Inheritance

The architecture has ONE Forensic FSM, not multiple independent Forensic states.

Each gate owns its own evidence. A PASS is local and is only a prerequisite for the next gate. PASS never inherits.

Database chain:

`DB_EXISTENCE -> DB_BINDING -> DB_TLS_ADMISSION -> DB_ROUND_TRIP -> PROMOTION`

Source chain:

`SOURCE_INDEPENDENCE -> NETWORK_ORIGIN_PROOF -> RESULT_TRANSPORT -> OFFICIAL_RESULT_PANEL -> CANDIDATE -> EXCEL_VS_WEB_MATCH -> CANONICAL_QUORUM -> TRUTH_ADMISSION`

Therefore:

- DB exists does not prove service access.
- Service access does not prove TLS admission.
- TLS admission does not prove a real write/read/hash round-trip.
- Source PASS does not prove runtime execution.
- HTTP acknowledgement does not prove forensic receipt.
- Stale evidence cannot prove the current runtime.

Hard rules: UNKNOWN is NOT PASS; missing evidence is DENY; conflicting evidence is DENY; stale evidence is DENY for the current runtime; no local/proxy/fake/replayed evidence; no automatic privileged trigger at boot.

Successor Bots MUST read this action record and preserve the one-FSM model. Any change that creates implicit PASS inheritance must be rejected and recorded.

Current N109 remains READY/BLOCKED on exact-live external execution. ROOM_01, Layer 1 and staircase remain locked.
