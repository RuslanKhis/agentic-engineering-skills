I've written the design and plan and the three phase 1 tickets; nothing is implemented and nothing is committed. You weren't available, so every scope answer is an assumption; the main ones are listed below and recorded in a table at the top of the design, which stays marked **draft** until you confirm them.

**What the proof of concept is:** one ADK agent you run locally in `adk web`. It has a single read-only search tool over the PDFs, split into one record per page. It answers in a few sentences, cites `[policy title, p.N]`, and says "not found in the policies, please contact HR" when they don't cover a question. It reaches the model through Vertex AI using your gcloud login, so there is no API key on disk. The model is pinned to `gemini-3.8-flash`, and I steered away from `gemini-3.6-flash` because it retires on Vertex on 2026-11-19.

**Does it fit your 6 hours:** yes, just. I counted your 6 hours as about 4.8 focused hours and held 25% back for rehearsal, leaving 3.6 hours. Phase 1 is three goals totalling 2.5–3.5 hours, and the skill's schedule script confirms it finishes within 2 working days:
- **Day 1, G01:** index the 30 PDFs by page and prove one live model call works.
- **Day 1, G02:** cited answers in `adk web`.
- **Day 2, G03:** five checked "gold" questions, plus a saved results table to fall back on if the live demo fails.

Everything else waits for phase 2 (about 22–42 hours): a larger question set labelled by an HR expert, better search, document version tracking, and hosting for named HR staff. To fit, I cut scope rather than shrinking estimates: simple keyword search, no tuning loop, five questions instead of a full set. This deliberately comes in under the skill's own starting figure for this kind of work, so treat the estimates as tight.

**Checks:**
- The schedule script passed (exit 0) under Python 3.13. I re-ran it after my last edits but didn't capture the exit status; the schedule figures hadn't changed.
- The skill's own tests passed (9 of 9).
- No tests that import `google.adk` were run: there is no code yet and the dependencies aren't installed.
- The design is about 1,880 words against the skill's target of about 1,200.

**Decisions still open (please confirm):**
1. Is the demo on Friday 2026-10-16? Today is a Friday, so I assumed next week.
2. May the PDFs be sent to Vertex AI in your company project, and in which region? This blocks only G01's live model call.
3. Are any PDFs scanned, superseded or country-specific? G01's ingest report will show this.
4. Are you new to ADK? I assumed yes, which multiplies every estimate by 1.5; if not, phase 1 has spare room.

Files are in `docs/`:
- `architecture/hr-policy-qa.md` — design and plan in one file
- `tickets/hr-policy-qa/G01-index-policies.md`
- `tickets/hr-policy-qa/G02-cited-answers.md`
- `tickets/hr-policy-qa/G03-gold-check.md`

`REPORT.md` (in this directory) has all six sections you asked for, including the questions I'd have asked and the friction log.

Next, type:

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G01-index-policies.md.
```