# Forensic Gate Semantics — Frozen Doctrine

## Purpose

This document freezes the meaning and interaction of forensic states so successor Bots do not interpret one successful observation as permission for a different gate.

## One FSM, not multiple forensic systems

All admission states belong to one forensic state machine.

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
    v
PROMOTION
```

A gate may expose PASS/FAIL/UNKNOWN, but each PASS is **local to that gate**.

## Non-inheritance rule

```text
PASS(G1) != PASS(G2)
PASS(G1) is only a prerequisite for evaluating G2
```

No gate may promote another gate by implication.

Examples:

```text
DB_EXISTS = PASS
    !=
DB_AUTHORIZED = PASS
```

```text
DB_TLS_ADMISSION = PASS
    !=
DB_ROUND_TRIP = PASS
```

```text
ROUND_TRIP = PASS
    !=
DOMAIN_TRUTH = PASS
```

## Evidence hierarchy

1. **Existence evidence** proves that a resource exists.
2. **Binding evidence** proves that the service has an explicit binding.
3. **TLS admission evidence** proves the binding satisfies the security contract.
4. **Round-trip evidence** proves an actual compact write/read/hash-match event.
5. **Promotion evidence** proves the system is authorized to promote the resulting evidence into the next architectural state.

Each layer requires its own evidence.

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
- infer domain truth from one receipt.

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
