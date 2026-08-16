# QUANT ENGINE L1 ENTRY CORRIDOR V1

## Purpose

This is the only governed conceptual entry boundary from `Project_Brain_AI` into `xsmbv23/Quant_Engine` while Layer 1 is locked.

## Flow

```text
DATA FOUNDATION
      ↓
COMPACT EVIDENCE
      ↓
BRAIN VERIFICATION
      ↓
STAIRCASE GATE S0..S6
      ↓
L1 ENTRY CORRIDOR
      ↓
ROOM DOOR
      ↓
QUANT ENGINE ROOM
```

## Current state

```text
STAIRCASE = LOCKED
L1 ENTRY   = DENY
PROMOTION  = DENY
```

## Required gates when eventually opened

- caller identity;
- caller layer;
- target room identity + version;
- corridor identity + version;
- capability token/reference;
- input contract hash;
- source lineage;
- freshness/nonce;
- payload hash;
- evidence binding;
- output contract;
- audit event.

## Forbidden shortcuts

```text
Chat → Quant Room             DENY
Data → Quant Room             DENY
Quant Room → Canonical Data  DENY
Quant Room → Promotion       DENY
Room A → Room B without corridor DENY
```

The existence of the repository does not open the staircase.
