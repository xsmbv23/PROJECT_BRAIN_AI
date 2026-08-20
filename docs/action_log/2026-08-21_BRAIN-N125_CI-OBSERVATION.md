# BRAIN-N125 — CI Observation Boundary / Canonical Lineage Hardening

## Session
DUAL-BOT-2026-08-21

## Authority
BOT_1 / `xsmbv23/Project_Brain_AI`

## Canonical forensic rule

There is exactly **ONE Forensic FSM**.

```text
DB_EXISTENCE
 -> DB_BINDING
 -> SECRET_RESOLUTION
 -> DB_TLS_ADMISSION
 -> NETWORK_ORIGIN_PROOF
 -> DB_ROUND_TRIP
 -> PROMOTION
```

The same non-inheritance rule applies to evidence lineage:

```text
PASS(GATE_N) != PASS(GATE_N+1)
```

No PASS crosses a gate or repository boundary.

## N125 execution observation

The exact-current repository commit observed before this action was:

```text
75aa403ad7a4dd8d8e311e893f7059323ac33660
```

After the canonical-lineage hardening patch, the current commit became:

```text
5a5b7141f60bf80140c9b83db890a8c5c3205cc5
```

The GitHub workflow-run observation surface returned **zero observable workflow runs** for that exact commit.

Therefore:

```text
CI_TESTED           = UNKNOWN
CI_RUNTIME_VERIFIED = UNKNOWN
```

No green CI state is inferred from repository structure or from the fact that the workflow file exists.

## Safe repair performed during N125

The validator had a subtle schema-drift weakness: canonical fields were described as authoritative, but legacy aliases could still satisfy production validation when canonical fields were absent.

The validator is now stricter:

- canonical `raw_artifact_sha256` is authoritative;
- canonical `semantic_fingerprint` is authoritative;
- legacy `raw_sha256` / `semantic_sha256` are readable only when `legacy_fixture=true`;
- an unmarked legacy alias cannot satisfy a production admission;
- canonical and legacy fields may coexist, but canonical wins;
- raw byte identity and semantic meaning remain distinct;
- validator remains non-mutating and non-authoritative.

Regression tests were added for all four cases.

## Promotion state

```text
PROMOTION     = DENY
ACTION_SPACE  = 0
ROOM_02       = LOCKED
STAIRCASE     = LOCKED
```

## Parallel Bot 2 handoff

BOT_2 / `xsmbv23/Quant_Engine` remains the safe parallel engineering plane. Its work is a local prerequisite only. It cannot open Brain gates or promote canonical source truth.

The current Quant Engine contract already records the same separation: Brain owns governance; Quant Engine owns Layer 1 execution; a Quant room is a function boundary, not a second Brain security boundary.

## Successor instruction

Do not convert unavailable CI observation into PASS. Do not rewrite the canonical state merely because another bot has progressed. Read `state/current_state.json`, `state/next_action.json`, the dual-bot coordination contract, and the Forensic FSM doctrine before any dependent action.

## Next action

`BRAIN-N125_WAIT_EXTERNAL` — remain at the CI observation boundary until an independently observable exact-current CI receipt exists. Safe non-dependent engineering may continue in Quant Engine under its own action chain, but Brain promotion remains DENY.
