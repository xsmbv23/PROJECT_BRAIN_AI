#!/usr/bin/env python3
"""V1.5E: headless end-to-end continuity verifier. Fail closed."""
from __future__ import annotations
import json, os, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ALLOC=ROOT/'coordination'/'worker_allocation_v1.json'
BUS=ROOT/'coordination'/'bus.jsonl'
RECEIPT=ROOT/'coordination'/'receipts'/'v1_5e.json'

def unwrap(p):
 x=json.loads(p.read_text(encoding='utf-8'))
 return json.loads(x['content']) if isinstance(x,dict) and isinstance(x.get('content'),str) else x

def health(url):
 try:
  r=urllib.request.urlopen(urllib.request.Request(url.rstrip('/')+'/health',headers={'User-Agent':'brain-v1-5e'}),timeout=15)
  return json.loads(r.read().decode())
 except Exception as e:return {'status':'UNREACHABLE','error':type(e).__name__}

def main():
 a=unwrap(ALLOC); h2=health(os.getenv('BOT2_URL','https://bot2-headless-worker.onrender.com')); h4=health(os.getenv('BOT4_URL','https://brain-bot4-worker.onrender.com'))
 checks={
  'allocation_bot1_only':a.get('issued_by')=='BOT1_LEAD' and a.get('authority')=='BOT1_ONLY',
  'canonical_cycle_bound':a.get('source_action_id')==a.get('cycle_id'),
  'parallel_workers':a.get('parallel') is True,
  'shared_mutation_forbidden':a.get('shared_mutation')=='FORBIDDEN',
  'promotion_denied':a.get('promotion')=='DENY',
  'bot2_headless':h2.get('status')=='ALLOCATION_OBSERVED',
  'bot4_headless':h4.get('status')=='ALLOCATION_OBSERVED',
 }
 status='PASS' if all(checks.values()) else 'HOLD'
 receipt={'schema':'v1_5e_e2e_receipt/v1','created_at':datetime.now(timezone.utc).isoformat(),'allocation_id':a.get('allocation_id'),'cycle_id':a.get('cycle_id'),'status':status,'checks':checks,'bot2':h2,'bot4':h4,'chat_execution_authority':'CLOSED','headless_worker_authority':'ACTIVE','canonical_mutation':'BOT1_ONLY','promotion':'DENY','next_action':'PERSIST_RESULT_AND_RECONCILE' if status=='PASS' else 'REPAIR_HEADLESS_PATH'}
 RECEIPT.parent.mkdir(parents=True,exist_ok=True); RECEIPT.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8'); print(json.dumps(receipt,sort_keys=True)); return 0 if status=='PASS' else 2
if __name__=='__main__':raise SystemExit(main())
