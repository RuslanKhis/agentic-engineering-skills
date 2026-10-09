I've written the design and the implementation plan, plus `REPORT.md`. Nothing was implemented or installed and no cloud or network commands were run. No tests were run: there is no application code yet and `google-adk` isn't installed.

**Files:**
- `docs/architecture/card-dispute-agent.md` — the design. It's marked **draft** because every decision rests on my 15 assumed answers (Q1–Q15), which are tabled at the top.
- `docs/plans/card-dispute-agent.md` — dependency-ordered goals, a 17-week schedule, and the run prompt for each ready goal.
- `REPORT.md` — sections 1–6 as you asked, including the friction log with `file:line` pointers into the skills.

**Main design decisions (all proposed, none accepted by you yet):**
- **One agent with four narrow tools.** Three read tools are tied to the customer from the verified login token. The fourth only saves a draft to the customer's own session.
- **Filing a case is not something the model can do.** The app shows a summary built by code from the stored draft. The customer confirms it with step-up authentication, and only then does ordinary code call core banking.
- **Rules live in code, not the model.** Eligibility, time limits and reason codes come from a versioned rule table owned by disputes ops and Compliance.
- **At most one case per confirmation.** Each confirmation gets a stored operation record whose ID is sent to core banking. If a submission's result is unknown, a reconciler checks status instead of resending. This depends on whether the core banking API supports that (open decision D-02).
- **The model never reads uploaded evidence**, and card numbers, CVVs and PINs are blocked at intake before anything is stored. This removes the riskiest prompt-injection route.
- **Hosting and model:** Cloud Run in an EU region, Vertex AI `gemini-3.8-flash`, and ADK 2.8.0 as the assumed version. I rejected `gemini-3.7-flash` because Vertex retires it on 2027-01-28, just before the planned go-live in early February 2027.

**Still open:**
- **D-01:** whether the model and the screening services are available in an EU region, plus quotas and prices. I couldn't check online, so costs are formulas only.
- **D-02:** the core banking dispute API's duplicate-submission and lookup behaviour.
- **D-03:** the dispute rule table, a baseline follow-up rate, and a labelled set of past disputes.
- **D-04 to D-07:** how step-up confirmation fits into the banking app, Cloud Run versus GKE, retention rules, and model-risk sign-off.

The regulatory points are assumptions for Compliance to confirm, not legal advice.

The next ready goal, G01, runs fully offline with fake services:

```text
/adk-engineer Carry out G01 from docs/plans/card-dispute-agent.md.
```