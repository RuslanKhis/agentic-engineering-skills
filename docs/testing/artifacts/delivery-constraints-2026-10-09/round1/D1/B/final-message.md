I've written the design and a plan for the triage proof of concept; no code yet, as you asked. Every product decision in it is my assumption (you weren't available), so both documents are marked draft.

**The design in short:** a plain Python loop sends each of the 50 emails to one ADK agent. In a single model call the agent returns:
- a category from a fixed list;
- a one-line reason;
- a "needs a human" flag;
- a draft reply.

The agent has no tools, so it can't send anything. A human copies the draft. Without a knowledge base, the drafts put any fact the email doesn't contain in a `[CONFIRM: …]` placeholder instead of promising refunds or dates.

For the demo, all 50 results are worked out in advance and shown as a static page, so it still works if the model is unavailable. One live email is optional. You label 15 emails for tuning the prompt and keep 35 aside, scored once at the end. That gives the head of support an accuracy figure on emails the prompt wasn't tuned on.

The model is `gemini-3.8-flash` (stable, no shutdown date in the skill's model table dated 8 October). The call cap is 2 per email and 600 for the day, which bounds spend. The model price wasn't checked because I had no network access.

**The 5 hours:** preparing and labelling the data takes about 30 minutes, building and a first measured run about 1¾ hours, prompt improvements and the final run about 1¼ hours, and the demo page about 45 minutes. That leaves about 45 minutes spare.

**Checks:** no tests exist and none were run. Nothing was implemented, and ADK isn't installed here. I only checked that the links between the documents work and that the model ID is in the model table.

**Decisions still open:**
- **Categories:** I proposed 8 (billing, refund or cancellation, account access, technical issue, how-to question, feature request, complaint, other). You or the head of support should set the real list.
- **Data policy:** whether the anonymised emails may go to the Gemini API, or must go through Vertex AI instead.
- **Knowledge base:** whether one exists. Without it, drafts stay fairly generic.
- **ADK version:** assumed to be 2.8.0; confirming it is part of the first build step.

`REPORT.md` covers the six things you asked for, including the friction log. The main friction points:
- **Document length:** the skill's ten-minute-read target and its template pull against each other, so the two documents total about 4,100 words.
- **Next-prompt format:** the skill gives two different formats.
- **Tuning versus scoring:** keeping 35 emails aside for scoring sits awkwardly with showing all 50 in the demo.

The first step is yours: put the 50 emails in `data/emails.jsonl`, write `data/categories.md` and label each email in `data/labels.csv`. Then type:

```text
/adk-engineer Carry out G01 — Triage all dev emails end to end, measured — from docs/plans/support-email-triage.md.
Read docs/architecture/support-email-triage.md and preserve its accepted decisions.
Use adk-model-and-output-contracts with adk-agent-instructions and adk-agent-evaluation.
Work within local code and at most 600 model calls on my Gemini API key, verify the G01 acceptance cases, and update
the plan with actual evidence and remaining blockers.
```

Files are in `docs/`:
- `REPORT.md`
- `docs/architecture/support-email-triage.md`
- `docs/plans/support-email-triage.md`