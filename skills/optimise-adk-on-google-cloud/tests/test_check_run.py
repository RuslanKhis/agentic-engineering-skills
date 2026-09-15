from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_run.py"
SPEC = importlib.util.spec_from_file_location("check_run", SCRIPT)
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


def example():
    def event(parts, role="model", **more):
        return {"invocationId": "synthetic-invocation", "author": "catalogue_agent",
                "content": {"role": role, "parts": parts}, **more}
    events = [
        event([{"functionCall": {"id": "lookup-1", "name": "get_schema", "args": {}}}]),
        event([{"functionResponse": {"id": "lookup-1", "name": "get_schema",
               "response": {"status": "success", "result": "user_id, revenue"}}}], "user"),
        event([{"text": "user_id, "}], partial=True),
        event([{"text": "revenue"}], partial=True),
        event([{"text": "user_id, revenue"}], finishReason="STOP"),
    ]
    expected = {"schema_version": 1, "answer_author": "catalogue_agent",
                "tools": [{"name": "get_schema", "result_equals": {"/status": "success"},
                           "result_contains": {"/result": ["user_id", "revenue"]}}],
                "answer_contains": ["user_id", "revenue"], "min_partial_events": 2}
    return events, expected


class RunChecks(unittest.TestCase):
    def setUp(self):
        self.events, self.expected = example()

    def rejected(self, reason=None):
        with self.assertRaises(checker.Rejected) as caught:
            checker.check_events(self.events, self.expected)
        if reason:
            self.assertEqual(str(caught.exception), reason)

    def test_valid_correlated_schema_and_complete_answer(self):
        result = checker.check_events(self.events, self.expected)
        self.assertEqual(result["correlated_tool_calls"], 1)
        self.assertEqual(result["visible_partial_events"], 2)
        self.assertEqual(result["cache_evidence"], "unknown")
        self.assertIsNone(result["maximum_cached_tokens_observed"])

    def test_late_provider_error_invalidates_final(self):
        self.events.append({"errorMessage": "SYNTHETIC_SECRET_VALUE"})
        self.rejected("reported_error")

    def test_truncated_answer_is_not_a_speed_improvement(self):
        self.events[-1]["finishReason"] = "MAX_TOKENS"
        self.rejected("incomplete_generation")

    def test_failure_with_plausible_data_is_rejected(self):
        response = self.events[1]["content"]["parts"][0]["functionResponse"]["response"]
        response.update(error="SYNTHETIC_PROVIDER_FAILURE", rate=0.85)
        self.rejected("reported_error")

    def test_failed_status_rejected_even_with_matching_schema(self):
        self.events[1]["content"]["parts"][0]["functionResponse"]["response"]["status"] = "failed"
        self.rejected("failed_tool_result")

    def test_response_requires_prior_correlated_call(self):
        self.events[0], self.events[1] = self.events[1], self.events[0]
        self.rejected("uncorrelated_tool_response")

    def test_answer_cannot_precede_tool_completion(self):
        self.events.insert(0, self.events.pop())
        self.rejected("answer_before_tools_complete")

    def test_repeated_tool_submission_fails_even_with_fresh_id(self):
        repeated = deepcopy(self.events[0])
        repeated["content"]["parts"][0]["functionCall"]["id"] = "lookup-2"
        self.events.insert(2, repeated)
        self.rejected("repeated_tool_call")

    def test_tool_fragment_after_final_rejected(self):
        late = deepcopy(self.events[0])
        late["partial"] = True
        self.events.append(late)
        self.rejected("tool_after_final")

    def test_text_after_final_rejected(self):
        self.events.append(deepcopy(self.events[-1]))
        self.rejected("text_after_final")

    def test_schema_must_come_from_expected_response(self):
        self.events[1]["content"]["parts"][0]["functionResponse"]["response"]["result"] = "unrelated"
        self.rejected("result_assertion_failed")

    def test_boolean_is_not_numeric_expected_value(self):
        self.expected["tools"][0]["result_equals"] = {"/result_flag": 1}
        self.events[1]["content"]["parts"][0]["functionResponse"]["response"]["result_flag"] = True
        self.rejected("result_assertion_failed")

    def test_wrong_author_and_thought_only_are_not_answers(self):
        for mutation in ("author", "thought"):
            events, expected = example()
            if mutation == "author":
                events[-1]["author"] = "other_agent"
            else:
                events[-1]["content"]["parts"][0]["thought"] = True
            with self.assertRaises(checker.Rejected):
                checker.check_events(events, expected)

    def test_missing_stop_is_not_implicitly_accepted(self):
        del self.events[-1]["finishReason"]
        self.rejected("missing_completion_metadata")

    def test_whitespace_partials_do_not_satisfy_streaming(self):
        self.events[2]["content"]["parts"][0]["text"] = "  "
        self.rejected("insufficient_partial_events")

    def test_mixed_invocations_cannot_be_combined_to_pass(self):
        self.events[-1]["invocationId"] = "other"
        self.rejected("mixed_invocations")

    def test_cache_configuration_is_not_cache_hit_evidence(self):
        self.expected["require_cache_hit"] = True
        self.rejected("cache_hit_not_observed")
        self.events[-1]["usageMetadata"] = {"cachedContentTokenCount": 0}
        self.rejected("cache_hit_not_observed")
        self.events[-1]["usageMetadata"]["cachedContentTokenCount"] = 1024
        self.assertEqual(checker.check_events(self.events, self.expected)["cache_evidence"], "hit")

    def test_snake_case_event_aliases_supported(self):
        source = json.dumps(self.events)
        for camel, snake in [("invocationId", "invocation_id"), ("finishReason", "finish_reason"),
                             ("functionCall", "function_call"), ("functionResponse", "function_response")]:
            source = source.replace(camel, snake)
        self.assertEqual(checker.check_events(json.loads(source), self.expected)["verdict"], "PASS")

    def test_conflicting_aliases_rejected(self):
        self.events[-1]["finish_reason"] = "MAX_TOKENS"
        self.rejected("conflicting_aliases")

    def test_no_assertions_and_unknown_contract_fields_invalid(self):
        for field in ("tools", "extra"):
            expected = deepcopy(self.expected)
            if field == "tools":
                expected[field] = [{"name": "get_schema"}]
            else:
                expected[field] = "not supported"
            with self.assertRaises(checker.InvalidInput):
                checker.check_events(self.events, expected)

    def test_json_pointer_escaping(self):
        self.assertEqual(checker.lookup({"a/b": {"x~y": [2]}}, "/a~1b/x~0y/0"), 2)

    def test_malformed_event_types_rejected(self):
        for replacement in ("wrong", [], 9):
            events = deepcopy(self.events)
            events[0]["content"] = replacement
            with self.assertRaises(checker.InvalidInput):
                checker.check_events(events, self.expected)

    def test_falsey_nonlist_parts_and_malformed_tool_fields_rejected(self):
        for value in ({}, False, 0, ""):
            events = deepcopy(self.events)
            events[-1]["content"]["parts"] = value
            with self.assertRaises(checker.InvalidInput):
                checker.check_events(events, self.expected)
        for partial in (False, True):
            for key, value in (("name", []), ("id", {}), ("args", "wrong")):
                events = deepcopy(self.events)
                events[0]["partial"] = partial
                events[0]["content"]["parts"][0]["functionCall"][key] = value
                with self.assertRaises(checker.InvalidInput):
                    checker.check_events(events, self.expected)

    def test_errors_at_known_content_and_part_envelopes_rejected(self):
        for location in ("content", "part", "tool"):
            events = deepcopy(self.events)
            if location == "content":
                events[-1]["content"]["error"] = "synthetic"
            elif location == "part":
                events[-1]["content"]["parts"].append({"error": "synthetic"})
            else:
                events[0]["content"]["parts"][0]["functionCall"]["error"] = "synthetic"
            with self.assertRaises(checker.Rejected):
                checker.check_events(events, self.expected)


class CommandChecks(unittest.TestCase):
    def run_cli(self, *arguments):
        return subprocess.run([sys.executable, str(SCRIPT), *arguments],
                              text=True, capture_output=True, timeout=10)

    def test_help_and_bad_arguments_hide_values(self):
        self.assertEqual(self.run_cli("--help").returncode, 0)
        result = self.run_cli("--SYNTHETIC_SECRET_FLAG")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("SYNTHETIC_SECRET", result.stdout + result.stderr)

    def test_cli_repeat_dry_run_and_errors_are_read_only_and_redacted(self):
        with tempfile.TemporaryDirectory() as directory:
            events, expected = example()
            root = Path(directory)
            ep, cp = root / "events.json", root / "expect.json"
            ep.write_text(json.dumps(events))
            cp.write_text(json.dumps(expected))
            before = {p.name: p.read_bytes() for p in root.iterdir()}
            first = self.run_cli("--events", str(ep), "--expect", str(cp))
            second = self.run_cli("--events", str(ep), "--expect", str(cp), "--dry-run")
            self.assertEqual((first.returncode, second.returncode), (0, 0))
            self.assertEqual(first.stdout, second.stdout)
            self.assertEqual(before, {p.name: p.read_bytes() for p in root.iterdir()})
            ep.write_text(json.dumps(events + [{"error": "SYNTHETIC_SECRET_VALUE"}]))
            failure = self.run_cli("--events", str(ep), "--expect", str(cp))
            self.assertEqual(failure.returncode, 3)
            self.assertNotIn("SYNTHETIC_SECRET_VALUE", failure.stdout + failure.stderr)
            self.assertNotIn(directory, failure.stdout + failure.stderr)

    def test_duplicate_keys_nonfinite_oversize_and_symlinks_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.json"
            for content in ('{"x":1,"x":2}', '[NaN]', '[1e309]', '{"nested":[-1e309]}',
                            '"' + "x" * 50 + '"'):
                path.write_text(content)
                with self.assertRaises(checker.InvalidInput):
                    checker.read_json(path, 40)
            link = Path(directory) / "link.json"
            link.symlink_to(path)
            with self.assertRaises(checker.InvalidInput):
                checker.read_json(link, 100)


if __name__ == "__main__":
    unittest.main()
