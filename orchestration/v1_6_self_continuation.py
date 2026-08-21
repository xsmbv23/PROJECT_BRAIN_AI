#!/usr/bin/env python3
"""Self-continuation planner: never promotes; selects the next safe action from persistent state."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):
 x=json.loads(p.read_text()); return json.loads(x['content']) if isinstance(x.get('content'),str) else x
def main():
 n=read(ROOT/'state/next_action.json')
 required={'ONE_FORENSIC_FSM','PASS_IS_LOCAL','NO_PASS_INHERITANCE','UNKNOWN_IS_NOT_PASS','DEFAULT_DENY','OWN_GATE_EVIDENCE_REQUIRED','FRESH_EVIDENCE_REQUIRED_FOR_PROMOTION','CHAT_IS_INTERFACE_ONLY'}
 missing=sorted(required-set(n.get('constraints',[])))
 if missing:
  print(json.dumps({'decision':'HOLD','reason':'DOCTRINE_INVARIANTS_MISSING','missing':missing})); return 2
 print(json.dumps({'decision':'CONTINUE','action_id':n['action_id'],'phase':n['phase'],'next':'fresh exact-current evidence; preserve DENY/HOLD on insufficiency'})); return 0
if __name__=='__main__': raise SystemExit(main())
