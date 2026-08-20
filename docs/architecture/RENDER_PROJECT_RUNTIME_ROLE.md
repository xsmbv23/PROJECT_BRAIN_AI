# Render Project Runtime Role

## Canonical Render Project

`prj-da03lim7bikc73ebcti0`

## Principle

The Render Project is part of the Forensic runtime boundary. It is not a decorative dashboard and it is not a replacement for repository authority.

GitHub remains the immutable implementation lineage. Render provides exact-current runtime observations, deployment identity, resource state, logs, and bounded execution evidence.

## Current services observed in the DATA workspace

### Brain control plane

`project-brain-ai`

- service: `srv-da0506u1egvs73ftsdng`
- repository: `xsmbv23/PROJECT_BRAIN_AI`
- runtime: Python
- plan: Free
- region: Oregon
- instances: 1
- start command: `python brain_server.py`
- role: Brain governance control plane

### Data / Quant runtime

`xsmb-quant`

- service: `srv-da0obdpt0dsc73a5ubbg`
- repository: `xsmbv23/xsmb-quant`
- runtime: Docker
- plan: Free
- region: Singapore
- instances: 1
- branch: `main`
- latest observed live commit: `0ae6d1ba6e82f18e676a41ef4fe119ae7329cfb0`
- role: canonical data/quant runtime; source truth remains owned by the data repository

### External observation / source collector

`brain-reality-probe`

- service: `srv-da1df0u417fc73aag830`
- repository: `xsmbv23/Project_Brain_AI`
- runtime: Python
- plan: Free
- region: Oregon
- instances: 1
- start command: `python tools/real_world_collector.py`
- role: external observation / source receipt collector

## Critical finding

`brain-reality-probe` is currently configured as a web service even though its start command is a one-shot collector. It successfully collects `ketqua16.net` source receipts, then exits early. Recent deploys are therefore marked `update_failed` after the collector exits.

This is an infrastructure-shape defect, not a forensic-data defect.

The collector has already demonstrated real source observation:

- source: `https://ketqua16.net/`
- HTTP 200
- TLS 1.3
- raw payload ~57 KB
- source SHA-256 emitted
- parse/normalization/classification intentionally not performed
- truth admission remains DENY

Therefore the collector must not be “fixed” by turning it into a fake persistent web server merely to satisfy Render's web-service lifecycle.

## Correct future shape

The one-shot collector belongs as a scheduled/worker execution boundary, while `project-brain-ai` remains the long-lived Brain governance service.

Conceptually:

```text
Render Project
│
├── project-brain-ai        [LONG-LIVED CONTROL PLANE]
│      │
│      └── governance / admission / forensic state
│
├── xsmb-quant               [DATA / QUANT RUNTIME]
│      │
│      └── canonical source-data processing
│
└── brain-reality-probe      [ONE-SHOT OBSERVER]
       │
       └── source receipt collection
```

## Forensic separation

Never infer:

`Render project contains service` -> `service has permission to all other services`.

Project membership is organizational/runtime topology only.

Authorization remains explicit per corridor and per room.

## OOM policy

All services remain single-instance on Render Free unless explicitly proven safe otherwise.

Brain remains dataset-free.

Collectors must process one bounded source artifact at a time.

No bulk source archive is loaded into Brain.

## Promotion rule

Render runtime evidence can satisfy an observation gate only when the exact-current deployment identity and the observation receipt are both captured.

Render runtime state does not override GitHub lineage or Forensic state contracts.

## Successor rule

A future Bot must audit the Render Project before creating a new runtime service. Existing services must be reused or explicitly classified as obsolete before duplication is allowed.
