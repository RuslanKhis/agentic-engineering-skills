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
        self.assertIn("## Dimensions: no row for Deployment", result.stdout)
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
        self.assertIn("over 90 days old", result.stdout)


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


STRATEGY = "Keep the current build and record this exit plan;"


class ReviewEstimates(unittest.TestCase):
    """Review findings: estimates hide in hyphens, words, dates and other cells."""

    def assert_figure(self, text, figure):
        result = run(replace(STRATEGY, f"Keep the current build and record this exit plan, {text};"))
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn(f"figure {figure!r}", result.stdout)

    def test_hyphenated_units(self):
        self.assert_figure("after a 3-week spike", "3-week")
        self.assert_figure("with a 2-week window", "2-week")

    def test_years_quarters_fortnights(self):
        self.assert_figure("over 2 years", "2 years")
        self.assert_figure("within 1 quarter", "1 quarter")
        self.assert_figure("in 3 fortnights", "3 fortnights")

    def test_number_words(self):
        self.assert_figure("in about three weeks", "three weeks")
        self.assert_figure("after a couple of months", "a couple of months")
        self.assert_figure("in a few sprints", "a few sprints")
        self.assert_figure("a twelve-month programme", "twelve-month")

    def test_invented_dates_in_estimate_sections(self):
        self.assert_figure("cutting over in Q3 2027", "Q3 2027")
        self.assert_figure("cutting over by March 2027", "March 2027")
        self.assert_figure("cutting over by 2027-03", "2027-03")

    def test_dates_outside_estimate_sections_pass(self):
        text = replace("- Identity (D7, C3):", "- The EU Data Act applies from January 2027. Identity (D7, C3):")
        self.assertEqual(run(text).returncode, 0, run(text).stdout)

    def test_assumption_in_another_cell_does_not_clear_a_figure(self):
        result = run(replace("| Rehost container and sessions | small | One adapter contract test; dump and restore |",
                             "| Rehost container and sessions | small | One adapter contract test taking 3 weeks |"))
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("figure '3 weeks'", result.stdout)

    def test_assumption_in_another_sentence_does_not_clear_a_figure(self):
        self.assert_figure("which takes 6 weeks. The rest is an assumption", "6 weeks")

    def test_assumption_label_covers_its_clause(self):
        text = replace(STRATEGY, "Keep the current build and record this exit plan (assumption: a 6-week move);")
        self.assertEqual(run(text).returncode, 0, run(text).stdout)


class ReviewOverpromise(unittest.TestCase):
    def test_negation_must_be_near(self):
        result = run(replace("Running on two clouds now",
                             "This is not what we expect, but the design is fully portable. Running on two clouds now"))
        self.assertIn("overpromise 'fully portable'", result.stdout)

    def test_more_negations(self):
        for text in ("Bedrock won't be a drop-in replacement", "Bedrock isn't a drop-in replacement"):
            with self.subTest(text=text):
                self.assertEqual(run(replace("Running on two clouds now", text + "; running on two clouds now"))
                                 .returncode, 0)

    def test_new_phrases(self):
        for phrase in ("no vendor lock-in", "a cloud-agnostic design", "a seamless switch", "seamlessly move"):
            with self.subTest(phrase=phrase):
                result = run(replace("Running on two clouds now", f"It gives {phrase}; running on two clouds now"))
                self.assertIn("overpromise", result.stdout)

    def test_not_cloud_agnostic_passes(self):
        text = replace("Running on two clouds now", "The design is not cloud-agnostic; running on two clouds now")
        self.assertEqual(run(text).returncode, 0, run(text).stdout)

    def test_quoted_stakeholder_words_pass(self):
        straight = replace("Running on two clouds now", 'The board asked for "zero lock-in"; running on two clouds now')
        self.assertEqual(run(straight).returncode, 0, run(straight).stdout)
        curly = replace("Running on two clouds now", "The board asked for \u201cno vendor lock-in\u201d; running on two clouds now")
        self.assertEqual(run(curly).returncode, 0, run(curly).stdout)
        quote = replace("## Concern and scope\n", "## Concern and scope\n\n> Can we have zero lock-in?\n")
        self.assertEqual(run(quote).returncode, 0, run(quote).stdout)


class ReviewDimensions(unittest.TestCase):
    def test_dimension_needs_its_own_row(self):
        text = replace("| Deployment | Not a concern: one Cloud Run container with no Agent Runtime features, so the "
                       "deployment rehosts as a container. |",
                       "| Rollout | Assessed: the deployment rehosts as a container. |")
        result = run(text)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("## Dimensions: no row for Deployment", result.stdout)

    def test_framework_row_label_accepted(self):
        text = replace("| Agent framework | Assessed:", "| Framework | Assessed:")
        self.assertEqual(run(text).returncode, 0, run(text).stdout)

    def test_not_a_concern_cell_needs_reason(self):
        line = next(l for l in ASSESSMENT.splitlines() if l.startswith("| Deployment |"))
        result = run(replace(line, "| Deployment | Not a concern |"))
        self.assertIn("'not a concern' needs a reason", result.stdout)


class ReviewCoverage(unittest.TestCase):
    def test_uncited_design_decision_warns(self):
        design = DESIGN.replace("## Open decisions", "| D10 | C1 | Weekly export | Audit | — | Export test |\n\n## Open decisions")
        result = run(ASSESSMENT, design=design)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("D10 is cited by no Component classification row", result.stdout)
        self.assertNotIn("D9 is cited by no", result.stdout)


class ReviewCommands(unittest.TestCase):
    def fence(self, block):
        return run(replace("## Open questions\n", "## Open questions\n\n" + block + "\n"))

    def test_cloudformation(self):
        result = self.fence("```yaml\nAWSTemplateFormatVersion: '2010-09-09'\nResources: {}\n```\n")
        self.assertIn("CloudFormation", result.stdout)
        result = self.fence("```yaml\nResources:\n  Q:\n    Type: AWS::SQS::Queue\n```\n")
        self.assertIn("CloudFormation", result.stdout)

    def test_untagged_bicep(self):
        result = self.fence("```\nresource app 'Microsoft.App/containerApps@2024-03-01' = {}\n```\n")
        self.assertIn("Bicep", result.stdout)

    def test_cloud_cli_commands(self):
        for command in ("aws ecs create-service --cluster triage", "$ az containerapp up -n triage",
                        "gcloud run deploy triage", "kubectl apply -f app.yaml", "terraform apply",
                        "eksctl create cluster", "helm install triage ./chart"):
            with self.subTest(command=command):
                result = self.fence(f"```bash\n{command}\n```\n")
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("cloud CLI command", result.stdout)

    def test_ordinary_block_passes(self):
        self.assertEqual(self.fence("```text\nclassify -> retrieve -> draft\n```\n").returncode, 0)


class ReviewFalsePositives(unittest.TestCase):
    def test_no_recommendations_sentence(self):
        start = ASSESSMENT.index("None of these is a ticket")
        end = ASSESSMENT.index("## Open questions")
        result = run(ASSESSMENT[:start] + "No recommendations.\n\n" + ASSESSMENT[end:])
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_pydanticai_alias(self):
        text = replace("frameworks: [langgraph, microsoft-agent-framework, pydantic-ai]",
                       "frameworks: [langgraph, microsoft-agent-framework, pydanticai]")
        text = text.replace("| Pydantic AI |\n", "| PydanticAI |\n", 1)
        result = run(text)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertNotIn("not in the reference", result.stdout)

    def test_email_is_not_a_placeholder(self):
        text = replace("(CTO; it decides whether", "(CTO, <cto@insurer.example>; it decides whether")
        self.assertEqual(run(text).returncode, 0, run(text).stdout)

    def test_ninety_day_freshness(self):
        result = run(replace("| https://adk.dev/sessions/session/ | 2026-10-26 |",
                             "| https://adk.dev/sessions/session/ | 2026-07-20 |"))
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("over 90 days old", result.stdout)

if __name__ == "__main__":
    unittest.main()
