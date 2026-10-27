import importlib.util
import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("apply_template", ROOT / "scripts" / "apply_template.py")
apply_template = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(apply_template)


def _ns(value):
    return SimpleNamespace(**{k: _ns(v) for k, v in value.items()}) if isinstance(value, dict) else value


class FakeTemplate:
    """Parses the camelCase JSON the way Template.from_json does, for the fields the script reads."""

    def __init__(self, raw):
        self.name = raw["name"]
        flag = raw["templateMetadata"]["multiLanguageDetection"]["enableMultiLanguageDetection"]
        self.template_metadata = _ns({"multi_language_detection": {"enable_multi_language_detection": flag}})

    @classmethod
    def from_json(cls, text):
        return cls(json.loads(text))


class FakeV1:
    Template = FakeTemplate

    class UpdateTemplateRequest(SimpleNamespace):
        pass


class FakeClient:
    def __init__(self, result_flag=True):
        self.requests, self.result_flag = [], result_flag

    def update_template(self, request):
        self.requests.append(request)
        meta = _ns({"multi_language_detection": {"enable_multi_language_detection": self.result_flag}})
        return SimpleNamespace(name=request.template.name, template_metadata=meta)


class ApplyTemplateTests(unittest.TestCase):
    def run_main(self, argv, client):
        out = io.StringIO()
        with redirect_stdout(out):
            apply_template.main(argv, client=client, modelarmor_v1=FakeV1)
        return out.getvalue()

    def test_template_file_enables_multi_language_detection(self):
        spec = json.loads((ROOT / "infra/modelarmor/input-template.json").read_text())
        self.assertTrue(spec["templateMetadata"]["multiLanguageDetection"]["enableMultiLanguageDetection"])
        # untouched by this change
        self.assertEqual(spec["filterConfig"]["piAndJailbreakFilterSettings"]["confidenceLevel"], "MEDIUM_AND_ABOVE")
        self.assertNotIn("modalities", spec["templateMetadata"])

    def test_update_is_masked_to_the_one_field_with_a_stable_request_id(self):
        client = FakeClient()
        self.run_main([], client)
        self.run_main([], client)
        first, second = client.requests
        self.assertEqual(first.update_mask, {"paths": [
            "template_metadata.multi_language_detection.enable_multi_language_detection"]})
        self.assertEqual(first.request_id, second.request_id)

    def test_dry_run_makes_no_call(self):
        client = FakeClient()
        self.assertIn("would update", self.run_main(["--dry-run"], client))
        self.assertEqual(client.requests, [])

    def test_failed_read_back_is_an_error(self):
        with self.assertRaises(SystemExit):
            self.run_main([], FakeClient(result_flag=False))


if __name__ == "__main__":
    unittest.main()
