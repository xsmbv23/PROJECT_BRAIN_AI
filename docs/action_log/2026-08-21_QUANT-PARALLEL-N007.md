# QUANT-N007 — Safe Parallel Source Admission Work

## Why this action is allowed

Brain is currently waiting for an independently observable exact-current external CI/governance receipt. Its Brain action space is zero and promotion remains DENY.

The frozen state explicitly allows `QUANT-N007_SOURCE_SEMANTIC_EXTRACTION` as **local prerequisite work only**. This work must not reopen Brain gates or promote evidence. fileciteturn756file0L2-L2

## Work completed

In `xsmbv23/Quant_Engine`:

- added `contracts/source_registry_v1.json`
- added `quant/source_registry.py`
- added `tests/test_source_registry.py`

The registry now makes source admission fail closed:

```text
UNREGISTERED SOURCE
    -> DENY

REGISTERED SOURCE + NO ADAPTER
    -> DENY

REGISTERED SOURCE + ADAPTER
    -> CANDIDATE ONLY
```

Primary pair remains:

```text
ketqua16.net  = PRIMARY_TARGET
xsmb.com.vn    = INDEPENDENT_IDENTITY_B
```

Ads are explicitly classified as non-truth content. The registry does not treat page chrome or advertising as result evidence.

## Frozen boundaries

```text
BRAIN_ACTION_SPACE = 0
BRAIN_PROMOTION = DENY
LAYER_1_PROMOTION = LOCKED
QUANT_REGISTRY_PASS != TRUTH_ADMISSION
ADAPTER_PASS != CANONICAL_TRUTH
CANONICAL_TRUTH != BRAIN_PROMOTION
```

The Quant Engine README already defines the same boundary: Brain is the frozen governance/persistent-memory control plane and Quant Engine is Layer 1 execution/research; Quant rooms cannot reinterpret or reopen Brain foundation. fileciteturn760file0L2-L2

## Next safe Quant action

`QUANT-N008` — inspect and harden collector contracts for `ketqua16` and `xsmb` so each collector emits compact source-identity, transport, official-panel, raw-byte hash, semantic hash, and failure receipts without retaining bulk data in the Brain runtime.

This remains a local prerequisite only. No Brain promotion gate may change as a consequence.
