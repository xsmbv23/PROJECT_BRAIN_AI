from __future__ import annotations

import hashlib
import unittest
from tools.validate_chat_to_deliberation import validate


class ChatToDeliberationTests(unittest.TestCase):
    def payload(self) -> dict:
        content = "BOT2 says: audit historical acquisition before canonical backfill."
        return {
            "bridge_id": "CHAT_TO_DELIBERATION_V1",
            "message_id": "CHAT-20260821-001",
            "source": "USER_RELAY",
            "target_bots": ["BOT1_LEAD", "BOT2_QUANT", "BOT3_EXECUTION"],
            "relayed_at": "2026-08-21T11:00:00Z",
            "content_sha256": hashlib.sha256(content.encode()).hexdigest(),
            "content": content,
            "interpretation": {
                "claims": ["historical acquisition needs audit"],
                "proposals": ["audit canonical acquisition path"],
                "challenges": [],
                "requested_actions": ["inspect historical_fetcher"],
                "evidence_refs": [],
                "epistemic_status": "REPORTED",
            },
            "next_action_status": "ACKNOWLEDGED",
        }

    def test_valid_relay(self):
        ok, reason = validate(self.payload())
        self.assertTrue(ok, reason)

    def test_chat_cannot_be_represented_as_verified_without_review(self):
        payload = self.payload()
        payload["interpretation"]["epistemic_status"] = "VERIFIED"
        ok, _ = validate(payload)
        self.assertTrue(ok)

    def test_hash_mismatch_denied(self):
        payload = self.payload()
        payload["content_sha256"] = "0" * 64
        ok, reason = validate(payload)
        self.assertFalse(ok)
        self.assertEqual(reason, "CONTENT_SHA256_MISMATCH")

    def test_invalid_source_denied(self):
        payload = self.payload()
        payload["source"] = "BOT2_DIRECT"
        ok, reason = validate(payload)
        self.assertFalse(ok)
        self.assertEqual(reason, "INVALID_SOURCE")


if __name__ == "__main__":
    unittest.main()
