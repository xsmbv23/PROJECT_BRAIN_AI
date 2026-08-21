#!/usr/bin/env python3
"""Static/integration contract checks for BOT1 allocation -> worker -> reconciliation."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):
 v=json.loads(p.read_text(encoding='utf-8'))
 if isinstance(v,dict) and isinstance(v.get('content'),str): return json.loads(v['content'])
 return v
def main():
 m=load(ROOT/'coordination/worker_allocation_v1.json')
 n=load(ROOT/'coordination/next_action_matrix_v1.json')
 assert m['issued_by']=='BOT1_LEAD' and m['authority']=='BOT1_ONLY'
 assert m['cycle_id']==n['cycle_id'], 'allocation cycle drift'
 assert m['parallel'] is True
 assert m['shared_mutation']=='FORBIDDEN'
 assert m['canonical_state_mutation']=='BOT1_ONLY'
 assert m['promotion']=='DENY'
 assert set(m['workers'])=={'BOT2_QUANT','BOT4_EXECUTION'}
 for wid,a in m['workers'].items():
  assert a['write_scope'].startswith('coordination/inbox/')
  assert a['deliverable'].startswith('persistent result')
 print('V1.5C_CONTRACT_PASS')
if __name__=='__main__': main()
