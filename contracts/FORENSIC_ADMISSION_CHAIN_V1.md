# FORENSIC ADMISSION CHAIN V1

## Canonical status

This contract defines ONE forensic admission state machine shared by Project_Brain_AI and Quant_Engine.

There are not multiple independent forensic systems. Gate results are local observations inside one FSM and one append-only evidence ledger.

## Admission chain

```text
DB_EXISTENCE
  -> DB_BINDING
  -> SECRET_RESOLUTION
  -> DB_TLS_ADMISSION
  -> NETWORK_ORIGIN_PROOF
  -> DB_ROUND_TRIP
  -> PROMOTION
```

## Fundamental laws

1. `PASS(G_n) !=> PASS(G_n+1)`.
2. A gate PASS proves only that gate's predicate.
3. A later gate must execute independently and receive fresh evidence.
4. `UNKNOWN` is never converted to PASS by inference.
5. `FAIL` is preserved as evidence.
6. Retry is a new forensic event.
7. Historical receipts are append-only and may never be overwritten or deleted by a retry.
8. External events may not be fabricated by Brain, Bot, chat, or a local workaround.
9. `WAIT_EXTERNAL_EVENT` is a valid active hold, not an error and not permission to invent work.
10. Promotion requires all preceding gates to have independently admissible evidence.

## Gate semantics

- `DB_EXISTENCE`: database resource exists. This does not grant service access.
- `DB_BINDING`: service has an explicit `DATABASE_URL` binding. This does not prove TLS or connectivity.
- `SECRET_RESOLUTION`: the binding resolves through the approved secret-management boundary without exposing the secret to GitHub, logs, action receipts, or Brain output. This does not prove DB connectivity.
- `DB_TLS_ADMISSION`: resolved connection metadata satisfies the admitted TLS policy (`require`, `verify-ca`, `verify-full`). This does not prove durable evidence write/read.
- `NETWORK_ORIGIN_PROOF`: the service reaches the authorized database endpoint through the approved network path. This does not prove persistence integrity.
- `DB_ROUND_TRIP`: one compact metadata envelope is written, read back, and independently verified by SHA-256. This proves durable evidence-path execution.
- `PROMOTION`: final admission decision. It may PASS only when every prerequisite has fresh admissible evidence.

## Non-inheritance rule

```text
DB_EXISTS = PASS
    != DB_BOUND
    != SECRET_RESOLVED
    != DB_TLS_ADMITTED
    != NETWORK_ORIGIN_PROVEN
    != DB_ROUND_TRIP
    != PROMOTION
```

Likewise:

```text
DB_TLS_ADMITTED = PASS
    != DB_ROUND_TRIP
```

## Protected-room model

```text
corridor_key
   +
room_key
   +
inner_latch / external release
   = admission
```

Correct corridor and room keys do not manufacture an inner release.

## Cross-repository ownership

- `Project_Brain_AI`: governance control plane, security/admission, forensic state, evidence integrity.
- `Quant_Engine`: calculation/execution rooms only.
- Data source repositories: source truth only.

Quant_Engine must not recreate Brain's forensic authority.

## Successor protocol

Every successor Bot must, in order:

```text
READ architecture contracts
  -> READ state/current_state.json
  -> READ state/next_action.json
  -> CHECK exact-current evidence
  -> EXECUTE only if current state authorizes it
  -> APPEND action result
  -> UPDATE current/next state atomically in intent
  -> HAND OFF
```

If an action-log document says one next step but `state/next_action.json` says another, the machine-readable `state/next_action.json` is authoritative for execution; the discrepancy must be recorded and resolved without deleting history.

## OOM law

Render Free 512 MB is a hard boundary. 320 MiB remains the conservative guard. No foundation action may bulk-load source datasets into Brain runtime.

## Sealing rule

This V1 contract's semantics are immutable. Any future semantic change requires a new contract version and a new forensic action receipt. Do not silently rewrite V1 meaning.
