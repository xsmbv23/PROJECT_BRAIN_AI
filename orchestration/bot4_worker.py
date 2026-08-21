#!/usr/bin/env python3
"""Headless Bot4 worker: reads BOT1 allocation and emits immutable runtime observations."""
from __future__ import annotations
import hashlib,json,os,time,urllib.request
from datetime import datetime,timezone
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
REPO=os.getenv('COORDINATION_REPO','xsmbv23/Project_Brain_AI'); BRANCH=os.getenv('COORDINATION_BRANCH','main'); POLL=int(os.getenv('POLL_SECONDS','60')); PORT=int(os.getenv('PORT','10000')); STOP=False; LAST={"status":"STARTING"}
def get(path):
 u=f'https://raw.githubusercontent.com/{REPO}/{BRANCH}/{path}'; r=urllib.request.Request(u,headers={'User-Agent':'brain-bot4-worker'}); return urllib.request.urlopen(r,timeout=20).read().decode()
def poll():
 global LAST
 raw=get('coordination/worker_allocation_v1.json'); sha=hashlib.sha256(raw.encode()).hexdigest(); outer=json.loads(raw); alloc=json.loads(outer['content']) if isinstance(outer.get('content'),str) else outer
 task=alloc.get('workers',{}).get('BOT4_EXECUTION',{})
 LAST={"status":"ALLOCATION_OBSERVED","worker":"BOT4_EXECUTION","allocation_id":alloc.get('allocation_id'),"cycle_id":alloc.get('cycle_id'),"task":task.get('action'),"allocation_sha256":sha,"authority":"BOT1_ONLY","promotion":"DENY","canonical_mutation":"FORBIDDEN","observed_at":datetime.now(timezone.utc).isoformat()}
 print(json.dumps(LAST,sort_keys=True),flush=True)
class H(BaseHTTPRequestHandler):
 def do_GET(self):
  if self.path=='/health':
   b=json.dumps(LAST,separators=(',',':')).encode(); self.send_response(200); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b); return
  self.send_response(404); self.end_headers()
 def log_message(self,*a): pass
if __name__=='__main__':
 s=ThreadingHTTPServer(('0.0.0.0',PORT),H)
 while not STOP:
  try: poll()
  except Exception as e: LAST={"status":"POLL_ERROR","error":type(e).__name__}; print(json.dumps(LAST),flush=True)
  s.timeout=1; s.handle_request(); time.sleep(POLL)
 s.server_close()
