# BOUNDED FIXTURE PROTOCOL V1

## Purpose

The bounded fixture exists to prove the pipeline mechanics without pretending that a fixture is live XSMB evidence.

## Required labels

Every fixture must declare:

- `fixture_id`
- `fixture_version`
- `fixture_status=VERIFICATION_ONLY`
- `source_type`
- `source_identity`
- `source_sha256`
- `payload_sha256`
- `observed_date` if applicable
- `is_real_world_observation`

If `is_real_world_observation=false`, the record can verify code mechanics but can never satisfy a production-data evidence gate.

## Chain

```text
fixture bytes
   |
   v
SHA verification
   |
   v
FULL_27 structural validation
   |
   +---- invalid ---> DENY
   |
   v
provenance/quorum decision
   |
   +---- conflict ---> CONFLICT / DENY
   |
   v
canonical FULL_27
   |
   v
TAIL_27 derivation
   |
   v
one-day shard
   |
   v
manifest root
   |
   v
compact evidence
   |
   v
Brain corridor
   |
   v
promotion = DENY
```

## Anti-fabrication rule

A fixture may prove:

- parser correctness;
- schema correctness;
- hashing;
- derivation;
- manifest construction;
- corridor mechanics;
- fail-closed behavior.

A fixture may NOT prove:

- historical market truth;
- source quorum for a real date;
- production completeness;
- production promotion eligibility.

## Memory rule

The runner must process the fixture as bounded bytes/records and must not concatenate historical datasets.
