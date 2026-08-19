# ORIGIN_METADATA_PROBE_V1

## Purpose

`ORIGIN_METADATA_PROBE` proves the identity and provenance of a live network source before source data can enter the canonical data-admission chain.

## Required observations

For each requested source URL the probe must capture a compact, non-secret envelope containing:

1. requested hostname;
2. requested scheme;
3. final hostname after redirects;
4. final scheme;
5. redirect chain length;
6. response status;
7. response content type;
8. observed response timestamp;
9. bounded response byte count;
10. source-body SHA-256 computed from the bounded raw capture when capture is admitted;
11. canonicality result;
12. independence identity result.

Credentials, cookies, authorization headers, proxy credentials, and secrets MUST NOT enter the evidence envelope.

## Canonicality rules

```text
REQUESTED_HOST == FINAL_HOST
    does NOT prove canonicality by itself.

FINAL_HOST == known canonical host
    MAY satisfy canonicality only when the source registry independently defines
    that host as canonical for the requested source.

REDIRECT to advertisement/tracker host
    MUST be classified as non-source navigation.

HTTPS is required.
```

## Independence rules

Two sources are independent only when their provenance identities are independently established. Different URLs or subdomains under the same publisher/CDN/control plane are NOT automatically independent.

`DIFFERENT_HOSTNAME_ALONE_IS_NOT_SUFFICIENT_FOR_PROVEN` remains mandatory.

## PASS conditions

The probe may return `PASS` only when all are true:

- HTTPS was observed;
- requested source identity is known;
- final source identity is either identical to the requested canonical identity or is an explicitly registered canonical redirect;
- no advertisement/tracker redirect is classified as source content;
- response metadata is internally consistent;
- source identity is independently established;
- no required field is UNKNOWN;
- the probe evidence is fresh for the current execution cycle;
- the evidence envelope hash is persisted before admission.

## DENY conditions

Any of the following forces `DENY`:

- unknown origin;
- unknown canonicality;
- unknown independence;
- HTTP instead of HTTPS;
- unregistered final host;
- ad/tracker redirect treated as source;
- stale evidence;
- missing evidence hash;
- contradictory metadata;
- oversized/unbounded capture;
- credential leakage.

## State semantics

`PASS` is local to this gate. It is a prerequisite for the next gate and is never inherited by another gate.

The complete admission chain remains:

```text
DB_EXISTENCE
  -> DB_BINDING
  -> DB_TLS_ADMISSION
  -> DB_ROUND_TRIP
  -> PROMOTION
```

and the broader data chain remains:

```text
NETWORK_ORIGIN_PROOF
  -> DURABLE_ROUND_TRIP
  -> PROMOTION
  -> DATA_ADMISSION
  -> RESEARCH_ADMISSION
  -> EVIDENCE_ANALYSIS
  -> REPORTING
```

## Successor instruction

Never implement an origin probe from this document alone. The runtime contract, state machine, current-state evidence, and action log must agree. If they disagree, `UNKNOWN_IS_NOT_PASS` and `DEFAULT_DENY` apply.
