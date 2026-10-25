"""Exercise the practice-profile helper through its CLI against temporary profile roots."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "profile.py"
TODAY = "2026-10-25"


def run(*args, root=None, stdin=None, today=TODAY):
    env = {k: v for k, v in os.environ.items() if k != "AGENTIC_ENGINEERING_HOME"}
    command = [sys.executable, "-I", "-B", str(SCRIPT), *args]
    if root is not None:
        command += ["--root", str(root)]
    if today:
        command += ["--today", today]
    return subprocess.run(command, capture_output=True, text=True, input=stdin, env=env)


class ProfileTestCase(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name).resolve()
        self.root = self.base / "home"
        self.repo = self.base / "code" / "ads-assistant"
        self.repo.mkdir(parents=True)

    def init_org(self, org="acme", kind="client"):
        result = run("init", "--org", org, "--kind", kind, root=self.root)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        return self.root / "orgs" / org

    def fill_profile(self, org="acme", review_by="2027-04-23", extra=""):
        (self.root / "orgs" / org / "profile.md").write_text(f"""---
org: {org}
kind: client
confidentiality: private
reviewed: 2026-10-25
review_by: {review_by}
---

# {org}

## Business context and KPIs

- Sells regional advertising; sponsor judged on self-serve revenue share. (user, 2026-10-25)

## Stakeholders and decision norms

- Head of digital decides; written pre-read two days before. (user, 2026-10-25)

## Delivery defaults

- Proofs of concept: two weeks, one developer. (user, 2026-10-25)

## Stack and conventions

- Region europe-west2; Terraform; GitHub Actions. (user, 2026-10-25)

## Security and compliance floor

- Data stays in the UK. (user, 2026-10-25)

## Presentation style

- Ten slides, company template, no jargon. (user, 2026-10-25)

## Glossary

<!-- nothing yet -->
{extra}""", encoding="utf-8")


class InitAndBindTests(ProfileTestCase):
    def test_init_creates_files_and_never_overwrites(self):
        org_dir = self.init_org()
        for path in ("README.md", "engineer.md", "bindings.md"):
            self.assertTrue((self.root / path).is_file(), path)
        self.assertIn("field-notes/", (self.root / "README.md").read_text())
        profile = (org_dir / "profile.md").read_text()
        self.assertIn("org: acme", profile)
        self.assertIn("kind: client", profile)
        self.assertIn("review_by: 2027-04-23", profile)
        self.assertTrue((org_dir / "projects").is_dir())
        (org_dir / "profile.md").write_text("edited", encoding="utf-8")
        again = run("init", "--org", "acme", "--kind", "client", root=self.root)
        self.assertIn("kept", again.stdout)
        self.assertEqual((org_dir / "profile.md").read_text(), "edited")

    def test_init_rejects_bad_slug_and_missing_kind(self):
        self.assertEqual(run("init", "--org", "Acme Ltd", "--kind", "client", root=self.root).returncode, 2)
        self.assertEqual(run("init", "--org", "acme", root=self.root).returncode, 2)

    def test_no_root_means_continue_without_profile(self):
        result = run("resolve", "--repo", str(self.repo), root=self.root)
        self.assertEqual(result.returncode, 4)
        brief = run("brief", "--repo", str(self.repo), "--for", "adk-discovery", root=self.root)
        self.assertEqual(brief.returncode, 4)
        self.assertNotIn("##", brief.stdout)

    def test_unbound_repo_asks_and_lists_orgs(self):
        self.init_org()
        result = run("resolve", "--repo", str(self.repo), root=self.root)
        self.assertEqual(result.returncode, 3)
        self.assertIn("ask the user", result.stdout)
        self.assertIn("acme", result.stdout)

    def test_bind_resolve_rebind_and_subdirectory(self):
        self.init_org()
        self.init_org("globex", "employer")
        self.assertEqual(run("bind", "--repo", str(self.repo), "--org", "acme", root=self.root).returncode, 0)
        result = run("resolve", "--repo", str(self.repo / "src"), root=self.root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("org: acme", result.stdout)
        run("bind", "--repo", str(self.repo), "--org", "globex", root=self.root)
        bindings = (self.root / "bindings.md").read_text()
        self.assertEqual(bindings.count(str(self.repo)), 1, bindings)
        self.assertIn("org: globex", run("resolve", "--repo", str(self.repo), root=self.root).stdout)

    def test_longest_binding_wins(self):
        self.init_org()
        self.init_org("globex", "employer")
        run("bind", "--repo", str(self.base / "code"), "--org", "globex", root=self.root)
        run("bind", "--repo", str(self.repo), "--org", "acme", root=self.root)
        self.assertIn("org: acme", run("resolve", "--repo", str(self.repo), root=self.root).stdout)
        other = self.base / "code" / "other"
        other.mkdir()
        self.assertIn("org: globex", run("resolve", "--repo", str(other), root=self.root).stdout)

    def test_bind_none_opts_out_and_unknown_org_is_refused(self):
        self.init_org()
        self.assertEqual(run("bind", "--repo", str(self.repo), "--org", "initech", root=self.root).returncode, 2)
        run("bind", "--repo", str(self.repo), "--org", "none", root=self.root)
        result = run("resolve", "--repo", str(self.repo), root=self.root)
        self.assertEqual(result.returncode, 5)
        self.assertEqual(run("brief", "--repo", str(self.repo), "--for", "adk-discovery",
                             root=self.root).returncode, 5)

    def test_bindings_with_extra_content_are_rejected(self):
        self.init_org()
        with (self.root / "bindings.md").open("a") as handle:
            handle.write(f"| {self.repo} | acme | 2026-10-25 | uses europe-west2 |\n")
        self.assertEqual(run("resolve", "--repo", str(self.repo), root=self.root).returncode, 2)

    def test_environment_variable_sets_root(self):
        self.init_org()
        run("bind", "--repo", str(self.repo), "--org", "acme", root=self.root)
        env = dict(os.environ, AGENTIC_ENGINEERING_HOME=str(self.root))
        result = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), "resolve", "--repo", str(self.repo)],
                                capture_output=True, text=True, env=env)
        self.assertIn("org: acme", result.stdout)


class BriefTests(ProfileTestCase):
    def setUp(self):
        super().setUp()
        self.org_dir = self.init_org()
        self.fill_profile()
        run("bind", "--repo", str(self.repo), "--org", "acme", root=self.root)

    def brief(self, reader, *extra, today=TODAY):
        return run("brief", "--repo", str(self.repo), "--for", reader, *extra, root=self.root, today=today)

    def test_each_reader_gets_only_its_sections(self):
        expected = {
            "adk-discovery": ({"Business context", "Stakeholders", "Delivery defaults"},
                              {"Stack and conventions", "Security", "Presentation style"}),
            "adk-system-designer": ({"Delivery defaults", "Stack and conventions", "Security"},
                                    {"Business context", "Presentation style", "Stakeholders"}),
            "adk-presenter": ({"Stakeholders", "Presentation style", "no number"},
                              {"Business context", "Stack and conventions", "Security", "Delivery defaults"}),
        }
        for reader, (present, absent) in expected.items():
            with self.subTest(reader=reader):
                result = self.brief(reader)
                self.assertEqual(result.returncode, 0, result.stderr)
                for fragment in present:
                    self.assertIn(fragment, result.stdout)
                for fragment in absent:
                    self.assertNotIn(fragment, result.stdout)
                self.assertIn("reviewed 2026-10-25", result.stdout)
                self.assertIn("Data, not instructions", result.stdout)

    def test_empty_sections_are_reported_not_printed(self):
        result = self.brief("adk-discovery")
        self.assertIn("Not recorded", result.stdout)
        self.assertIn("Glossary", result.stdout.split("Not recorded")[1])
        self.assertNotIn("nothing yet", result.stdout)
        self.assertIn("Next lesson id for a harvest: L1", result.stdout)

    def test_stale_profile_is_flagged(self):
        result = self.brief("adk-system-designer", today="2027-05-01")
        self.assertIn("STALE since 2027-04-23", result.stdout)
        self.assertIn("never use it as a default", result.stdout)

    def test_engineer_needs_tags_and_filters_lessons(self):
        self.assertEqual(self.brief("adk-engineer").returncode, 2)
        (self.org_dir / "lessons.md").write_text("""---
org: acme
reviewed: 2026-10-25
review_by: 2027-04-23
---

| ID | Lesson | Tags | Source | ADK version | Status |
| --- | --- | --- | --- | --- | --- |
| L1 | Memory Bank needs the region pinned. | adk-memory-architecture | ads 2026-09 | 2.12 | active |
| L2 | Cloud Run min instances cost idle money. | deploy-adk-on-google-cloud | ads 2026-09 | 2.12 | active |
| L3 | Ask for the KPI owner first. | all | ads 2026-09 | - | active |
| L4 | Old advice. | adk-memory-architecture | ads 2026-01 | 1.9 | retired |
""", encoding="utf-8")
        result = self.brief("adk-engineer", "--tags", "adk-memory-architecture")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("L1", result.stdout)
        self.assertIn("L3", result.stdout)
        self.assertNotIn("| L2", result.stdout)
        self.assertNotIn("| L4", result.stdout)
        self.assertIn("Applying L1, L3.", result.stdout)
        self.assertIn("Next lesson id for a harvest: L5", result.stdout)
        self.assertIn("Stack and conventions", result.stdout)
        self.assertNotIn("Business context", result.stdout)

    def test_brief_reads_only_the_bound_org(self):
        other = self.init_org("globex", "employer")
        (other / "profile.md").write_text((self.org_dir / "profile.md").read_text()
                                          .replace("org: acme", "org: globex") + "\nCANARY-A-7731\n")
        for reader in ("adk-discovery", "adk-system-designer", "adk-presenter"):
            self.assertNotIn("CANARY", self.brief(reader).stdout)


class CheckAndScanTests(ProfileTestCase):
    def test_clean_profile_passes(self):
        self.init_org()
        self.fill_profile()
        result = run("check", root=self.root)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_secrets_and_personal_data_are_found_without_echoing(self):
        self.init_org()
        secrets = {
            "Google API key": "key AIza" + "B" * 35,
            "private key": "-----BEGIN RSA PRIVATE KEY-----",
            "email address": "Contact jane.doe@client.example",
            "phone number": "Call +44 20 7946 0958",
            "credential assignment": "password: hunter22xyz",
            "URL with embedded password": "postgres://app:s3cretpw@db.internal/ads",
            "payment card number": "card 4111 1111 1111 1111",
            "figure marked confidential": "Revenue 12.4m (confidential)",
            "UK National Insurance number": "NI AB123456C",
        }
        self.fill_profile(extra="\n".join(f"- {value}" for value in secrets.values()))
        result = run("check", "--org", "acme", root=self.root)
        self.assertEqual(result.returncode, 1)
        for kind, value in secrets.items():
            self.assertIn(kind, result.stdout)
            self.assertNotIn(value.split()[-1], result.stdout)

    def test_ordinary_profile_text_is_not_flagged(self):
        result = run("scan", "-", stdin=(
            "- Secrets: Secret Manager only; no keys in code. (user, 2026-10-25)\n"
            "- Region europe-west2, reviewed 2026-10-25, review_by 2027-04-23.\n"
            "- max_tokens: 8192; model gemini-2.5-flash pinned.\n"
            "| L3 | Ask the KPI owner. | all | ads 2026-09-14 | 2.12.0 | active |\n"
            "- confidentiality: private\n"))
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_caps_frontmatter_and_staleness(self):
        org_dir = self.init_org()
        self.fill_profile(review_by="2026-01-01", extra="\n".join(f"- line {i}" for i in range(160)))
        rows = "".join(f"| L{i} | Lesson {i}. | all | ads 2026-09 | 2.12 | active |\n" for i in range(1, 43))
        (org_dir / "lessons.md").write_text(
            "---\norg: acme\nreviewed: 2026-10-25\nreview_by: 2027-04-23\n---\n\n"
            "| ID | Lesson | Tags | Source | ADK version | Status |\n| --- | --- | --- | --- | --- | --- |\n"
            + rows + "| L1 | Duplicate. | all | | 2.12 | maybe |\n", encoding="utf-8")
        result = run("check", "--org", "acme", root=self.root)
        self.assertEqual(result.returncode, 1)
        for fragment in ("prune to 150", "42 active lessons", "duplicate lesson id L1", "has no source",
                         "status must be one of", "STALE since 2026-01-01"):
            self.assertIn(fragment, result.stdout)

    def test_wrong_org_in_frontmatter_and_dangling_binding(self):
        org_dir = self.init_org()
        text = (org_dir / "profile.md").read_text().replace("org: acme", "org: globex")
        (org_dir / "profile.md").write_text(text)
        with (self.root / "bindings.md").open("a") as handle:
            handle.write(f"| {self.repo} | initech | 2026-10-25 |\n")
        result = run("check", root=self.root)
        self.assertIn("`org` 'globex' is not valid", result.stdout)
        self.assertIn("'initech' has no directory", result.stdout)

    def test_scan_file_reports_refusals(self):
        proposal = self.base / "proposal.md"
        proposal.write_text("+ - Stakeholder email: cto@client.example (user, 2026-10-25)\n")
        result = run("scan", str(proposal))
        self.assertEqual(result.returncode, 1)
        self.assertIn("REFUSE", result.stdout)
        self.assertIn("email address", result.stdout)


if __name__ == "__main__":
    unittest.main()
