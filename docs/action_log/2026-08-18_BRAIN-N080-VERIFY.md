# BRAIN-N080-VERIFY — Exact-Current Promotion Shortcut Intercepted

## Exact-current deployment evidence

Render service: `srv-da0506u1egvs73ftsdng`

Exact-current deployment:

```text
commit = e07735bd17a3e309eb814e4553404ddc9be3d899
deploy = dep-da21go7lk1mc73aj34sg
status = LIVE
```

The previously expected correction commit `376a22fd7cb26aec1ebba93711769d8d75a45d90` was NOT the deployed commit. The live deployment before this verification was `d447510ffd9e0902cc81f1e93373cd8e399608c4`, whose exact-current source still contained the old shortcut:

```text
BOUND_TLS -> PROMOTION=ALLOW
```

This discrepancy was treated as deployment drift, not as a reason to weaken the forensic gate. A fresh deployment of the current main branch was triggered and reached LIVE as `dep-da21go7lk1mc73aj34sg`.

## Exact boot evidence from LIVE commit e07735bd...

```text
runtime_boot_gate = PASS
commit_sha = e07735bd17a3e309eb814e4553404ddc9be3d899
DB_BINDING = BOUND_TLS
DB_TLS_ADMISSION = PASS
DB_ROUND_TRIP = NOT_PROVEN
PROMOTION = DENY
room_02 = LOCKED
staircase = LOCKED
```

Foundation verifier:

```text
82 expected in the original N080 instruction
85 actual tests
85/85 PASS
```

The increase from 82 to 85 is explicitly recorded as a test-suite expansion; it is not treated as evidence loss.

Memory:

```text
tracemalloc_peak_bytes = 1,626,308
memory_guard_bytes = 335,544,320
```

This remains far below the 320 MiB forensic Render guard.

Deterministic replay verifier:

```text
replay = PASS
contract_hash = 84c0ad581343556dba75a813401d3b8618b060ed96ab5fc44c8e99f3c773205b
contract_hash_repeat = same
no_pass_inheritance = true
pass_locality = true
unknown_not_pass = true
ev_negative_deny = true
ev_nan_deny = true
ev_infinite_deny = true
ev_unknown_deny = true
ev_zero_not_pass = true
external_event_manufactured = false
mutation = NONE
room_02_unlocked = false
staircase_unlocked = false
```

## Critical Forensic finding

The old live deployment proved the importance of exact-current evidence: its source at commit `d447...` still had the shortcut. The new LIVE deployment at `e077...` proves the correction is actually running.

Therefore N080-VERIFY is CLOSED.

## Admission decision

```text
DB_EXISTENCE        = external evidence available
DB_BINDING          = PASS
DB_TLS_ADMISSION    = PASS
DB_ROUND_TRIP       = NOT_PROVEN
PROMOTION           = HARD DENY
LAYER_1             = LOCKED
STAIRCASE           = LOCKED
```

No gate PASS is inherited by the next gate.

## Successor

`BRAIN-N081` — prove the remaining database admission gates without credentials in repository/evidence:

1. establish `NETWORK_ORIGIN_PROOF` where required;
2. execute a real compact metadata write/read round-trip through the already observed `BOUND_TLS` binding;
3. hash the canonical envelope and the read-back envelope with SHA-256;
4. require exact match;
5. only then permit promotion evaluation;
6. keep promotion DENY on any UNKNOWN, mismatch, missing receipt, or non-exact-current deployment.
