# BRAIN-N067 — QUANT-N002 False-Pass Correction

## Forensic event

A user-supplied claim stated that GitHub Actions run `32098912473` (`#90`) was a PASS.
The Brain independently queried the exact workflow run by its immutable Run ID.

Result:

```text
repository = xsmbv23/Quant_Engine
run_id = 32098912473
job_id = 95595513698
job = test
status = completed
conclusion = failure
```

The `Run #90` display label was therefore correctly rejected as evidence of PASS.

## Exact failure evidence

The workflow executed 82 tests and ended:

```text
FAILED (failures=2, errors=3)
Process completed with exit code 1
```

Observed failures/errors:

1. `test_collection_can_be_partial` — `CoverageReport.missing` returned `datetime.date` while the declared contract/test expects canonical ISO strings.
2. Three N003 anti-illusion tests used invalid four-value fixtures against the explicit Room 01 27-value domain.
3. `test_execution_signature_is_deterministic_for_same_code` expected `python_implementation` at receipt top level although the implementation correctly nests it inside `execution_signature`.
4. One bounded collector test emitted a `ResourceWarning` for an unclosed HTTP response; this is non-gating but was corrected.

## Corrective actions already committed to Quant_Engine main

- `f7b065e2236d8ee69c73b5bb97c72411d7c32908` — canonicalize missing-day evidence to ISO dates.
- `7fd7d01dde96517e87bfa1c4f587384dd11570b7` — replace invalid N003 fixtures with bounded valid 27-value fixtures.
- `1d6e24b0501b190f6c958fcbe08...` — align room receipt test with nested execution signature.
- `1fa007eefa43b68b636347a513a5749ced90853a` — close collector response explicitly.

The final current commit is `1fa007eefa43b68b636347a513a5749ced90853a`.

## FSM decision

```text
QUANT-N002 previous claim = PASS      -> REJECTED
QUANT-N002 verified run   = FAILURE   -> PRESERVED
ACTION_SPACE              = 0
PROMOTION                 = DENY
ROOM_02                    = LOCKED
STAIRCASE                  = LOCKED
```

No domain-truth claim was made. No historical receipt was overwritten.

## Successor doctrine

```text
Run Number (#90) != Run ID != conclusion

Only exact external evidence may move a gate:

EXTERNAL RUN
    -> immutable Run ID
    -> exact commit
    -> workflow identity
    -> completed status
    -> official conclusion
    -> receipt
    -> local gate evaluation
    -> state transition
```

A failed external run is evidence and must be retained. A repaired code commit is **not** itself a PASS receipt. A new workflow run must execute against the repaired exact-current commit before QUANT-N002 can reopen its action space.

## Next

`BRAIN-N068` — consume the fresh QUANT-N002 workflow result for the repaired commit `1fa007eefa43b68b636347a513a5749ced90853a`. If conclusion is failure, preserve and continue repair. If conclusion is success, verify receipt independently before releasing action space. No pass inheritance.
