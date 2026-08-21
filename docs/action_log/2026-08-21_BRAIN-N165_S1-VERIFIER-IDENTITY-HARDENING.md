# BRAIN-N165 — S1 Verifier Identity Hardening

## Trigger

E2E S1 audit found that the machine-checkable verifier had not fully caught up with `S1_CANONICAL_EVIDENCE_V2`.

## Finding

The verifier required the V1 field set and only format-checked `raw_byte_sha256` while hashing the referenced artifact for `raw_artifact_sha256`.

That created two integrity gaps:

```text
contract V2 artifact_path / raw_artifact_sha256 / raw_byte_sha256
        !=
verifier V1 required fields
```

and:

```text
raw_byte_sha256
    = 64 hex chars
    !=
raw_byte_sha256 proven against actual bytes
```

A fabricated-but-well-formed raw-byte hash could therefore survive the verifier until a later layer.

## Action

Hardened `tools/verify_s1_canonical_evidence.py` to:

- require the complete V2 identity field set;
- require `artifact_path` to resolve inside the evidence root;
- compute SHA-256 directly from the referenced artifact bytes;
- verify both `raw_artifact_sha256` and `raw_byte_sha256` against those bytes;
- retain fail-closed behavior;
- preserve promotion DENY when any evidence is missing or inconsistent.

Added regression tests covering:

- missing V2 identity fields;
- raw-byte hash mismatch;
- raw-artifact hash mismatch;
- valid V2 fixture pass.

Commits:

```text
verifier = 9d70079701d9ca0c3bec1539c4226369a79ea9b1
 tests   = 6fb42944ac0149369a35f4c5f5a020ac2841f2c
```

## Verification boundary

GitHub currently exposes no workflow run/status for the test commit. Therefore:

```text
IMPLEMENTED       = YES
TESTED             = UNKNOWN
RUNTIME_VERIFIED   = UNKNOWN
S1_ADMISSION       = BLOCKED
PROMOTION          = DENY
```

No evidence was manufactured and no canonical dataset was created.

## Peer coordination

Quant Engine remains responsible for local Layer 1 / source-collector hardening. Brain owns S1 admission semantics. The peer's parallel N011/N012 work cannot substitute for a real durable S1 canonical artifact or admission receipt.

## E2E continuation

Next high-value chain:

```text
S1 verifier hardening
  -> obtain real durable canonical artifact + manifest
  -> S1 admission
  -> S2 research validation
  -> S3 backtest reachability
```

Downstream gates remain locked until their own evidence exists.
