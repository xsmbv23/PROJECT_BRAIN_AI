# BRAIN-N017 — Live Render Runtime Gate

## Execution evidence

The `xsmb-quant` Render service deployed commit `a68a4384d485b375cdc5c09f595a32e425b52d56` and reached `live` at `2026-08-16T14:57:35Z`.

Render service configuration remains:

- Free plan
- 1 instance
- Docker runtime
- Singapore region
- auto deploy from `main`

Observed service memory after deployment was approximately 13.5 MB on the stable instance, far below the 320 MB conservative guard and 512 MB platform ceiling. CPU was negligible in the sampled interval.

## Brain service

`project-brain-ai` also deployed commit `8661cbe7796d24ee83292e2968abb3ac2ba1c04c` and reached `live` at `2026-08-16T14:59:00Z`.

Observed memory was approximately 29.0 MB at the sampled point. CPU was approximately 0.043 CPU units at the sampled point. This remains well below the 320 MB guard.

## Critical limitation

The Render-native environment update did NOT establish a verified `DATABASE_URL` linkage to the existing Postgres authority. Therefore durable evidence write/read-back is still **NOT VERIFIED**.

No credential was committed to GitHub. No second evidence authority was created. No promotion occurred.

## State

```text
DEPLOYMENT: PASS
MEMORY GUARD: PASS (sampled)
DATABASE LINKAGE: PENDING
DURABLE READ-BACK: PENDING
PROMOTION: DENY
LAYER 1: LOCKED
STAIRCASE: LOCKED
```

## Next action

BRAIN-N018: establish a verified Render-native Postgres linkage using supported platform linkage/secret mechanisms, then perform one compact evidence write and restart-safe read-back. If linkage cannot be proven, remain DENY/PENDING.
