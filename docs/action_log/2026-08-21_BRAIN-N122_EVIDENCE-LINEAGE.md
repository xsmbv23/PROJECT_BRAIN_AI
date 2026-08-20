# BRAIN-N122 — Evidence Lineage Audit

## Scope

Audit the lineage between real source observation, raw evidence, semantic extraction, Quant-derived evidence, Brain admission envelopes, and durable Forensic promotion.

## Result

The repository now contains an explicit canonical lineage contract at:

`docs/FORENSIC_EVIDENCE_LINEAGE.md`

The contract fixes the following invariants:

```text
RAW_HASH != SEMANTIC_HASH
LOCAL_RECEIPT != EXTERNAL_OBSERVATION
PUBLIC_WEB_AGREEMENT != RENDER_RUNTIME_RECEIPT
TRUTH_ADMISSION != DATABASE_PROMOTION
DERIVED_DATA CANNOT OVERWRITE SOURCE_TRUTH
PASS_IS_LOCAL
NO_PASS_INHERITANCE
```

## Current state observed

The authoritative current state reports:

- ONE_FORENSIC_FSM
- PASS_IS_LOCAL
- PASS_IS_PREREQUISITE_ONLY
- NO_PASS_INHERITANCE
- UNKNOWN_IS_NOT_PASS
- DEFAULT_DENY
- OWN_GATE_EVIDENCE_REQUIRED
- FRESH_EVIDENCE_REQUIRED_FOR_PROMOTION
- Brain = governance control plane
- Layer 1 / Room 01 remains the active data-admission room
- Room 02 and staircase remain locked
- action_space = 0
- promotion = DENY

## Important correction for successor Bots

The database admission chain is not a collection of independent Forensic states. It is one monotonic admission chain whose gates answer different questions.

```text
DB_EXISTENCE
 -> DB_BINDING
 -> SECRET_RESOLUTION
 -> DB_TLS_ADMISSION
 -> NETWORK_ORIGIN_PROOF
 -> DB_ROUND_TRIP
 -> PROMOTION
```

A PASS at one gate never becomes a PASS at another gate by inheritance.

Likewise, source/data admission is a distinct evidence domain within the same overall Forensic FSM:

```text
SOURCE_OBSERVATION
 -> RESULT_TRANSPORT
 -> OFFICIAL_PANEL
 -> CANDIDATE
 -> EXCEL_VS_WEB_MATCH
 -> CANONICAL_QUORUM
 -> TRUTH_ADMISSION
```

Truth admission and database promotion remain separate.

## Parallel Bot boundary

Another Bot is actively progressing the repository. This action therefore performs **safe documentation-only work** and does not rewrite `state/current_state.json` or `state/next_action.json`.

The current successor handoff remains authoritative in the repository. This action is additive and must not steal, reset, or fork the other Bot's active action sequence.

## Promotion decision

No promotion was performed.

No Layer 1 unlock beyond the existing state was performed.

No staircase unlock was performed.

No credential was accessed, exposed, fabricated, or stored.

## Next safe action

Wait for the authoritative `state/next_action.json` sequence to advance, then audit the exact-current evidence lineage against the newly produced receipts. Any mismatch must be appended as a new forensic finding rather than repairing history.
