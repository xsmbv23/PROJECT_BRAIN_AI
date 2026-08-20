# BRAIN-N109 — Protected Exact-Live Trigger Implementation

## Action

The repository already contained a transport probe and a privileged execution bridge, but the bridge exposed execution through a GET path. That violated the separation between read-only health observation and privileged forensic execution.

The bridge has therefore been hardened:

```text
GET /health
GET /governance
GET /
        = READ-ONLY

POST /forensic/trigger-transport-probe
        + X-Forensic-Probe-Token
        = PRIVILEGED EXECUTION
```

The subprocess remains fixed:

```text
[sys.executable, tools/transport_probe.py]
```

The HTTP response is only dispatch/execution evidence. It never returns receipt contents and never performs promotion.

## Immutable forensic rule

This source change does NOT verify the live deployment.

It does NOT mutate:

```text
last_verified_runtime_commit
last_verified_deploy
```

The previous verified runtime remains authoritative until exact-current runtime evidence is observed.

## Capability boundary

The current Render tool surface can inspect the service, deploys and logs, but does not expose an authenticated arbitrary HTTP invocation primitive for:

```text
POST /forensic/trigger-transport-probe
X-Forensic-Probe-Token: <secret>
```

No local curl, proxy, guessed endpoint, or secret exposure is permitted as a substitute.

## Current verdict

```text
SOURCE IMPLEMENTATION       = UPDATED
PRIVILEGED METHOD            = POST ONLY
GET SIDE EFFECT              = REMOVED
TOKEN GATE                   = REQUIRED
SUBPROCESS                    = FIXED
LIVE RUNTIME VERIFICATION    = NOT PROVEN
last_verified_*              = PRESERVED
PROMOTION                    = DENY
SOURCE_CHAIN                 = DENY
ROOM_01                      = LOCKED
LAYER_1                      = LOCKED
STAIRCASE                    = LOCKED
```

## Next admitted action

`BRAIN-N109` remains the only admitted action: execute the exact current Render deployment through the protected POST path, then independently verify the persisted TransportReceipt and bind it to the exact runtime identity.

If the exact live invocation capability is unavailable, N109 remains open and denied. No inference is allowed.
