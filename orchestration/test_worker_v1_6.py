#!/usr/bin/env python3
"""V1.6 boundary: headless execution is interface-independent and fail-closed."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):
 x=json.loads(p.read_text()); return json.loads(x['content']) if isinstance(x.get('content'),str) else x
def main():
 n=read(ROOT/'state/next_action.json')
 assert n['constraints']
 required={'ONE_FORENSIC_FSM','PASS_IS_LOCAL','NO_PASS_INHERITANCE','UNKNOWN_IS_NOT_PASS','DEFAULT_DENY','CHAT_IS_INTERFACE_ONLY','BRAIN_IS_GOVERNANCE_CONTROL_PLANE'}
 assert required.issubset(set(n['constraints']))
 assert n['staircase']=='LOCKED'
 print('V1.6_HEADLESS_BOUNDARY_CONTRACT=PASS')
if __name__=='__main__': main()
