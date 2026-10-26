# Governance pack jurisdictions: checks and fresh-agent trials

*26 October 2026. Skill: `skills/adk-governance-pack`. Research:
[Australia](../research/au-ai-privacy-law-2026-10-26.md),
[United States](../research/us-ai-privacy-law-2026-10-26.md),
[EU](../research/eu-ai-privacy-law-2026-10-26.md),
[United Kingdom](../research/uk-ai-privacy-law-2026-10-26.md).*

The owner asked which privacy and AI laws the governance pack must consider,
with Australian law first, then the United States, the EU and the UK. The
pack now screens jurisdictions before drafting, records them in every
draft's front matter, and carries per-regime sections and references.

## What was checked

| Layer | Result |
| --- | --- |
| Package validation (`scripts/validate_skills.py`) | 25 packages, 0 errors, 0 warnings; governance `SKILL.md` 347 lines, description 1,022 characters |
| Checker suite (`skills/adk-governance-pack/tests`) | 36 tests pass on Python 3.9 (`python3 -I`) and 3.11, including every template failing until filled and every filled template passing with all four jurisdictions |
| Full `scripts/check_repo.py` (Python 3.12 virtual environment with `requirements-dev.txt`, outside the repository) | Passed: 966 tests run, 59 optional SDK checks skipped |
| Evaluation cases | 4 activation cases (3 positive, 1 near-miss) and 3 scenarios appended; structure valid, model activation not run |
| Legal facts | Taken from the four research notes, read 26 October 2026; only items a note marks as read at a primary source are stated as fact, the rest are marked "reported; not confirmed at the source on 2026-10-26" or left out |

The system `python3` is 3.9 on this machine; `adk-agent-security`'s helper
needs 3.11, so the full check ran in a 3.12 environment. Activation and
scenario cases are labels, not measured selection.

## Trials

Three fresh general-purpose subagents (model inherited from the
coordinator, Claude Opus 5.5; reasoning setting not recorded), each given
only the skill's `SKILL.md` path, a project directory with a synthetic
brief, design and plan, and one user request. No expected answers, no web
access, no practice profile.

| Trial | Fixture (sha256 prefix) | Request | Expected screen |
| --- | --- | --- | --- |
| T1 | `au-hr`: brief `2f4e82a6`, design `8028fbfc`, plan `fe7c7336` | Australian retailer's internal HR assistant; Gemini in Sydney; manager attendance summaries; prompts logged; error bodies to a US-region error tracker | `[au]` |
| T2 | `uk-bank`: brief `bbc7a57f`, design `ab4403a1`, plan `f95818f1` | UK bank chatbot with an Irish subsidiary's EU customers; explains declined overdrafts; Sydney support with log and transcript access | `[au, eu, uk]` |
| T3 | `us-hiring`: brief `d6246ce7`, design `e4e1f9fe`, plan `237ac836` | California-headquartered client's résumé screener for California and New York City; age impact ratio 0.74; Sydney engineers read the evaluation set | `[au, us]` |

Fixtures and outputs are kept in the session scratchpad under
`governance-trials/` (`fixtures/`, `trial-1-au-hr/`, `trial-2-uk-bank/`,
`trial-3-us-hiring/`), outside the repository.

### Outcomes, inspected by the coordinator

| Assertion | T1 | T2 | T3 |
| --- | --- | --- | --- |
| Screen picks the right regimes, in order, with a reason for each left out | Pass: `[au]`; the US error tracker treated as an APP 8 overseas disclosure, not a US trigger | Pass: `[au, eu, uk]`; Australia scoped to the consultancy; US out as an assumption for counsel | Pass: `[au, us]`; EU and UK out with reasons |
| Regime sections only for regimes in scope | Pass: no GDPR or AI Act sections, no records of processing; APP compliance check and inventory instead | Pass: records and a transfer annex with SCC and IDTA or Addendum rows for Sydney access | Pass: no records or annex |
| Counsel flags where they should be | Pass: `yes` on four documents by judgement (attendance summaries for performance conversations); the questionnaire `no` | Pass: `yes` on all seven (credit decision explanations) | Pass: `yes` on all five; NYC answer left to counsel with the Local Law 144 prerequisites |
| Uncomfortable evidence surfaced | Masking missed union and medical phrases (M2); absence reasons in summaries (M3); unmasked bodies to Sentry (D6) | Vulnerability recall 41 of 50 (M2); unmasked transcripts read from Sydney; no transfer terms | Age ratio 0.74 below four-fifths (M2); recruiters opened 6% of "not recommended" (M3) |
| Final checker | Exit 0 | Exit 0 after fixing 3 errors | Exit 0 after fixing 1 error |
| Ease (agent's score) | 4 of 5 | 3 of 5 | 4 of 5 |

All three listed the waits to add (workplace surveillance notice, union
consultation, transfer terms, CPPA approval, NYC audit and notice) and
added them to the plan, because the pack was a plan goal.

After the fixes below, the coordinator reran the final checker on all three
packs. T2 and T3 still pass, and the false children, health care and court
triggers in T3 are gone. T1's security questionnaire now fails with
`counsel_required: no`: the new performance-management phrases catch the
attendance summaries in the brief, so the checker floor now agrees with the
judgement the T1 agent made on its other four documents. That is the
intended result. The drafts were left as the agents wrote them.

## Friction log and what changed

| # | Friction (trial) | Change |
| --- | --- | --- |
| 1 | No fallback when the model page and lifecycle table cannot be read (T1, T2, T3) | SKILL.md: write retirement date and processing region as `gap:` lines, propose the check as a goal, never assume |
| 2 | Memo template's practice-profile bullet contradicts "do not mention it" (T1, T2) | Bullet removed; profile facts are cited inline where used |
| 3 | Phrase list missed "attendance summary" for "performance conversations" (T1) | Employment triggers add performance management, conversations, reviews, ratings and attendance records or summaries, with a test |
| 4 | Negated draft lines ("n/a: no PHI, MDR or under-13 data", "No court order") fired triggers (T1, T2, T3) | A draft clause that says "n/a:", "no" or "not" before the phrase does not trigger; a bare table cell still does; sources are always scanned in full; tests |
| 5 | A wrapped statement with `checked` on the next line failed the date check (T1, T2) | The checker accepts `checked` anywhere in the same statement; bullets absorb indented continuation lines; tests |
| 6 | The skill's own citation form `docs/x.md §4` read as a statute section (T2) | `§` after `.md ` is not a legal reference; test |
| 7 | Records template column "Solely automated significant decision" fired its own trigger (T2) | Column renamed |
| 8 | `for:` only in the memo template, though `counsel_required: no` depends on it (T1, T2, T3) | `for:` added to every template |
| 9 | Source triggers make `no` unreachable for a high-stakes system (T2, T3) | Kept as the intended floor; SKILL.md now says so and why |
| 10 | GDPR-worded required headings in Australian packs (T1) | "People and data categories" and "Recipients and regions"; the checker still accepts the old headings |
| 11 | Unclear whether out-of-scope regime bullets in shared sections are deleted (T1, T3) | SKILL.md and template comments: delete them too |
| 12 | Unclear what Australian sections hold when Australia is in only through the consultancy (T2, T3) | SKILL.md and the screen reference: client rows `n/a:`, inventory for the consultancy's own policy, no Guidance for AI Adoption mapping |
| 13 | System card instruction paragraph passed only by accident (T3) | Turned into a one-line HTML comment; SKILL.md says comments are deleted |
| 14 | Provider citation date example disagreed with the reference (T1, T2, T3) | Example uses the reference's own read date |
| 15 | US reference silent on age discrimination, New York State and state breach statutes; Local Law 144 thin (T3) | Local Law 144 detail from the DCWP page; the uncovered laws are named as counsel questions, not stated |
| 16 | CPPA ADMT date for a use starting before 1 January 2027 (T3) | Reference: the duties apply from 1 January 2027; earlier start is `counsel:` |
| 17 | Public website reachable from anywhere; group of companies with two controllers (T2) | Screen reference: rules for incidental visitors and group structures; privacy reference: one transfer row per exporting entity |
| 18 | No DORA clock; DSIT row missing from the questionnaire template (T2) | DORA named as `counsel:` without a clock; DSIT row added |
| 19 | Queensland workplace rules not covered (T1) | Reference: staff outside NSW are a counsel question |
| 20 | Waits must exist before the checker runs; direct client questions have no home; urgent waits not flagged (T1, T3) | SKILL.md hand-over: add waits first and to "Depends on", answer the direct question in the memo summary, list waits due within 14 days first |
| 21 | `hypothesis:` missing from the SKILL.md marker list (T2) | Added |
| 22 | Consumer Duty rows had no template home (T2) | Reference: rows of the Impacts table |

Not changed: the worktree sandbox refusing some shell probes (environment);
no plan state word for "drafted, not sent" beyond writing it in the
evidence; the NIST AI 600-1 action IDs, which a record that lacks them must
show as a gap.

## Limits

The trials checked form and judgement on synthetic records, not the law.
No counsel reviewed the drafts. US state privacy thresholds, Illinois law,
BIPA and several California 2026 statutes rest on secondary sources and are
marked so in the reference.
