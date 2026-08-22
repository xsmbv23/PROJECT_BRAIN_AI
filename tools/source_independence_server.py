"""BOT3 Render compatibility entrypoint.

The canonical BOT3 headless worker lives in orchestration.bot3_worker.
Render historically started this module as the web-service entrypoint; keep
that entrypoint stable while delegating execution to the canonical worker so
BOT3 cannot be accidentally reduced to a one-shot HTTP probe service.
"""
from __future__ import annotations

import runpy


if __name__ == "__main__":
    runpy.run_module("orchestration.bot3_worker", run_name="__main__")
