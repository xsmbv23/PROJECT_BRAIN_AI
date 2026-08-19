# Forensic Gate Semantics — Frozen Doctrine

## Purpose

This document freezes the meaning and interaction of forensic states so successor Bots do not interpret one successful observation as permission for a different gate.

## One FSM, not multiple forensic systems

All admission states belong to one forensic state machine. The database chain and source-data chain are related admission paths inside the same governance model; they are not separate forensic systems.

A gate may expose PASS/FAIL/UNKNOWN, but each PASS is **local to that gate**.

```text
PASS_IS_LOCAL_TO_GATE
PASS(G1) != PASS(G2)
PASS(G1) is only a prerequisite for evaluating G2
```

## Database admission chain

```text
DB_EXISTENCE
    |
    v
DB_BINDING
    |
    v
DB_TLS_ADMISSION
    |
    v
DB_ROUND_TRIP
    |
    | WRITE -> READ -> REHASH -> MATCH
    v
PROMOTION
```

Meaning:

- `DB_EXISTENCE=PASS` proves only that the database resource exists.
- `DB_BINDING=PASS` proves only that the service has an explicit runtime binding.
- `DB_TLS_ADMISSION=PASS` proves only that the binding satisfies the TLS contract.
- `DB_ROUND_TRIP=PASS` proves an actual compact write/read/re-hash/match event.
- `PROMOTION=PASS` is a separate authorization decision requiring fresh evidence.

Therefore:

```text
DB_EXISTS = PASS
    != DB_BINDING = PASS

DB_BINDING = PASS
    != DB_TLS_ADMISSION = PASS

DB_TLS_ADMISSION = PASS
    != DB_ROUND_TRIP = PASS

DB_ROUND_TRIP = PASS
    != DOMAIN_TRUTH = PASS
```

## Source-data admission chain

```text
SOURCE_REGISTRY
    |
    v
NETWORK_ORIGIN_PROOF
    |
    v
RAW_CAPTURE
    |
    v
L3 MULTI-SOURCE RECONCILIATION
    |
    v
L4 STABILITY / DRIFT
    |
    v
CANONICAL_DATASET
    |
    v
FEATURE -> EDGE -> EV -> P&L/ROI admission
```

The source chain follows the same non-inheritance rule:

```text
NETWORK_REACHABLE
    != CANONICAL_SOURCE_PROVEN

CANONICAL_SOURCE_PROVEN
    != RAW_SOURCE_TRUTH_ADMITTED

RAW_CAPTURE
    != CANONICAL_DATASET

CANONICAL_DATASET
    != FEATURE_ADMITTED

FEATURE_IMPLEMENTED
    != FEATURE_ADMITTED

EDGE_IMPLEMENTED
    != EDGE_ADMITTED

EV_IMPLEMENTED
    != EV_ADMITTED

ANY_CODE_EXISTS
    != EXECUTABLE_AUTHORITY
```

## Code-state doctrine

The following are deliberately distinct:

```text
IMPLEMENTED
ADMITTED
AUTHORIZED
EXECUTABLE
```

A module may be implemented and still be forbidden to execute because its upstream evidence gate is DENY.

## Waiting is a valid forensic state

If a gate requires an external event and that event has not happened, the correct state is:

```text
READY / WAITING / EXECUTION_NOT_TRIGGERED
```

This is not a failure and not permission to manufacture evidence.

The system must not:

- alter triggers merely to obtain a green result;
- fabricate a receipt;
- substitute a different runtime for the requested runtime;
- treat an absent execution as a PASS;
- overwrite earlier failures;
- infer domain truth from one receipt;
- use a downstream PASS to retroactively satisfy an upstream gate.

## Advertisement and redirect boundary

Advertisements, promotional links, prediction pages, forums, affiliate destinations, navigation links, and redirect targets are outside the source-truth boundary unless a dedicated contract explicitly admits them.

```text
AD_PRESENT_ON_SOURCE_PAGE
    != SOURCE_TRUTH

REDIRECT_TARGET
    != CANONICAL_SOURCE_IDENTITY

FINAL_HOST
    != CANONICAL_IDENTITY_WITHOUT_PROOF

HOSTNAME_DIFFERENCE
    != INDEPENDENCE_PROOF
```

## N011 doctrine

N011 is a transport-only independent runtime observation.

Required runtime identity:

```text
runtime_source_identity = (SOURCE_URL, EXECUTION_RUNTIME)
```

The first Render observation and the GitHub Actions observation are distinct events because runtime identity differs.

N011 may capture HTTP status, byte count, SHA-256, and runtime identity only.

N011 must not parse the source, extract 27 fields, normalize, map domain values, or promote canonical truth.

If the workflow has not been executed, N011 remains:

```text
IMPLEMENTED = YES
EXECUTED = NO
RECEIPT_2 = NOT_CAPTURED
PROMOTION = DENY
```

## Canonical truth rule

```text
single receipt != domain understanding
```

Preferred canonical quorum remains unreachable below three independent valid observations. Two receipts may establish stability evidence, but do not by themselves establish domain truth.

## Successor instruction

Never “optimize” these distinctions away. They are security and forensic invariants, not verbosity. Any future change that merges gates must first prove that the change preserves local PASS semantics, explicit evidence provenance, default deny, and immutability.
