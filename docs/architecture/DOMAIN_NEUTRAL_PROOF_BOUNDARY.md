# Domain-Neutral Proof Boundary

The Brain proof layer is deliberately domain-neutral.

## Principle

```text
FORENSIC CONTROL PLANE
        |
        +-- PROOF / BREAK / REPLAY
        |
        +-- XSMB ENGINE
        |
        +-- QUANT ENGINE
        |
        +-- FUTURE ENGINE
```

The proof layer verifies execution integrity, identity, provenance, mutation response, trace integrity, and evidence consistency. It does not own domain semantics.

## Domain separation

### XSMB

Owns lottery-specific source truth, scraper provenance, source-date rules, full27/tail27 lineage, and lottery-specific calculations.

### Quant / Securities

Owns market-source truth, trading calendars, OHLCV/EOD provenance, feature definitions, no-lookahead rules, model identity, backtest semantics, risk/execution logic, and portfolio accounting.

### Brain

Owns governance, admission, forensic evidence, immutable state transitions, corridor/room security, proof protocol, promotion gates, and successor handoff.

## Non-negotiable

A passing proof test must never be interpreted as proof of economic correctness.

```text
REPRODUCIBLE != CORRECT
PROVEN PIPELINE != PROFITABLE STRATEGY
```

This boundary prevents the future Quant Engine from inheriting accidental lottery assumptions and prevents future lottery engines from inheriting financial-market assumptions.
