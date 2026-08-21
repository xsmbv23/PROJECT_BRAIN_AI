#!/usr/bin/env python3
"""Headless supervisor: observes workers and emits a deterministic runtime receipt."""
from __future__ import annotations
import hashlib,json,os,time,urllib.request,threading
from datetime import datetime,timezone
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
REPO=os.getenv('COORDINATION_REPO','xsmbv23/Project_Brain_AI'); BRANCH=os.getenv('COORDINATION_BRANCH','main'); BOT2=os.getenv('BOT2_URL','https://bot2-headless-worker.onrender.com'); BOT4=os.getenv('BOT4_URL','https://brain-bot4-worker.onrender.com'); POLL=int(os.getenv('POLL_SECONDS','60')); PORT=int(os.getenv('PORT','10000')); HEALTH_RETRIES=int(os.getenv('HEALTH_RETRIES','4')); RETRY_DELAY=float(os.getenv('HEALTH_RETRY_DELAY','2')); LAST={"status":"STARTING"}; RECEIPT={}
def get_raw(path):
 u=f'https://raw.githubusercontent.com/{REPO}/{BRANCH}/{path}'; r=urllib.request.Request(u,headers={'User-Agent':'brain-headless-orchestrator'}); return urllib.request.urlopen(r,timeout=20).read().decode()
def health(url):
 last={"status":"UNREACHABLE","error":"UNKNOWN"}
 for attempt in range(1,HEALTH_RETRIES+1):
  try:
   r=urllib.request.Request(url.rstrip('/')+'/health',headers={'User-Agent':'brain-headless-orchestrator'}); body=urllib.request.urlopen(r,timeout=15).read().decode(); value=json.loads(body); value['health_attempt']=attempt; return value
  except Exception as e:
   last={"status":"UNREACHABLE","error":type(e).__name__,"health_attempt":attempt}
   if attempt < HEALTH_RETRIES: time.sleep(RETRY_DELAY * attempt)
 return last
def cycle():
 raw=get_raw('coordination/worker_allocation_v1.json'); outer=json.loads(raw); alloc=json.loads(outer['content']) if isinstance(outer.get('content'),str) else outer; return alloc,hashlib.sha256(raw.encode()).hexdigest()
def tick():
 global LAST,RECEIPT
 alloc,alloc_sha=cycle(); h2=health(BOT2); h4=health(BOT4); observed=(h2.get('status')=='ALLOCATION_OBSERVED' and h4.get('status')=='ALLOCATION_OBSERVED'); now=datetime.now(timezone.utc).isoformat()
 LAST={"schema":"headless-orchestrator/v1","observed_at":now,"allocation_id":alloc.get('allocation_id'),"cycle_id":alloc.get('cycle_id'),"bot2":h2,"bot4":h4,"canonical_mutation":"BOT1_ONLY","promotion":"DENY","next_action":"RECONCILE_WORKER_OBSERVATIONS","health_status":"PASS" if observed else "HOLD"}
 if observed and RECEIPT.get('allocation_sha256')!=alloc_sha:
  r={"schema":"headless-runtime-receipt/v1","receipt_type":"HEADLESS_RUNTIME_RECEIPT","issued_at":now,"allocation_id":alloc.get('allocation_id'),"cycle_id":alloc.get('cycle_id'),"allocation_sha256":alloc_sha,"bot2_observed_at":h2.get('observed_at'),"bot4_observed_at":h4.get('observed_at'),"execution_authority":"HEADLESS_WORKER","chat_session_execution":"CLOSED","canonical_mutation":"BOT1_ONLY","forensic_promotion":"DENY","result":"OBSERVATION_COMPLETE","next_action":"RECONCILE_WORKER_OBSERVATIONS"}
  r['receipt_sha256']=hashlib.sha256(json.dumps(r,sort_keys=True,separators=(',',':')).encode()).hexdigest(); RECEIPT=r; print(json.dumps(r,sort_keys=True),flush=True)
 print(json.dumps(LAST,sort_keys=True),flush=True)
class H(BaseHTTPRequestHandler):
 def do_GET(self):
  if self.path=='/health' or self.path=='/receipt':
   b=json.dumps(LAST if self.path=='/health' else RECEIPT,separators=(',',':')).encode(); self.send_response(200); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b); return
  self.send_response(404); self.end_headers()
 def log_message(self,*a): pass
if __name__=='__main__':
 s=ThreadingHTTPServer(('0.0.0.0',PORT),H); t=threading.Thread(target=lambda: [tick() or time.sleep(POLL) for _ in iter(int,1)],daemon=True); t.start(); print(json.dumps({"status":"HTTP_READY","component":"HEADLESS_SUPERVISOR","port":PORT}),flush=True); s.serve_forever()
