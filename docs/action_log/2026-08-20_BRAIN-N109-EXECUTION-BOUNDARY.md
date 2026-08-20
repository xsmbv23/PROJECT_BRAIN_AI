# BRAIN-N109 — Exact-Live Execution Boundary

## Objective
Execute the fixed N108 transport bridge against the exact live Brain runtime and obtain a probe-produced TransportReceipt. No source/proxy/local substitute is admissible.

## Exact current Render state observed

Service:

- name: `project-brain-ai`
- service id: `srv-da0506u1egvs73ftsdng`
- current live deployment: `dep-da3601e7bikc7398va4g`
- deployed commit: `0f1bad29e07368ca9b870d2c9bd2c72ef91efa8c`
- status: `live`
- plan: `free`
- instances: `1`
- runtime: Python

## Forensic state-authority finding

The persistent state intentionally keeps:

- `last_verified_runtime_commit = 2d4415a875df3582aa26df4598f4f409c3c23027`
- `last_verified_deploy = dep-da2tjk7qj5pc738ht64g`

while the currently deployed revision is `0f1bad29e07368ca9b870d2c9bd2c72ef91efa8c` / `dep-da3601e7bikc7398va4g`.

This is **not a corruption**. It is an explicit forensic drift marker: deployment existence is not runtime verification. The state authority must not advance `last_verified_*` until exact-current runtime evidence is independently observed.

## Execution attempt / capability boundary

The repository's current `brain_server.py` exposes the foundation boot gate and optional environment-driven capture/DB hooks, but the exact protected HTTP path named by the N109 contract (`/forensic/trigger-transport-probe`) is not present in the inspected current server source. The repository search also did not resolve that endpoint string.

The Render control surface available to this agent can inspect services/deploys/logs and trigger deployments, but it does not provide an authenticated arbitrary HTTP invocation primitive with the protected `FORENSIC_PROBE_TOKEN`.

Therefore the exact N109 action cannot be truthfully marked executed by this agent.

## Forbidden substitutions

Do NOT:

- run the transport probe locally and call it live evidence;
- use a proxy or external relay;
- use a guessed endpoint;
- expose or print `FORENSIC_PROBE_TOKEN`;
- modify the probe merely to make an endpoint appear;
- accept HTTP 202/HTTP success as forensic PASS;
- promote `SOURCE_CHAIN` from source inspection;
- rewrite `last_verified_*` to the newer deployment without runtime evidence.

## Current verdict

```text
N109 exact-live execution = BLOCKED_BY_CAPABILITY_BOUNDARY
CURRENT_DEPLOYMENT       = LIVE_BUT_UNVERIFIED
LAST_VERIFIED_RUNTIME    = PRESERVED
TRANSPORT_RECEIPT        = NOT_PROVEN
SOURCE_PROMOTION         = DENY
ROOM_01                   = LOCKED
LAYER_1                   = LOCKED
STAIRCASE                 = LOCKED
```

## Success condition

N109 may close only when the exact current deployment executes the unchanged fixed bridge and produces a probe-created TransportReceipt whose hash is independently bound to the exact runtime/deployment identity.

## Next admitted action

`BRAIN-N109` remains the only admitted action. The missing capability is an authenticated exact-live request path for the already-authorized fixed bridge. No alternate evidence path may replace it.
