# BRAIN-N070 — FORENSIC STATE RECONCILIATION DOCTRINE

## Purpose

This document is a permanent successor-readable rule. It prevents runtime evidence from silently outrunning persistent state and prevents test evidence from being promoted into domain truth.

## Core invariant

`RUNTIME STATE != PERSISTENT STATE` is a detectable condition called `FORENSIC DRIFT`.

A runtime action/evidence state that is newer than the persistent successor state is classified as:

`DRIFT_TYPE = STATE_LAG_DRIFT`

## Non-negotiable rule

```text
DRIFT != 0
    => PROMOTION = DENY
    => STAIRCASE = LOCKED
    => LAYER_1 = LOCKED
    => NO RECEIPT_2
    => NO CANONICALIZATION
    => NO PARSER_BUILD
    => NO DOMAIN EXECUTION
```

## Evidence separation

The following are different evidence classes and MUST NOT be conflated:

```text
UNIT TEST RECEIPT
COLLECTOR RECEIPT
CANONICAL INPUT
ROOM EXECUTION
DOMAIN TRUTH
```

A unit-test result is not a collector receipt. A collector receipt is not canonical source truth. No test fixture may be promoted merely because tests pass.

## Reconciliation flow

```text
CAPTURE REALITY
      |
      v
CAPTURE PERSISTENT STATE
      |
      v
COMPARE ACTION / COMMIT / GATES
      |
      +---- equal ----> DRIFT = 0
      |
      +---- mismatch -> STATE_LAG_DRIFT
                           |
                           v
                       PROMOTION DENY
                           |
                           v
                   SYNC PERSISTENT STATE
                           |
                           v
                     VERIFY AGAIN
                           |
                    +------+------+
                    |             |
                 DRIFT=0       DRIFT!=0
                    |             |
                    v             v
               NEXT ACTION      HALT
```

## Database admission chain

Database existence, authorization, TLS admission, and durable round-trip are sequential gates. A PASS at an earlier gate does not imply PASS at a later gate.

```text
DB_EXISTS
   -> DB_BINDING
      -> DB_TLS_ADMISSION
         -> DB_ROUND_TRIP
            -> PROMOTION
```

`DB_EXISTS = PASS` never means `DB_ACCESS = PASS`.

`BOUND_TLS = PASS` never means `DB_ROUND_TRIP = PASS`.

Only the evidence belonging to each gate can change that gate's state.

## Current supplied reconciliation evidence

Runtime evidence supplied for N070:

- commit: `f66c80e8a9a95b09df466caa22f7e97f8f6d1d2`
- foundation: PASS
- tests: PASS
- memory peak: 992 KB
- database binding: `DENY_TLS`
- database round-trip: `UNREACHED`
- promotion: DENY
- staircase: LOCKED
- layer 1: LOCKED

Persistent state supplied for comparison:

- last action: `BRAIN-N063`
- next action: `BRAIN-N064`
- state: `WAIT_EXTERNAL_EVENT`

Classification:

`STATE_LAG_DRIFT`

## Required repair

Repair the persistent state to represent the observed runtime evidence. Do not alter code merely to manufacture agreement. Do not create `RECEIPT_2` until drift is zero.

After synchronization, the next action is a drift-zero verification. Only after `DRIFT = 0` may the collector proceed to generate a real collector receipt.

## Forensic law

```text
EVIDENCE -> STATE -> ACTION
```

The chain is one-way for authority. Action must never rewrite historical evidence. State may be advanced only by observed evidence. Historical action logs are append-only.

## EV<0 / edge doctrine

All later domain/quant work must explicitly preserve the edge search and `EV < 0` handling. A negative expected value is a valid decision outcome and must never be converted to a positive signal by fallback, smoothing, synthetic data, lookahead, or parser coercion.

Unknown, missing, conflicting, or unverifiable edge evidence remains `UNKNOWN`/`DENY`, never `PASS`.
