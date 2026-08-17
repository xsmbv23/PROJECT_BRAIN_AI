# QUANT-N003-PROOF — Protocol Freeze

## Purpose

This action records the exact N003-PROOF doctrine for successor Bots. It is a protocol freeze, not a proof result.

## Current status

```text
N003 invariants       = IMPLEMENTED_NOT_PROVEN
N003 proof             = READY
N004                  = LOCKED
Brain                 = FROZEN
Promotion             = DENY
```

## Required proof

The actual bounded real replay path must produce compact receipts and prove:

```text
FRESH_1 = REPLAY_1 = REPLAY_2 = FRESH_2
```

across canonical input, semantic feature snapshot, execution signature, semantic trace, output hash, and empty-state reason where applicable.

The proof must then survive adversarial mutation families:

- input mutation
- feature mutation
- trace mutation
- trace collision
- hash-preserving semantic attack
- fake-empty attack
- input sensitivity/dead-pipeline attack
- partial corruption
- cross-environment replay
- filesystem branch attack
- anti-hardcode attack

## Non-inference rules

```text
TEST PASS != EVIDENCE PASS
REPRODUCIBLE != CORRECTNESS
SAME OUTPUT != SAME PATH
UNKNOWN != PASS
LOCAL PASS != RENDER PASS
```

No result may be promoted merely because a test runner exits zero.

## Repository handoff

Quant Engine now contains:

```text
FOUNDATION_ADMISSION.md
FOUNDATION_HANDOFF.md
ROOM_TEMPLATE_V1.md
docs/proof/N003_PROOF_PROTOCOL.md
evidence/N003_PROOF_RECEIPT.schema.json
```

The receipt schema is deliberately compact and contains no bulk source payload or credential.

## Next action

`QUANT-N003-PROOF` — execute the actual proof matrix against the real bounded fixture. Record PASS, DENY, or UNREACHED with compact forensic receipts. Never manufacture a PASS when the actual runtime path cannot be executed.
