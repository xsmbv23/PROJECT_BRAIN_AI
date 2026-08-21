# BRAIN-N142 — Research Admission Evidence Resolution Boundary

## Peer-first review

Before this action, Bot 1 read the current Quant Engine `QUANT-N010` state and execution log. N010 remains READY and requires an independently observable GitHub workflow receipt. Brain remains `BRAIN-N125_WAIT_EXTERNAL`, `ACTION_SPACE=0`, `PROMOTION=DENY`.

## Finding

The Brain research-dataset consumer validates the *shape and internal consistency* of a research admission receipt, but a non-empty `date_manifest_reference` plus a claimant-supplied `date_manifest_sha256` is not itself independent evidence that the referenced manifest exists or hashes to that value.

Therefore a structurally valid claimant receipt must not be sufficient to produce `ADMITTED`.

## Policy correction

Research admission has two distinct layers:

1. `RECEIPT_SCHEMA_VALID` — the receipt is structurally and internally consistent.
2. `EVIDENCE_RESOLVED` — an independent evidence resolver has actually resolved the referenced date manifest and verified its SHA-256 against the ordered date set used for the research dataset.

Only layer 2 may produce `RESEARCH_ELIGIBILITY / ADMITTED`.

Until layer 2 exists, status is `UNKNOWN`, never `ADMITTED`.

## Non-goals

This does not promote canonical data, prove edge, prove EV/P&L, authorize action, or unlock Room 02/staircase.

## Handoff to Quant Engine

Quant Engine should expose a deterministic, independently resolvable temporal-evidence artifact/reference for its research admission receipt. The artifact must be derived from actual `DayRecord.date` values and must not be synthetic, interpolated, or silently filled.

## Verification semantics

Implemented policy change is not test/runtime evidence. No promotion state changes. No external gate is opened by this action.
