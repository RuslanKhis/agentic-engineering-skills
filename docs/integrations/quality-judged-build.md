# Build order for time-boxed, quality-judged work

A worked example that spans the skills: a few hours, a document pack, labelled
development cases, unseen holdout cases, and an evaluator who reads the
predictions, the method and a short report. The order puts the core judgment
first and every other control after the first measurement. It uses the bundled
helpers on synthetic documents with real bytes, so each step runs locally in
well under an hour of agent time, with no provider call and no cloud service.

The prompts use Claude Code's `/` form; in Codex replace the leading `/` with
`$`, and in Google clients ask to use the skill by name. Set `SKILL_DIR` to the
installed location of the named skill and `PYTHON` to an interpreter whose
SQLite includes FTS5 (Python 3.11 or later from python.org or Homebrew does).

## 1. Scope gate, ten minutes

```text
/adk-system-designer Design an ADK assistant that drafts a planning decision
with reasons and conditions from a case file and the local plan. I have four
hours and $25. It is judged on five holdout predictions, the method and a
short report. Record the scope gate, choose the first slice, list the deferred
controls with reasons, and name the three documents the reviewer will read.
Design only; keep it to one page.
```

Expect the design to open with the scope-gate table from the
[design template](../../skills/adk-system-designer/assets/system-design-template.md)
and to defer officer revisions, export acknowledgement, saved-stage recovery and
hosting with a one-line reason each. The first slice is the core judgment end to
end on the development cases with a call budget and a stop. Anything that
proposes a revision workflow or a cloud roadmap as an early goal has skipped
the gate.

## 2. Qualify the inputs, about an hour

Ingestion first. The memory skill ships four one-page PDFs (a text page, a
header-only scan with an embedded image, a table page and a drawing with a
scale bar) and the inventory its generator wrote:

```bash
SKILL_DIR=skills/adk-memory-architecture
"$PYTHON" "$SKILL_DIR/scripts/qualify_ingestion.py" \
  --inventory "$SKILL_DIR/assets/ingestion-fixture/inventory.json"
```

The report routes `scanned-page.pdf` to `ocr_or_vision`, `table-page.pdf` and
`drawing-page.pdf` to `both`, and extracts "6.0 m" and "1:200" as separate
fields. On a real pack, build the inventory from the project's extractor (or
`--pdf` with `pypdf` installed), calibrate the thresholds on the corpus, and
keep the report with the case. The
[ingestion reference](../../skills/adk-memory-architecture/references/document-ingestion.md)
explains each column.

Then retrieval against a gold set. The fixture holds a synthetic local plan
with a two-page policy, a policy that cites "Table 2 of the Design SPD", and
four questions with the operative units a reviewer would cite:

```bash
"$PYTHON" "$SKILL_DIR/scripts/local_retrieval.py" \
  --gold "$SKILL_DIR/assets/retrieval-gold.json" --k 4
```

The sufficiency report shows the SPD table reached through a deterministic
lookup of the named reference, one bounded second round, no unresolved
references and recall 1.0 per question on the fixture. The same command on the
project's own gold set is the measurement that every later retrieval change is
compared against; a cap is raised only when that measurement shows the cap
caused a miss. See the
[retrieval reference](../../skills/adk-memory-architecture/references/retrieval-strategy.md).

```text
/adk-memory-architecture Qualify our case-file and local-plan pack: produce the
per-page ingestion report, route scans and drawings, then build the local
heading-unit index and measure recall on our gold set of operative sections for
the five development cases. Report recall per case and the sufficiency problems.
No provider calls.
```

## 3. Core judgment end to end, the largest share of time

Draft decisions on the development cases with the plainest contract that can
produce the deliverable: retrieval report in, decision with reasons and
conditions out, two exemplars from other cases, one judge. Then categorise
every defect and change one thing per iteration.

```text
/adk-agent-evaluation Our draft stage produces decisions for the five labelled
development cases. Run the baseline through the plainest contract, label every
defect by category (missed policy, wrong attribution, unsupported fact, weak
condition, wrong outcome, contract failure), and make the first change target
the largest category. Use the other cases' labels as leave-one-out exemplars.
Re-measure after each change and keep the category table in
evaluation/summary.md. Keep the holdout untouched.
```

The prompt the stage sends follows the skeleton in
[quality iteration](../../skills/adk-agent-evaluation/references/quality-iteration.md):
role and task, the judgment the model owns in one paragraph, the inputs by
label, a schema sized to the decision, and two trimmed exemplars. Source IDs,
quotes, offsets and coverage counts stay in code. The error table is data:

```json
[{"case": "dev-003", "category": "missed_policy", "detail": "H3 criterion c not applied",
  "stage": "retrieval", "fix_candidate": "lookup of cited policy numbers"},
 {"case": "dev-006", "category": "weak_condition", "detail": "splay condition contradicts waiver",
  "stage": "draft", "fix_candidate": "consistency check in code"}]
```

Stop iterating when the largest remaining category needs a deferred control, or
when the time reserved for step 5 is reached.

## 4. Content safeguards in code

Every fresh draft passes the application's consistency rules before a reviewer
sees it. Save this draft as `draft.json`; it reproduces the pattern where a
condition imposes a visibility splay that its own reason says was waived:

```json
{
  "decision": "approve",
  "reasons": [
    {"id": "r1", "text": "The highway authority waived the visibility splay for this access.",
     "supports": "approve", "policies": ["G4"], "waives": ["visibility splay"]}
  ],
  "conditions": [
    {"id": "c1", "text": "Provide a 2.4 m by 43 m visibility splay before first use.",
     "requires": ["visibility splay"], "reason_id": "r1"}
  ],
  "decisive_issues": [{"id": "i1", "label": "access", "operative_policy_found": true}],
  "warnings": [
    {"stage": "retrieval", "code": "search_truncated", "message": "Search for policy G4 was truncated at 24 pages.", "could_change_decision": false},
    {"stage": "draft", "code": "search_truncated", "message": "retrieval: Search for policy G4 was truncated at 24 pages.", "could_change_decision": false},
    {"stage": "review", "code": "search_truncated", "message": "draft: Search for policy G4 was truncated at 24 pages.", "could_change_decision": false},
    {"stage": "review", "code": "missing_drawing", "message": "No elevation drawing for the gate.", "could_change_decision": true}
  ]
}
```

```bash
"$PYTHON" skills/adk-workflow-design/scripts/draft_consistency.py --draft draft.json --top 3
```

Exit code 1: the blocker names the condition and the reason that waives it.
The triage presents the one warning that could change the decision first and
collapses the three copies of the truncated search into one. Remove the
condition and the command exits 0. The
[content safeguards reference](../../skills/adk-workflow-design/references/content-safeguards.md)
adds the hostile-source fixture, the abstention rule and the adversarial review
framing; adapt the rules to the application's policy.

```text
/adk-workflow-design Add in-code consistency checks to the drafting stage:
a condition cannot require what a reason waives, a refusal carries no
conditions, every reason cites a policy, decision and reasons agree. Triage
warnings across stages by materiality, delimit source text and label imperative
sentences, and ask the reviewer for the strongest reason the draft is wrong.
Add the hostile-source fixture to the tests.
```

## 5. Deliverable run with the frozen method

```text
/adk-agent-evaluation Freeze the current snapshot and regenerate the five
holdout predictions with it, spending the reserved deliverable budget first.
Record snapshot identity, model, settings and prompt version with the run.
If the budget cannot cover the run, say so in the report instead of running
a development probe.
```

The rule is in
[progressive validation](../../skills/adk-agent-evaluation/references/progressive-validation.md#keep-the-deliverable-and-the-method-together):
the judged predictions come from the method the report describes, or the report
says they do not and why. The campaign envelope from
[live campaigns](../../skills/adk-operational-guardrails/references/live-campaigns.md)
carries the deliverable reservation as a named line that diagnostics cannot draw
on.

## 6. Report within the reader's budget

Three documents, named in the plan: the design (method and accepted decisions),
`evaluation/summary.md` (latest result per case with the category table, linked
to raw run records under `evaluation/runs/`), and the plan itself (remaining
limits and deferred controls). Budget top-ups and attempt ceilings are ledger
lines, not decision records. The
[evidence budget](../../skills/adk-agent-evaluation/references/execution-evidence.md#keep-the-evidence-within-a-readers-budget)
gives the rule.

## 7. Only then: interface, revisions, export, recovery, hosting

Each deferred control becomes its own ticket under the
[design-to-tickets walkthrough](design-to-implementation.md), after the
development score and the holdout run exist. When `to-tickets` runs under this
order, the first ready ticket is the core judgment path and no interface ticket
precedes the first quality measurement.

## What this example establishes

The helpers run on synthetic fixtures with real bytes: four PDFs, a synthetic
plan with a gold set, and invented drafts. They establish that the routing,
retrieval, fusion and consistency mechanisms behave as described. They run no
OCR engine, no embedding model, no provider call and no ADK code, and they claim
no domain review of the fictional policies. A project's own corpus, gold set,
labels and policy rules supply the evidence that matters; the order above is
how to get it in the time available.
