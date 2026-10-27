import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from pipeline.checkpoints import CheckpointStore
from pipeline.config import Settings
from pipeline.model import ChatModel
from pipeline.resume import resume_case
from pipeline.sources import case_spans, load_case, load_policies
from tests.doubles import ScriptedTransport

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "cases" / "dev"


def tree_hashes(root: Path) -> dict:
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file()}


def model(replies):
    transport = ScriptedTransport(replies)
    return ChatModel("https://gw.test/v1", "gemini-3.5-flash", transport=transport), transport


def copy_run(tmp: str, run: str) -> CheckpointStore:
    shutil.copytree(ROOT / "runs" / run, Path(tmp) / run)
    return CheckpointStore(tmp)


def draft_for(case_id: str, doc_version: str) -> dict:
    return {"decision": "approve", "reasons": [{"id": "R1", "text": "ok", "citations": [f"DAS@{doc_version}:p1:1"]}],
            "conditions": [], "citations": [], "conflicts": [], "gaps": []}


class ResumeTests(unittest.TestCase):
    def run_case(self, case_id, run, store, writer=None, reviewer=None, drafts=ROOT / "drafts"):
        w, wt = writer or model([])
        r, rt = reviewer or (w, wt)
        out = resume_case(CASES / case_id, run, Settings(), w, r, store, drafts_dir=drafts)
        return out, wt, rt

    def test_fully_saved_run_costs_nothing_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = copy_run(tmp, "PA-2026-0141-r3")
            before = tree_hashes(Path(tmp))
            result, transport, _ = self.run_case("PA-2026-0141", "PA-2026-0141-r3", store)
            self.assertEqual(transport.sends, 0)
            self.assertEqual(result["decision"], "approve")
            self.assertEqual(tree_hashes(Path(tmp)), before)

    def test_missing_export_is_rebuilt_in_a_new_run_with_zero_sends(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = copy_run(tmp, "PA-2026-0141-r3")
            (Path(tmp) / "PA-2026-0141-r3" / "export.json").unlink()
            before = tree_hashes(Path(tmp))
            result, transport, _ = self.run_case("PA-2026-0141", "PA-2026-0141-r3", store)
            self.assertEqual(transport.sends, 0)
            self.assertEqual(result["decision"], "approve")
            after = tree_hashes(Path(tmp))
            self.assertTrue(all(after[k] == v for k, v in before.items()))   # parent untouched
            self.assertIn("PA-2026-0141-r4/export.json", after)
            # a second request reconnects to the continuation: still no sends, no further run
            self.run_case("PA-2026-0141", "PA-2026-0141-r3", store)
            self.assertEqual(tree_hashes(Path(tmp)), after)

    def test_resubmitted_statement_invalidates_source_writer_review_but_not_constraints(self):
        case = load_case(CASES / "PA-2026-0147")
        ids = {s.span_id for s in case_spans(case, load_policies())}
        draft = draft_for("PA-2026-0147", "2")
        review = {"verdict": "accept", "claims": [{"reason_id": "R1", "support": "supported", "span_ids": ["DAS@2:p1:1"]}],
                  "findings": []}
        self.assertIn("DAS@2:p1:1", ids)
        with tempfile.TemporaryDirectory() as tmp:
            store = copy_run(tmp, "PA-2026-0147-r1")
            before = tree_hashes(Path(tmp))
            result, transport, _ = self.run_case("PA-2026-0147", "PA-2026-0147-r1", store,
                                                 writer=model([draft, review]), drafts=Path(tmp) / "none")
            self.assertEqual(transport.sends, 2)
            after = tree_hashes(Path(tmp))
            self.assertTrue(all(after[k] == v for k, v in before.items()))
            man = json.loads((Path(tmp) / "PA-2026-0147-r2" / "manifest.json").read_text())
            stages = man["continuation"]["stages"]
            self.assertEqual(stages["constraints"], {"reused_from": "PA-2026-0147-r1"})
            self.assertTrue(stages["writer"]["executed"] and stages["review"]["executed"])
            self.assertIn("source spans or parser changed", man["continuation"]["invalidated"]["source"][0])
            sent = json.dumps(transport.sent)
            self.assertIn("DAS@2:p1:1", sent)
            self.assertNotIn("DAS@1:", sent)       # the edited diagnostic and old spans never reach the model
            self.assertEqual(store.load("PA-2026-0147-r2", "writer")["payload"], draft)

    def test_amended_draft_keeps_writer_inputs_but_rereviews(self):
        review = {"verdict": "accept", "claims": [{"reason_id": "R1", "support": "supported", "span_ids": []},
                                                  {"reason_id": "R2", "support": "supported", "span_ids": []}],
                  "findings": []}
        with tempfile.TemporaryDirectory() as tmp:
            store = copy_run(tmp, "PA-2026-0152-r1")
            result, writer_transport, transport = self.run_case("PA-2026-0152", "PA-2026-0152-r1", store,
                                                                reviewer=model([review]))
            self.assertEqual(writer_transport.sends, 0)     # no writer call
            self.assertEqual(transport.sends, 1)            # only the review
            self.assertIn("obscure-glazed", result["conditions"][0])
            man = json.loads((Path(tmp) / "PA-2026-0152-r2" / "manifest.json").read_text())
            self.assertEqual(man["review"]["draft_revision"], "r2")
            self.assertIn("draft_sha256", man["review"])
            # asking again finds the new review qualified
            _, transport2, _ = self.run_case("PA-2026-0152", "PA-2026-0152-r1", store)
            self.assertEqual(transport2.sends, 0)

    def test_review_is_not_committed_if_draft_changes_during_review(self):
        from pipeline.stages import StageFailed
        review = {"verdict": "accept", "claims": [{"reason_id": "R1", "support": "supported", "span_ids": []},
                                                  {"reason_id": "R2", "support": "supported", "span_ids": []}],
                  "findings": []}
        with tempfile.TemporaryDirectory() as tmp:
            drafts = Path(tmp) / "drafts"
            shutil.copytree(ROOT / "drafts", drafts)
            store = copy_run(tmp, "PA-2026-0152-r1")
            rev = model([review])
            real = rev[1].__call__

            def amend_midway(*args):
                out = real(*args)
                path = drafts / "PA-2026-0152" / "r3.json"
                rec = json.loads((drafts / "PA-2026-0152" / "r2.json").read_text())
                rec["revision"] = "r3"
                rec["draft"]["gaps"] = ["new gap"]
                path.write_text(json.dumps(rec))
                return out
            rev[0].transport = amend_midway
            with self.assertRaises(StageFailed):
                self.run_case("PA-2026-0152", "PA-2026-0152-r1", store, reviewer=rev, drafts=drafts)
            self.assertIsNone(store.load("PA-2026-0152-r2", "review"))

    def test_changed_model_setting_rejects_saved_stages(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = copy_run(tmp, "PA-2026-0141-r3")
            w, t = model([])
            w.model = "another-model"
            with self.assertRaises(AssertionError):     # the double refuses an unscripted send
                resume_case(CASES / "PA-2026-0141", "PA-2026-0141-r3", Settings(), w, w, store)
            self.assertEqual(t.sends, 1)

    def test_stage_by_stage_like_the_served_route(self):
        """Each ADK agent builds its own Continuation; only continuation_run_id travels in state."""
        from pipeline import stages
        from pipeline.constraints import site_constraints
        from pipeline.resume import Continuation
        review = {"verdict": "accept", "claims": [{"reason_id": "R1", "support": "supported", "span_ids": []},
                                                  {"reason_id": "R2", "support": "supported", "span_ids": []}],
                  "findings": []}
        case = load_case(CASES / "PA-2026-0152")
        spans = case_spans(case, load_policies())
        with tempfile.TemporaryDirectory() as tmp:
            store = copy_run(tmp, "PA-2026-0152-r1")
            w, wt = model([])
            r, rt = model([review])
            make = lambda rid: Continuation(store, "PA-2026-0152-r1", case, spans, Settings(), w, r,
                                            ROOT / "drafts", run_id=rid)
            c1 = make(None)
            draft = c1.obtain_draft(lambda: stages.run_writer(w, case, spans, 60000))
            c2 = make(c1.run_id)
            c2.draft = draft
            rev = c2.obtain("review", lambda: stages.run_review(r, draft, spans, 60000))
            c3 = make(c2.run_id)
            c3.draft = draft
            c3.obtain("source", lambda: ({"span_ids": [sp.span_id for sp in spans]}, {}))
            c3.obtain("constraints", lambda: (site_constraints(case["address"]), {}))
            c3.lookup("writer"); c3.lookup("review")
            out = c3.publish(draft, rev)
            self.assertEqual((wt.sends, rt.sends), (0, 1))
            self.assertEqual(c3.run_id, "PA-2026-0152-r2")
            for stage in ("source", "constraints", "writer", "review", "export"):
                self.assertIsNotNone(store.load("PA-2026-0152-r2", stage), stage)
            self.assertEqual(out["conditions"], ["The east-facing bathroom window shall be obscure-glazed."])


if __name__ == "__main__":
    unittest.main()
