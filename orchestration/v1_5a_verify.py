#!/usr/bin/env python3
"""Deterministic V1.5A verification: prove the background path without LLM/provider assumptions."""
from __future__ import annotations
import hashlib, json
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUTBOX=ROOT/'coordination'/'worker_outbox'
RESULTS=ROOT/'coordination'/'worker_results'
RECON=ROOT/'coordination'/'reconciliation'

def now(): return datetime.now(timezone.utc).isoformat()
def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True).encode()).hexdigest()
def lines(path):
    if not path.exists(): return []
    out=[]
    for x in path.read_text(encoding='utf-8').splitlines():
        if x.strip():
            try: out.append(json.loads(x))
            except json.JSONDecodeError: pass
    return out

def main():
    cycle_dirs=sorted([p for p in OUTBOX.iterdir() if p.is_dir()]) if OUTBOX.exists() else []
    if not cycle_dirs:
        raise SystemExit('V1.5A_UNREACHED: no worker task envelope exists')
    cycle=cycle_dirs[-1].name
    checks=[]
    for worker in ('BOT2_QUANT','BOT4_EXECUTION'):
        task=OUTBOX/cycle/f'{worker}.json'
        result=RESULTS/cycle/f'{worker}.jsonl'
        claims=RESULTS/cycle/f'{worker}.claims.jsonl'
        task_records=lines(result)
        checks.append({'worker_id':worker,'task_exists':task.exists(),'claim_exists':claims.exists(),'result_exists':result.exists(),'result_count':len(task_records),'immutable_result_receipt':len(task_records)<=1})
    passed=all(c['task_exists'] and c['claim_exists'] and c['result_exists'] and c['immutable_result_receipt'] for c in checks)
    receipt={'schema':'worker-v1_5a-verification/v1','recorded_at':now(),'cycle_id':cycle,'status':'PASS' if passed else 'HOLD','checks':checks,'browser_dependency':'NONE_FOR_VERIFICATION_PATH','canonical_mutation':'FORBIDDEN','forensic_promotion':'DENY','receipt_sha256':None}
    receipt['receipt_sha256']=digest(receipt)
    path=RECON/f'{cycle}.v1_5a.jsonl'; path.parent.mkdir(parents=True,exist_ok=True); path.open('a',encoding='utf-8').write(json.dumps(receipt,sort_keys=True)+'\n')
    print(json.dumps(receipt,sort_keys=True))
    return 0 if passed else 2
if __name__=='__main__': raise SystemExit(main())
