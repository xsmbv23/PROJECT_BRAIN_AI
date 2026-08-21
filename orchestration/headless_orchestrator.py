#!/usr/bin/env python3
"""Headless supervisor. It never promotes; it continuously observes worker health and allocation."""
from __future__ import annotations
import json,os,time,urllib.request
from datetime import datetime,timezone
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
REPO=os.getenv('COORDINATION_REPO','xsmbv23/Project_Brain_AI'); BRANCH=os.getenv('COORDINATION_BRANCH','main'); BOT2=os.getenv('BOT2_URL','https://bot2-headless-worker.onrender.com'); BOT4=os.getenv('BOT4_URL','https://brain-bot4-worker.onrender.com'); POLL=int(os.getenv('POLL_SECONDS','60')); PORT=int(os.getenv('PORT','10000')); LAST={"status":"STARTING"}
def get_raw(path):
 u=f'https://raw.githubusercontent.com/{REPO}/{BRANCH}/{path}'; r=urllib.request.Request(u,headers={'User-Agent':'brain-headless-orchestrator'}); return urllib.request.urlopen(r,timeout=20).read().decode()
def health(url):
 try:
  r=urllib.request.Request(url.rstrip('/')+'/health',headers={'User-Agent':'brain-headless-orchestrator'}); return json.loads(urllib.request.urlopen(r,timeout=15).read().decode())
 except Exception as e: return {"status":"UNREACHABLE","error":type(e).__name__}
def cycle():
 raw=get_raw('coordination/worker_allocation_v1.json'); outer=json.loads(raw); alloc=json.loads(outer['content']) if isinstance(outer.get('content'),str) else outer
 return alloc

def tick():
 global LAST
 alloc=cycle(); h2=health(BOT2); h4=health(BOT4)
 reachable=(h2.get('status')=='ALLOCATION_OBSERVED' and h4.get('status')=='ALLOCATION_OBSERVED')
 LAST={"schema":"headless-orchestrator/v1","observed_at":datetime.now(timezone.utc).isoformat(),"allocation_id":alloc.get('allocation_id'),"cycle_id":alloc.get('cycle_id'),"bot2":h2,"bot4":h4,"canonical_mutation":"BOT1_ONLY","promotion":"DENY","next_action":"RECONCILE_WORKER_OBSERVATIONS","health_status":"PASS" if reachable else "HOLD"}
 print(json.dumps(LAST,sort_keys=True),flush=True)
class H(BaseHTTPRequestHandler):
 def do_GET(self):
  if self.path=='/health':
   b=json.dumps(LAST,separators=(',',':')).encode(); self.send_response(200); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b); return
  self.send_response(404); self.end_headers()
 def log_message(self,*a): pass
if __name__=='__main__':
 s=ThreadingHTTPServer(('0.0.0.0',PORT),H)
 while True:
  try: tick()
  except Exception as e: LAST={"status":"SUPERVISOR_ERROR","error":type(e).__name__}; print(json.dumps(LAST),sort_keys=True,flush=True)
  s.timeout=1; s.handle_request(); time.sleep(POLL)
