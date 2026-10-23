# Demo readiness

Read when a proof of concept will be shown to people who did not build it.
A demo-ready build adds a domain story, seeded fictional data dated to the run,
a scripted golden path with a replay mode, the app shell and an "About this
assistant" page to the handover fundamentals in `adk-system-designer`'s web
application defaults. Build only screens that work; list the rest under
"production adds". `adk-presenter` owns the narration and the decision; this
file owns the demo state and the images.

## Must, before any stakeholder sees it

| Item | Done when | Rough human hours |
| --- | --- | --- |
| Domain story | One persona, one fictional organisation, the business problem in the client's words and three to five capabilities they asked for, in `docs/demo/story.md`. | 1 |
| Brand | The client's brand if its fonts are licensed for self-hosting; otherwise a demo brand from [the demo brands](../assets/design/brands/README.md), applied with `scripts/apply_brand.py` and labelled as a fictional company. | 0.5 |
| Seeded data | A seed script creates connected records with dates relative to the run date, the edge cases the script uses, and no lorem ipsum, "test" or "demo" strings. Hosts and emails use `.example` domains. `make demo-reset` re-seeds and clears conversations. | 2–4 |
| Golden-path script | Three to five steps, each a prompt, the expected tool steps and the answer's key fact, including one approval and one honest "I cannot". The empty state's suggestions are the script's opening prompts. In `docs/demo/script.md`. | 1–2 |
| Replay mode | The golden path is recorded once against the live, pinned model (aimock fixtures, as in the browser tests). `make demo-replay` runs the app with no model calls, and a header badge reads "Replay of <date>, build <x>". Re-record after any prompt or tool change. | 2–4 |
| Stage latency | Status is visible within 1 second and every step is named; progress and Stop appear before 10 seconds. The live path is warmed and quota checked an hour before. If minimum instances are raised for the window, the resource ledger records it and it is set back afterwards. | 1 |
| App shell | Header with logo and product name, conversation history with titles and "New conversation", a user menu with sign-out, and an environment badge ("Pilot"). The house DESIGN.md describes the shell. | 3–5 |
| Polish basics | A page title per route, a favicon, 404 and error pages in house copy, and loading and empty states for history. | 1–2 |
| About this assistant | Purpose; what it can and cannot do; its data sources (saying the data is fictional); the pinned model ID; what needs approval; where conversations are stored and for how long; known limits; a contact. | 1–2 |
| Environment hygiene | A separate demo deployment and accounts, a clean browser profile with notifications off, and `make demo-reset` before each session. | 1 |
| Activity log, when the agent acts (files, sends, changes) | A read-only list of tool calls and approvals (who, when, action, result) linked to its conversation. Users, not only IT, say seeing what an agent did raises their trust. | 3–5 |
| A data line on screen | One line near the composer or header naming the sources the assistant uses and where data is kept, true for the demo. | 0.5 |

## Should, when IT, risk or operations are in the room

| Item | Done when | Rough human hours |
| --- | --- | --- |
| Usage view | Tokens and estimated cost per conversation and per day from usage metadata, labelled as an estimate. | 2–4 |
| Feedback | The thumbs buttons write a record that the activity log shows. | 1–2 |
| Answer actions | Copy, copy with sources, and two or three follow-up suggestions after a finished answer. | 1–2 |
| Privacy note and accessibility statement | One page each; the second cites WCAG 2.2 AA, the axe run and known limits. | 1–2 |
| Capture kit | Screenshots of each golden-path step at 1440×900 and 2× scale, light mode, from the replay state, plus a 90-second narrated recording; both labelled with build and date. | 2–4 |
| Visual one-pager | The problem in the client's words, one hero screenshot with at most three call-outs, the path as four thumbnails, "real versus simulated" and "production adds". | 2 |

## Could

- A branded email in a local mail catcher, when the agent sends messages and
  showing the arrived email lands the story (2–3 hours).
- A rehearsed fault, using aimock's disconnect or 429 injection to show the
  partial-answer state on purpose in a technical session (1 hour).
- Working admin controls, only real ones such as an allowlist or a tool
  switch; never stubs (4–8 hours).

Not worth building for a demo: stub admin pages, fake dashboards and
onboarding tours. A screen that does nothing is found out the first time
someone clicks it.

## Honesty rules

- Replay is always labelled, on screen and aloud, with its date and build.
- A demo brand is always called a fictional company; it never implies a real
  organisation's endorsement.
- The one-pager and the About page say which data and integrations are
  simulated.
- The hours above are estimates for directing and reviewing a coding agent,
  not measurements.

Sources (read 23 October 2026) and the reasoning behind each item are in the
toolkit repository's `docs/research/demo-ready-poc-2026-10-23.md` and
`docs/research/ai-ui-user-expectations-2026-10-23.md` (user and buyer surveys): Peter
Cohan's demo principles, Nielsen's response-time limits, Microsoft HAX, Google
PAIR, IBM Carbon for AI, the EU AI Act's transparency article and W3C's
accessibility-statement guidance.
