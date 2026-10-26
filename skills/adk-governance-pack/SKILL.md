---
name: adk-governance-pack
description: >-
  Draft the governance papers a client's legal, privacy and security
  reviewers ask for about a Google ADK agent application, from its discovery
  brief, design and plan evidence: an EU AI Act classification memo
  (prohibited practices, Annex III high-risk, Article 50 transparency,
  provider and deployer roles), an AI impact assessment along ISO/IEC 42005
  mapped to the NIST AI RMF and its generative AI profile, a GDPR DPIA input
  pack, a system card, records-of-processing rows and a security
  questionnaire answer bank. Every statement cites a contract, decision or
  evidence ID or is flagged for counsel; drafts, not legal advice. Use
  before a pilot or production decision, or when a DPO, counsel or CISO asks
  for these papers. Do not activate to build redaction, screening or logging
  controls (protect-adk-sensitive-data), to threat-model or harden the agent
  (adk-agent-security), for release gates (adk-release-engineering), or to
  present results (adk-presenter).
license: MIT
metadata:
  author: Ruslan Khissamiyev
  source-book: Agentic Engineering
  source-chapter: "cross-cutting"
  sources-reviewed: "2026-10-25"
  version: "2026.10.26"
---

# ADK governance pack

Turn what the project has recorded into the drafts a client's reviewers
sign: the AI Act classification, the impact assessment, the DPIA inputs,
the system card, records-of-processing rows and security questionnaire
answers. The deliverable is documents under `docs/governance/<topic>/`;
the skill changes no code and gives no legal advice. Counsel, the DPO and
the CISO decide; the drafts give them the facts with their IDs and the
questions only they can answer.

## Read the record first

Read, noting the ID or path of every fact you will use: the discovery
brief (`docs/discovery/<topic>.md`: harms, data register, cost of a wrong
answer, stakeholders, decision calendar), the design
(`docs/architecture/<topic>.md`: profile, requirements, the contracts
table, decisions on data, identity, model and hosting, the security
posture and the security-baseline table, accepted risks and deferred
controls), the plan and tickets (goals, status lines, measurement records
`M1`, incident records `I1`, calendar waits `W1`), evaluation reports, and
`protect-adk-sensitive-data` evidence (what is masked or rejected, with
measured coverage). Use the project's own names when its documents live
elsewhere.

List what the record does not hold before drafting: no data-flow for logs,
no retention decision, an unmeasured bias check, no named owner, an
evaluation report the plan cites that does not exist. Each becomes a
`gap:` line in the draft and a proposed goal for the specialist that owns
the control, never an invented answer; a missing report is cited through
the plan's M record with the gap beside it.

Check the pinned model on the provider's current model page (or the dated
lifecycle table `adk-model-and-output-contracts` ships): its retirement
date and where it processes data, which the page can list separately from
where its endpoint is available. A model retired or retiring before the
decision's horizon, or processing outside the region a contract promises,
is a limit and a gap for that skill.

## Size the pack to the profile

| Profile (design's scope gate) | Write |
| --- | --- |
| Proof of concept | [POC note](assets/poc-note-template.md): one page, classification and data-flow summary, the questions the full pack must settle before production |
| Internal tool | Classification memo, DPIA input pack (its screening may conclude a DPIA is not required; the DPO decides), records-of-processing rows; the questionnaire when the CISO asks; the system card when it goes to all staff or a deck will cite it |
| MVP or pilot, production | The full pack: all six documents |

Size by the profile the design records, not by the word "rollout": an
internal tool rolled out to every employee is still an internal tool.
When the client asks for one document, write that one, plus the
classification memo if none exists, because every other document cites it.
A real-data POC in an employment, credit, education or other Annex III
area gets the classification memo, not just the note.

Each draft's front matter sets `counsel_required`: `yes` when counsel must
review it before anyone relies on it (any `counsel:` item that blocks the
decision, and always on an Annex III trigger), `no` when the reviewer named
in `for:` can rely on it alone, `pending` until you know.

## Draft each document

Copy each template into `docs/governance/<topic>/` under its own name
(`classification-memo.md`, `impact-assessment.md`, `dpia-input-pack.md`,
`system-card.md`, `processing-records.md`, `security-questionnaire.md`, or
`poc-note.md`) and fill it in this order, because later ones cite earlier
ones:

1. **Classification memo** ([template](assets/classification-memo-template.md)):
   read [EU AI Act](references/eu-ai-act.md). Roles first, then Article 5,
   Annex III with the Article 6(3) facts, Article 50, the model provider's
   obligations and the dates.
2. **DPIA input pack** and **records-of-processing rows**
   ([DPIA template](assets/dpia-input-pack-template.md),
   [records template](assets/processing-records-template.md)): read
   [privacy and records](references/privacy-and-records.md). One data flow
   per path personal data takes, including logs, memory and evaluation
   sets.
3. **Impact assessment** ([template](assets/impact-assessment-template.md)):
   read [impact assessment](references/impact-assessment.md).
4. **System card** and **security questionnaire**
   ([card](assets/system-card-template.md),
   [questionnaire](assets/security-questionnaire-template.md)): read
   [system card and questionnaire](references/system-card-and-questionnaire.md).

Hold every draft to these rules; the checker enforces the first four:

- **Cite or flag.** Every bullet, table row and paragraph cites a design,
  plan or evidence ID (`C3`, `D2`, `SB14`, `G05/A2`, `M1`, `I1`, `W1`), a
  project file by path (`docs/discovery/<topic>.md §4`, not "the brief"),
  or a dated source (`source: Head of TA, 2026-10-20`), or is marked
  `assumption:`, `counsel:`, `gap:`, `deferred:` or `n/a:` with its reason.
  A statement the user makes in the conversation is cited as
  `source: <role>, <date>`. A provider fact taken from these references
  rather than the page itself says so (`source: adk-governance-pack
  reference, read 2026-10-25`); re-read the page for anything a decision
  rests on.
- **Conclusions are counsel's.** Write the facts and the proposed
  conclusion; the role, the classification, the legal basis, whether a
  DPIA or FRIA is required and whether a derogation holds each carry
  `counsel:`.
- **Annex III forces counsel.** The checker sets the floor: any of its
  Annex III phrases (ranking candidates, CVs, credit scoring, life or health
  insurance pricing, biometrics, admissions and the rest) in the draft or
  its sources requires `counsel_required: yes`, even when the draft argues
  the Article 6(3) derogation. Set it yourself whenever a fact could place
  the system in an Annex III area that the phrase list misses. Uses listed under an out-of-scope heading,
  and the memo's Article 5 and high-risk checklists, do not trigger it;
  the system's own description and its records do.
- **Dates carry their check.** Write when a law or article applies in
  words ("2 August 2026") and add `checked <YYYY-MM-DD>`, the day you or
  the reference last confirmed it at the source. Project dates stay in ISO
  form, so the checker tells the two apart.
- **Planned is not in place.** Use the status words in the system card
  reference; a control evidenced locally is not "in production".
- **One home per fact.** Model-provider data use lives in the DPIA input
  pack; the questionnaire and system card cite it. Figures match the
  plan's M records exactly.

## Check the drafts

Run the checker from the project root with Python 3.9 or later, resolving
`SKILL_DIR` to this skill's directory and passing every record the drafts
cite:

```bash
python3 "$SKILL_DIR/scripts/check_governance.py" docs/governance/<topic>/ \
  --source docs/discovery/<topic>.md --source docs/architecture/<topic>.md \
  --source docs/plans/<topic>.md
```

Exit 0 means every required section is filled, every statement cites or is
flagged, every cited R, C, D, SB, M, I, W or O ID exists in a source, the
Annex III flag is set where triggered, and every applicability date carries
its check; warnings name checked dates older than 180 days to re-confirm
and cited `docs/` files that do not exist.
Fix every error; a passing run checks form, not the law.

## Hand over

When the pack is a plan goal, fill its Evidence: the document paths, the
checker result, the counsel questions outstanding, and the gaps proposed as
goals. The goal completes when the checker passes and the drafts are sent
to the named reviewers; their sign-off (DPIA, legal review, works council
consultation, security approval) is a calendar wait `W<n>` in the plan
that the production goals depend on, requested the day the drafts go out.
Add a missing wait to the plan's schedule when the pack is a plan goal or
the user asked you to update the plan, then cite its ID; otherwise cite
the waits that exist and list the new ones, unnumbered, in your closing
message for the plan's owner.

End with: where the files are, the checker's result, the proposed
classification in one line with its counsel flag, the counsel questions
that block the next decision, the gaps and the goal each needs, the waits
to schedule, and the prompt for the next step, for example:

```text
/adk-presenter Prepare the production-approval presentation from
docs/plans/<topic>.md; cite docs/governance/<topic>/system-card.md for
limits and oversight, and show the open counsel questions as risks.
```

Local drafting authorises no contact with regulators, the client's
counsel or data subjects; it reads the project's records and the sources
these references cite.

Independent community project; not affiliated with or endorsed by Google.
