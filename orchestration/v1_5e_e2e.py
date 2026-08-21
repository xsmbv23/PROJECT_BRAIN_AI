#!/usr/bin/env python3
"""Triple-worker headless E2E continuity verifier. Fail closed."""
from __future__ import annotations
import json, os, urllib.request
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ALLOC=ROOT/'coordination'/'worker_allocation_v2.json'
RECEIPT=ROOT/'coordination'/'receipts'/'v1_5e.json'
WORKERS={
    'BOT2_QUANT': os.getenv('BOT2_URL','https://brain-bot2-worker-v2.onrender.com'),
    'BOT3_REALITY': os.getenv('BOT3_URL','https://brain-bot3-worker.onrender.com'),
    'BOT4_EXECUTION': os.getenv('BOT4_URL','https://brain-bot4-worker-v2.onrender.com'),
}
def unwrap(p):
    x=json.loads(p.read_text(encoding='utf-8'))
    return json.loads(x['content']) if isinstance(x,dict) and isinstance(x.get('content'),str) else x
def health(url):
    try:
        r=urllib.request.urlopen(urllib.request.Request(url.rstrip('/')+'/health',headers={'User-Agent':'brain-v1-5e'}),timeout=15)
        return json.loads(r.read().decode())
    except Exception as e: return {'status':'UNREACHABLE','error':type(e).__name__}
def result(url):
    try:
        r=urllib.request.urlopen(urllib.request.Request(url.rstrip('/')+'/result',headers={'User-Agent':'brain-v1-5e'}),timeout=15)
        return json.loads(r.read().decode())
    except Exception as e: return {'result':'UNREACHABLE','error':type(e).__name__}
def main():
    a=unwrap(ALLOC); observations={wid:{'health':health(url),'result':result(url)} for wid,url in WORKERS.items()}
    checks={
      'allocation_bot1_only':a.get('issued_by')=='BOT1_LEAD' and a.get('authority')=='BOT1_ONLY',
      'canonical_cycle_bound':a.get('cycle_id')=='BRAIN-N175-S1-CANONICAL-EVIDENCE-VERIFIER',
      'parallel_workers':a.get('parallel') is True,
      'shared_mutation_forbidden':a.get('shared_mutation')=='FORBIDDEN',
      'promotion_denied':a.get('promotion')=='DENY',
      'all_workers_active':set(a.get('active_workers',[]))==set(WORKERS),
    }
    for wid,obs in observations.items():
        checks[f'{wid}_headless']=obs['health'].get('status')=='ALLOCATION_OBSERVED'
        checks[f'{wid}_result_pass']=obs['result'].get('result')=='PASS'
        checks[f'{wid}_identity']=obs['result'].get('allocation_id')==a.get('allocation_id') and obs['result'].get('cycle_id')==a.get('cycle_id')
        checks[f'{wid}_authority']=obs['result'].get('promotion')=='DENY' and obs['result'].get('canonical_mutation')=='FORBIDDEN'
    status='PASS' if all(checks.values()) else 'HOLD'
    receipt={'schema':'v1_5e_triple_worker_e2e_receipt/v1','created_at':datetime.now(timezone.utc).isoformat(),'allocation_id':a.get('allocation_id'),'cycle_id':a.get('cycle_id'),'status':status,'checks':checks,'workers':observations,'chat_execution_authority':'CLOSED','headless_worker_authority':'ACTIVE','canonical_mutation':'BOT1_ONLY','promotion':'DENY','next_action':'PERSIST_RESULT_AND_RECONCILE' if status=='PASS' else 'REPAIR_HEADLESS_PATH'}
    RECEIPT.parent.mkdir(parents=True,exist_ok=True); RECEIPT.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8'); print(json.dumps(receipt,sort_keys=True)); return 0 if status=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
