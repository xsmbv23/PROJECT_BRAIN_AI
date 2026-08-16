# BRAIN-N015 — Execution Boundary Closure Record

## Status
IMPLEMENTATION COMPLETE / RUNTIME PERSISTENCE PENDING

## What is now guaranteed by code

`xsmb-quant/verification/evidence_envelope.py` creates a deterministic compact evidence object containing hashes and bounded runtime metadata only. It rejects bulk-payload fields by contract.

## What is NOT yet claimed

No claim is made that Render restart persistence has passed. A repository file is not a runtime persistence test.

## Required runtime gate

```text
LIVE RUN
  -> compact envelope
  -> durable evidence sink
  -> service restart/redeploy
  -> read-back
  -> recompute evidence hash
  -> compare
```

Any missing sink/read-back/hash match is `PENDING/DENY`.

## Fosennic controls

- source truth remains FULL_27;
- TAIL_27 is derived only;
- one source remains quorum-denied;
- evidence cannot contain bulk payloads;
- Render 512MB is hard ceiling;
- 320MB is conservative guard;
- promotion remains DENY;
- Layer 1 and staircase remain LOCKED.

## Next action

BRAIN-N016: implement and verify an actual durable evidence sink and restart-safe read-back. Do not advance to Layer 1 based on code existence alone.
