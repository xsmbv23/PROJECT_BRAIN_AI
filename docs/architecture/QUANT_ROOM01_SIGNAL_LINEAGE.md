# Quant Engine Room 01 — Signal Lineage

This document is a durable handoff from the frozen Brain foundation to Layer 1 `xsmbv23/Quant_Engine`.

## Authority split

- `Project_Brain_AI` = Governance / Forensic control plane and persistent architecture authority.
- `Quant_Engine` = Layer 1 intelligence/execution plane.
- Chat = communication interface only.

The Brain database admission chain remains frozen and must not be reopened by Room 01.

## Legacy lineage

V5.8 and V16.0 legacy cores are **research lineage only**. They may contribute raw hypotheses:

- frequency/distribution counting;
- recency comparison;
- T-1/T-2/T-7 temporal comparison;
- digit head/tail imbalance;
- missing/continuity awareness.

They are not executable authority. Do not copy their Excel/stateful/crawler implementation into Layer 1.

## Critical Room 01 correction

A naive implementation that first excludes the last three days and then tries to calculate T-1/T-2 temporal echoes destroys the very observations needed to calculate those features.

Therefore the correct sequence is:

```text
CANONICAL BOUNDED WINDOW
        |
        v
EXTRACT ALL FEATURES
  |       |       |
  |       |       +--> T-7
  |       +----------> T-2
  +------------------> T-1
        |
        +--> frequency
        +--> digit imbalance
        +--> recency flag
        |
        v
APPLY SELECTION POLICY
        |
        v
CANDIDATE OUTPUT
```

**Recency exclusion is a feature/selection policy, not an early destructive data filter.**

This distinction is mandatory for forensic observability and temporal feature correctness.

## Causal boundary

T-1, T-2 and T-7 refer only to earlier rows already present in the admitted EOD window. Room 01 must never request or reconstruct future observations.

## Quant boundary

Room 01 emits measurable raw features. It does not claim probability, predictive edge, or profitability. Any later scoring/prediction room must treat Room 01 output as observations, not truth about the future.

## Memory boundary

Room 01 maximum working window is 30 days. Whole-history materialization is forbidden.

## Immutable handoff

Successor Bots must preserve this correction. A future implementation that reintroduces early recency filtering before temporal extraction is a regression and must be denied.
