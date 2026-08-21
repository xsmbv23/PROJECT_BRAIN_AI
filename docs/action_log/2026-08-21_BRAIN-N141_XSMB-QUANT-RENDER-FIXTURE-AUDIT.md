# BRAIN-N141 — xsmb-quant Render Fixture Runtime Audit

## Peer prerequisite read

Before this action, Brain read the current Quant Engine `state/next_action.json`.
Quant Engine remains at `QUANT-N010`; its completion gate requires observable workflow-execution evidence and explicitly preserves `external_runtime_truth=NOT_PROVEN`, with the queued strategy `RESEARCH_DATASET_ADMISSION`.

## Exact-current observation

Render service:

- service: `xsmb-quant`
- service id: `srv-da0obdpt0dsc73a5ubbg`
- runtime: Docker
- region: Singapore
- plan: Free
- repo: `xsmbv23/xsmb-quant`
- start command: Dockerfile `CMD ["python", "foundation_gate.py"]`

Current Dockerfile contains:

`ENV RUN_BOUNDED_FIXTURE=1`

`foundation_gate.py` then automatically executes:

`fixtures/2026-08-12/full27_fixture.json`

through `verification/render_safe_runner.py` on process startup.

The emitted runtime result explicitly sets:

- bounded fixture status based on the runner exit code
- `promotion = DENY`
- fixture path in the evidence

## Assessment

This is **not** evidence of canonical source truth and must never be presented as such. The implementation correctly labels the bounded fixture path as bounded/fixture evidence and keeps promotion denied.

However, because this is the Render runtime of the DATA authority, automatically executing a fixture on every boot is a high-value runtime-boundary hardening target. It can create operational noise and, if consumers later mistake the generic runtime health/status for data-plane reality, can blur the distinction between:

`fixture execution`

and

`REAL_SOURCE observation`.

Therefore:

`FIXTURE_RUNTIME_VERIFIED != REAL_SOURCE_RUNTIME_VERIFIED`

and

`RENDER_SERVICE_LIVE != DATA_TRUTH_PROVEN`.

## Required policy response

Do not silently remove or replace the fixture path. Before mutation, the owning data-plane worker must decide whether the fixture is needed as a bounded boot self-test. If retained, its output must remain explicitly namespaced as fixture evidence and must not satisfy any real-source admission gate.

If disabled by default, the replacement must preserve a bounded health/self-test without creating a synthetic-data truth path.

## Cross-repo handoff

Owner: data-plane / `xsmb-quant` worker.

Required next check:

1. Read this log before changing the Docker runtime boundary.
2. Read the current data-plane admission contract and Render manifest.
3. Decide whether `RUN_BOUNDED_FIXTURE=1` is intentionally required at boot.
4. If it is retained, add an explicit runtime contract proving fixture evidence cannot be consumed as REAL_SOURCE evidence.
5. If it is disabled, preserve bounded health and document the exact evidence transition.
6. Do not claim REAL_SOURCE runtime truth from this service without independent external observation.

## Status

`IMPLEMENTED = NO` for this audit finding; no mutation was made to `xsmb-quant`.

`VERIFIED = OBSERVED_CONFIGURATION_ONLY`

`PROMOTED = NO`

`PROMOTION = DENY`
