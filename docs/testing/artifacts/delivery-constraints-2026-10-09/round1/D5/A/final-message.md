Happy to help design this. I checked the project first: there's no code or architecture notes yet, so this is a greenfield design and I'll start from your description.

**The journey as I understand it (please correct me):** an account executive finishes a sales call. Gong records and transcribes it. Today the AE writes the summary, next steps and any deal changes into the Salesforce opportunity by hand, which is slow, uneven, or skipped. The goal is that a few minutes after the call, the opportunity holds an accurate summary and update without the AE retyping it.

**The shape I'd propose so far (not decided yet):**

- **One ADK agent with no write tools.** It reads one transcript and returns a structured, schema-validated proposal: the summary, next steps, and any suggested field changes, each with a quote from the transcript as evidence.
- **Ordinary code around the agent.** It fetches the transcript, finds the matching opportunity, and writes to Salesforce only after a check.
- **Why the split matters:** the transcript is untrusted input, because anything a prospect says ends up in the model's context. If one agent could both read that text and write to Salesforce, someone on a call could steer what gets written. Keeping the model's output as a proposal that code validates, with an approval step before the write, is cheap now and hard to add later.
- **One agent is enough.** I don't see a reason for a multi-agent setup unless your answers below create one.

Before I size or detail anything, I need answers to the questions that set the scope. Defaults are in brackets, so you can reply "defaults" or just answer the ones that differ.

**Scope and capacity**

1. **Deadline:** when must the first useful version exist, and will it be continued afterwards? *[No deadline; continued]*
2. **Builders:** how many people, roughly how many hours each, and how familiar are they with ADK and GCP? *[One developer, part time, new to ADK]*
3. **Budget:** how much money is there for models and cloud? *[A small allowance]*
4. **Users:** who uses or judges it? Is it a demo for sales leadership, a few AEs trying it, or the whole sales team every day? *[You, reading the design]*

**Data and effects.** These set the risk level, whatever we call the project:

5. **Data:** real Gong transcripts (customer conversations, names, possibly pricing) or anonymised samples? A production Salesforce org, or a sandbox? *[A few anonymised transcripts, Salesforce sandbox]*
6. **What it may change in Salesforce.** This is the biggest design fork:
   - **a)** Only add a call summary to the opportunity (a note, activity, or one custom summary field). Low risk, because it only appends.
   - **b)** Also update next steps or other qualification fields (for example MEDDICC).
   - **c)** Also change forecast fields: stage, close date, amount. These feed pipeline reports, so a wrong value reaches people beyond the AE.

   *[(a) now, (b) as a reviewed suggestion]*
7. **Approval before a write:** does the AE confirm the update first (in Slack, an email link, or a simple page), or does it write automatically? *[AE approves before anything is written; automatic writes only in the sandbox]*

**One technical question:** how are calls linked to opportunities today? Does Gong already associate each call with a Salesforce opportunity, or would the system have to match by account, contacts and date? If Gong already links them, the agent never has to guess which deal a call belongs to. If not, matching becomes its own step that needs a human check whenever it's ambiguous. If you don't know, I'll treat it as something to check early.

With your answers I'll do three things:

- state the delivery profile (proof of concept, internal tool, or pilot);
- estimate phase 1 against your hours and show you the cut line between what ships first and what waits;
- write the design and phased plan to `docs/architecture/` and `docs/plans/`.