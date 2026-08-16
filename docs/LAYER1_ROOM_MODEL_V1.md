# LAYER 1 — ROOM / LOCKED-DOOR MODEL V1

## Design decision

Layer 1 should be a separate repository from the Brain governance repository.

The exact repository name is intentionally not fixed yet.

```text
PROJECT_BRAIN_AI
    = governance / memory / security / evidence / orchestration

LAYER 1 REPOSITORY
    = intelligence rooms
```

This separation is desirable because Brain must remain the authority that governs intelligence, not become the intelligence itself.

## Room principle

Every sensor, mechanism, formula, function, algorithm, or model is treated as one **Room**.

A Room is not merely a Python file. It has a contract.

```text
ROOM
├── identity
├── purpose
├── input contract
├── output contract
├── dependencies
├── allowed corridors
├── required capabilities
├── layer classification
├── version
├── source hash
├── implementation
├── tests
├── evidence contract
├── failure states
├── audit policy
└── door state
```

## Door principle

No Room is directly callable just because its code can be imported.

Every entrance requires:

```text
caller identity
    ↓
caller layer
    ↓
corridor authorization
    ↓
capability authorization
    ↓
input contract
    ↓
lineage / evidence
    ↓
nonce / freshness
    ↓
payload integrity
    ↓
ROOM DOOR
    ↓
execution
    ↓
output contract
    ↓
evidence
    ↓
return through authorized corridor
```

Default:

```text
DOOR = LOCKED
```

## Why separate repository

The Layer 1 repository may evolve faster than Brain. It must not be allowed to rewrite Brain governance or data truth.

Brain owns:

- authority;
- layer definitions;
- corridor registry;
- capability policy;
- evidence rules;
- promotion decision;
- continuity state.

Layer 1 owns:

- implementation of intelligence rooms;
- room-local tests;
- room-local calculations;
- room-local experimental artifacts.

Layer 1 does NOT own promotion authority.

## Room taxonomy

Recommended initial classes:

```text
SENSOR ROOM
    observes / measures

MECHANISM ROOM
    transforms a verified input under a deterministic contract

FUNCTION ROOM
    bounded reusable computation

ALGORITHM ROOM
    multi-step deterministic/statistical procedure

MODEL ROOM
    learned or parameterized inference

AGGREGATOR ROOM
    combines outputs from other rooms

DECISION ROOM
    produces a candidate decision/evidence, never final promotion
```

## Dependency direction

Preferred direction:

```text
DATA
 ↓
SENSOR
 ↓
MECHANISM / FUNCTION
 ↓
ALGORITHM
 ↓
MODEL
 ↓
AGGREGATOR
 ↓
DECISION CANDIDATE
 ↓
BRAIN EVIDENCE CORRIDOR
 ↓
GOVERNANCE
```

Forbidden:

```text
ROOM → raw source mutation
ROOM → Brain policy mutation
ROOM → promotion mutation
ROOM → another protected Room without corridor
ROOM → hidden global state
```

## Room-to-room communication

Even inside Layer 1, communication is explicit.

```text
Room A
  │
  │ corridor A→B
  │ capability
  │ evidence
  │ lineage
  ▼
Room B
```

Do not turn the Layer 1 repository into a giant import graph with invisible authority.

Imports may exist for pure implementation helpers, but **authority-bearing communication** must use the governed corridor model.

## Room manifest

Each Room should eventually have a machine-readable manifest, for example:

```text
rooms/<ROOM_ID>/room.yaml
rooms/<ROOM_ID>/README.md
rooms/<ROOM_ID>/src/*
rooms/<ROOM_ID>/tests/*
rooms/<ROOM_ID>/evidence/*
```

The manifest becomes the door specification.

## Door states

```text
LOCKED
  no execution allowed

OPEN_FOR_TEST
  bounded fixture only

OPEN_FOR_VERIFIED_INPUT
  only authorized corridor + capability

QUARANTINED
  implementation exists but evidence/contract failure blocks use

DEPRECATED
  cannot receive new production evidence
```

There should be no generic `OPEN` state.

## Versioning

A Room version change must create a new identity.

```text
ROOM_ID
ROOM_VERSION
SOURCE_SHA
CONTRACT_SHA
TEST_SHA
EVIDENCE_SHA
```

Changing an algorithm silently is forbidden.

## Fosennic implication

The separate Layer 1 repository is not a new floor with unrestricted access.

It is a floor containing many locked rooms whose doors are individually governed by Brain.

The staircase opens only when the foundation is sealed.

Even after the staircase opens, every Room remains locked until its own contract and evidence pass.
