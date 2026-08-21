# Worker Runtime V1.4 — Provider Execution Test and Secret/Cost Gate

V1.4 hardens the provider boundary before any real credential is enabled.

## Required execution states

```text
NO_PROVIDER_SECRET
  -> BLOCKED_PROVIDER

INVALID_BUDGET
  -> BLOCKED_PROVIDER

PROMPT_OVER_BUDGET
  -> BLOCKED_PROVIDER

PROVIDER_TIMEOUT / NETWORK_ERROR
  -> RETRYABLE_PROVIDER_ERROR

MALFORMED_PROVIDER_RESPONSE
  -> PROVIDER_MALFORMED_RESPONSE

VALID_PROVIDER_RESPONSE
  -> LLM_COMPLETED + ADVISORY_ONLY
```

## Authority invariant

A provider response is advisory worker output only. It cannot mutate canonical state, open a forensic gate, or promote the project.

## Secret invariant

Credentials are runtime-only inputs. They must not appear in task envelopes, result receipts, reconciliation ledgers, Git history, or logs.

## Budget invariant

Every request is bounded by explicit prompt-character, output-token, and timeout limits. Invalid or missing limits fail closed.

## Testing policy

The fail-closed path is tested without a live provider or secret. A live provider smoke test is a separate operation requiring explicit secret configuration and must not be inferred from unit-test success.
