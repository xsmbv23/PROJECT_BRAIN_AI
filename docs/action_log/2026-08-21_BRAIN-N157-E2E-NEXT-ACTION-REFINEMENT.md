# BRAIN-N157 — E2E next-action binding

## Peer read

Quant Engine remains on QUANT-N010. Its completion gate requires independently observable workflow execution evidence; the Brain gate remains untouched.

## Finding

The E2E schema exists, but the current next-action state can still be interpreted as a permanent wait state because the immediate executable action is not explicit enough when the external observation gate is blocked.

## E2E binding

Current mission segment:
S2_VALID_RESEARCH

Immediate blocker:
independently observable exact-current evidence for the currently active gate is unavailable; Quant-N010 is safe parallel preparation only.

Own safe action:
continue Brain-side S2 admission-boundary audit without opening any Brain gate; specifically inspect and harden consumer-side acceptance rules that can be validated from repository-local contracts and code.

Peer required action:
Quant must continue N010 and, when available, provide exact workflow run/attempt/commit/result evidence; it must not infer Brain promotion from local workflow success.

Required evidence to exit S2:
1. date-aligned research dataset receipt;
2. temporal evidence reference;
3. date manifest reference and SHA-256;
4. no-lookahead/temporal integrity result;
5. independently verifiable execution/observation receipt.

Downstream impact:
S3_VALID_BACKTEST and all later segments remain blocked until S2 exit evidence exists. Safe preparation is allowed but PASS cannot be inherited downstream.

## Rule

Every next action must connect the immediate task to an E2E segment and identify what evidence changes the segment state. Waiting is a state; it is not a substitute for the safe engineering action available during the wait.
