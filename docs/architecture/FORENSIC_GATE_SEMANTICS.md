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
SECRET_RESOLUTION
    |
    v
DB_TLS_ADMISSION
    |
    v
NETWORK_ORIGIN_PROOF
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
- `SECRET_RESOLUTION=PASS` proves only that the runtime resolved the required secret without exposing it.
- `DB_TLS_ADMISSION=PASS` proves only that the binding satisfies the TLS contract.
- `NETWORK_ORIGIN_PROOF=PASS` proves only that the observed connection originates from the admitted runtime path.
- `DB_ROUND_TRIP=PASS` proves an actual compact write/read/re-hash/match event.
- `PROMOTION=PASS` is a separate authorization decision requiring fresh evidence.

Therefore:

```text
DB_EXISTS = PASS
    != DB_BINDING = PASS

DB_BINDING = PASS
    != SECRET_RESOLUTION = PASS

SECRET_RESOLUTION = PASS
    != DB_TLS_ADMISSION = PASS

DB_TLS_ADMISSION = PASS
    != NETWORK_ORIGIN_PROOF = PASS

NETWORK_ORIGIN_PROOF = PASS
    != DB_ROUND_TRIP = PASS

DB_ROUND_TRIP = PASS
    != PROMOTION = PASS
```

### Reachability, not inheritance

A successful earlier gate only makes the next gate **reachable**. It never writes the next gate's state.

```text
G1 PASS
  |
  +--> G2 becomes REACHABLE
         |
         +--> G2 PASS: G3 becomes REACHABLE
         +--> G2 FAIL: stop
         +--> G2 UNKNOWN: stop
```

If an upstream gate is FAIL or UNKNOWN, downstream gates are `UNREACHED`; they are not PASS and must not be inferred.

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

## Parallel-Agent Isolation Doctrine

A second Bot, Quant Engine, or any other subsystem may work in parallel. Parallel work is a **separate execution stream**, not a shortcut through the Brain FSM.

```text
PARALLEL WORK
     |
     +--> may produce LOCAL_PREREQUISITE evidence
     |
     +--> may produce TEST evidence
     |
     +--> may improve code/contracts
     |
     X--> cannot unlock Brain gate automatically
     X--> cannot promote Brain
     X--> cannot inherit Brain PASS
```

Evidence from another Bot is admissible only when the Brain contract explicitly defines:

1. the producing runtime identity;
2. the exact artifact/receipt identity;
3. the evidence type and scope;
4. the freshness requirement;
5. the verification method.

A GitHub workflow being triggered is not evidence that the workflow passed. An unavailable workflow observation remains UNKNOWN.

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

## Render/OOM invariant

Brain is a governance control plane, not a bulk data processor.

```text
512 MB = HARD PLATFORM BOUNDARY
320 MiB = OPERATIONAL GUARD
```

Raw crawl bodies, large datasets, and bulk evidence must remain outside Brain memory. Brain receives compact envelopes and hashes. Data owns source truth; Quant Engine owns calculation.

## Successor instruction

Never “optimize” these distinctions away. They are security and forensic invariants, not verbosity. Any future change that merges gates must first prove that the change preserves local PASS semantics, explicit evidence provenance, default deny, and immutability.

Before taking any action, a successor Bot must read:

```text
state/current_state.json
state/next_action.json
docs/architecture/FORENSIC_GATE_SEMANTICS.md
```

Then it must identify the **current gate** and the **current action-space restriction**. If `action_space=0`, it must not invent an execution receipt or promote state. Safe documentation, contract verification, and other explicitly permitted local prerequisites may continue, but they remain local evidence only.
