"""Offline tests of the write-back rules against a fake backend. No SDK, network or credentials."""
import unittest
from datetime import timedelta
from types import SimpleNamespace

from fieldline import memory_ledger as L
from fieldline import memory_tools as T
from fieldline.memory_governor import MemoryGovernor, MemoryUnavailable, validate
from fieldline.memory_ledger import MemoryLedger, now


class FakeBackend:
    """Per-user store, like Memory Bank's (app, user) scope. Can be told to fail or to time out."""

    def __init__(self):
        self.facts: dict[str, list[str]] = {}
        self.writes = 0
        self.fail_write: Exception | None = None
        self.fail_search: Exception | None = None
        self.fail_erase: Exception | None = None
        self.lose_response = False  # write lands, caller sees a timeout
        self.during_write = None  # callable run while a write is "in flight"

    async def write(self, *, user_id, fact_id, text, session_id):
        self.writes += 1
        if self.during_write:
            await self.during_write()
        if self.fail_write:
            raise self.fail_write
        self.facts.setdefault(user_id, []).append(text)
        if self.lose_response:
            raise TimeoutError

    async def search(self, *, user_id, query):
        if self.fail_search:
            raise self.fail_search
        return list(self.facts.get(user_id, []))

    async def erase(self, *, user_id, text):
        if self.fail_erase:
            raise self.fail_erase
        self.facts[user_id] = [t for t in self.facts.get(user_id, []) if t != text]


def ctx(user, inv="inv-1", call="call-1"):
    return SimpleNamespace(user_id=user, invocation_id=inv, function_call_id=call)


class Base(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.backend = FakeBackend()
        self.gov = MemoryGovernor(MemoryLedger(":memory:"), self.backend)
        T.set_governor(self.gov)
        self.addCleanup(T.set_governor, None)

    async def save(self, user, topic, text, site="", inv="inv-1", call="call-1"):
        res = T.remember(topic, text, ctx(user, inv, call), site_id=site)
        await self.gov.commit(user, "s1")
        return res


class ConsentTests(Base):
    async def test_no_consent_means_zero_writes_and_nothing_staged(self):
        res = await self.save("eng-ravi", "answer_style", "metric torque values")
        self.assertEqual(res["status"], "not_enabled")
        self.assertEqual(self.backend.writes, 0)
        self.assertEqual(self.gov.ledger.list_live("eng-ravi"), [])

    async def test_consent_is_recorded_with_version_and_source(self):
        self.gov.grant_consent("eng-ravi", source="app-settings")
        rec = self.gov.ledger.consent_record("eng-ravi")
        self.assertEqual((rec["state"], rec["policy_version"], rec["source"]), ("granted", L.POLICY_VERSION, "app-settings"))

    async def test_stale_policy_version_needs_fresh_consent(self):
        self.gov.grant_consent("eng-ravi")
        self.gov.ledger._x("UPDATE consent SET policy_version='old'")
        res = await self.save("eng-ravi", "kit", "own fibre splicer")
        self.assertEqual(res["status"], "not_enabled")
        self.assertEqual(self.backend.writes, 0)

    async def test_consent_withdrawn_between_stage_and_commit_blocks_write(self):
        self.gov.grant_consent("eng-ravi")
        T.remember("kit", "own harness", ctx("eng-ravi"))
        self.gov.ledger.set_consent("eng-ravi", "withdrawn", "app-settings")
        await self.gov.commit("eng-ravi")
        self.assertEqual(self.backend.writes, 0)

    async def test_model_has_no_consent_tool(self):
        self.assertFalse([n for n in dir(T) if "consent" in n.lower()])


class SaveTests(Base):
    async def asyncSetUp(self):
        self.gov.grant_consent("eng-ravi")
        self.gov.grant_consent("eng-mia")

    async def test_save_lands_in_backend_and_ledger_as_accepted(self):
        res = await self.save("eng-ravi", "answer_style", "metric torque values")
        self.assertEqual(res["status"], "staged")
        self.assertEqual(self.backend.facts["eng-ravi"], ["metric torque values"])
        self.assertEqual(self.gov.list_memories("eng-ravi")[0]["status"], "accepted")

    async def test_replayed_tool_call_is_one_row_one_write(self):
        await self.save("eng-ravi", "kit", "own harness")
        await self.save("eng-ravi", "kit", "own harness")  # same invocation + call id
        await self.gov.commit("eng-ravi")
        self.assertEqual(self.backend.writes, 1)
        self.assertEqual(len(self.gov.list_memories("eng-ravi")), 1)

    async def test_only_allowlisted_topics_and_clean_text(self):
        for topic, text, site in [("health", "bad back", ""), ("kit", "gate code is 4471", ""),
                                  ("kit", "call me on 07700900123", ""), ("kit", "a\nb", ""),
                                  ("kit", "x" * 201, ""), ("site_note", "park on the lane", ""),
                                  ("kit", "own harness", "NW-0417")]:
            self.assertEqual((await self.save("eng-ravi", topic, text, site))["status"], "refused", (topic, text))
        self.assertEqual(self.backend.writes, 0)
        self.assertIsNone(validate("site_note", "park on the lane", "NW-0522"))

    async def test_site_note_is_tagged_with_its_site(self):
        await self.save("eng-ravi", "site_note", "I park on the lane", "nw-0522")
        self.assertEqual(self.backend.facts["eng-ravi"], ["At site NW-0522: I park on the lane"])


class IsolationTests(Base):
    async def asyncSetUp(self):
        self.gov.grant_consent("eng-ravi")
        self.gov.grant_consent("eng-mia")

    async def test_preference_on_shared_site_never_reaches_other_engineer(self):
        await self.save("eng-ravi", "site_note", "I park on the lane, not the yard", "NW-0417")
        self.assertEqual(await self.gov.recall("eng-mia", "parking at NW-0417"), [])
        self.assertEqual(self.gov.list_memories("eng-mia"), [])
        self.assertEqual(len(await self.gov.recall("eng-ravi", "parking at NW-0417")), 1)

    async def test_other_engineers_memory_id_cannot_be_read_corrected_or_forgotten(self):
        await self.save("eng-ravi", "kit", "own harness")
        mid = self.gov.list_memories("eng-ravi")[0]["memory_id"]
        self.assertEqual(self.gov.correct("eng-mia", "i2", "c2", mid, "x")["status"], "not_found")
        self.assertEqual((await T.forget_memory(mid, ctx("eng-mia")))["status"], "not_found")
        self.assertEqual(len(self.gov.list_memories("eng-ravi")), 1)

    async def test_withdrawing_one_engineer_leaves_the_other_intact(self):
        await self.save("eng-ravi", "kit", "own harness")
        await self.save("eng-mia", "kit", "fibre splicer")
        await self.gov.withdraw_consent("eng-ravi")
        self.assertEqual(self.backend.facts["eng-ravi"], [])
        self.assertEqual(self.backend.facts["eng-mia"], ["fibre splicer"])
        self.assertEqual(await self.gov.recall("eng-mia", "kit"), ["fibre splicer"])


class CorrectAndForgetTests(Base):
    async def asyncSetUp(self):
        self.gov.grant_consent("eng-ravi")
        await self.save("eng-ravi", "answer_style", "imperial torque values")
        self.mid = self.gov.list_memories("eng-ravi")[0]["memory_id"]

    async def test_correct_replaces_old_value_in_backend_ledger_and_recall(self):
        res = T.correct_memory(self.mid, "metric torque values", ctx("eng-ravi", "inv-2", "call-2"))
        self.assertEqual(res["status"], "staged")
        await self.gov.commit("eng-ravi")
        self.assertEqual(self.backend.facts["eng-ravi"], ["metric torque values"])
        self.assertEqual(await self.gov.recall("eng-ravi", "torque"), ["metric torque values"])
        self.assertEqual([m["text"] for m in self.gov.list_memories("eng-ravi")], ["metric torque values"])

    async def test_forget_removes_from_backend_and_clears_text_from_ledger(self):
        res = await T.forget_memory(self.mid, ctx("eng-ravi"))
        self.assertEqual(res["status"], "forgotten")
        self.assertEqual(self.backend.facts["eng-ravi"], [])
        self.assertEqual(self.gov.list_memories("eng-ravi"), [])
        self.assertIsNone(self.gov.ledger.get("eng-ravi", self.mid)["text"])

    async def test_forget_when_provider_erase_fails_still_suppresses_recall_and_retries(self):
        self.backend.fail_erase = ConnectionError("down")
        res = await T.forget_memory(self.mid, ctx("eng-ravi"))
        self.assertEqual(res["status"], "forgotten_pending_provider")
        self.assertEqual(await self.gov.recall("eng-ravi", "torque"), [])  # backend still holds it; filtered
        self.backend.fail_erase = None
        await self.gov.sweep_all()
        self.assertEqual(self.backend.facts["eng-ravi"], [])

    async def test_withdraw_while_erase_failing_stays_erasing_and_blocks_regrant(self):
        self.backend.fail_erase = ConnectionError("down")
        res = await self.gov.withdraw_consent("eng-ravi")
        self.assertEqual(res["pending_provider_erase"], 1)
        self.assertEqual(self.gov.ledger.consent_state("eng-ravi"), "erasing")
        self.assertFalse(self.gov.grant_consent("eng-ravi"))
        self.assertEqual((await self.save("eng-ravi", "kit", "y kit", inv="i9", call="c9"))["status"], "not_enabled")

    async def test_forgotten_while_write_in_flight_is_erased_afterwards(self):
        T.remember("kit", "own harness", ctx("eng-ravi", "inv-3", "call-3"))
        fid = [r for r in self.gov.ledger.list_live("eng-ravi") if r["text"] == "own harness"][0]["id"]

        async def forget_now():
            self.gov.ledger.tombstone("eng-ravi", fid)

        self.backend.during_write = forget_now
        await self.gov.commit("eng-ravi")
        self.assertNotIn("own harness", self.backend.facts["eng-ravi"])

    async def test_expiry_forgets_old_facts(self):
        self.gov.ledger._x("UPDATE facts SET expires_at=?", ((now() - timedelta(days=1)).isoformat(),))
        await self.gov.sweep_all()
        self.assertEqual(self.backend.facts["eng-ravi"], [])
        self.assertEqual(self.gov.list_memories("eng-ravi"), [])


class OutageTests(Base):
    async def asyncSetUp(self):
        self.gov.grant_consent("eng-ravi")

    async def test_write_outage_does_not_raise_and_is_visible_then_retried(self):
        self.backend.fail_write = ConnectionError("down")
        res = await self.save("eng-ravi", "kit", "own harness")  # commit must not raise
        self.assertEqual(res["status"], "staged")
        self.assertEqual(self.gov.list_memories("eng-ravi")[0]["status"], "failed")
        self.backend.fail_write = None
        await self.gov.commit("eng-ravi")  # next turn retries
        self.assertEqual(self.gov.list_memories("eng-ravi")[0]["status"], "accepted")
        self.assertEqual(self.backend.facts["eng-ravi"], ["own harness"])

    async def test_retries_are_bounded(self):
        self.backend.fail_write = ConnectionError("down")
        await self.save("eng-ravi", "kit", "own harness")
        for _ in range(10):
            await self.gov.commit("eng-ravi")
        self.assertEqual(self.backend.writes, L.MAX_ATTEMPTS)
        self.assertEqual(self.gov.list_memories("eng-ravi")[0]["status"], "failed")

    async def test_timeout_after_landing_is_reconciled_not_duplicated(self):
        self.backend.lose_response = True
        await self.save("eng-ravi", "kit", "own harness")
        self.assertEqual(self.gov.list_memories("eng-ravi")[0]["status"], "indeterminate")
        self.backend.lose_response = False
        await self.gov.commit("eng-ravi")
        self.assertEqual(self.backend.facts["eng-ravi"], ["own harness"])  # one copy
        self.assertEqual(self.gov.list_memories("eng-ravi")[0]["status"], "accepted")

    async def test_recall_outage_raises_rather_than_returning_empty(self):
        self.backend.fail_search = ConnectionError("down")
        with self.assertRaises(MemoryUnavailable):
            await self.gov.recall("eng-ravi", "torque")
        self.assertEqual(self.gov.recall_failures, 1)

    async def test_recall_for_user_without_consent_does_not_touch_backend(self):
        self.backend.fail_search = ConnectionError("down")
        self.assertEqual(await self.gov.recall("eng-nobody", "torque"), [])

    async def test_failure_logs_carry_no_fact_text(self):
        self.backend.fail_write = ConnectionError("secret-looking own harness")
        with self.assertLogs("fieldline.memory", level="WARNING") as cap:
            await self.save("eng-ravi", "kit", "own harness")
        self.assertNotIn("own harness", "\n".join(cap.output))


if __name__ == "__main__":
    unittest.main()
