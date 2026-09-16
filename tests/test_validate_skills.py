"""Exercise package checks using temporary, independently constructed packages."""

from __future__ import annotations

from contextlib import redirect_stdout
import io
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_skills import main, validate_repository


class PackageValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.package = self.root / "skills" / "sample-skill"
        (self.package / "agents").mkdir(parents=True)
        self.frontmatter = (
            "name: sample-skill\n"
            "description: Help build a sample feature when it is requested.\n"
            "license: MIT\n"
            "compatibility: Python 3.12 or newer.\n"
            "allowed-tools: Read Bash(python:*)\n"
            "metadata:\n  author: A maintainer\n  version: '1.0'\n"
        )
        self.write_skill()
        (self.package / "LICENSE").write_text("MIT License\n", encoding="utf-8")
        self.interface = (
            "interface:\n"
            "  display_name: Sample Skill\n"
            "  short_description: Build and check a sample feature\n"
            "  default_prompt: Use $sample-skill to build the requested feature.\n"
            "policy:\n  allow_implicit_invocation: true\n"
        )
        self.write_interface()

    def write_skill(self, body="# Sample skill\n\nBuild the requested feature.\n"):
        (self.package / "SKILL.md").write_text(
            f"---\n{self.frontmatter}---\n\n{body}", encoding="utf-8"
        )

    def write_interface(self):
        (self.package / "agents" / "openai.yaml").write_text(self.interface, encoding="utf-8")

    def errors(self):
        return validate_repository(self.root).errors

    def assert_error(self, fragment):
        errors = self.errors()
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_valid_package_with_compatibility_and_host_policy(self):
        for setting in ("true", "false"):
            with self.subTest(setting=setting):
                self.interface = self.interface.replace("true", setting)
                self.write_interface()
                report = validate_repository(self.root)
                self.assertEqual([], report.errors)
                self.assertEqual(1, len(report.packages))
                self.assertGreater(report.packages[0].words, 0)
        self.interface = self.interface.split("policy:")[0]
        self.write_interface()
        self.assertEqual([], self.errors())

    def test_yaml_flow_and_block_scalars_are_parsed(self):
        self.frontmatter = (
            "name: sample-skill\n"
            "description: >-\n  Build a useful feature\n  when requested.\n"
            "metadata: {version: '1', author: Maintainer}\n"
        )
        self.write_skill()
        self.assertEqual([], self.errors())

    def test_malformed_yaml_and_unsafe_tags_are_rejected(self):
        for bad in ("description: [unclosed\n", "description: !!python/object:os.system {}\n"):
            with self.subTest(yaml=bad):
                self.frontmatter = "name: sample-skill\n" + bad
                self.write_skill()
                self.assert_error("invalid YAML")

    def test_duplicate_keys_at_both_mapping_depths_are_rejected(self):
        for duplicate in ("name: sample-skill\n", "metadata: {author: first, author: second}\n"):
            with self.subTest(yaml=duplicate):
                self.frontmatter = "name: sample-skill\ndescription: Build a feature.\n" + duplicate
                self.write_skill()
                self.assert_error("duplicate key")

    def test_frontmatter_requires_delimiters_mapping_and_body(self):
        for content, expected in (
            ("# Instructions only", "must begin with YAML frontmatter"),
            ("---\nname: sample-skill\n", "no closing"),
            ("---\n- name\n---\nBody", "must be a mapping"),
            ("---\n" + self.frontmatter + "---\n", "instructions are empty"),
        ):
            with self.subTest(content=content):
                (self.package / "SKILL.md").write_text(content, encoding="utf-8")
                self.assert_error(expected)

    def test_missing_or_blank_fields_are_rejected(self):
        for name, description in (("", "A feature"), ("sample-skill", " ")):
            with self.subTest(name=name, description=description):
                self.frontmatter = f"name: '{name}'\ndescription: '{description}'\n"
                self.write_skill()
                self.assert_error("must be a non-empty string")
        self.frontmatter = "name: sample-skill\n"
        self.write_skill()
        self.assert_error("description must be a non-empty string")

    def test_name_must_match_and_follow_specification(self):
        for name in ("other-skill", "Sample-skill", "sample--skill", "-sample", "sample-", "s" * 65):
            with self.subTest(name=name):
                self.frontmatter = f"name: {name}\ndescription: Build a feature.\n"
                self.write_skill()
                self.assertTrue(self.errors())

    def test_description_and_compatibility_limits(self):
        self.frontmatter = "name: sample-skill\ndescription: " + "a" * 1025 + "\n"
        self.write_skill()
        self.assert_error("description exceeds 1024")
        self.frontmatter = "name: sample-skill\ndescription: Build a feature.\ncompatibility: " + "a" * 501 + "\n"
        self.write_skill()
        self.assert_error("compatibility exceeds 500")

    def test_metadata_must_have_string_keys_and_values(self):
        for metadata in ("{version: 1}", "{1: version}", "[version]", "null"):
            with self.subTest(metadata=metadata):
                self.frontmatter = f"name: sample-skill\ndescription: Build a feature.\nmetadata: {metadata}\n"
                self.write_skill()
                self.assert_error("metadata must map string keys to string values")

    def test_required_bundled_files_must_exist(self):
        for relative in ("LICENSE", "SKILL.md", "agents/openai.yaml"):
            with self.subTest(resource=relative):
                path = self.package / relative
                original = path.read_bytes()
                path.unlink()
                self.assert_error("missing or unreadable resource")
                path.write_bytes(original)

    def test_nested_markdown_resolves_from_its_own_directory(self):
        (self.package / "references").mkdir()
        (self.package / "assets").mkdir()
        (self.package / "assets" / "diagram.svg").write_text("<svg/>", encoding="utf-8")
        (self.package / "references" / "guide.md").write_text(
            "[Back](../SKILL.md#sample-skill) ![Drawing](../assets/diagram.svg)\n", encoding="utf-8"
        )
        self.write_skill("[Read guide](references/guide.md#part-one)\n[Official](https://example.com/missing)\n")
        self.assertEqual([], self.errors())

    def test_missing_link_targets_are_rejected_in_references_too(self):
        (self.package / "references").mkdir()
        (self.package / "references" / "guide.md").write_text("[Missing](missing.md)\n", encoding="utf-8")
        self.write_skill("[Read guide](references/guide.md)\n")
        self.assert_error("invalid local link 'missing.md'")

    def test_reference_style_links_and_images_are_checked(self):
        for body in ("[Guide][resource]\n\n[resource]: absent.md\n", "![Diagram][image]\n\n[image]: absent.svg\n"):
            with self.subTest(markdown=body):
                self.write_skill(body)
                self.assert_error("invalid local link")

    def test_code_examples_are_not_treated_as_links(self):
        self.write_skill(
            "```markdown\n[Illustration](missing.md)\n![Image](missing.svg)\n```\n\n"
            "`[Inline example](also-missing.md)`\n\n"
            "    [Indented example](missing-too.md)\n\n"
            "[In this document](#heading)\n"
        )
        self.assertEqual([], self.errors())

    def test_percent_encoded_file_names_and_balanced_parentheses(self):
        (self.package / "guide (local).md").write_text("# Guide\n", encoding="utf-8")
        self.write_skill("[Guide](guide%20(local).md)\n")
        self.assertEqual([], self.errors())

    def test_links_cannot_escape_package_even_when_target_exists(self):
        (self.root / "skills" / "outside.md").write_text("Outside\n", encoding="utf-8")
        for target in ("../outside.md", "%2E%2E/outside.md"):
            with self.subTest(target=target):
                self.write_skill(f"[Outside]({target})\n")
                self.assert_error("escapes its skill package")

    def test_absolute_and_file_scheme_local_links_are_rejected(self):
        for target in (str(self.package / "LICENSE"), (self.package / "LICENSE").as_uri()):
            with self.subTest(target=target):
                self.write_skill(f"[License]({target})\n")
                self.assert_error("must be relative to its skill package")

    def test_symlink_escape_is_rejected_without_reading_its_contents(self):
        external = self.root / "external.md"
        external.write_text("External contents\n", encoding="utf-8")
        (self.package / "linked.md").symlink_to(external)
        self.write_skill("[Link](linked.md)\n")
        self.assert_error("escapes its skill package")

    def test_internal_file_symlink_is_allowed(self):
        (self.package / "linked.md").symlink_to("SKILL.md")
        self.assertEqual([], self.errors())

    def test_directory_symlink_escape_is_rejected(self):
        external = self.root / "external"
        external.mkdir()
        (self.package / "linked-dir").symlink_to(external, target_is_directory=True)
        self.assert_error("directory symlink escapes its skill package")

    def test_internal_directory_symlink_is_allowed_without_following_cycles(self):
        (self.package / "references").mkdir()
        (self.package / "references" / "guide.md").write_text("# Guide\n", encoding="utf-8")
        (self.package / "ref-link").symlink_to("references", target_is_directory=True)
        (self.package / "references" / "cycle").symlink_to("..", target_is_directory=True)
        self.write_skill("[Guide](ref-link/guide.md)\n")
        self.assertEqual([], self.errors())

    def test_invalid_path_bytes_fail_without_crashing(self):
        self.write_skill("[Invalid](guide%00.md)\n")
        self.assert_error("invalid local link")

    def test_interface_invocation_must_name_this_skill_exactly(self):
        for prompt in ("Use /sample-skill to help.", "Use $other-skill to help.", "Use $sample-skill-extra to help."):
            with self.subTest(prompt=prompt):
                self.interface = (
                    "interface:\n  display_name: Sample\n"
                    "  short_description: Build and check a sample feature\n"
                    f"  default_prompt: {prompt}\n"
                )
                self.write_interface()
                self.assert_error("default_prompt must explicitly invoke $sample-skill")

    def test_interface_yaml_duplicates_and_invalid_policy_are_rejected(self):
        self.interface += "policy: {allow_implicit_invocation: false}\n"
        self.write_interface()
        self.assert_error("duplicate key")
        self.interface = self.interface.split("policy:")[0] + "policy: {allow_implicit_invocation: 'false'}\n"
        self.write_interface()
        self.assert_error("allow_implicit_invocation must be a boolean")

    def test_interface_requires_strings_and_bounded_summary(self):
        for short in ("Too short", "a" * 65, ""):
            with self.subTest(short=short):
                self.interface = (
                    "interface:\n  display_name: Sample\n"
                    f"  short_description: '{short}'\n"
                    "  default_prompt: Use $sample-skill to help.\n"
                )
                self.write_interface()
                self.assertTrue(self.errors())

    def test_python_is_compiled_without_imports_or_side_effects(self):
        marker = self.root / "should-not-exist"
        script = self.package / "helper.py"
        script.write_text(
            "import a_package_that_does_not_exist\n"
            f"open({str(marker)!r}, 'w').write('executed')\n", encoding="utf-8"
        )
        self.assertEqual([], self.errors())
        self.assertFalse(marker.exists())
        self.assertFalse((self.package / "__pycache__").exists())
        script.write_text("def broken(:\n  pass\n", encoding="utf-8")
        self.assert_error("Python syntax check failed")

    def test_line_count_is_only_a_warning(self):
        self.write_skill("Line of instructions.\n" * 501)
        report = validate_repository(self.root)
        self.assertEqual([], report.errors)
        self.assertEqual(1, len(report.warnings))

    def test_cli_exit_status_distinguishes_success_and_failure(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(0, main(["--root", str(self.root)]))
            self.write_skill("[Missing](absent.md)\n")
            self.assertEqual(1, main(["--root", str(self.root)]))

    def test_missing_or_empty_collection_is_an_error(self):
        with tempfile.TemporaryDirectory() as other:
            root = Path(other)
            self.assertTrue(validate_repository(root).errors)
            (root / "skills").mkdir()
            self.assertTrue(validate_repository(root).errors)

    def test_broken_package_symlink_is_not_silently_skipped(self):
        (self.root / "skills" / "broken-skill").symlink_to("missing-package", target_is_directory=True)
        self.assert_error("repository skill directories must not be symlinks")


if __name__ == "__main__":
    unittest.main()
