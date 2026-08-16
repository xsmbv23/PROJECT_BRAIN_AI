# BRAIN-N036 — Inner-Latch / Occupant Release Gate

## New security tier

High-security rooms are not opened merely because the visitor has:

- the correct corridor;
- the correct layer edge;
- the correct capability;
- the correct room key.

For selected high-security rooms, an additional independent gate exists:

```text
CORRIDOR
  ↓ sensor
LIGHT / WARNING
  ↓
ROOM DOOR
  ↓ correct external key + capability
DOOR REQUEST
  ↓
DOORBELL / RING EVENT
  ↓
INNER LATCH REMAINS SECURED
  ↓
AUTHORIZED PRESENCE INSIDE
  ↓
INNER RELEASE
  ↓
ENTRY PERMITTED
```

## Critical invariant

`external_authorized != entry_authorized` for rooms requiring inner release.

The external visitor may prove that they are allowed to request entry, but cannot prove that they are allowed to force the door open.

## Room policy

`InnerLatchPolicy` binds:

- room id;
- security level;
- whether inner release is mandatory;
- authorized occupant capabilities.

## State machine

```text
SECURED → RINGING → RELEASED
```

No direct:

```text
SECURED → RELEASED
```

for a high-security room.

## Fail-closed conditions

- wrong room → DENY
- no external authorization → DENY
- release without active ring → DENY
- unauthorized occupant capability → DENY
- entry before inner release → DENY

## Architectural purpose

This is not a cosmetic UI feature. It is a separate authorization boundary and must remain independent from the corridor sensor and external room lock.

## OOM boundary

The mechanism is a tiny finite-state object. It does not load datasets, historical XSMB data, or external services. It therefore does not materially increase Render memory pressure.

## Status

IMPLEMENTED / VERIFICATION PENDING.

Layer 1 remains LOCKED.
Foundation promotion remains DENY until complete deterministic verification and closure audit.
