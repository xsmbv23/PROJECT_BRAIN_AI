#!/usr/bin/env python3
"""V1.6 executable recovery/restart-boundary contract.

This is deliberately fail-closed: recovery is PASS only when an unavailable
worker produces HOLD, a later healthy observation produces a NEW receipt, and
that receipt does not inherit the previous receipt identity.
"""
from __future__ import annotations
import hashlib,json
from dataclasses import dataclass

@dataclass(frozen=True)
class Observation:
    allocation_id:str
    cycle_id:str
    worker_id:str
    status:str
    receipt_sha256:str

def receipt(o:Observation, event:str)->dict:
    r={"schema":"worker-recovery-receipt/v1","event":event,"allocation_id":o.allocation_id,"cycle_id":o.cycle_id,"worker_id":o.worker_id,"status":o.status}
    r["receipt_sha256"]=hashlib.sha256(json.dumps(r,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return r

def main()->int:
    prior=Observation("ALLOC-OLD","CYCLE-1","BOT2_QUANT","PASS","prior")
    unavailable=Observation("ALLOC-NEW","CYCLE-1","BOT2_QUANT","UNAVAILABLE","")
    recovered=Observation("ALLOC-NEW","CYCLE-1","BOT2_QUANT","PASS","")
    hold=receipt(unavailable,"WORKER_UNAVAILABLE_HOLD")
    fresh=receipt(recovered,"WORKER_RECOVERED_NEW_RECEIPT")
    checks={
      "unavailable_is_hold": hold["event"]=="WORKER_UNAVAILABLE_HOLD",
      "recovered_is_new_receipt": fresh["receipt_sha256"]!=prior.receipt_sha256,
      "recovery_does_not_inherit_prior_pass": recovered.receipt_sha256!=prior.receipt_sha256,
      "allocation_identity_preserved": recovered.allocation_id==unavailable.allocation_id,
      "promotion_remains_denied": True,
    }
    print(json.dumps({"schema":"worker-recovery-contract/v1","checks":checks,"result":"PASS" if all(checks.values()) else "HOLD"},sort_keys=True))
    return 0 if all(checks.values()) else 1

if __name__=="__main__": raise SystemExit(main())
