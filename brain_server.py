from brain.server import Handler
from http.server import HTTPServer
import os

from tools.runtime_boot_gate import main as run_foundation_boot_gate


if __name__ == "__main__":
    if run_foundation_boot_gate() != 0:
        raise SystemExit("FOUNDATION_BOOT_GATE_DENY")
    HTTPServer(("0.0.0.0", int(os.environ.get("PORT", "10000"))), Handler).serve_forever()
