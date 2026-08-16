# COMMUNICATION SECURITY V1

Every message is a controlled room-to-room transition.

## Envelope

```json
{
  "message_id": "...",
  "project_id": "XSMB_FORENSIC",
  "source_room": "XSMB_DATA",
  "destination_room": "BRAIN_GOVERNANCE",
  "source_layer": "L0_DATA",
  "destination_layer": "L0_GOVERNANCE",
  "corridor_id": "DATA_EVIDENCE_EXPORT_V1",
  "capability": "EVIDENCE_WRITE",
  "nonce": "...",
  "issued_at": "...",
  "expires_at": "...",
  "lineage": ["..."],
  "payload_sha256": "..."
}
```

## Gate order

```text
identity
 ↓
project
 ↓
layer
 ↓
corridor
 ↓
capability
 ↓
nonce/freshness
 ↓
lineage
 ↓
payload hash
 ↓
policy
 ↓
post-verification
 ↓
audit append
```

Failure at any gate => `DENY` and terminal halt for that message.

## Corridor registry

### DATA_EVIDENCE_EXPORT_V1

```text
source: XSMB_DATA
source_layer: L0_DATA
sink: BRAIN_GOVERNANCE
sink_layer: L0_GOVERNANCE
capability: EVIDENCE_WRITE
mutation: false
```

### GOVERNANCE_DECISION_READ_V1

```text
source: BRAIN_GOVERNANCE
source_layer: L0_GOVERNANCE
sink: XSMB_BUILD_RUNTIME
sink_layer: L0_BUILD
capability: GOVERNANCE_READ
mutation: false
```

No unregistered corridor is valid.

## Replay protection

Nonce must be unique within its project/corridor scope and freshness window. A previously accepted nonce is denied on replay.

## Secret policy

Credentials, database URLs, cookies, tokens and private capability material must never appear in messages, evidence payloads, logs or action ledger records.
