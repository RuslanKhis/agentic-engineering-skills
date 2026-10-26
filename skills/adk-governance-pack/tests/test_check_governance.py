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
TODAY = "2026-10-26"

POC_NOTE = """---
document: poc-note
system: Policy Q&A assistant
jurisdictions: [au, eu]
counsel_required: no
sources: docs/discovery/policy.md, docs/architecture/policy.md
---

# Governance note: Policy Q&A assistant

## Classification

- Employees ask questions about internal policies and receive answers grounded in the policy library (C1, D2).
- Australia: in scope, because consultancy staff in Sydney support the service (D3).
- United States: n/a: no US client, staff or customers.
- EU: in scope, because the client employs staff in the Netherlands (D3).
- United Kingdom: n/a: no UK establishment or staff.
- New Zealand: n/a: no New Zealand client, staff or customers.
- Singapore: n/a: no Singapore client, staff or customers.
- Canada: n/a: no Canadian client, staff or customers.
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
| D3 | europe-west4 hosting; support from Sydney |
| SB14 | No content in logs |
"""

SCREEN = """## Jurisdiction screen

| Regime | In scope | Trigger facts | Reason |
| --- | --- | --- | --- |
| Australia | yes | Consultancy staff in Sydney (D3) | The consultancy's own handling; counsel: Privacy Act reach |
| United States | no | No US data subjects (D3) | n/a: no US client or people |
| EU | no | No EU people (D3) | n/a: Australian staff only |
| United Kingdom | no | No UK people (D3) | n/a: no UK establishment |
| New Zealand | no | No New Zealand people (D3) | n/a: no NZ client or people |
| Singapore | no | No Singapore people (D3) | n/a: no Singapore client or people |
| Canada | no | No people in Canada (D3) | n/a: no Canadian client or people |
"""

AU_MEMO = """---
document: regulatory-memo
jurisdictions: [au]
counsel_required: pending
---

# Regulatory memo: HR assistant

## Summary

- Australia only (D3).

""" + SCREEN + """
## System and intended purpose

- Answers HR policy questions for staff (C1).

## Roles

- counsel: the client is an APP entity; the employee records exemption does not cover the consultancy (D3).

## Australia: Privacy Act and APPs

- APP 8 facts: model processing in Sydney (D3).

## Australia: Automated decisions (APP 1.7)

- n/a: no decision about a person (C1).

## Australia: Sector, state and government AI policy

- n/a: private client, no sector regulator (D2).

## Applicable dates

- APP 1.7 applies from 10 December 2026 (checked 2026-10-26).

## Questions for counsel

- counsel: is prompt logging computer surveillance (D3)?
"""


BANNER = ("> **Drafting aid output, not legal advice.** Prepared to support the reviewer named in `for:`. "
          "It is not reviewed until that reviewer records a decision in Review and sign-off.\n")
SIGNOFF = ("\n## Review and sign-off\n\n| Reviewer (role) | Scope reviewed | Decision | Date |\n"
           "| --- | --- | --- | --- |\n| Privacy officer | This document | pending | pending |\n")


def framed(text):
    """Add what every draft carries (status, banner, sign-off) unless the test wrote it."""
    if not text.startswith("---\ndocument:"):
        return text
    if "\nstatus:" not in text.split("\n---\n", 1)[0]:
        text = text.replace("---\ndocument:", "---\nstatus: draft\ndocument:", 1)
    if "not legal advice" not in text:
        head, sep, body = text.partition("\n---\n")
        text = head + sep + "\n" + BANNER + body
    if "## Review and sign-off" not in text:
        text = text.rstrip("\n") + "\n" + SIGNOFF
    return text


def run(*args, files=None, frame=True):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        paths = {}
        for name, text in (files or {}).items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(framed(text) if frame else text, encoding="utf-8")
            paths[name] = str(path)
        argv = [paths.get(a[1:], a) if a.startswith("@") else a for a in args]
        result = subprocess.run([sys.executable, "-I", str(SCRIPT), "--today", TODAY, *argv],
                                capture_output=True, text=True)
        return result


def with_line(draft, line):
    return draft.replace("The question text is not written to logs (SB14).", line)


class CheckGovernance(unittest.TestCase):
    def test_clean_note_passes_with_sources(self):
        result = run("@note.md", "--source", "@design.md", files={"note.md": POC_NOTE, "design.md": DESIGN})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("ok", result.stdout)
        self.assertIn("jurisdictions: au, eu", result.stdout)

    def test_uncited_statement_fails(self):
        draft = with_line(POC_NOTE, "The question text is not written to logs.")
        result = run("@note.md", files={"note.md": draft})
        self.assertEqual(result.returncode, 1)
        self.assertIn("cites no ID", result.stdout)

    def test_markers_and_dated_sources_count_as_citations(self):
        draft = with_line(POC_NOTE, "assumption: the question text is not logged.\n\n"
                                    "Google Cloud does not train on prompts (source: Google Cloud docs, 2026-10-25).")
        result = run("@note.md", files={"note.md": draft})
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_missing_and_empty_sections_fail(self):
        draft = POC_NOTE.split("## Data flow summary")[0] + "## Data flow summary\n\n## Questions for counsel\n\n- counsel: x\n"
        result = run("@note.md", files={"note.md": draft})
        self.assertIn("empty section: ## Data flow summary", result.stdout)
        memo = "---\ndocument: regulatory-memo\njurisdictions: [eu]\ncounsel_required: pending\n---\n\n## Summary\n\n- n/a: draft\n"
        result = run("@memo.md", files={"memo.md": memo})
        self.assertIn("missing section: ## Roles", result.stdout)
        self.assertIn("missing section: ## EU: High-risk classification", result.stdout)
        self.assertNotIn("Australia: Privacy Act", result.stdout)
        self.assertEqual(result.returncode, 1)

    def test_required_sections_follow_jurisdictions(self):
        result = run("@memo.md", files={"memo.md": AU_MEMO})
        self.assertEqual(result.returncode, 0, result.stdout)
        with_us = AU_MEMO.replace("jurisdictions: [au]", "jurisdictions: [au, us]")
        result = run("@memo.md", files={"memo.md": with_us})
        self.assertIn("missing section: ## United States: Preemption status and FTC claims", result.stdout)
        self.assertNotIn("EU: Prohibited practices", result.stdout)

    def test_regime_section_without_its_jurisdiction_fails(self):
        draft = AU_MEMO.replace("## Applicable dates", "## EU: Other regimes\n\n- n/a: no EU users (D3).\n\n## Applicable dates")
        result = run("@memo.md", files={"memo.md": draft})
        self.assertEqual(result.returncode, 1)
        self.assertIn("belongs to EU, which jurisdictions does not list", result.stdout)

    def test_missing_empty_unknown_and_unordered_jurisdictions_fail(self):
        missing = POC_NOTE.replace("jurisdictions: [au, eu]\n", "")
        self.assertIn("jurisdictions is missing or empty", run("@n.md", files={"n.md": missing}).stdout)
        empty = POC_NOTE.replace("jurisdictions: [au, eu]", "jurisdictions: []")
        result = run("@n.md", files={"n.md": empty})
        self.assertEqual(result.returncode, 1)
        self.assertIn("jurisdictions is missing or empty", result.stdout)
        unknown = POC_NOTE.replace("jurisdictions: [au, eu]", "jurisdictions: [au, jp]")
        self.assertIn("unknown jurisdiction jp", run("@n.md", files={"n.md": unknown}).stdout)
        unordered = POC_NOTE.replace("jurisdictions: [au, eu]", "jurisdictions: [eu, au]")
        self.assertIn("order au, us, eu, uk, nz, sg, ca", run("@n.md", files={"n.md": unordered}).stdout)
        late = POC_NOTE.replace("jurisdictions: [au, eu]", "jurisdictions: [au, ca, nz]")
        self.assertIn("order au, us, eu, uk, nz, sg, ca", run("@n.md", files={"n.md": late}).stdout)
        bare = POC_NOTE.replace("jurisdictions: [au, eu]", "jurisdictions: au, eu")
        self.assertEqual(run("@n.md", files={"n.md": bare}).returncode, 0)

    def test_screen_must_name_every_regime(self):
        draft = AU_MEMO.replace("| United Kingdom | no | No UK people (D3) | n/a: no UK establishment |\n", "")
        result = run("@memo.md", files={"memo.md": draft})
        self.assertEqual(result.returncode, 1)
        self.assertIn("names no row for United Kingdom", result.stdout)
        note = POC_NOTE.replace("- United States: n/a: no US client, staff or customers.\n", "")
        self.assertIn("names no row for United States", run("@n.md", files={"n.md": note}).stdout)

    def test_records_and_transfer_annex_need_gdpr_regime(self):
        records = ("---\ndocument: processing-records\njurisdictions: [au, us]\ncounsel_required: pending\n---\n\n"
                   "## Processing activities\n\n- n/a: no rows (D3).\n")
        result = run("@r.md", files={"r.md": records})
        self.assertIn("applies under GDPR or UK GDPR only", result.stdout)
        self.assertEqual(run("@r.md", files={"r.md": records.replace("[au, us]", "[au, uk]")}).returncode, 0)

    def test_legacy_document_types_still_read(self):
        memo = AU_MEMO.replace("document: regulatory-memo", "document: classification-memo")
        result = run("--json", "@memo.md", files={"memo.md": memo})
        self.assertEqual(json.loads(result.stdout)[0]["document"], "regulatory-memo")
        pack = "---\ndocument: dpia-input-pack\njurisdictions: [eu]\ncounsel_required: pending\n---\n"
        self.assertIn("missing section: ## EU: Legal basis", run("@p.md", files={"p.md": pack}).stdout)

    def test_annex_iii_trigger_forces_counsel(self):
        draft = POC_NOTE.replace("Employees ask questions about internal policies",
                                 "Recruiters rank candidates by CV")
        result = run("@note.md", files={"note.md": draft})
        self.assertEqual(result.returncode, 1)
        self.assertIn("counsel trigger (employment", result.stdout)
        fixed = draft.replace("counsel_required: no", "counsel_required: yes")
        self.assertEqual(run("@note.md", files={"note.md": fixed}).returncode, 0)

    def test_other_regime_triggers_force_counsel(self):
        cases = {
            "children": "The tutor app is directed at children aged 8 to 12 (C1).",
            "biometrics": "Callers are verified by voiceprint before account changes (C1).",
            "public-body clients": "The client is a non-corporate Commonwealth entity (D2).",
            "housing": "The agent supports tenant screening for property managers (C1).",
            "automated decisions": "Refunds under $50 are a solely automated decision (C1).",
            "health care": "Summaries feed treatment decisions in the clinic (C1).",
        }
        for area, line in cases.items():
            result = run("--json", "@note.md", files={"note.md": with_line(POC_NOTE, line)})
            data = json.loads(result.stdout)[0]
            self.assertIn(area, data["counsel_triggers"], line)
            self.assertEqual(result.returncode, 1, line)

    def test_negated_trigger_phrases_do_not_fire(self):
        for line in ("n/a: the service is not likely to be accessed by children (C1).",
                     "No solely automated decisions are made; a person approves each refund (C1)."):
            result = run("--json", "@note.md", files={"note.md": with_line(POC_NOTE, line)})
            self.assertEqual(json.loads(result.stdout)[0]["counsel_triggers"], [], line)

    def test_drafter_negation_skips_a_trigger_but_a_bare_cell_does_not(self):
        for line in ("n/a: no PHI, MDR device or under-13 data is processed (C1).",
                     "No court order stays a state law relied on here (checked 2026-10-26)."):
            result = run("--json", "@note.md", files={"note.md": with_line(POC_NOTE, line)})
            self.assertEqual(json.loads(result.stdout)[0]["counsel_triggers"], [], line)
        table = "| Use | Applies | Evidence |\n| --- | --- | --- |\n| Hiring decisions | n/a: none | C1 |"
        result = run("--json", "@note.md", files={"note.md": with_line(POC_NOTE, table)})
        self.assertEqual(json.loads(result.stdout)[0]["counsel_triggers"], ["employment"])

    def test_performance_management_uses_trigger(self):
        line = "Managers get an attendance summary before a performance conversation (C1)."
        result = run("--json", "@note.md", files={"note.md": with_line(POC_NOTE, line)})
        self.assertIn("employment", json.loads(result.stdout)[0]["counsel_triggers"])

    def test_wrapped_statement_may_carry_checked_on_another_line(self):
        bullet = ("- Annex III obligations apply from 2 December 2027 (Art. 113(c)(i),\n"
                  "  checked 2026-10-26; C1).")
        self.assertEqual(run("@note.md", files={"note.md": with_line(POC_NOTE, bullet)}).returncode, 0)
        prose = ("Annex III obligations apply from 2 December 2027 (Art. 113(c)(i),\n"
                 "checked 2026-10-26; C1).")
        self.assertEqual(run("@note.md", files={"note.md": with_line(POC_NOTE, prose)}).returncode, 0)

    def test_project_section_sign_is_not_a_statute(self):
        line = "The FCA said on 8 June 2026 that existing rules apply (docs/discovery/x.md §4)."
        result = run("@note.md", files={"note.md": with_line(POC_NOTE, line)})
        self.assertNotIn("legal applicability date", result.stdout)

    def test_trigger_in_source_file_forces_counsel(self):
        brief = "# Discovery brief\nThe assistant screens job applicants before interviews.\n"
        result = run("@note.md", "--source", "@brief.md", "--source", "@design.md",
                     files={"note.md": POC_NOTE, "brief.md": brief, "design.md": DESIGN})
        self.assertEqual(result.returncode, 1)
        self.assertIn("brief.md:2", result.stdout)

    def test_out_of_scope_section_is_not_scanned_for_triggers(self):
        card = """---
document: system-card
jurisdictions: [au]
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

## Automated-decision disclosure

- n/a: no output decides or feeds a decision about a person (C1).

## AI disclosure and hand-off

- The chat says it is an AI at the start and on request (C4).

## Data

- Policy passages only (D2).

## Contact

- source: sponsor, 2026-10-25: hr-ai@example.com
"""
        result = run("@card.md", files={"card.md": card})
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_screening_sections_are_not_scanned_for_triggers(self):
        memo = AU_MEMO.replace("| Australia | yes | Consultancy staff in Sydney (D3) |",
                               "| Australia | yes | Consultancy staff in Sydney (D3); no children, biometrics or hiring |")
        result = run("--json", "@memo.md", files={"memo.md": memo})
        self.assertEqual(json.loads(result.stdout)[0]["counsel_triggers"], [], result.stdout)

    def test_word_migration_and_model_performance_do_not_trigger(self):
        draft = with_line(POC_NOTE, "Database migration and model performance evaluation run in CI (D3).")
        self.assertEqual(run("@note.md", files={"note.md": draft}).returncode, 0)

    def test_legal_date_needs_checked_note(self):
        draft = POC_NOTE.replace(" (checked 2026-10-20)", "")
        result = run("@note.md", files={"note.md": draft})
        self.assertEqual(result.returncode, 1)
        self.assertIn("legal applicability date", result.stdout)

    def test_australian_us_and_uk_references_need_checked_dates(self):
        lines = (
            "APP 1.7 applies from 10 December 2026 (C1).",
            "The Privacy Act s 26WH assessment applies since 22 February 2018 (C1).",
            "CPPA ADMT duties apply from January 1, 2027 (C1).",
            "Colorado SB 26-189 takes effect for decisions from 1 January 2027 (C1).",
            "UK GDPR Articles 22A to 22D are in force since 5 February 2026 (C1).",
            "The DUAA complaints duty commenced on 19 June 2026 (C1).",
        )
        for line in lines:
            result = run("@note.md", files={"note.md": with_line(POC_NOTE, line)})
            self.assertIn("legal applicability date", result.stdout, line)
            fixed = line.replace(" (C1).", " (checked 2026-10-26; C1).")
            self.assertEqual(run("@note.md", files={"note.md": with_line(POC_NOTE, fixed)}).returncode, 0, fixed)

    def test_possessive_before_a_number_is_not_a_section_reference(self):
        line = "The client's 2 workshops run from 3 November 2026 onwards (C1)."
        self.assertEqual(run("@note.md", files={"note.md": with_line(POC_NOTE, line)}).returncode, 0)

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
        draft = POC_NOTE.replace("Policy Q&A assistant\njurisdictions", "<system>\njurisdictions")
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
        self.assertEqual(data[0]["jurisdictions"], ["au", "eu"])
        self.assertEqual(data[0]["errors"], [])

    def test_filled_templates_need_no_extra_citations(self):
        """Boilerplate a drafter keeps verbatim must pass once placeholders hold IDs."""
        for template in sorted((SKILL / "assets").glob("*-template.md")):
            text = template.read_text(encoding="utf-8")
            text = re.sub(r"counsel_required: .*", "counsel_required: yes", text)
            text = re.sub(r"jurisdictions: .*", "jurisdictions: [au, us, eu, uk, nz, sg, ca]", text)
            text = re.sub(r"form_url: .*", "form_url: https://www.digital.gov.au/ai/impact-assessment-tool", text)
            text = re.sub(r"form_checked: .*", f"form_checked: {TODAY}", text)
            previous = None
            while previous != text:
                previous, text = text, re.sub(r"<[A-Za-z][^<>\n]*>", "C1", text)
            result = run("@draft.md", files={"draft.md": text})
            self.assertEqual(result.returncode, 0, f"{template.name}: {result.stdout}{result.stderr}")

    def test_iso_project_dates_and_read_dates_are_not_applicability_dates(self):
        line = ("- counsel: Article 22 applies to rejections from the pilot on 2026-12-01; "
                "the GDPR text was read 2 March 2026 (C1).")
        self.assertEqual(run("@note.md", files={"note.md": with_line(POC_NOTE, line)}).returncode, 0)

    def test_bare_marker_does_not_count(self):
        draft = with_line(POC_NOTE, "Logs are kept for a period the design does not record anywhere. gap:")
        self.assertIn("cites no ID", run("@note.md", files={"note.md": draft}).stdout)

    def test_omitted_baseline_rule_may_be_named_as_gap(self):
        draft = with_line(POC_NOTE, "gap: no penetration test (SB24 is not in the design's table).")
        result = run("@note.md", "--source", "@design.md", files={"note.md": draft, "design.md": DESIGN})
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_transparency_checklist_does_not_trigger_biometrics(self):
        memo_row = "\n## Transparency obligations (Article 50)\n\n- 50(3) emotion recognition or biometric categorisation: n/a: none.\n"
        draft = POC_NOTE.replace("## Questions for counsel", memo_row + "\n## Questions for counsel")
        result = run("--json", "@note.md", files={"note.md": draft})
        self.assertEqual(json.loads(result.stdout)[0]["counsel_triggers"], [])

    def test_templates_fail_until_filled(self):
        templates = sorted((SKILL / "assets").glob("*-template.md"))
        self.assertEqual(len(templates), 9)
        for template in templates:
            result = subprocess.run([sys.executable, "-I", str(SCRIPT), "--today", TODAY, str(template)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 1, f"{template.name}: {result.stdout}{result.stderr}")
            self.assertIn("placeholder", result.stdout, template.name)


FOUR_ROW_SCREEN = """## Jurisdiction screen

| Regime | In scope | Trigger facts | Reason |
| --- | --- | --- | --- |
| Australia | yes | Consultancy staff in Sydney (D3) | The consultancy's own handling |
| United States | no | No US data subjects (D3) | n/a: no US client or people |
| EU | no | No EU people (D3) | n/a: Australian staff only |
| United Kingdom | no | No UK people (D3) | n/a: no UK establishment |
"""

FORM_ANSWERS = """---
document: government-form-answers
jurisdictions: [au]
counsel_required: yes
for: Assessing officer
form: DTA AI impact assessment tool
form_version: v1.0
form_url: https://www.digital.gov.au/ai/impact-assessment-tool
form_checked: 2026-10-26
---

# Draft answers for the DTA AI impact assessment tool: Benefits enquiry assistant

This is not the official form. It drafts answers in the form's own order for the agency's officers.

## Form and version

- DTA AI impact assessment tool v1.0 (checked 2026-10-26).

## Who completes and approves

| Role in the form | Who | Evidence |
| --- | --- | --- |
| Assessing officer | agency: name and position once named | gap: not named |

## Draft answers

| # | Question (paraphrase) | Draft answer | Evidence | Who decides |
| --- | --- | --- | --- | --- |
| 1.4 | Use case description | Answers enquiries about payment dates from published guidance (C1) | C1 | agency: approves |
| 3.5 | Privacy risk | assumption: medium, because prompts may carry personal information | C2 | agency: the assessing officer rates it |

## Questions for the agency

- agency: which records disposal authority applies to transcripts?

## Questions for counsel

- counsel: does any output inform an administrative decision under an Act?
"""


class SevenRegimes(unittest.TestCase):
    """New Zealand, Singapore and Canada join the screen after the first four."""

    def test_four_row_screen_now_fails_with_a_fix(self):
        memo = AU_MEMO.replace(SCREEN, FOUR_ROW_SCREEN)
        result = run("@memo.md", files={"memo.md": memo})
        self.assertEqual(result.returncode, 1)
        self.assertIn("names no row for New Zealand", result.stdout)
        self.assertIn("names no row for Canada", result.stdout)
        self.assertIn("the screen now covers seven regimes", result.stdout)

    def test_ca_alone_does_not_name_canada(self):
        memo = AU_MEMO.replace("| Canada | no | No people in Canada (D3) | n/a: no Canadian client or people |",
                               "| CA | no | No people there (D3) | n/a: no client or people |")
        result = run("@memo.md", files={"memo.md": memo})
        self.assertIn("names no row for Canada", result.stdout)
        quebec = memo.replace("| CA | no | No people there (D3) |", "| Quebec | no | No Quebec people (D3) |")
        self.assertEqual(run("@memo.md", files={"memo.md": quebec}).returncode, 0)

    def test_new_regimes_require_their_memo_and_pack_sections(self):
        memo = AU_MEMO.replace("jurisdictions: [au]", "jurisdictions: [au, nz, sg, ca]")
        result = run("@memo.md", files={"memo.md": memo})
        for heading in ("New Zealand: Privacy Act and IPPs", "Singapore: PDPA and roles",
                        "Singapore: AI governance frameworks", "Canada: Automated decisions",
                        "Canada: Employment, sector and government AI policy"):
            self.assertIn(f"missing section: ## {heading}", result.stdout)
        pack = "---\ndocument: privacy-impact-input-pack\njurisdictions: [nz, sg, ca]\ncounsel_required: pending\n---\n"
        result = run("@p.md", files={"p.md": pack})
        for heading in ("New Zealand: IPP compliance check", "Singapore: PDPA obligations check",
                        "Canada: Quebec PIA and s 17 facts"):
            self.assertIn(f"missing section: ## {heading}", result.stdout)

    def test_new_regime_section_without_its_code_fails(self):
        memo = AU_MEMO.replace("## Applicable dates", "## Singapore: PDPA and roles\n\n- n/a: no Singapore people (D3).\n\n"
                                                     "## Applicable dates")
        self.assertIn("belongs to Singapore", run("@memo.md", files={"memo.md": memo}).stdout)

    def test_transfer_annex_follows_regimes_with_a_transfer_rule(self):
        annex = ("---\ndocument: transfer-assessment\njurisdictions: [au]\ncounsel_required: pending\n---\n\n"
                 "## Transfers\n\n- n/a: none (D3).\n\n## Destination and access facts\n\n- n/a: none (D3).\n\n"
                 "## Supplementary measures\n\n- n/a: none (D3).\n\n## Questions for counsel\n\n- counsel: none.\n")
        result = run("@a.md", files={"a.md": annex})
        self.assertIn("APP 8 facts belong in the input pack", result.stdout)
        singapore = annex.replace("[au]", "[au, sg]").replace(
            "## Questions for counsel", "## Singapore: Transfer Limitation Obligation\n\n- n/a: none (D3).\n\n"
                                        "## Questions for counsel")
        self.assertEqual(run("@a.md", files={"a.md": singapore}).returncode, 0, run("@a.md", files={"a.md": singapore}).stdout)
        canada = annex.replace("[au]", "[ca]")
        self.assertIn("missing section: ## Canada: Quebec s 17 and Alberta service providers",
                      run("@a.md", files={"a.md": canada}).stdout)

    def test_agency_marker_counts_as_a_citation(self):
        draft = with_line(POC_NOTE, "agency: the agency names the accountable use case owner.")
        result = run("--json", "@note.md", files={"note.md": draft})
        data = json.loads(result.stdout)[0]
        self.assertEqual(data["errors"], [])
        self.assertEqual(data["agency_items"], 1)

    def test_new_law_references_need_checked_dates(self):
        lines = (
            "IPP 3A applies from 1 May 2026 (C1).",
            "The Biometric Processing Privacy Code applies to existing processing from 3 August 2026 (C1).",
            "The PDPA breach rules apply since 1 February 2021 (C1).",
            "Law 25 s 12.1 is in force since 22 September 2023 (C1).",
            "The PIPEDA breach record applies from 1 November 2018 (C1).",
            "The Ontario rule under the Working for Workers Four Act, 2024 applies from January 1, 2026 (C1).",
            "The PPIP Act Part 6A scheme applies from 28 November 2023 (C1).",
            "The NSW Cyber Security Policy reporting duty applies from 1 July 2026 (C1).",
            "The DTA impact assessment applies to in-scope use cases by 15 December 2026 (C1).",
        )
        for line in lines:
            result = run("@note.md", files={"note.md": with_line(POC_NOTE, line)})
            self.assertIn("legal applicability date", result.stdout, line)
            fixed = line.replace(" (C1).", " (checked 2026-10-26; C1).")
            self.assertEqual(run("@note.md", files={"note.md": with_line(POC_NOTE, fixed)}).returncode, 0, fixed)

    def test_new_counsel_triggers(self):
        cases = {
            "public-body clients": (
                "The client is a NSW agency running a public service chatbot (D2).",
                "The use case is registered on the AIAF Platform (D2).",
                "High-risk bands go to the AI Review Committee (D2).",
                "The consultancy works under a State contract with the agency (D2).",
                "The client is a federal department in Ottawa (D2).",
                "The department expects AIA level III (D2).",
                "The client is a Singapore statutory board (D2).",
                "The client is a Crown entity in Wellington (D2).",
            ),
            "automated decisions": ("Refund refusals are exclusively automated for Quebec customers (C1).",),
            "biometrics": ("The voice agent runs emotion inference on callers (C1).",),
        }
        for area, lines in cases.items():
            for line in lines:
                result = run("--json", "@note.md", files={"note.md": with_line(POC_NOTE, line)})
                data = json.loads(result.stdout)[0]
                self.assertIn(area, data["counsel_triggers"], line)
                self.assertEqual(result.returncode, 1, line)

    def test_trigger_near_misses_stay_quiet(self):
        for line in ("n/a: not a NSW agency; a private retailer (D2).",
                     "The Biometric Processing Privacy Code does not apply: no face or voice processing (C1).",
                     "The State contract exemption (s 7B(5)) is named for completeness (D2).",
                     "CA Civ. Code 1798.100 rights are handled by the US team (D2).",
                     "No decision is exclusively automated; a person approves each one (C1)."):
            result = run("--json", "@note.md", files={"note.md": with_line(POC_NOTE, line)})
            self.assertEqual(json.loads(result.stdout)[0]["counsel_triggers"], [], line)


class GovernmentFormAnswers(unittest.TestCase):
    """Draft answers for an official form name it, date it and never claim to be it."""

    def test_clean_answers_pass(self):
        result = run("--json", "@f.md", files={"f.md": FORM_ANSWERS})
        data = json.loads(result.stdout)[0]
        self.assertEqual(data["errors"], [], result.stdout)
        self.assertGreaterEqual(data["agency_items"], 4)

    def test_form_fields_are_required(self):
        draft = FORM_ANSWERS.replace("form_checked: 2026-10-26\n", "").replace("form_version: v1.0\n", "")
        result = run("@f.md", files={"f.md": draft})
        self.assertIn("form_version is missing", result.stdout)
        self.assertIn("form_checked must be the ISO date", result.stdout)
        self.assertEqual(result.returncode, 1)

    def test_stale_form_check_warns(self):
        draft = FORM_ANSWERS.replace("form_checked: 2026-10-26", "form_checked: 2026-06-01")
        result = run("@f.md", files={"f.md": draft})
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("form_checked 2026-06-01 is over 90 days old", result.stdout)
        future = FORM_ANSWERS.replace("form_checked: 2026-10-26", "form_checked: 2027-01-01")
        self.assertIn("form_checked 2027-01-01 is in the future", run("@f.md", files={"f.md": future}).stdout)

    def test_must_say_it_is_not_the_official_form(self):
        draft = FORM_ANSWERS.replace("This is not the official form. ", "")
        self.assertIn("must say this is not the official form", run("@f.md", files={"f.md": draft}).stdout)

    def test_needs_australia_and_its_sections(self):
        draft = FORM_ANSWERS.replace("jurisdictions: [au]", "jurisdictions: [nz]")
        self.assertIn("jurisdictions must list au", run("@f.md", files={"f.md": draft}).stdout)
        short = FORM_ANSWERS.split("## Questions for the agency")[0]
        self.assertIn("missing section: ## Questions for the agency", run("@f.md", files={"f.md": short}).stdout)


class ReviewAndSignOff(unittest.TestCase):
    """Every draft says it is a drafting aid and leaves the decision to its reviewer."""

    def test_framed_draft_passes(self):
        self.assertEqual(run("@note.md", files={"note.md": POC_NOTE}).returncode, 0)

    def test_missing_banner_fails(self):
        draft = framed(POC_NOTE).replace(BANNER, "")
        result = run("@note.md", files={"note.md": draft}, frame=False)
        self.assertIn("missing the drafting-aid banner", result.stdout)

    def test_missing_signoff_fails(self):
        draft = framed(POC_NOTE).replace(SIGNOFF, "\n")
        result = run("@note.md", files={"note.md": draft}, frame=False)
        self.assertIn("missing section: ## Review and sign-off", result.stdout)

    def test_signoff_needs_a_reviewer_row(self):
        draft = framed(POC_NOTE).replace("| Privacy officer | This document | pending | pending |\n", "")
        result = run("@note.md", files={"note.md": draft}, frame=False)
        self.assertIn("no reviewer row", result.stdout)

    def test_unknown_decision_fails(self):
        draft = framed(POC_NOTE).replace("| pending | pending |", "| looks fine | pending |")
        self.assertIn("decision must be one of", run("@n.md", files={"n.md": draft}, frame=False).stdout)

    def test_draft_cannot_carry_a_decision(self):
        draft = framed(POC_NOTE).replace("| pending | pending |", "| approved | 2026-10-25 |")
        result = run("@n.md", files={"n.md": draft}, frame=False)
        self.assertIn("status is draft but a reviewer decision is recorded", result.stdout)

    def test_reviewed_document_needs_a_dated_decision(self):
        reviewed = framed(POC_NOTE).replace("status: draft", "status: reviewed")
        self.assertIn("every sign-off decision is pending",
                      run("@n.md", files={"n.md": reviewed}, frame=False).stdout)
        undated = reviewed.replace("| pending | pending |", "| approved with changes | pending |")
        self.assertIn("needs the date the reviewer signed", run("@n.md", files={"n.md": undated}, frame=False).stdout)
        future = reviewed.replace("| pending | pending |", "| approved | 2027-01-01 |")
        self.assertIn("is in the future", run("@n.md", files={"n.md": future}, frame=False).stdout)
        signed = reviewed.replace("| pending | pending |", "| approved | 2026-10-25 |")
        self.assertEqual(run("@n.md", files={"n.md": signed}, frame=False).returncode, 0)

    def test_status_must_be_draft_or_reviewed(self):
        draft = framed(POC_NOTE).replace("status: draft", "status: final")
        self.assertIn("status must be draft or reviewed", run("@n.md", files={"n.md": draft}, frame=False).stdout)

    def test_signoff_rows_are_not_held_to_cite_or_flag(self):
        result = run("@note.md", files={"note.md": POC_NOTE})
        self.assertNotIn("Privacy officer", result.stdout)

    def test_every_template_carries_banner_and_signoff(self):
        for template in sorted((SKILL / "assets").glob("*-template.md")):
            text = template.read_text(encoding="utf-8")
            with self.subTest(template=template.name):
                self.assertIn("not legal advice", text)
                self.assertIn("not\n> reviewed until", text)
                self.assertIn("## Review and sign-off", text)
                self.assertIn("status: draft", text)


if __name__ == "__main__":
    unittest.main()
