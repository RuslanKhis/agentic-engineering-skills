I've written the design and the implementation plan, but nothing is agreed yet. You weren't available, so every decision rests on 12 assumed answers. Each one is listed at the top of the design with the decisions that depend on it.

**Recommended shape:** one ADK agent with two read-only tools (list my claims, get one of my claims), plus the expense policies included directly in the agent's instructions. It runs as a small web app on Cloud Run. Google's sign-in gateway (IAP) restricts access to your Workspace users.

- **Own claims only:** the app looks up the signed-in employee itself and passes that ID to the database queries. The model can't name another employee, so asking for a colleague's claim just returns "not found among your claims".
- **No AI-written SQL:** the tools run two fixed queries through a database role that can only read one limited view. The assistant can't change anything in the database.
- **Honest failures:** if the database is down, it says it can't reach the expense system rather than "you have no claims".
- **Policy answers:** every answer cites a policy section, or says the policy doesn't cover it and points to the finance inbox.
- **Model:** Vertex AI `gemini-3.5-flash`, because its retirement date (2027-05-19 or later) is well after the pilot.

**Plan:** in week 1 each engineer takes one goal in parallel: G01 (cited policy answers, scored on 30 or more labelled questions) and G02 (own-claims lookup against a test database). Week 2 is the signed-in chat page with saved conversations (G03). Week 3 is the pilot deployment (G04), which is blocked until a GCP project is authorised. Two questions for your DBA run alongside: how the app reaches the database, and how a Workspace email maps to an employee record.

**Checks:** I only checked the documents themselves. The links between them work, and the model choices match the lifecycle table that ships with the skills. Nothing was built, so no tests ran; the ADK libraries aren't installed and no network or cloud commands were allowed. ADK 2.8.0 is an assumption (it's what the skills were checked against), and confirming it is the first item of G01. I couldn't look up prices or region availability, so the cost estimate is a formula, not a figure.

**Decisions most likely to change the design:**
- whether finance staff need to see other employees' claims, for example as approvers;
- where the database runs and who grants the read-only role;
- which column links a Workspace email to an employee;
- how large the policy documents are (over roughly 50k tokens means switching to a search step instead of putting them in the prompt);
- data-residency region;
- how long chats containing claim data may be kept (I assumed 30 days).

The design is about 3,750 words, longer than the skill's two-to-four-page guideline for a pilot; I didn't trim it.

`REPORT.md` has the six sections you asked for, including the friction log with pointers into the skill files.

Next prompt, from the plan's "Resume here" section:

```text
/adk-engineer Carry out G01 — Cited policy answers, measured from docs/plans/expense-assistant.md.
Read docs/architecture/expense-assistant.md and preserve its accepted decisions.
Use adk-agent-instructions with adk-agent-evaluation and adk-model-and-output-contracts.
Work within local code and, only if authorised, a capped Vertex run in a dev project; verify
G01's acceptance cases, and update the plan with actual evidence and remaining blockers.
```

Files are in the project folder:
- docs/architecture/expense-assistant.md
- docs/plans/expense-assistant.md
- REPORT.md