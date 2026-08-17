# QUANT-N007 HANDOFF — First Real Source Acquisition

Brain remains frozen as Governance Control Plane. The active Layer 1 execution plane is `xsmbv23/Quant_Engine`.

N007 intentionally changes the phase from architecture hardening to real-source acquisition.

## Source selected

`ketqua16.net` is the first narrow real-source acquisition surface. Its public HTTP page was independently verified. The page contains XSMB/traditional lottery content as well as advertisements/navigation content.

## Forensic rule for advertisements

The collector captures HTTP response bytes only. It does not run browser JavaScript, click links, interpret ad instructions, or allow page content to become execution authority. Advertisement content is therefore part of the opaque raw artifact, not an instruction channel.

## Collector

`xsmbv23/Quant_Engine/collectors/ketqua16_raw.py`

Contract:

```text
explicit business_date
 -> bounded HTTP response bytes <= 2 MiB
 -> SHA-256 before parse
 -> append-only raw artifact
 -> compact provenance receipt
 -> acquisition_status boundary
```

No parse, normalization, source merge, or canonical promotion is allowed at this stage.

## Execution plane

The first collector workflow is deliberately outside the Render Free service to preserve the 512 MiB boundary. GitHub Actions is the collector execution plane; Render remains protected from collector memory spikes.

## Admission relationship

The collector produces observation only. It cannot alter Brain's Forensic FSM and cannot grant database admission or canonical truth.

```text
COLLECTION
   !=
ADMISSION
   !=
CANONICAL TRUTH
```

## Current status

```text
source surface verified       = PASS
collector contract            = PASS
bounded memory                = PASS
raw-before-parse              = PASS
ads/javascript authority      = DENY
canonical promotion           = DENY
first real runtime receipt    = UNREACHED
```

The successor must not mistake the existence of the workflow for proof that the workflow executed. A real capture receipt is required evidence.

Next Quant Engine action: `QUANT-N008`.
