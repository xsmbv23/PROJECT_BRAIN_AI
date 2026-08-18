# FORENSIC ADMISSION CHAIN V1

## Immutable rule

There is one Forensic admission state machine, not multiple independent Forensic systems.

A PASS is local to its gate. A PASS never transfers to another gate.
UNKNOWN is never PASS. Default is DENY.

```text
EVIDENCE -> STATE -> ACTION
```

## Admission sequence

```text
RESOURCE_EXISTENCE
    -> SERVICE_BINDING
    -> SECRET_RESOLUTION
    -> TLS_ADMISSION
    -> NETWORK_ORIGIN_PROOF
    -> DURABLE_ROUND_TRIP
    -> PROMOTION
```

## Gate semantics

| Gate | Question | PASS means |
|---|---|---|
| RESOURCE_EXISTENCE | Does the resource exist? | Existence is evidenced |
| SERVICE_BINDING | Is the runtime bound to the required secret reference? | Binding is evidenced |
| SECRET_RESOLUTION | Did runtime resolve the reference without exposing the secret? | Resolution is evidenced |
| TLS_ADMISSION | Does the binding satisfy TLS policy? | TLS admission is evidenced |
| NETWORK_ORIGIN_PROOF | Does the exact current runtime reach the declared origin? | Origin is evidenced |
| DURABLE_ROUND_TRIP | Did a compact envelope write/read and hash-match? | Durable evidence is evidenced |
| PROMOTION | May the durable capability be admitted? | Explicit promotion decision exists |

## No pass inheritance

```text
RESOURCE_EXISTS = PASS
```

does not mean:

```text
SERVICE_ACCESS = PASS
```

Likewise:

```text
TLS_ADMISSION = PASS
```

does not mean:

```text
DURABLE_ROUND_TRIP = PASS
```

Each transition requires its own exact-current observable evidence.

## Security model

The building model is:

```text
corridor credential
      +
room credential
      +
inner release for protected rooms when required
      +
observable evidence at every transition
      =
permission to proceed
```

Knowing that a resource exists is not possession of its access key.

## Mandatory ordering

Before promotion, the infrastructure chain must be complete. Only after promotion may downstream data/research/reporting layers be admitted.

```text
NETWORK_ORIGIN_PROOF
        -> DURABLE_ROUND_TRIP
        -> PROMOTION
        -> DATA_ADMISSION
        -> RESEARCH_ADMISSION
        -> EVIDENCE_ANALYSIS
        -> REPORTING
```

## Reporting boundary

```text
REPORT != ACTION
EVIDENCE != ACTION_AUTHORIZATION
PREDICTION != EXECUTION
```

Reporting is a read-only presentation boundary. It cannot grant authorization.

## Brain boundary

Brain is the Governance Control Plane. It must not become a bulk-data store or heavy computation runtime. Heavy workloads stay outside the Render Free 512 MB Brain runtime; Brain receives compact evidence envelopes.

## Current mandatory state

```text
STATE = WAIT_EXTERNAL_EVENT
ACTION_SPACE = 0
ACTION = MANDATORY_NO_OP
NETWORK_ORIGIN_PROOF = NOT_PROVEN
DURABLE_ROUND_TRIP = NOT_PROVEN
PROMOTION = DENY
LAYER_1 = LOCKED
STAIRCASE = LOCKED
```

## Successor instruction

Future Bots must read this document before acting. They must not infer a later gate from an earlier PASS, an old deployment, an in-memory result, or a hypothesis.

Exact-current observable evidence is authoritative.

While the declared external event is absent, operational mutation is forbidden; only non-mutating forensic documentation is allowed.
