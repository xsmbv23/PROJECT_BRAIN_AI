#!/usr/bin/env python3
"""Deterministic BOT1 worker dispatcher."""
from __future__ import annotations
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
STATE=ROOT/'state'/'current_state.json'; NEXT=ROOT/'state'/'next_action.json'
MATRIX=ROOT/'coordination'/'worker_allocation_v1.json'; OUTBOX=ROOT/'coordination'/'worker_outbox'
def read_json(p):
 v=json.loads(p.read_text(encoding='utf-8'))
 if isinstance(v,dict) and isinstance(v.get('content'),str):
  try:return json.loads(v['content'])
  except json.JSONDecodeError:pass
 return v
def sid(*p):return hashlib.sha256('|'.join(p).encode()).hexdigest()[:20]
def main():
 state=read_json(STATE); nxt=read_json(NEXT); m=read_json(MATRIX); cycle=m['cycle_id']
 if m['issued_by']!='BOT1_LEAD' or m['authority']!='BOT1_ONLY': raise SystemExit('ALLOCATION_AUTHORITY_INVALID')
 for wid,a in m['workers'].items():
  d=OUTBOX/cycle; d.mkdir(parents=True,exist_ok=True); path=d/f'{wid}.json'
  if path.exists(): continue
  task=f'TASK-{cycle}-{wid}-{sid(cycle,wid,a["action"])}'
  env={'schema':'forensic-worker-task/v1','created_at':datetime.now(timezone.utc).isoformat(),'allocation_id':m['allocation_id'],'cycle_id':cycle,'task_id':task,'worker_id':wid,'role':a['department'],'task':a['action'],'deliverable':a['deliverable'],'canonical_state':state['state'],'canonical_next_action':nxt['action_id'],'lease':{'lease_id':f'LEASE-{sid(task)}','state':'PENDING','attempt':1},'write_scope':a['write_scope'],'authority':{'forensic_gate':'NONE','promotion':'DENY','canonical_state_mutation':'FORBIDDEN'},'completion':{'result':'UNKNOWN','evidence_refs':[]}}
  path.write_text(json.dumps(env,indent=2)+'\n',encoding='utf-8'); print('created',path)
if __name__=='__main__':raise SystemExit(main())
