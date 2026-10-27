import json
from pathlib import Path
import shutil
import tempfile
import unittest

from pipeline.checkpoints import CheckpointStore
from pipeline.config import Settings
from pipeline.model import ChatModel
from pipeline.resume import resume_case
from tests.doubles import ScriptedTransport

ROOT = Path(__file__).resolve().parents[1]


class ResumeTests(unittest.TestCase):
    def test_saved_stages_are_not_paid_for_again(self):
        with tempfile.TemporaryDirectory() as tmp:
            shutil.copytree(ROOT / "runs" / "PA-2026-0141-r3", Path(tmp) / "PA-2026-0141-r3")
            (Path(tmp) / "PA-2026-0141-r3" / "export.json").unlink()
            transport = ScriptedTransport([])
            model = ChatModel("https://gw.test/v1", "m", transport=transport)
            result = resume_case(ROOT / "cases" / "dev" / "PA-2026-0141", "PA-2026-0141-r3", Settings(),
                                 model, model, CheckpointStore(tmp))
        self.assertEqual(transport.sends, 0)
        self.assertEqual(result["decision"], "approve")


if __name__ == "__main__":
    unittest.main()
