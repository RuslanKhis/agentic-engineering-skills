# Trial report: adk-discovery on "SMB advertising"

Trial root: `<trial-discovery-root>/`
Outputs: `transcript.md`, `docs/discovery/smb-advertising.md`, `helper-output.txt`, this file.
Skill under trial: `<repo>/skills/adk-discovery/` (read only; nothing modified).

## 1. Skill files read, in order

1. `SKILL.md` (139 lines)
2. `references/discovery-interview.md` (103 lines), because SKILL.md line 46 says to open with its first question
3. `references/opportunity-portfolio.md` (99 lines), SKILL.md line 62
4. `references/technology-fit.md` (129 lines), SKILL.md line 68
5. `references/handoff-to-design.md` (68 lines), SKILL.md line 120
6. `assets/discovery-brief-template.md` (118 lines), SKILL.md line 110
7. `scripts/rank_opportunities.py` (246 lines), to know what table shape it parses before writing the brief
8. `agents/openai.yaml` (4 lines), incidental

In practice all four references plus the template had to be read before the first question could be asked properly, because the interview reference (lines 100-103) links to the other three and the brief template, and the question table (interview lines 44-60) is only usable once you know what the brief needs. Roughly 900 lines of instruction for a conversation that produces one document. `tests/test_rank_opportunities.py` and `LICENSE` were not read.

## 2. Friction log

Blunt, with file and line. Ordered roughly by how much each cost.

1. **Three different versions of the final designer prompt.** `SKILL.md` lines 126-130 give a bare prompt (no use case, measure, baseline or date) and call it "normally". `references/handoff-to-design.md` lines 49-55 give a filled version with `<O-ID>`, measure, baseline, counter-metric, decision and date. `assets/discovery-brief-template.md` lines 112-118 give a third variant (measure "against the baseline in the brief", no counter-metric). I had to decide which was authoritative and chose the handoff one because it was richest. The skill should carry one prompt, in one place, and SKILL.md should point to it. None of the three names stakeholders, which the trial asked me to check (see section 3).

2. **The helper cannot be run where the skill says to run it.** `SKILL.md` lines 84-89 say "Fill the portfolio table in the brief ... Run the helper", but the section ordering puts "Rank, choose and define the measure" (line 80) before "Write the brief" (line 108). You cannot run `--brief docs/discovery/<topic>.md` on a brief you have not written. In practice the order is: draft the brief, run the helper, edit the brief to quote the output, then finish the conversation. The skill should say that explicitly, or tell the agent to write the table first and the rest after.

3. **Template gives a wrong helper command.** `assets/discovery-brief-template.md` line 37: `scripts/rank_opportunities.py --brief <this file>`. Run from the project root as SKILL.md line 84 requires, that path does not exist (verified: "No such file or directory"). SKILL.md line 88 and portfolio line 39 use `"$SKILL_DIR/scripts/rank_opportunities.py"`. One command, three spellings, one of them broken.

4. **"Open with the first question of that mode" is not a question.** `SKILL.md` lines 46-47 point to `references/discovery-interview.md`; for the rough-area mode (interview lines 19-26) what is there is a quoted paragraph starting "I would first understand where advertisers abandon...". It is a stance, not a question with a decision and a default. The question table (lines 44-60) starts with "What does the business sell", which is the no-use-case opener. I turned the paragraph into a question myself. Say which row of the table is the opener for each mode.

5. **The per-turn question format is heavy and nobody says what to skip.** `SKILL.md` lines 47-49 and interview lines 37-39: one to three questions per turn, each with the decision it changes and a default. The table has fifteen questions. At the mandated rate that is five to fifteen turns before a brief exists, every question carrying two sub-clauses. The trial user already answered five of the fifteen in their first message; the skill says "infer what the request already says" (interview line 38) but never says which questions are mandatory and which can be dropped. I used five agent turns and still had to compress three questions into most of them. A "must ask" / "ask if not inferable" split would halve the conversation.

6. **Section "Rank, choose and define the measure" is a fourteen-item checklist written as one sentence.** `SKILL.md` lines 99-106: measure, baseline, counter-metric, leading indicator, threshold sentences, hypothesis chain, systems and access, cost of a wrong answer, review, automate or augment, what changes for people, 90-day sentence, press release. It duplicates template section 4 (template lines 47-80) almost item for item. I had to tick off the template, not the sentence. Keep the list in the template and have SKILL.md say "fill section 4 completely".

7. **"Five judgements per candidate (value, feasibility, data readiness, risk, fit)" counts fit as a judgement scored like the others.** `SKILL.md` line 83. `references/opportunity-portfolio.md` lines 26-31 scores four columns; `fit` is a category from a different reference. Minor, but it made me check whether fit was supposed to get a 1-5.

8. **The stakeholder sentence demands a cost estimate that the handoff forbids.** `references/technology-fit.md` lines 117-125: "It costs about [per-item cost or staff time] to run, and [role] keeps it current, including [model upgrades the vendor requires]". `references/handoff-to-design.md` line 19: "Discovery writes no contracts, no architecture, no goals and no estimates." I wrote "for the designer to state" in that slot. Either drop the cost slot from the discovery version of the sentence or say it is left blank.

9. **`llm` means "one call, no tool loop", but the realistic shape of O1 is LLM plus code lookups.** `references/technology-fit.md` line 36 defines `llm` strictly; lines 83-96 then describe hybrids ("workflow outside, agent inside", "LLM interprets, code decides") with no instruction on which `Fit` value a hybrid takes. The helper accepts only the six values (`rank_opportunities.py` line 33). I recorded `llm` and explained in prose; a different agent could defensibly write `agent` for the same design and the brief would then send the designer a different message. One line saying "a hybrid takes the fit of its model-driven step" would settle it.

10. **Whether the stakeholder sentence is needed for every candidate or only the chosen one is ambiguous.** `SKILL.md` lines 66-78 say "for each candidate ... Explain the choice in the stakeholder sentence"; the template (lines 52-53) asks for it only in section 4 for the chosen one. I wrote the full sentence once and one-line fits for the rest. Say which.

11. **"A reason to pick lower" is ambiguous.** `SKILL.md` line 93: "a risk of 4 or 5 or data readiness of 1 or 2 is a reason to pick lower". Lower rank? Lower risk? Lower ambition? I read it as "pick a lower-ranked, lower-risk candidate". Rewrite.

12. **The helper's `--pick`, `--weights` and `--json` flags are undocumented in SKILL.md.** `rank_opportunities.py` lines 197-200. `--pick` is exactly what SKILL.md line 94 ("when the user's judgement overrides the order") needs, and the helper emits the "ranked N, not 1" warning only with it (verified with `--pick O3`). Only `--weights` is mentioned, in portfolio line 42. Mention `--pick` next to the override instruction.

13. **Running example that may not exist.** `SKILL.md` lines 49-50: "Keep one real case (one advertiser, one claim, one order) as the running example." The user in this trial had no documented case; I had to have the product owner invent one. Say what to do when there is none (construct a typical case and label it assumed), as the skill already does for assumed answers.

14. **Source-name preambles in every reference.** `references/discovery-interview.md` lines 3-15 and `references/technology-fit.md` lines 3-14 open with lists of frameworks and consultancies. They justify the skill to a human reader; for the agent they are 25 lines before the first usable instruction. Move them to the research notes they already cite.

15. **Vendor pricing and lifecycle numbers inside a discovery reference.** `references/technology-fit.md` lines 98-109 quote Gemini batch pricing ratios and Vertex lifecycle promises with "verify the live table before quoting". Discovery writes no estimates and the trial had no web access, so this is dead weight here; it belongs to the designer. The reference itself says the numbers are to be re-read before use, which is an instruction to not use what you just read.

16. **Template reference link is relative to the skill, not to the brief.** `assets/discovery-brief-template.md` line 36: `[technology fit](../references/technology-fit.md)`. Once the brief is saved at `docs/discovery/<topic>.md` in the user's project that link is dead. I replaced it with plain text. The template should not carry skill-relative links.

17. **Template line 37 says the helper "adds up the scores" but the brief must also quote findings.** SKILL.md line 91 says "Quote its ranking and its findings"; the template has no slot for the helper output. I put it under the table. Add a line to section 3.

18. **The scope-gate row "familiarity with ADK and GCP" is designer vocabulary.** `assets/discovery-brief-template.md` line 88. A product owner will not know; expect "unknown: ask" every time. Fine as a row, but the skill could say "expect to mark this ask".

19. **Helper cell stripping.** `rank_opportunities.py` line 46 strips `` ` ``, `*` and `_` from every cell, so a measure such as `time_to_first_creative` would be reported as `timetofirstcreative`. Not hit in this trial; worth a note or a narrower regex.

20. **"Keeping the project's own document convention where one exists" with no way to detect one.** `SKILL.md` lines 110-112. Harmless in a fresh directory; in a real repo the agent has to guess what counts as a convention. Say "look in `docs/` for an existing brief or ADR format".

What was *not* friction: the mode statement (SKILL.md lines 36-44), the measured-versus-reported discipline (line 59), the "name the mistake" list (lines 74-77), the counter-metric and threshold-sentence rules, and the helper's findings all worked and shaped the output usefully. The template sections 5 to 7 are good.

## 3. Handoff prompt

Produced, in both the transcript (agent turn 6) and brief section 8, using the handoff-reference form rather than the bare SKILL.md form:

- Use case: yes (O1, one sentence).
- Measure: yes (product-choice step completion rate).
- Baseline: yes (62%, 1,327 of 2,140, Q3 2026).
- Counter-metrics: yes (refunds 3%, escalations ~35 a week).
- Decision and date: yes (proof-of-concept decision 29 October 2026; production decision after the four-week build).
- Stakeholders: **not in the prompt.** None of the three prompt templates has a stakeholder slot; the prompt says "treat its confirmed answers as settled", and the stakeholders are in brief section 6. If the trial wanted them in the prompt, the skill's templates do not ask for it. Adding "the sponsor is <role>" to the prompt would be a one-line change.

Helper verdict on the brief: exit 0, no blocking, no warnings, "Ready for adk-system-designer" (`helper-output.txt`).

## 4. Temptation to write contracts, architecture or goals

Yes, three times:

- When settling the fit of O1 I started describing the shape ("a short form, one model call with a schema, code looks up price and availability via the product service"). That is a sketch of architecture. The skill says discovery "writes no contracts, architecture, goals or code" (SKILL.md lines 29-30; handoff line 19). I kept the fit and the one observable reason, left the shape in the stakeholder sentence as the technology-fit reference requires, and wrote nothing about components or ADK.
- The threshold sentences read like outcome contracts. The interview reference (lines 79-82) explicitly says the designer turns them into contracts, so writing the sentences is in scope; writing the contract is not. I stopped at the sentences.
- The stakeholder sentence's cost slot (technology-fit line 123) pulled toward an estimate; handoff line 19 forbids estimates. I wrote "for the designer to state".

The line itself is clear once you have read `handoff-to-design.md`; the pull comes from the technology-fit reference, which describes hybrids and costs in enough detail that an agent naturally starts designing.

## 5. Time and rating

Time spent: about 45 minutes of agent work: roughly 10 reading the 900 lines, 15 on the conversation, 15 on the brief, 5 on the helper and checks.

Ease of following: **3 of 5.** The structure (mode, friction, fit, rank, measure, brief, handoff) is sound and the helper is a genuine help. What costs points: three copies of the final prompt that disagree, a helper that cannot be run at the point the skill says to run it (and one broken command spelling), the fourteen-item sentence that duplicates the template, and an opener that is not a question. Each is a small edit; together they make the first run slower than the content deserves.
