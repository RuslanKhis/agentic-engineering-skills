"""Contract tests for the optional bounded tool result callback.

A fake tool context stands in for ADK's ``ToolContext``; these tests establish
the callback's envelope and artifact round trip only, not ADK's callback
dispatch, artifact service behaviour or a hosted result.
"""

import asyncio
import base64
import importlib.util
import json
from pathlib import Path
import unittest

ASSET = Path(__file__).resolve().parents[1] / "assets" / "bounded_tool_result.py"
SPEC = importlib.util.spec_from_file_location("bounded_tool_result", ASSET)
bounded = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bounded)


class FakeTool:
    def __init__(self, name="get_rows"):
        self.name = name


class FakeToolContext:
    """Mirrors the 2.8.0 shape used by the asset: function_call_id and artifacts."""

    def __init__(self, function_call_id="call-1", fail=False):
        self.function_call_id = function_call_id
        self.fail = fail
        self.store = {}

    async def save_artifact(self, filename, artifact, custom_metadata=None):
        if self.fail:
            raise ValueError("Artifact service is not initialized.")
        versions = self.store.setdefault(filename, [])
        versions.append(artifact)
        return len(versions) - 1

    async def load_artifact(self, filename, version=None):
        versions = self.store.get(filename)
        if not versions:
            return None
        return versions[-1 if version is None else version]


def decode(part):
    data = part["inline_data"]["data"] if isinstance(part, dict) else part.inline_data.data
    if isinstance(data, str):
        data = base64.b64decode(data)
    return json.loads(data.decode("utf-8"))


def run(callback, *args):
    return asyncio.run(callback(*args))


class BoundedResultChecks(unittest.TestCase):
    def setUp(self):
        self.callback = bounded.build_bounded_after_tool_callback(max_bytes=200, preview_bytes=40)
        self.context = FakeToolContext()

    def test_small_dict_and_non_dict_results_are_left_to_the_framework(self):
        self.assertIsNone(run(self.callback, FakeTool(), {}, self.context, {"status": "success", "rows": [1, 2]}))
        self.assertIsNone(run(self.callback, FakeTool(), {}, self.context, "x" * 5000))
        self.assertIsNone(run(self.callback, FakeTool(), {}, self.context, None))
        self.assertEqual(self.context.store, {})

    def test_oversized_result_returns_bounded_envelope_and_artifact_round_trip(self):
        original = {"status": "success", "rows": [{"id": i, "note": "n" * 20} for i in range(20)]}
        result = run(self.callback, FakeTool(), {"n": 20}, self.context, original)
        self.assertEqual(set(result), {"status", "preview", "artifact", "version", "truncated",
                                       "original_bytes", "artifact_state"})
        self.assertEqual(result["status"], "success")
        self.assertIs(result["truncated"], True)
        self.assertEqual(result["version"], 0)
        self.assertEqual(result["artifact"], "tool-result-get_rows-call-1.json")
        self.assertEqual(result["artifact_state"], "saved")
        self.assertLessEqual(len(result["preview"].encode("utf-8")), 40)
        self.assertTrue(json.dumps(original, ensure_ascii=False, sort_keys=True).startswith(result["preview"]))
        self.assertEqual(result["original_bytes"], len(bounded.serialise(original)))
        stored = asyncio.run(self.context.load_artifact(result["artifact"], result["version"]))
        self.assertEqual(decode(stored), original)
        self.assertLess(len(bounded.serialise(result)), result["original_bytes"])

    def test_second_save_increments_version_and_names_follow_call_id(self):
        payload = {"blob": "y" * 500}
        first = run(self.callback, FakeTool(), {}, self.context, payload)
        second = run(self.callback, FakeTool(), {}, self.context, payload)
        self.assertEqual((first["version"], second["version"]), (0, 1))
        other = run(self.callback, FakeTool("Export Rows!"), {}, FakeToolContext("call/2"), payload)
        self.assertEqual(other["artifact"], "tool-result-Export_Rows_-call_2.json")

    def test_preview_cuts_on_a_utf8_boundary(self):
        payload = {"text": "é" * 400}
        result = run(self.callback, FakeTool(), {}, self.context, payload)
        preview = result["preview"]
        self.assertLessEqual(len(preview.encode("utf-8")), 40)
        self.assertEqual(preview, bounded.serialise(payload).decode("utf-8")[:len(preview)])

    def test_failure_status_is_preserved_rather_than_relabelled(self):
        result = run(self.callback, FakeTool(), {}, self.context, {"status": "error", "detail": "d" * 500})
        self.assertEqual(result["status"], "error")
        self.assertIs(result["truncated"], True)

    def test_missing_or_failing_artifact_service_still_bounds_the_result(self):
        failing = FakeToolContext(fail=True)
        result = run(self.callback, FakeTool(), {}, failing, {"blob": "z" * 500})
        self.assertEqual((result["artifact"], result["version"], result["artifact_state"]),
                         (None, None, "save_failed"))
        self.assertIs(result["truncated"], True)
        self.assertNotIn("Artifact service", json.dumps(result))

        class Bare:
            pass

        bare = run(self.callback, FakeTool(), {}, Bare(), {"blob": "z" * 500})
        self.assertEqual(bare["artifact_state"], "unavailable")
        self.assertEqual(bare["artifact"], None)

    def test_invalid_limits_are_rejected(self):
        for kwargs in ({"max_bytes": 0}, {"preview_bytes": 0}, {"max_bytes": -1}):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError):
                    bounded.build_bounded_after_tool_callback(**kwargs)


if __name__ == "__main__":
    unittest.main()
