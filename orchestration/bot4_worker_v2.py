#!/usr/bin/env python3
"""Headless Bot4 V2 worker bound to allocation V2."""
from __future__ import annotations
import hashlib,json,os,time,urllib.request,threading
from datetime import datetime,timezone
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
REPO=os.getenv('COORDINATION_REPO','xsmbv23/Project_Brain_AI'); BRANCH=os.getenv('COORDINATION_BRANCH','main'); POLL=int(os.getenv('POLL_SECONDS','60')); PORT=int(os.getenv('PORT','10000')); LAST={"status":"STARTING"}; RESULT={"status":"STARTING"}
def get(path):
 r=urllib.request.Request(f'https://raw.githubusercontent.com/{REPO}/{BRANCH}/{path}',headers={'User-Agent':'brain-bot4-worker-v2'}); return urllib.request.urlopen(r,timeout=20).read().decode()
def poll():
 global LAST,RESULT
 try:
  raw=get('coordination/worker_allocation_v2.json'); sha=hashlib.sha256(raw.encode()).hexdigest(); outer=json.loads(raw); alloc=json.loads(outer['content']) if isinstance(outer.get('content'),str) else outer; task=alloc.get('workers',{}).get('BOT4_EXECUTION',{}); nxt=json.loads(get('state/next_action.json'))
  LAST={"status":"ALLOCATION_OBSERVED","worker":"BOT4_EXECUTION","allocation_id":alloc.get('allocation_id'),"cycle_id":alloc.get('cycle_id'),"task":task.get('action'),"allocation_sha256":sha,"authority":"BOT1_ONLY","promotion":"DENY","canonical_mutation":"FORBIDDEN","observed_at":datetime.now(timezone.utc).isoformat()}
  checks={"allocation_present":bool(alloc.get('allocation_id')),"task_present":bool(task.get('action')),"cycle_present":bool(alloc.get('cycle_id')),"canonical_next_action_present":bool(nxt)}
  RESULT={"schema":"headless-worker-result/v2","result_type":"EXECUTION_RECEIPT","worker":"BOT4_EXECUTION","allocation_id":alloc.get('allocation_id'),"cycle_id":alloc.get('cycle_id'),"allocation_sha256":sha,"checks":checks,"result":"PASS" if all(checks.values()) else "HOLD","promotion":"DENY","canonical_mutation":"FORBIDDEN","observed_at":datetime.now(timezone.utc).isoformat()}
  print(json.dumps(RESULT,sort_keys=True),flush=True)
 except Exception as e:
  RESULT={"schema":"headless-worker-result/v2","result_type":"EXECUTION_RECEIPT","worker":"BOT4_EXECUTION","result":"HOLD","error":type(e).__name__,"promotion":"DENY","canonical_mutation":"FORBIDDEN","observed_at":datetime.now(timezone.utc).isoformat()}; print(json.dumps(RESULT,sort_keys=True),flush=True)
class H(BaseHTTPRequestHandler):
 def do_GET(self):
  if self.path in ('/health','/healthz','/') or self.path=='/result':
   payload=RESULT if self.path=='/result' else LAST; b=json.dumps(payload,separators=(',',':')).encode(); self.send_response(200); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b); return
  self.send_response(404); self.end_headers()
 def log_message(self,*a):pass
if __name__=='__main__':
 s=ThreadingHTTPServer(('0.0.0.0',PORT),H); t=threading.Thread(target=lambda:[poll() or time.sleep(POLL) for _ in iter(int,1)],daemon=True); t.start(); s.serve_forever()
