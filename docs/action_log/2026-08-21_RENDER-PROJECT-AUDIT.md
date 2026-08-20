# RENDER-PROJECT-AUDIT — 2026-08-21

## Render Project

`prj-da03lim7bikc73ebcti0`

## Decision

The existing Render Project is part of the runtime evidence boundary and must be audited/reused before creating additional services.

## Exact observed topology

- `project-brain-ai` — `srv-da0506u1egvs73ftsdng` — Python — Free — Oregon — long-lived Brain control plane.
- `xsmb-quant` — `srv-da0obdpt0dsc73a5ubbg` — Docker — Free — Singapore — data/quant runtime.
- `brain-reality-probe` — `srv-da1df0u417fc73aag830` — Python — Free — Oregon — one-shot external observer.
- Render Postgres — `xsmb-runtime-db` — `dpg-da07g0ou01pc738i3ldg-a` — PostgreSQL 18 — Singapore — available.

## Critical runtime observation

`brain-reality-probe` is shaped as a web service but runs `python tools/real_world_collector.py`. The collector successfully fetched `https://ketqua16.net/`, recorded HTTP 200, TLS 1.3, raw-byte count and SHA-256, then intentionally remained observation-only and exited. Render consequently marked the web-service deploy `update_failed`.

This must not be “fixed” by making the collector fake a long-lived web server. The lifecycle shape is wrong; the forensic collector behavior is correct.

## Forensic meaning

The Render Project is topology, not authority.

Project membership does not grant cross-service access.

GitHub remains implementation lineage.

Render remains exact-current runtime evidence.

Brain remains governance/control plane.

Data/Quant remains data owner and calculation runtime.

Collectors remain observation-only.

## Next action

`BRAIN-N064` — correct the observer execution shape using a bounded scheduled/worker boundary while preserving the existing collector, receipt schema, source hash, TLS evidence, default-deny truth admission, and 320 MiB Brain memory guard. Do not duplicate services and do not promote data truth merely because collection succeeded.
