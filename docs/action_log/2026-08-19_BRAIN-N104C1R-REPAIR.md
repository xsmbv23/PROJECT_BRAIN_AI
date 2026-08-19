# BRAIN-N104C.1R.REPAIR — Exact Runtime Receipt Repair

## Decision

The original `BRAIN-N104C.1` receipt remains immutable and remains pinned to its original runtime commit:

`36a1504594d58ed516bbe3ba0d71d81326d69003`

The exact-current runtime is:

`2d4415a875df3582aa26df4598f4f409c3c23027`

Because these differ, the original `N104C.1` receipt gate remains `DENY`.

## Repair action

A fresh receipt was created specifically for:

`BRAIN-N104C.1R.REPAIR`

Receipt:

`evidence/receipts/N104C.1R.REPAIR_action_receipt.json`

Its pinned runtime commit is exactly:

`2d4415a875df3582aa26df4598f4f409c3c23027`

## Non-inheritance rules

- Original N104C.1 receipt was not edited.
- Repair receipt does not replace N104C.1 receipt.
- Repair receipt cannot be used as evidence that N104C.1 itself executed on the new runtime.
- A later Git commit does not inherit an earlier action receipt.
- Transport probe remains locked.
- Canonical quorum remains deny.
- Truth admission remains deny.
- Layer 1 and staircase remain locked.

## Gate result

```text
EXACT_CURRENT_RUNTIME              = 2d4415a...
N104C.1_ORIGINAL_RECEIPT_COMMIT    = 36a1504...
N104C.1R.REPAIR_RECEIPT_COMMIT      = 2d4415a...
ORIGINAL_RECEIPT_MUTATED           = FALSE
RECEIPT_INHERITANCE                = FALSE
REPAIR_RECEIPT_PIN                 = MATCH
N104C.1 ORIGINAL GATE              = DENY
N104C.1R REPAIR RECEIPT GATE       = PASS (receipt created and correctly pinned)
TRANSPORT                          = LOCKED
PROMOTION                          = DENY
LAYER_1                            = LOCKED
STAIRCASE                          = LOCKED
```

## Important forensic distinction

The repair receipt proves the repair artifact is pinned to the exact-current runtime commit. It does **not** retroactively make the old N104C.1 receipt valid. A fresh execution/evidence receipt for the original action would be required if N104C.1 is to be re-executed.
