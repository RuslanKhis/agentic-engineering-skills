"""Exercise the portability checker through its CLI with a filled claims-triage assessment."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SKILL = Path(__file__).resolve().parents[1]
SCRIPT = SKILL / "scripts" / "check_portability.py"
TEMPLATE = SKILL / "assets" / "portability-assessment-template.md"
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "claims-triage"
TODAY = "2026-10-26"
ASSESSMENT = (FIXTURES / "assessment.md").read_text(encoding="utf-8")
DESIGN = (FIXTURES / "design.md").read_text(encoding="utf-8")
PLAN = (FIXTURES / "plan.md").read_text(encoding="utf-8")
INSTALLED = ("adk-agent-evaluation", "adk-agent-observability", "adk-portability-planning")


def run(assessment=ASSESSMENT, *extra, design=DESIGN, plan=PLAN, raw=None):
    """Run the checker in a temporary project with a fake skills directory."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        skills = root / "skills"
        for name in INSTALLED:
            (skills / name).mkdir(parents=True)
            (skills / name / "SKILL.md").write_text(f"---\nname: {name}\n---\n", encoding="utf-8")
        target = root / "docs" / "portability" / "claims-triage.md"
        target.parent.mkdir(parents=True)
        if raw is not None:
            target.write_bytes(raw)
        else:
            target.write_text(assessment, encoding="utf-8")
        argv = [str(target), "--skills-dir", str(skills), "--today", TODAY]
        for flag, text in (("--design", design), ("--plan", plan)):
            if text is not None:
                path = root / f"{flag[2:]}.md"
                path.write_text(text, encoding="utf-8")
                argv += [flag, str(path)]
        return subprocess.run([sys.executable, "-I", str(SCRIPT), *argv, *extra], capture_output=True, text=True)


def replace(old, new, text=ASSESSMENT):
    if old not in text:
        raise AssertionError(f"fixture text not found: {old!r}")
    return text.replace(old, new, 1)


class FilledExample(unittest.TestCase):
    def test_fixture_passes(self):
        result = run()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(result.stdout.startswith("ok"), result.stdout)
        self.assertNotIn("error:", result.stdout)

    def test_json_output(self):
        result = run(ASSESSMENT, "--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        summary = json.loads(result.stdout)
        self.assertTrue(summary["ok"])
        self.assertEqual(summary["targets"], ["aws", "azure"])
        self.assertEqual(summary["classes"]["expensive dependency"], 2)
        self.assertEqual(summary["errors"], [])

    def test_fixture_passes_against_installed_skills(self):
        result = subprocess.run([sys.executable, "-I", str(SCRIPT), str(FIXTURES / "assessment.md"),
                                 "--design", str(FIXTURES / "design.md"), "--plan", str(FIXTURES / "plan.md"),
                                 "--today", TODAY], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unfilled_template_fails_on_placeholders(self):
        result = subprocess.run([sys.executable, "-I", str(SCRIPT), str(TEMPLATE), "--today", TODAY],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("unfilled placeholder <topic>", result.stdout)
        self.assertNotIn("missing section", result.stdout)


class Structure(unittest.TestCase):
    def test_missing_heading(self):
        result = run(replace("## Open questions\n", "## Questions\n"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing section: ## Open questions", result.stdout)

    def test_headings_out_of_order(self):
        start = ASSESSMENT.index("## Recommended strategy")
        end = ASSESSMENT.index("## Phased outline")
        block = ASSESSMENT[start:end]
        moved = ASSESSMENT[:start] + ASSESSMENT[end:]
        moved = moved.replace("## Sources", block + "## Sources", 1)
        result = run(moved)
        self.assertEqual(result.returncode, 1)
        self.assertIn("out of order", result.stdout)

    def test_empty_section(self):
        start = ASSESSMENT.index("## Open questions\n") + len("## Open questions\n")
        end = ASSESSMENT.index("## Sources")
        result = run(ASSESSMENT[:start] + "\n" + ASSESSMENT[end:])
        self.assertIn("empty section: ## Open questions", result.stdout)

    def test_leftover_placeholder(self):
        result = run(replace("- Does group IT have a date", "- <question for stakeholders> Does group IT have a date"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("unfilled placeholder <question for stakeholders>", result.stdout)

    def test_placeholder_in_code_span_is_ignored(self):
        result = run(replace("- Pinned Gemini Flash model", "- Pinned Gemini Flash model (see `docs/<topic>.md`)"))
        self.assertEqual(result.returncode, 0, result.stdout)


class FrontMatter(unittest.TestCase):
    def test_primary_build_must_name_gcp_and_adk(self):
        result = run(replace("primary_build: GCP + Google ADK (unchanged)", "primary_build: AWS + LangGraph"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("primary_build must name GCP and ADK", result.stdout)

    def test_status_and_targets_vocabulary(self):
        result = run(replace("status: draft", "status: final").replace("targets: [aws, azure]", "targets: [aws, oci]"))
        self.assertIn("status must be draft or reviewed", result.stdout)
        self.assertIn("unknown target oci", result.stdout)

    def test_missing_field(self):
        result = run(replace("concern: The insurer's CTO", "worry: The insurer's CTO"))
        self.assertIn("front matter: missing concern", result.stdout)

    def test_target_and_framework_must_be_assessed(self):
        start = ASSESSMENT.index("## Cloud alternatives\n")
        end = ASSESSMENT.index("## Agent framework alternatives")
        azure_only = ("## Cloud alternatives\n\n| Responsibility | GCP (design ID) | Azure | Difference | Portability |\n"
                      "| --- | --- | --- | --- | --- |\n| Hosting | Cloud Run (D1) | Container Apps | Image runs as is "
                      "| moderate |\n\n")
        text = ASSESSMENT[:start] + azure_only + ASSESSMENT[end:]
        text = text.replace("frameworks: [langgraph,", "frameworks: [openai-agents, langgraph,", 1)
        result = run(text)
        self.assertEqual(result.returncode, 1)
        self.assertIn("## Cloud alternatives: aws is listed in the front matter but not assessed here", result.stdout)
        self.assertIn("## Agent framework alternatives: openai-agents is listed", result.stdout)
        self.assertNotIn("azure is listed", result.stdout)


class Classification(unittest.TestCase):
    def test_unknown_class(self):
        result = run(replace("| D3 | replaceable adapter |", "| D3 | portable |"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("class 'portable' for Sessions is not one of", result.stdout)

    def test_empty_why(self):
        result = run(replace("| Hosting | D1 | provider-specific by choice | A Cloud Run container |",
                             "| Hosting | D1 | provider-specific by choice |  |"))
        self.assertIn("Hosting has no Why", result.stdout)

    def test_expensive_dependency_without_exit_path_warns(self):
        line = next(l for l in ASSESSMENT.splitlines() if l.startswith("| Policy corpus retrieval"))
        cells = line.split("|")
        cells[5] = " — "
        result = run(replace(line, "|".join(cells)))
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("expensive dependency Policy corpus retrieval has no exit path", result.stdout)

    def test_dimension_missing_and_unreasoned_not_a_concern(self):
        text = replace("| Deployment | Not a concern: one Cloud Run container with no Agent Runtime features, so the "
                       "deployment rehosts as a container. |", "| Rollout | Not a concern: |")
        result = run(text)
        self.assertIn("## Dimensions: deployment is not assessed", result.stdout)
        self.assertIn("'not a concern' needs a reason", result.stdout)


class Citations(unittest.TestCase):
    def test_invented_id(self):
        result = run(replace("(D9; design-only)", "(D9, D14; design-only)"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("cites D14, which neither the design nor the plan contains", result.stdout)

    def test_invented_measurement_cannot_launder_a_figure(self):
        result = run(replace("14 hands-on hours (M2)", "14 hands-on hours (M7)"))
        self.assertIn("cites M7", result.stdout)

    def test_missing_design_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "a.md"
            target.write_text(ASSESSMENT, encoding="utf-8")
            result = subprocess.run([sys.executable, "-I", str(SCRIPT), str(target), "--design",
                                     str(Path(tmp) / "nope.md"), "--today", TODAY], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("does not exist", result.stdout)

    def test_ids_unchecked_without_design_or_plan_warns(self):
        result = run(ASSESSMENT, design=None, plan=None)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("cited IDs were not checked", result.stdout)

    def test_source_without_date(self):
        result = run(replace("| https://adk.dev/sessions/session/ | 2026-10-26 |", "| https://adk.dev/sessions/session/ |  |"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("is not a date", result.stdout)

    def test_source_without_url(self):
        result = run(replace("| https://adk.dev/sessions/session/ |", "| adk.dev sessions page |"))
        self.assertIn("source has no http(s) URL", result.stdout)

    def test_future_dates(self):
        result = run(replace("| https://adk.dev/sessions/session/ | 2026-10-26 |",
                             "| https://adk.dev/sessions/session/ | 2026-11-02 |").replace(
            "sources_checked: 2026-10-26", "sources_checked: 2026-12-01"))
        self.assertIn("source read date 2026-11-02 is in the future", result.stdout)
        self.assertIn("sources_checked 2026-12-01 is in the future", result.stdout)

    def test_old_source_warns(self):
        result = run(replace("| https://adk.dev/sessions/session/ | 2026-10-26 |",
                             "| https://adk.dev/sessions/session/ | 2026-01-05 |"))
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("over 180 days old", result.stdout)


class Figures(unittest.TestCase):
    def test_hours_without_measurement_or_assumption(self):
        result = run(replace("Keep the current build and record this exit plan;",
                             "Keep the current build and record this exit plan, which a move would take 6 weeks to use;"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("figure '6 weeks'", result.stdout)

    def test_person_days_and_price(self):
        result = run(replace("| Safety screening | medium |", "| Safety screening (12 person-days, $4,000) | medium |"))
        self.assertIn("needs a plan measurement", result.stdout)

    def test_figure_with_assumption_or_measurement_passes(self):
        text = replace("Keep the current build and record this exit plan;",
                       "Keep the current build and record this exit plan (assumption: a move takes 6 weeks);")
        self.assertEqual(run(text).returncode, 0)

    def test_provider_limit_outside_estimate_sections_passes(self):
        text = replace("- Identity (D7, C3):", "- Sessions: AgentCore Runtime caps a session at 8 hours. Identity (D7, C3):")
        self.assertEqual(run(text).returncode, 0, run(text).stdout)

    def test_price_outside_estimate_sections_still_fails(self):
        result = run(replace("- Identity (D7, C3):", "- Identity costs $400 a month. Identity (D7, C3):"))
        self.assertIn("figure '$4'", result.stdout)

    def test_m365_is_not_a_measurement(self):
        text = replace("- Identity (D7, C3):", "- Identity (D7, C3), as with M365 tenants:")
        self.assertEqual(run(text).returncode, 0, run(text).stdout)
        result = run(replace("Keep the current build and record this exit plan;",
                             "Keep the current build and record this exit plan, 6 weeks like M365;"))
        self.assertIn("figure '6 weeks'", result.stdout)

    def test_figures_in_sources_are_ignored(self):
        text = replace("| Cost of avoiding lock-in |", "| Cost of avoiding lock-in (2019 essay, 12 months of data) |")
        self.assertEqual(run(text).returncode, 0)


class Overpromise(unittest.TestCase):
    def test_overpromise_fails(self):
        result = run(replace("Keep the current build and record this exit plan;",
                             "The design is fully portable, so keep the current build and record this exit plan;"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("overpromise 'fully portable'", result.stdout)

    def test_each_phrase(self):
        for phrase in ("seamless migration", "drop-in replacement", "zero lock-in", "100% portable",
                       "completely cloud-agnostic", "no lock-in"):
            with self.subTest(phrase=phrase):
                result = run(replace("Running on two clouds now", f"With {phrase}, running on two clouds now"))
                self.assertIn("overpromise", result.stdout)

    def test_negated_phrase_passes(self):
        text = replace("Running on two clouds now", "A move is not a seamless migration, and running on two clouds now")
        self.assertEqual(run(text).returncode, 0)
        self.assertEqual(run(replace("Running on two clouds now",
                                     "Bedrock isn't a drop-in replacement; running on two clouds now")).returncode, 0)


class ImplementationContent(unittest.TestCase):
    def test_terraform_block(self):
        block = '```hcl\nresource "aws_ecs_service" "triage" {}\n```\n\n'
        result = run(replace("## Open questions\n", "## Open questions\n\n" + block))
        self.assertEqual(result.returncode, 1)
        self.assertIn("hcl code block", result.stdout)

    def test_untagged_terraform_resource(self):
        block = '```\nresource "azurerm_container_app" "triage" {}\n```\n\n'
        result = run(replace("## Open questions\n", "## Open questions\n\n" + block))
        self.assertIn("Terraform resource", result.stdout)

    def test_kubernetes_manifest(self):
        block = "```yaml\napiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: triage\n```\n\n"
        result = run(replace("## Open questions\n", "## Open questions\n\n" + block))
        self.assertEqual(result.returncode, 1)
        self.assertIn("Kubernetes manifest", result.stdout)

    def test_iam_policy(self):
        block = '```json\n{"Version": "2012-10-17", "Statement": []}\n```\n\n'
        result = run(replace("## Open questions\n", "## Open questions\n\n" + block))
        self.assertIn("IAM policy", result.stdout)


class Recommendations(unittest.TestCase):
    def test_uninstalled_specialist(self):
        result = run(replace("- **Specialist:** `adk-agent-observability`", "- **Specialist:** `adk-cloud-migrator`"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("specialist adk-cloud-migrator is not an installed skill", result.stdout)

    def test_recommendation_needs_fields(self):
        result = run(replace("- **Rationale:** a target's exporter then changes without a code change (D8).\n", ""))
        self.assertIn("has no Rationale", result.stdout)

    def test_none_passes(self):
        start = ASSESSMENT.index("None of these is a ticket")
        end = ASSESSMENT.index("## Open questions")
        self.assertEqual(run(ASSESSMENT[:start] + "None.\n\n" + ASSESSMENT[end:]).returncode, 0)


class Effort(unittest.TestCase):
    def test_unknown_effort_word(self):
        result = run(replace("| Identity and access | medium |", "| Identity and access | moderate |"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("effort 'moderate' for Identity and access", result.stdout)

    def test_empty_drivers(self):
        line = next(l for l in ASSESSMENT.splitlines() if l.startswith("| Safety screening | medium |"))
        cells = line.split("|")
        cells[3] = " "
        result = run(replace(line, "|".join(cells)))
        self.assertIn("Safety screening has no Drivers", result.stdout)

    def test_reevaluation_sized_small_warns(self):
        result = run(replace("| Policy corpus rebuild | medium |", "| Policy corpus rebuild | small |"))
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("at least medium", result.stdout)


class Unreadable(unittest.TestCase):
    def test_missing_file(self):
        result = subprocess.run([sys.executable, "-I", str(SCRIPT), "/nonexistent/portability.md"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("cannot read", result.stderr)

    def test_not_utf8(self):
        self.assertEqual(run(raw=b"---\ntopic: \xff\xfe\n---\n").returncode, 2)

    def test_no_front_matter(self):
        result = run("# Portability assessment\n\n## Summary for the reader\n")
        self.assertEqual(result.returncode, 2)
        self.assertIn("no front matter", result.stderr)


if __name__ == "__main__":
    unittest.main()
