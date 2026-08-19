# Forensic Admission Chain — Immutable Doctrine

## Core invariant

```text
REALITY
  ↓
EVIDENCE
  ↓
GATE EVALUATION
  ↓
STATE
  ↓
AUTHORIZED ACTION
```

Never reverse this direction.

## State semantics

`PASS_IS_LOCAL_TO_GATE` means a PASS belongs only to the gate that produced it.
A PASS is a prerequisite for downstream evaluation, not inherited authorization.

`UNKNOWN_IS_NOT_PASS`.

`DEFAULT_DENY`.

`NO_PASS_INHERITANCE`.

`NO_STATE_MANIPULATION`: persistent state records the result; it never creates evidence.

`NO_CIRCULAR_EVIDENCE`: a state, action log, receipt, or manifest cannot prove the proposition that it merely declares without independent underlying evidence.

## Capture doctrine

```text
CAPTURE_CAPABILITY
  ≠ CAPTURE_SUCCESS
  ≠ EVIDENCE_VALID
  ≠ CANONICAL_ADMITTED
```

`READY` means specification/implementation path exists and execution has not necessarily begun.
`ACTIVE` means an authorized execution is actually in progress. Neither state is evidence of success.

## Source independence

- Same proven upstream → `INDEPENDENCE=DENY`.
- Unknown upstream → `INDEPENDENCE=UNKNOWN` → DENY.
- Different upstream/hostname is evidence supporting independence, not automatic PASS.
- Independence PASS requires all declared independence factors to be proven.
- Matching results alone are never independence evidence.

## Target immutability

`TARGET_DATE` is fixed before execution.

If the target is `2026-08-12`, absence of that date is a target-date failure/unknown condition. Do not silently substitute the nearest date. A different date is a different execution target.

## Source predeclaration

Source identities are fixed before execution.

Do not silently replace Source B after observing that Source B failed. Fallback sources require a predeclared fallback policy and distinct execution identity.

## Failure taxonomy

`FAIL` and `UNKNOWN` are distinct forensic outcomes.

- `FAIL`: evidence exists and contradicts the gate condition.
- `UNKNOWN`: required evidence is unavailable or insufficient.

Both may result in `DENY`, but their forensic reasons must remain distinct.

## Provenance

Individual hashes are not enough to prove relationships.

A provenance manifest must bind:

- target date
- source identities
- raw artifact SHA-256 values
- canonicalization version
- independence evidence
- reconciliation result
- canonical artifact SHA-256

The manifest itself has a SHA-256 and is retained as evidence.

```text
RAW_A ─┐
       ├─> PROVENANCE_MANIFEST ─> CANONICAL_ARTIFACT ─> CANONICAL_SHA
RAW_B ─┘
```

The manifest proves the relationship between artifacts; a set of hashes alone does not.

## Anti-ad boundary

Advertisements, tracking elements, redirectors, recommendations, and prediction content are non-truth page content.

```text
TRANSPORT
  ↓
PAGE STRUCTURE
  ↓
CANONICAL RESULT BOUNDARY
  ↓
RESULT DATA
```

If the canonical result boundary is ambiguous, DENY.

## Promotion rule

Canonical promotion requires fresh evidence for the exact target and every gate in the admission chain. `current_state.json` is a state reflection, never a source of truth.

## Bot successor rule

Every successor MUST read this doctrine before modifying Foundation or Data Admission. Any proposed optimization that weakens these invariants is invalid, even if it improves apparent completion rate or throughput.
