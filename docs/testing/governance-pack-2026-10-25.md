# Governance pack: checks and fresh-agent trials

*25 October 2026. Skill: `skills/adk-governance-pack`. Research:
[governance-pack-2026-10-25.md](../research/governance-pack-2026-10-25.md).*

## What was checked

| Layer | Result |
| --- | --- |
| Package validation (`scripts/validate_skills.py`) | 24 packages, 0 errors, 0 warnings |
| Checker suite (`skills/adk-governance-pack/tests`) | 21 tests pass, including every template failing until filled and every template passing once its placeholders hold IDs |
| Full `scripts/check_repo.py` (repo `.venv`, Python 3.12) | Passed: 867 tests run, 807 pass, 60 optional SDK checks skipped |
| Evaluation cases | 6 activation cases (2 positive, 3 near-miss for this skill, 1 positive for `protect-adk-sensitive-data` on the redact-logs prompt) and 2 scenarios appended; structure valid, model activation not run |
| Legal facts | Read in the Official Journal text on 25 October 2026; see the research note for what stayed secondary |

Activation and scenario cases are labels, not measured selection; no
fresh-session routing run was made.

## Trials

Two fresh general-purpose subagents (model inherited from the coordinator,
Claude Opus 5.5; reasoning setting not recorded), each given only the absolute path of
the skill's `SKILL.md`, a project directory with a synthetic discovery
brief, design and plan, and one user request. No expected answers. Both
were cut off by an API usage limit part-way through and resumed with their
context once it reset; nothing was rerun from scratch.

| Trial | Fixture (sha256 prefix) | Request | Profile |
| --- | --- | --- | --- |
| T1 | `cv-screening`: brief `6f5e086b`, design `b18aa2b4`, plan `5566b7ea` | "Kestrel's counsel and DPO have asked for the governance papers on the shortlisting assistant before they sign off the pilot. Draft what they need from our docs." | Pilot; ranks job applicants (Annex III point 4) |
| T2 | `policy-qa`: brief `9d2679b3`, design `7c2c16dc`, plan `2c987362` | "Harbourside's DPO wants to know whether we need a DPIA and what the EU AI Act requires before we roll the policy assistant out to all staff, and their CISO wants answers for the security questionnaire. Prepare what they need." | Internal tool; staff policy Q&A (Article 50 only expected) |

Fixtures and outputs are retained under
`/private/tmp/claude-501/governance-trials/` (`fixtures/`, `trial-1-cv/`,
`trial-2-policy/`), outside the repository.

### Outcomes, inspected by the coordinator

| Assertion | T1 | T2 |
| --- | --- | --- |
| Documents sized to the profile | Pass: all six for a pilot | Pass: memo, DPIA inputs, processing rows, questionnaire for an internal tool; no impact assessment or card |
| Annex III handled correctly | Pass: point 4 proposed, `counsel_required: yes`, derogation facts both ways, profiling noted, conclusion left to counsel | Pass: point 4 and 5(c) (the client is an insurer) considered and proposed out of scope, flagged `counsel:` |
| Roles | Pass: client provider and deployer, agency developer, Article 25 triggers listed, GDPR roles kept apart | Pass |
| Dates | Pass: Annex III 2 December 2027, Article 50 2 August 2026, revised Article 4 27 July 2026, each `checked 2026-10-25` | Pass |
| Uncomfortable evidence surfaced | Pass: M3 adverse-impact 0.76 below C5's 0.8; 80% of below-line candidates rejected unread, against R3 | Pass: masking missed 4 of 50 (C5); pilot ran on real staff data before DPIA screening; HR spot check conflicts with C4 |
| Planned versus in place | Pass: "in place, tested locally" | Pass |
| Checker | Exit 0 on all six, after fixing its own errors | Exit 0 on all four, after fixing its own errors |
| Found beyond the fixture | The pinned `gemini-2.5-flash` listed as retired 20 October 2026; ML processing listed as Europe multi-region against C6's europe-west4 | Same retirement; no recorded region for several services |

Output length: T1 about 11,000 words over six documents (DPIA input pack
3,568), T2 about 6,600 over four. No word budget was set, following the
designer's lesson that a number makes the model cut substance; review
whether a summary-first rule is needed after real client use.

The coordinator reran the final checker on both packs after the fixes
below: all ten documents pass; the policy memo no longer reports a false
biometrics area, and the evaluation reports both plans cite but the
fixtures lack are now warned.

## Friction log and what changed

| # | Friction (trial) | Change |
| --- | --- | --- |
| 1 | Memo template line "Blocking questions: <count>; see Questions for counsel." fails the checker verbatim (T1, T2) | Template line carries `counsel:`; new test fills every template with IDs and requires a pass |
| 2 | Processing-records boilerplate line "Only while the agency processes…" fails verbatim (T1, T2) | Folded into the section heading |
| 3 | Templates invite "brief section" citations the checker rejects (T1) | Placeholders now ask for `docs/discovery/<topic>.md §n`; SKILL.md says cite by path |
| 4 | Article 50(3) row trips the biometrics trigger in every memo (T1, T2) | Transparency section excluded from trigger scanning, with a test |
| 5 | Legal-date rule fires on project dates beside an article ("Article 35… W1, requested 2026-10-01") (T1) | Applicability dates are those written in words; ISO and "read/updated" dates ignored; SKILL.md tells drafters to write legal dates in words |
| 6 | Template and reference SB IDs the design lacks fail the invented-ID check (T1, T2) | SB IDs on `gap:`, `n/a:` or `deferred:` lines exempt; questionnaire template says to cite only the design's rules |
| 7 | New waits cannot be numbered without editing the plan (T1, T2) | SKILL.md: add the wait to the plan when the pack is a goal or the user asked; otherwise list it unnumbered |
| 8 | Missing cited evidence files pass; a bare `gap:` passes (T1) | Checker warns on cited `docs/` files that do not exist; a marker needs text after it |
| 9 | Nothing prompts a model retirement or processing-region check (T1, T2) | SKILL.md "Read the record" adds the check and the lifecycle source |
| 10 | Unclear how to cite provider pages known only from the references (T1, T2) | SKILL.md gives the citation form and says to re-read what a decision rests on |
| 11 | Impact IDs H1/B1 not accepted as citations (T1) | Accepted |
| 12 | `counsel_required` undefined per document (T2) | Defined in SKILL.md |
| 13 | "Rollout" against an internal-tool profile (T2) | Size by the recorded profile; internal tool adds the system card when going to all staff |
| 14 | Prose said "insurance" and "employment" facts force counsel while the phrase list did not (T2) | SKILL.md separates the checker's floor from the drafter's judgement |
| 15 | Certifications page unreadable (T2) | Reference: cite a readable page or the client's report, else `gap:` |

Not changed: the worktree guard refusing commands containing `git` in
`/private/tmp` (harness, not skill); a trial's note that the docs connector
favours hosted documents (the skill's local files are deliberate). A
reviewer should also know the legal-date check now misses an applicability
date written in ISO form; the guidance asks for words instead.

## Limits

Two trials, one model, one condition, no baseline; they show that the
skill is followable and its checker usable on these fixtures, not that the
drafts would satisfy a real counsel or DPO. No lawyer reviewed the outputs.
Activation was not measured.
