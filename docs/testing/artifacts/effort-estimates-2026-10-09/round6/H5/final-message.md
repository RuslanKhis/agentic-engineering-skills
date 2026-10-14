I've written the design, the plan and 27 tickets for phase 1. Nothing is implemented, and the design is still a draft: every product answer in it was assumed, because you weren't available to answer questions.

**Profile:** production service. Customers are outside the company, the data is personal, and the system writes to Guidewire ClaimCenter, the system of record.

**How it works:**
- **The agent:** one ADK agent with four small tools, and those tools can only edit the customer's own claim draft.
- **Photos:** read by a separate model call that has no tools, so text hidden in a photo can't trigger an action.
- **Creating the claim:** done by ordinary code, never by the model, and only after the customer presses Confirm on the exact draft shown.
- **No duplicate claims:** each confirmed draft gets a durable submission record. If the response from Guidewire is lost, the system checks whether the claim exists before sending again.
- **Hosting:** Cloud Run, Cloud SQL and a storage bucket in an EU region. The model is `gemini-3.8-flash` on Vertex AI, pinned to that exact version.

**Cut line (please confirm or move it):**
- **Phase 1 (G01–G27):** builds everything up to a controlled pilot and EU general availability on 12 March 2027. That date is my assumption for "five months".
- **Effort:** 428–723 human hours against 2,850 available after a 25% reserve. The schedule check passes, finishing in 61–97 of 100 working days.
- **What sets the date:** outside waits, not engineering hours: the Guidewire sandbox, the external pen test and the pilot itself.
- **Risk to the date:** if the Guidewire sandbox takes 15–20 days instead of 5–10, general availability slips by up to a week. Only doing three things together brings it back to exactly 100 days: more hours from the security reviewer, splitting the Guidewire work between two engineers, and requesting the sandbox this week.
- **Phase 2 (G28–G34), after general availability:** itemised contents claims, a second market, adding photos to an existing claim, a fallback model, cost tuning, turning production samples into test cases, and passing drafts to the phone team.

**Decisions still open:**
- **Guidewire:** whether ClaimCenter can safely accept a repeated request, and how to look a claim up by our reference (G01).
- **EU availability:** whether the model and the data-screening services are offered in the chosen EU region (G02).
- **Data protection:** the DPIA outcome, which sets retention periods and the "you're talking to AI" notice; it blocks the pilot (G04).
- **For you:** the market and languages, whether the team is fully dedicated, and the budget.

**Shortfalls and session notes:**
- **Too long:** the design and plan come to about 13,450 words against the skill's ~8,000 guide, and tickets are about 220 words each against ~150.
- **Not looked up:** prices and provider facts, because network access was off, so the costs are symbolic.
- **Rule broken:** early scratch calculations wrote files to `/tmp`, outside the working directory. I deleted them before writing any project files.
- **Tests:** no tests that import `google.adk` exist or could run here. The schedule helper's own 10 tests pass.

Files are in `docs/`:
- docs/architecture/home-claim-intake.md
- docs/plans/home-claim-intake.md
- docs/tickets/home-claim-intake/ (G01–G27)
- REPORT.md (with the questions I would have asked, the checks, and the problems I hit with the skill)

Next prompt (G02–G06 are also ready and can run in parallel):

```text
/adk-engineer Carry out G01 from docs/plans/home-claim-intake.md.
```