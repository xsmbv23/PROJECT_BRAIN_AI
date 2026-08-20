# BRAIN-N114 — Runtime ACTION_RECEIPT Boundary

## What changed

N114 was hardened into a two-boundary design:

```text
RUNTIME BOOT
   |
   +--> read-only historical ACTION_RECEIPT gate
   |       |
   |       +--> missing => admission DENY only
   |
   +--> foundation / access / DB / source checks
   |
   +--> POST-BOUNDARY RECEIPT ISSUER
   |       |
   |       +--> writes compact receipt to durable PostgreSQL
   |
   +--> service becomes LIVE
           |
           +--> GET /governance
                    |
                    +--> read-only exact-current receipt verifier
```

The verifier never calls the issuer.

The boot gate never consults the receipt it has just issued.

This creates the required evidence boundary without allowing the admission
layer to manufacture its own PASS.

## Exact evidence already observed

On deployment commit:

`82f2ac4332ab336af187c6b1458b091c865507a8`

Render instance:

`srv-da0506u1egvs73ftsdng-w5wzm`

The post-boundary issuer successfully emitted:

```text
status                 = ISSUED_FOR_NEXT_RUNTIME
action_id              = BRAIN-N113
receipt_sha256         = 1a652d45a9e1dd53d7a652022032426432cdc9e166d7c6f8cfd87fd511a949e6
evidence_sha           = 6bb0396ff6671ce2fe36fbc20c4c52b6ca662a0f23e91773dbd3c9cc1debe4fc
deployment_identity    = srv-da0506u1egvs73ftsdng-hibernate-855f594546-w5wzm
deployment_identity_type = RENDER_INSTANCE_ID
pass_is_local          = true
promotes               = false
```

The runtime explicitly kept:

```text
admission_gate = DENY
canonical_quorum = DENY
room_02 = LOCKED
staircase = LOCKED
```

Foundation tests remained `209/209 PASS` and tracemalloc remained far below
320 MiB.

## Important correction

The durable receipt is tied to the exact runtime instance. Therefore a receipt
from a previous deployment must NOT be accepted by a new deployment. This is
intentional replay protection.

To prove the receipt for the current deployment without same-boot
self-verification, the current deployment exposes a read-only `/governance`
boundary which performs the durable receipt read/validation. It does not issue
receipts and it does not mutate state.

## Current runtime status

The latest code revision is:

`e23a5baa645753306a1a829a2ffcf72015a8f07b`

Render deployment:

`dep-da38hngu01pc73854hh0`

At the last observation the deployment was `update_in_progress`; its runtime
had started `python brain_server.py` but exact-current `/governance` evidence
has not yet been captured.

Therefore N114 remains:

```text
IMPLEMENTATION = PASS
ISSUER = PROVEN
CURRENT_RECEIPT_VERIFICATION = NOT_YET_PROVEN
PROMOTION = DENY
```

## Successor rule

Never convert `ISSUED_FOR_NEXT_RUNTIME` into `PASS_LOCAL` for the same boot.
The next evidence must come from the read-only governance verifier of the
same deployment instance. A deployment change invalidates the previous
instance-bound receipt.
