# BRAIN-N087 — Reporting / Edge / EV Invariants

## Status

Documentation-only action. The foundation remains in `MANDATORY_NO_OP` because `NETWORK_ORIGIN_PROOF` is not proven by exact-current runtime evidence.

## Mandatory successor rules

Every future Bot MUST preserve these invariants:

1. **Forensic direction is immutable.** Exact-current runtime evidence outranks old deployment descriptions, cached assumptions, and hypotheses.
2. **Every real edge must be traceable.** A decision edge requires source evidence, target evidence, time alignment, an observable comparison, cost model, and explicit uncertainty state.
3. **Synthetic/fabricated edge is DENY.** If the edge cannot be observed from authoritative evidence, it is not an admitted edge.
4. **EV < 0 is DENY at every level.** Negative EV cannot be hidden by aggregation or by a positive parent-level result. This applies from an individual pair through candidate sets, strategies, sessions, days, portfolios, research admission, and execution admission.
5. **PASS is local to its gate.** No PASS is inherited by another gate.
6. **Unknown is not pass.** Missing probability, payoff, cost, source result, or audit field must remain explicit and deny the affected decision.
7. **Legacy UI remains stable.** Existing interface routes must remain functional. Menu improvements may optimize navigation but must not silently change semantics or erase legacy access.
8. **Audit reports must be detailed and reproducible.** For every date, report how many pairs were predicted, exactly which pairs, how many hit, exactly which hit, total stake, losing stake, payout, net P&L, ROI, EV by pair, aggregate EV, denied pairs, deny reasons, source evidence references, and audit status.
9. **No arithmetic from missing data.** Do not infer hit counts, stakes, losses, payouts, or ROI.
10. **Brain remains governance control plane.** Reporting presents evidence; reporting does not authorize execution.

## Daily report canonical definitions

- `prediction_count`: number of pairs admitted by the prediction gate for that date.
- `predicted_pairs`: exact two-digit pairs, preserving leading zeros.
- `hit_count`: admitted predicted pairs that occur in the authoritative result for that date.
- `hit_pairs`: exact pairs that hit.
- `total_stake`: recorded stakes of admitted predictions only.
- `total_loss`: recorded stakes attributable to losing admitted predictions.
- `total_payout`: gross recorded payout attributable to winning admitted predictions.
- `net_pnl`: `total_payout - total_stake`.
- `roi_percent`: `((total_payout - total_stake) / total_stake) * 100` when stake > 0; otherwise `NOT_APPLICABLE`.
- `ev_by_pair`: EV calculated with the same source/cost assumptions used for admission.
- `ev_total`: aggregate EV, without allowing negative component EV to be concealed.

## Data boundary

Advertising and navigation noise from lottery sites is not source truth. The scraper must separate page chrome/ads from authoritative result content before hashing and derivation.

## OOM boundary

Brain remains dataset-free. Large source data must be streamed, branched, chunked, or delegated to the Data/Engine layer. Do not load unbounded source datasets into the 512 MB Render Free process.

## Next action

Remain at `BRAIN-N086_WAIT_NETWORK_ORIGIN_PROOF` until the real external infrastructure event is observed. This document and `contracts/forensic_quant_reporting_contract_v1.json` are allowed while waiting because they are non-mutating forensic documentation.
