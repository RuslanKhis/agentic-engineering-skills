"""Exercise the schema checker through its public CLI using temporary fixtures."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_response_schema.py"
CLEAN = {"type": "object", "title": "Decision",
         "properties": {"status": {"type": "string", "enum": ["READY", "REFUSE"]},
                        "reason": {"type": ["string", "null"]},
                        "items": {"type": "array", "items": {"type": "integer", "minimum": 0}, "maxItems": 5}},
         "required": ["status", "reason", "items"], "additionalProperties": False}


class SchemaCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, document, name="schema.json"):
        path = self.root / name
        path.write_text(document if isinstance(document, str) else json.dumps(document))
        return path

    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, check=False)

    def check(self, document, *args):
        result = self.run_cli("--schema", str(self.write(document)), *args)
        self.assertIn(result.returncode, (0, 1), result.stderr)
        return result.returncode, json.loads(result.stdout)

    def labels(self, data):
        return {(row["finding"], str(row.get("detail"))) for row in data["findings"]}

    def test_help_and_bad_arguments(self):
        self.assertEqual(self.run_cli("--help").returncode, 0)
        self.assertEqual(self.run_cli().returncode, 2)
        self.assertEqual(self.run_cli("--schema", str(self.root / "absent.json")).returncode, 2)
        self.assertEqual(self.run_cli("--schema", str(self.write("{not json"))).returncode, 2)
        self.assertEqual(self.run_cli("--schema", str(self.write('{"a": 1, "a": 2}'))).returncode, 2)
        self.assertEqual(self.run_cli("--schema", str(self.write("[1, 2]"))).returncode, 2)
        self.assertEqual(self.run_cli("--schema", str(self.root)).returncode, 2)
        for option in ("--max-depth", "--max-properties", "--max-enum", "--max-name-length", "--max-bytes"):
            self.assertEqual(self.run_cli("--schema", str(self.write(CLEAN)), option, "0").returncode, 2)
        link = self.root / "link.json"
        link.symlink_to(self.write(CLEAN))
        self.assertEqual(self.run_cli("--schema", str(link)).returncode, 2)

    def test_clean_schema_is_inspected_and_deterministic(self):
        code, data = self.check(CLEAN)
        self.assertEqual(code, 0)
        self.assertEqual(data["status"], "inspected")
        self.assertEqual(data["findings"], [])
        self.assertTrue(data["read_only"])
        self.assertEqual(data["stats"]["property_count"], 3)
        self.assertEqual(data["stats"]["required_count"], 3)
        self.assertEqual(data["stats"]["max_depth"], 2)
        self.assertEqual(data["stats"]["nullable_styles"]["type_array_null"], 1)
        first = self.run_cli("--schema", str(self.write(CLEAN))).stdout
        self.assertEqual(first, self.run_cli("--schema", str(self.write(CLEAN))).stdout)
        self.assertNotIn(str(self.root), first)

    def test_unsupported_keywords_exit_one(self):
        document = {"type": "object", "properties": {
            "code": {"type": "string", "pattern": "^[A-Z]+$", "minLength": 2, "maxLength": 8},
            "amount": {"type": "number", "multipleOf": 0.5, "exclusiveMinimum": 0, "exclusiveMaximum": 10},
            "choice": {"oneOf": [{"type": "string"}, {"type": "integer"}]},
            "merged": {"allOf": [{"type": "object"}]},
            "fixed": {"const": "x"},
            "tags": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
            "extra": {"type": "object", "patternProperties": {"^x": {"type": "string"}}, "dependentRequired": {"a": ["b"]}},
            "conditional": {"if": {"type": "string"}, "then": {"minLength": 1}, "else": {"type": "integer"}},
            "negated": {"not": {"type": "null"}}},
            "required": ["code"]}
        code, data = self.check(document)
        self.assertEqual(code, 1)
        self.assertEqual(data["status"], "unsupported_keywords")
        found = {detail for label, detail in self.labels(data) if label == "unsupported_keyword"}
        self.assertEqual(found, {"pattern", "minLength", "maxLength", "multipleOf", "exclusiveMinimum",
                                 "exclusiveMaximum", "oneOf", "allOf", "const", "uniqueItems",
                                 "patternProperties", "dependentRequired", "if", "then", "else", "not"})
        paths = {row["path"] for row in data["findings"] if row["finding"] == "unsupported_keyword"}
        self.assertIn("#/properties/code", paths)

    def test_refs_are_resolved_and_unresolved_refs_fail(self):
        document = {"$defs": {"Node": {"type": "object", "properties": {
            "name": {"type": "string"}, "children": {"type": "array", "items": {"$ref": "#/$defs/Node"}}},
            "required": ["name"]}},
            "type": "object", "properties": {"tree": {"$ref": "#/$defs/Node"}}, "required": ["tree"]}
        code, data = self.check(document)
        self.assertEqual(code, 0)
        self.assertEqual(data["stats"]["ref_count"], 2)
        self.assertEqual(data["stats"]["recursive_ref_count"], 1)
        self.assertEqual(data["stats"]["property_count"], 3)
        self.assertIn(("recursive_ref", "#/$defs/Node"), self.labels(data))
        document["properties"]["missing"] = {"$ref": "#/$defs/Absent"}
        document["properties"]["remote"] = {"$ref": "https://example.invalid/schema.json"}
        code, data = self.check(document)
        self.assertEqual(code, 1)
        self.assertEqual(data["stats"]["unresolved_ref_count"], 2)
        self.assertIn(("unresolved_ref", "#/$defs/Absent"), self.labels(data))

    def test_size_yardsticks_report_review_findings_without_failing(self):
        deep = {"type": "object", "properties": {"level": {"type": "string"}}}
        document = {"type": "object", "properties": {"root": deep}, "required": ["root"]}
        node = deep
        for _ in range(3):
            child = {"type": "object", "properties": {"leaf": {"type": "string"}}}
            node["properties"]["next"] = child
            node = child
        document["properties"]["pick"] = {"type": "string", "enum": [f"option-{i}" for i in range(6)]}
        document["properties"]["a_very_long_property_name_" + "x" * 50] = {"type": "string"}
        document["properties"]["long_enum"] = {"type": "string", "enum": ["y" * 70]}
        code, data = self.check(document, "--max-depth", "3", "--max-properties", "4", "--max-enum", "5")
        self.assertEqual(code, 0)
        self.assertEqual(data["status"], "inspected")
        found = {label for label, _ in self.labels(data)}
        self.assertTrue({"nesting_depth_exceeds_limit", "property_count_exceeds_limit",
                         "enum_cardinality_exceeds_limit", "long_property_name", "long_enum_value",
                         "optional_fields_outnumber_required"} <= found)
        self.assertEqual(data["stats"]["max_depth"], 5)
        self.assertEqual(data["stats"]["enum_max"], 6)
        self.assertTrue(all(row["severity"] in ("review", "info") for row in data["findings"]))

    def test_nullable_styles_and_pydantic_flag(self):
        document = {"type": "object", "properties": {
            "a": {"anyOf": [{"type": "string"}, {"type": "null"}], "default": None, "title": "A"},
            "b": {"type": "string", "nullable": True},
            "c": {"type": ["integer", "null"]}}, "required": ["a", "b", "c"]}
        code, data = self.check(document, "--pydantic-json")
        self.assertEqual(code, 0)
        self.assertEqual(data["source"], "pydantic_model_json_schema")
        self.assertEqual(data["stats"]["nullable_styles"], {"anyof_null": 1, "nullable_keyword": 1, "type_array_null": 1})
        self.assertIn("mixed_nullable_styles", {label for label, _ in self.labels(data)})
        self.assertNotIn("unsupported_keyword", {label for label, _ in self.labels(data)})

    def test_structural_errors_and_unknown_keywords(self):
        document = {"type": "object", "properties": {"a": {"type": "string", "x-vendor": 1}}, "required": ["a", "ghost"]}
        code, data = self.check(document)
        self.assertEqual(code, 1)
        labels = self.labels(data)
        self.assertIn(("required_names_not_in_properties", "['ghost']"), labels)
        self.assertIn(("unrecognised_keyword", "x-vendor"), labels)
        code, data = self.check({"type": "object", "properties": {"a": "not-a-schema"}})
        self.assertEqual(code, 1)
        self.assertIn("schema_not_an_object", {label for label, _ in labels | self.labels(data)})

    def test_oversized_file_is_rejected(self):
        path = self.write(CLEAN)
        self.assertEqual(self.run_cli("--schema", str(path), "--max-bytes", "10").returncode, 2)


if __name__ == "__main__":
    unittest.main()
