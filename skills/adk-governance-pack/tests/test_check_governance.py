"""Exercise the governance checker through its CLI with hand-written drafts."""

import json
import re
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SKILL = Path(__file__).resolve().parents[1]
SCRIPT = SKILL / "scripts" / "check_governance.py"
TODAY = "2026-10-25"

POC_NOTE = """---
document: poc-note
system: Policy Q&A assistant
counsel_required: no
sources: docs/discovery/policy.md, docs/architecture/policy.md
---

# Governance note: Policy Q&A assistant

## Classification

- Employees ask questions about internal policies and receive answers grounded in the policy library (C1, D2).
- Article 50(1) of Regulation (EU) 2024/1689 applies from 2 August 2026 (checked 2026-10-20): users are told they are talking to an AI system (C4).
- No prohibited practice applies; counsel: confirm before the production decision.

## Data flow summary

| Step | Data | Where | Evidence |
| --- | --- | --- | --- |
| Question | Employee ID and question text | Cloud Run, europe-west4 | C2, D3 |
| Retrieval | Policy passages, no personal data | Vertex AI Search | D2 |

The question text is not written to logs (SB14).

## Questions for counsel

- counsel: Does the works council need to be informed before the pilot?
"""

DESIGN = """# System design: policy assistant
| ID | Invariant |
| --- | --- |
| C1 | Answers cite a policy passage |
| C2 | Employees see only their own records |
| C4 | The chat discloses it is an AI system |
| D2 | Vertex AI Search over the policy library |
| D3 | europe-west4 hosting |
| SB14 | No content in logs |
"""


def run(*args, files=None):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        paths = {}
        for name, text in (files or {}).items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
            paths[name] = str(path)
        argv = [paths.get(a[1:], a) if a.startswith("@") else a for a in args]
        result = subprocess.run([sys.executable, str(SCRIPT), "--today", TODAY, *argv],
                                capture_output=True, text=True)
        return result


class CheckGovernance(unittest.TestCase):
    def test_clean_note_passes_with_sources(self):
        result = run("@note.md", "--source", "@design.md", files={"note.md": POC_NOTE, "design.md": DESIGN})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("ok", result.stdout)

    def test_uncited_statement_fails(self):
        draft = POC_NOTE.replace("The question text is not written to logs (SB14).",
                                 "The question text is not written to logs.")
        result = run("@note.md", files={"note.md": draft})
        self.assertEqual(result.returncode, 1)
        self.assertIn("cites no ID", result.stdout)

    def test_markers_and_dated_sources_count_as_citations(self):
        draft = POC_NOTE.replace("The question text is not written to logs (SB14).",
                                 "assumption: the question text is not logged.\n\n"
                                 "Google Cloud does not train on prompts (source: Google Cloud docs, 2026-10-25).")
        result = run("@note.md", files={"note.md": draft})
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_missing_and_empty_sections_fail(self):
        draft = POC_NOTE.split("## Data flow summary")[0] + "## Data flow summary\n\n## Questions for counsel\n\n- counsel: x\n"
        result = run("@note.md", files={"note.md": draft})
        self.assertIn("empty section: ## Data flow summary", result.stdout)
        memo = "---\ndocument: classification-memo\ncounsel_required: pending\n---\n\n## Summary\n\n- n/a: draft\n"
        result = run("@memo.md", files={"memo.md": memo})
        self.assertIn("missing section: ## Roles", result.stdout)
        self.assertEqual(result.returncode, 1)

    def test_annex_iii_trigger_forces_counsel(self):
        draft = POC_NOTE.replace("Employees ask questions about internal policies",
                                 "Recruiters rank candidates by CV")
        result = run("@note.md", files={"note.md": draft})
        self.assertEqual(result.returncode, 1)
        self.assertIn("Annex III trigger (employment", result.stdout)
        fixed = draft.replace("counsel_required: no", "counsel_required: yes")
        self.assertEqual(run("@note.md", files={"note.md": fixed}).returncode, 0)

    def test_trigger_in_source_file_forces_counsel(self):
        brief = "# Discovery brief\nThe assistant screens job applicants before interviews.\n"
        result = run("@note.md", "--source", "@brief.md", "--source", "@design.md",
                     files={"note.md": POC_NOTE, "brief.md": brief, "design.md": DESIGN})
        self.assertEqual(result.returncode, 1)
        self.assertIn("brief.md:2", result.stdout)

    def test_out_of_scope_section_is_not_scanned_for_triggers(self):
        card = """---
document: system-card
counsel_required: no
---

## Intended use

- Answers policy questions for employees (C1).

## Out-of-scope use

- Hiring, promotion or dismissal decisions (C1).

## Limits

- assumption: answers only cover the policy library.

## Evaluation results

- 18 of 20 gold questions answered correctly (M1).

## Human oversight

- HR reviews flagged answers weekly (D2).

## Data

- Policy passages only (D2).

## Contact

- source: sponsor, 2026-10-25: hr-ai@example.com
"""
        result = run("@card.md", files={"card.md": card})
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_word_migration_and_model_performance_do_not_trigger(self):
        draft = POC_NOTE.replace("The question text is not written to logs (SB14).",
                                 "Database migration and model performance evaluation run in CI (D3).")
        self.assertEqual(run("@note.md", files={"note.md": draft}).returncode, 0)

    def test_legal_date_needs_checked_note(self):
        draft = POC_NOTE.replace(" (checked 2026-10-20)", "")
        result = run("@note.md", files={"note.md": draft})
        self.assertEqual(result.returncode, 1)
        self.assertIn("legal applicability date", result.stdout)

    def test_future_and_stale_checked_dates(self):
        future = POC_NOTE.replace("checked 2026-10-20", "checked 2027-01-01")
        self.assertIn("in the future", run("@note.md", files={"note.md": future}).stdout)
        stale = POC_NOTE.replace("checked 2026-10-20", "checked 2025-01-01")
        result = run("@note.md", files={"note.md": stale})
        self.assertEqual(result.returncode, 0)
        self.assertIn("warning", result.stdout)

    def test_invented_id_fails_against_sources(self):
        draft = POC_NOTE.replace("(C1, D2)", "(C9, D2)")
        result = run("@note.md", "--source", "@design.md", files={"note.md": draft, "design.md": DESIGN})
        self.assertIn("cites C9, which no source file contains", result.stdout)

    def test_placeholder_fails(self):
        draft = POC_NOTE.replace("Policy Q&A assistant\ncounsel", "<system>\ncounsel")
        draft = draft.replace("(SB14).", "(SB14). Owner: <name>.")
        result = run("@note.md", files={"note.md": draft})
        self.assertIn("unfilled placeholder <name>", result.stdout)

    def test_bad_front_matter_and_unknown_type_exit_2(self):
        self.assertEqual(run("@x.md", files={"x.md": "# no front matter\n"}).returncode, 2)
        self.assertEqual(run("@x.md", files={"x.md": "---\ndocument: essay\n---\n"}).returncode, 2)

    def test_counsel_field_required(self):
        draft = POC_NOTE.replace("counsel_required: no\n", "")
        self.assertIn("counsel_required must be", run("@note.md", files={"note.md": draft}).stdout)

    def test_json_output_and_directory_input(self):
        result = run("--json", "@pack/note.md", files={"pack/note.md": POC_NOTE})
        data = json.loads(result.stdout)
        self.assertEqual(data[0]["document"], "poc-note")
        self.assertEqual(data[0]["errors"], [])

    def test_filled_templates_need_no_extra_citations(self):
        """Boilerplate a drafter keeps verbatim must pass once placeholders hold IDs."""
        for template in sorted((SKILL / "assets").glob("*-template.md")):
            text = template.read_text(encoding="utf-8")
            text = re.sub(r"counsel_required: .*", "counsel_required: yes", text)
            previous = None
            while previous != text:
                previous, text = text, re.sub(r"<[A-Za-z][^<>\n]*>", "C1", text)
            result = run("@draft.md", files={"draft.md": text})
            self.assertEqual(result.returncode, 0, f"{template.name}: {result.stdout}{result.stderr}")

    def test_iso_project_dates_and_read_dates_are_not_applicability_dates(self):
        line = ("- counsel: Article 22 applies to rejections from the pilot on 2026-12-01; "
                "the GDPR text was read 2 March 2026 (C1).")
        draft = POC_NOTE.replace("The question text is not written to logs (SB14).", line)
        self.assertEqual(run("@note.md", files={"note.md": draft}).returncode, 0)

    def test_bare_marker_does_not_count(self):
        draft = POC_NOTE.replace("The question text is not written to logs (SB14).", "Logs are kept for a period the design does not record anywhere. gap:")
        self.assertIn("cites no ID", run("@note.md", files={"note.md": draft}).stdout)

    def test_omitted_baseline_rule_may_be_named_as_gap(self):
        draft = POC_NOTE.replace("The question text is not written to logs (SB14).",
                                 "gap: no penetration test (SB24 is not in the design's table).")
        result = run("@note.md", "--source", "@design.md", files={"note.md": draft, "design.md": DESIGN})
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_transparency_checklist_does_not_trigger_biometrics(self):
        memo_row = "\n## Transparency obligations (Article 50)\n\n- 50(3) emotion recognition or biometric categorisation: n/a: none.\n"
        draft = POC_NOTE.replace("## Questions for counsel", memo_row + "\n## Questions for counsel")
        result = run("--json", "@note.md", files={"note.md": draft})
        self.assertEqual(json.loads(result.stdout)[0]["annex_iii_areas"], [])

    def test_templates_fail_until_filled(self):
        templates = sorted((SKILL / "assets").glob("*-template.md"))
        self.assertEqual(len(templates), 7)
        for template in templates:
            result = subprocess.run([sys.executable, str(SCRIPT), "--today", TODAY, str(template)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 1, f"{template.name}: {result.stdout}{result.stderr}")
            self.assertIn("placeholder", result.stdout, template.name)


if __name__ == "__main__":
    unittest.main()
