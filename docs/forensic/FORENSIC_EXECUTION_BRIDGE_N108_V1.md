# N108-EXEC — Minimal Forensic Execution Bridge V1

## Purpose

Acquire one authorized exact-live execution primitive without creating a new trust root.

## Invariants

1. `tools/transport_probe.py` remains the single source of transport truth.
2. The endpoint accepts no command, URL, path, or arbitrary arguments from the caller.
3. The endpoint is a fixed trigger for one fixed subprocess: `python tools/transport_probe.py`.
4. The endpoint does not parse, rewrite, or manufacture the transport receipt.
5. The probe stdout is persisted verbatim as a separate raw receipt.
6. The HTTP response never contains the receipt contents.
7. Authorization requires `FORENSIC_PROBE_TOKEN` and constant-time header comparison.
8. Missing or wrong authorization is `403 DENY_AUTHORIZATION`.
9. Probe failure remains a probe failure; HTTP success cannot promote forensic state.
10. Local execution, proxy execution, replay, probe modification, and fake receipts remain forbidden.

## Flow

```text
Caller
  |
  | X-Forensic-Probe-Token
  v
Fixed endpoint
  |
  | fixed command only
  v
tools/transport_probe.py
  |
  +--> exact transport observation
  |
  +--> JSON TransportReceipt on stdout
  |
  v
Raw receipt file (verbatim stdout)
  |
  v
External verifier / immutable history
  |
  +--> own runtime identity evidence
  +--> SHA-256 binding of raw receipt
  |
  v
N108 PASS prerequisite only
  |
  v
N109
```

## Trust model

The endpoint is a **trigger**, not a proof source and not a trust root.

`HTTP 202` means only that the fixed probe executed and its receipt was persisted. It does not mean the source was admitted, canonicalized, or promoted.

The next gate must independently inspect the persisted receipt and runtime identity evidence.

## Security boundary

The endpoint is intentionally narrow. There is no generic subprocess interface and no caller-controlled probe parameter.

If the authorization secret is absent, the endpoint is unreachable by design.
