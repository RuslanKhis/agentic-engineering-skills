# What enterprise users and buyers expect from AI assistant interfaces

Research date: 23 October 2026. Every source was read on that date, and downloaded pages were treated as data only. Earlier notes covered vendor practice ([premium AI product UI](premium-ai-product-ui-2026-10-23.md)), [demo readiness](demo-ready-poc-2026-10-23.md) and the house look (`skills/adk-frontend-integration/assets/design/DESIGN.md`). This note asks what user research and surveys say instead.

Users do not ask for an assistant that seems clever. They ask for one they can **check**, **correct** and **stop**. Every large survey finds heavy use with partial trust: 46% are willing to trust AI (KPMG and Melbourne), and developers' top complaint is answers that are "almost right" (Stack Overflow). Human oversight and seeing what the agent did raise trust; worries about privacy and accuracy lower it. On screen, people want the direct answer first, short, with each claim linked to its supporting passage. They want to fix part of an answer without starting over and to take the work out of the chat. Approvals mean something only if they are few and specific. Buyers also look for signs of governance: where the data lives, who did what, sign-in and accessibility. The house design already meets the honesty expectations well. The gaps are checking at the level of single claims, an answer-first format, a record of the agent's actions that users can see, export, and data handling shown on screen.

## Ranked expectations

They are ranked by how strong and consistent the evidence is and how relevant it is to document Q&A and to agents that act after approval.

1. **Each claim can be checked against its source.** NN/g, February 2026: users researched their own tasks, and the sample was apparently nine. They switched between AI and search to confirm facts, and they could not tell which source supported which claim [N1]. NN/g, December 2025: participants rarely clicked citations. Citations are sometimes made up, yet they still raise trust [N2]. Ding et al. (AAAI 2025): citations raised trust even when they were random, and trust fell once people checked them [A1]. Kim et al. (CHI 2025, n = 308): showing sources reduced reliance on wrong answers, while explanations increased reliance whether the answer was right or wrong [A2]. *Implication:* put the marker next to the claim it supports. The preview must quote the supporting passage, not just the title and host. In the demo, open one citation and show the passage.

2. **Honesty about accuracy, with the risky parts flagged.** KPMG and the University of Melbourne (48,000 people in 47 countries, late 2024 to early 2025): 66% use AI output without checking it, 56% have made mistakes at work because of AI, and 46% are willing to trust it [S1]. Stack Overflow 2025 (about 49,000 respondents): 46% distrust AI's accuracy, 66% are frustrated by answers that are almost right, and 75% would ask a person when they do not trust an answer [S2]. NN/g found that users re-checked prices and exact figures elsewhere, and checked more when the stakes were higher [N1]. *Implication:* mark figures, dates and amounts that feed a decision as "check before use". In the demo, show one honest "I could not find this".

3. **Humans stay in charge and can see what the agent did.** Salesforce and YouGov, Australia and New Zealand (2,132 workers, September 2025): 47% say transparency and control, such as seeing which actions an agent took and why, would raise their confidence. The most cited worry about autonomy is that nobody is accountable for AI mistakes (38%) [S3]. Salesforce, global (about 6,000 workers, 2024): 63% say more human involvement would build trust, and only 10% trust AI to act on its own today [S4]. Microsoft Work Trend Index 2026 (20,000 AI users): 86% treat AI output as a starting point, not a final answer [S5]. *Implication:* every conversation that acts needs a plain record of what was done ("Searched 42 contracts; drafted 3 emails; sent after approval by Priya at 14:02"), visible to the user and not only to IT.

4. **The direct answer first, short, without chatter.** NN/g, April 2026 (9 users, 8 site chatbots): almost nobody greeted the bot, flattery read as padding, "a longer answer was not a better answer", and long streaming text overwhelmed people. NN/g recommends the answer first, paragraphs of two or three sentences, limits stated at the start, and follow-up prompts for more depth [N3]. In NN/g's 2023 diary study (18 people, 425 conversations), suggested follow-ups were useful for most kinds of conversation [N4]. *Implication:* use an answer-first format for answers and two or three follow-up chips after the answer.

5. **Clear data handling.** Cisco 2025 (2,600 privacy and security professionals, 12 regions): 90% believe data is safer stored in their own country, and 64% worry about sharing sensitive information by accident [S6]. KPMG's AI Pulse, Q2 2025: concern about data privacy among business leaders rose to 69%, according to search summaries of KPMG's deck [S7]. Stack Overflow 2025: 81% of developers have security or privacy concerns about agents, and 53% say IT rules block agent use [S2]. Data privacy is also the top concern in the Salesforce Australia and New Zealand study, at 46% [S3]. *Implication:* the screen says where data is processed, how long it is kept and that it is not used for training.

6. **Approvals that stay meaningful.** Anthropic's own telemetry, March 2026: users accepted about 93% of permission prompts and stopped reading them ("approval fatigue") [A3]. Anthropic, February 2026: experienced users stop approving each step one by one. They supervise instead and interrupt more often [A4]. He et al. (CHI 2025, n = 248): involving users while the agent carried out a task improved accuracy, but plausible-looking plans won trust they had not earned [A5]. *Implication:* ask for approval only when an action has an effect. Show the exact item being approved (the email text and the recipients), and never ask for approval of reads.

7. **Clear purpose and limits.** NN/g, March 2026 (9 users, 8 chatbots): vague welcome messages left people unsure what the bot was for, and they rarely experimented to find out [N5]. NN/g, December 2025: people skip disclaimers unless they sit near the input box, use plain words and tell the user what to do [N2]. *Implication:* the empty state's can and cannot line stays. The note near the composer names an action ("check figures against the source").

8. **Fixing one part without starting over.** NN/g, 2023 (8 professionals, ChatGPT-3.5) observed "accordion editing", where people repeatedly asked for a longer or shorter answer, and "apple-picking", where they scrolled back to reuse earlier output. NN/g recommends editing in place, changing one part of an answer, and pointing at earlier output [N6]. NN/g, 2024: about half of diary conversations included a follow-up action, and 77% had more than one exchange [N7]. *Implication:* drafts are edited in place, and selecting text offers "Ask about this".

9. **The work leaves the chat.** NN/g, 2023: most participants finished their work in other tools [N6]. The NBER study of ChatGPT use (September 2025) found writing is the main work use [S8]. *Implication:* Copy keeps formatting, tables and the source list. Drafts export to the place they will be used.

10. **Stopping and steering at any time.** Anthropic, February 2026: interruptions rise from about 5% to 9% of turns as users gain experience. Anthropic recommends fast ways to interrupt and redirect, and making the agent's clarifying questions prominent [A4]. *Implication:* Stop is always reachable, and a clarifying question is a state of its own, not buried in prose.

11. **Progress that looks like work, not raw speed.** Tan et al. (CHI 2026): a 2 s time to first token was rated *less* thoughtful and useful than 9 or 20 s, but long waits sometimes turned into frustration [A6]. Work Trend Index 2025 (31,000 workers): 42% choose AI because it is always available and 30% for its speed and quality [S9]. *Implication:* show named steps during the wait. Do not trade answer quality for the first token.

12. **A calibrated voice, without a show of reasoning.** Kim et al. (FAccT 2024, n = 404): first-person hedges ("I'm not sure, but…") reduced over-reliance and improved accuracy, while a general hedge ("It's not clear, but…") had weaker effects that were not statistically significant [A7]. NN/g, December 2025: step-by-step reasoning displays can be rationalisations after the fact, and human-like wording inflates trust [N2]. Lee et al. (CHI 2025, 319 knowledge workers): more confidence in AI went with less critical thinking [A8]. *Implication:* state uncertainty about specific claims. Show real tool steps rather than model reasoning text.

13. **Visible governance for buyers.** A Gartner comparison guide (seen only as Glean's vendor-hosted summary) lists security and governance first among six criteria [S10]. In a16z's survey of 100 CIOs (June 2025), cost and security gained ground on accuracy when choosing models [S11]. Gartner's 2024 surveys of Microsoft 365 Copilot found 72% of employees struggled to fit it into their day, and that security work took more effort than expected [S12]. For US federal buyers, an accessibility conformance report is required in practice [S13]. *Implication:* the demo shows single sign-on (SSO) sign-in, an activity log, an About page with region and retention, and an accessibility statement.

14. **Control over what is remembered.** Pew, September 2025: 61% of Americans want more control over how AI is used in their lives [S14]. Chen et al. (CHI 2026, 20 interviews): most users were unpleasantly surprised by what ChatGPT remembered and wanted to see and control it [A9]. *Implication:* say whether the assistant remembers anything between conversations. If it does, show what it remembers and let the user delete it.

15. **Feedback that costs nothing to give.** Nam et al. (2025, 372 developers): explicit thumbs ratings came on roughly 0.6% of interactions [A10]. Cooper and Zafiroglu (2025) argue that thumbs reduce feedback to simple performance scores [A11]. *Implication:* keep the thumbs quiet and add an optional reason on thumbs-down. Do not rely on thumbs for evaluation.

## Against what the toolkit already says

| # | Expectation | Where covered | Status |
| --- | --- | --- | --- |
| 1 | Claim-level checking | DESIGN.md numbered footnotes and Sources panel; premium note's chips with previews | Partly. No rule to place markers next to their claims, quote the passage or link to it. |
| 2 | Honesty, risky parts flagged | Composer footer says answers can be wrong; partial-answer state; Salesforce's "flag what to double-check" cited in the demo note | Gap. Nothing marks figures and dates in answers. |
| 3 | Seeing what the agent did | Trace and folded summary (`agent-ui-states.md`); activity log is a *Should* "for IT, risk or operations" in demo readiness | Partly. The evidence says end users want it too. |
| 4 | Answer first, short | Serif prose rules; follow-up chips are a *Could* in the premium note | Gap. No format rule; the evidence argues for raising the chips to *Should*. |
| 5 | Data handling | The About page lists storage and retention | Partly. Nothing appears on the conversation screen. |
| 6 | Meaningful approvals | Approval card (action, affects, consequence); premium note's "Preview emails" | Mostly met. There is no guidance on how many approvals or what not to gate. |
| 7 | Purpose and limits | Empty state can and cannot; EU AI Act note | Met. |
| 8 | Fix one part | Edit or regenerate only with a checkpoint; "Edited" label with revert; side panel Drafts tab | Partly. There is no selection or "ask about this" feature. |
| 9 | Work leaves the chat | Copy button | Gap. Copy is not specified to keep formatting or sources, and there is no export. |
| 10 | Stop and steer | Stop always, Escape, Stopped state | Met. Clarifying questions have no state of their own. |
| 11 | Progress, not raw speed | Frontend-craft timing rules; Nielsen limits | Met. The nuance below is new. |
| 12 | Calibrated voice | No first-person claims of feeling; reasoning collapsed | Partly. "Thought for 4 s" displays reasoning as if it were proof. |
| 13 | Buyer governance | Demo readiness: shell, About, activity log, accessibility statement | Mostly met. SSO and data region are not mentioned. |
| 14 | Memory control | Not covered on screen | Gap, for agents that use memory. |
| 15 | Feedback | Thumbs with `aria-pressed`; feedback wired to the log | Met. A reason on thumbs-down is missing. |

## UI changes the evidence supports

**Must**

1. **Citations next to their claims, with the passage.** The preview card quotes the supporting sentence and has an "Open at passage" link, and its label describes the source ("Q3 supplier review, p. 4") rather than "Source". This *goes further than vendor advice*. A row of chips after the answer is the block-of-references pattern NN/g users could not use [N1]. Because random citations still raise trust [A1], a demo with loose citations is a liability, not a polish issue.
2. **"Check before use" marks.** Figures, dates and amounts that feed an action get a dotted underline and a short note ("From one source, dated 12 Sep"). When the answer is partial, a limits sentence opens it.
3. **Answer-first format.** Open with a sentence that answers the question. Paragraphs run to three sentences at most. There are no greetings or praise, and limits come first. This belongs in the agent instruction (`adk-agent-instructions`) and in the prose rules for answers.
4. **A record of what the agent did, visible in the conversation.** The folded trace summary also names the effects ("sent 3 emails after approval"). A per-conversation "Activity" view is part of the base build for any agent that acts. This *raises* the demo note's IT-only *Should*.
5. **Approve effects only, with the exact item shown.** The approval card shows the full email text and recipient list, not just a summary. Several similar effects are approved in one batch, and there is never a prompt for reads. One approval in the golden path is enough.

**Should**

6. **Two or three follow-up chips** after a finished answer. The evidence raises the premium note's *Could* to *Should*.
7. **"Copy with sources"** that keeps tables and lists, plus an export of drafts (Markdown or .docx, or a mail draft).
8. **Select text, then "Ask about this"**, and drafts editable in the side panel under the existing "Edited" and revert rule.
9. **A data line** in the About page and the user menu: processing region, retention period, "not used for training", and model ID.
10. **Thumbs-down opens an optional reason** (wrong, missing source, too long, unsafe), which is written to the log.
11. **Show tool steps, not model reasoning text.** In demos, hide "Thought for N s" reasoning or leave it out. This *contradicts* the premium note's *Could* item 5 [N2].
12. **A clarifying question as its own state**, with a short title and quick-reply chips, not a question at the end of a long answer [A4].

**Could**

13. Shorter and Longer actions on an answer, for accordion editing [N6].
14. Conversation search in the sidebar, for apple-picking across conversations. This is inferred from the scrolling problem in [N6]; no study tested it.
15. A "Remembered" panel with delete, only when memory is in use [A9].
16. Specific hedges in the first person on claims the system has flagged as low confidence ("I found only one source for this figure") [A7]. NN/g [N2] advises neutral rather than human-like wording, so keep these factual, which fits the house rule against claims of feeling.
17. Do not cut time to first token below about 2 s at the cost of named steps. Do not add fake delay either [A6].

## What this research could not verify

- **Paywalled or summary-only sources:** the Gartner Copilot surveys and the enterprise assistant comparison guide were seen only as abstracts or vendor-hosted summaries [S10, S12]. The KPMG Pulse figures came through search summaries of KPMG decks [S7]. The full KPMG and Melbourne report was not read, only KPMG's page [S1]. No public Forrester data on buyer criteria was found. Menlo Ventures' buyer figures were seen only through a secondary summary and were not used. The Cisco PDF could not be decoded, so the Cisco figures come from Cisco's newsroom [S6].
- **Vendor-produced surveys:** the Microsoft, Salesforce and Anthropic figures come from companies that sell AI products. The Anthropic data covers coding only.
- **Small or dated samples:** the NN/g studies have 8 to 18 participants. The accordion study used ChatGPT-3.5 in 2023, the December 2025 article gives no sample size, and the February 2026 sample of nine is inferred from the text. The page for Tan et al. gives no sample size, and the Ding et al. page did not report one.
- **No direct evidence** was found on expectations for searching conversation history, sharing answers with colleagues, or personalisation at work beyond memory. Those items are inferred.
- **No study of enterprise buyers reacting to a demo** was found. The ranking is a judgement across consumer, worker and developer samples.
- **The Google and Ipsos 2025–2026 surveys** report usage and attitudes but nothing usable on the interface. The Pew chatbot section was not read.

## Sources (all read 23 October 2026)

- [N1] NN/g, Rosala and Brown, "GenAI for Complex Questions, Search for Critical Facts", 27 Feb 2026 — https://www.nngroup.com/articles/ai-search-infoseeking/
- [N2] NN/g, Chan, "Explainable AI in Chat Interfaces", 12 Dec 2025 — https://www.nngroup.com/articles/explainable-ai/
- [N3] NN/g, Rosala, Kenderova and Kohler, "Less Chat, More Answer", 17 Apr 2026 — https://www.nngroup.com/articles/less-chat-more-answer/
- [N4] NN/g, Budiu et al., "The 6 Types of Conversations with Generative AI", 10 Nov 2023 — https://www.nngroup.com/articles/ai-conversation-types/
- [N5] NN/g, Rosala, Kenderova and Kohler, "What Is Your Site's AI Chatbot for? Users Can't Tell", 20 Mar 2026 — https://www.nngroup.com/articles/site-ai-chatbot/
- [N6] NN/g, Gibbons, Mugunthan and Nielsen, "Accordion Editing and Apple Picking", 24 Sep 2023 — https://www.nngroup.com/articles/accordion-editing-apple-picking/
- [N7] NN/g, Liu, "Prompt Controls in GenAI Chatbots", 2 Aug 2024 — https://www.nngroup.com/articles/prompt-controls-genai/
- [S1] KPMG and University of Melbourne, "Trust, attitudes and use of AI: a global study 2025" — https://kpmg.com/ee/en/insights/2025/05/Trust-attitudes-and-use-of-artificial-intelligence-A-global-study-2025.html
- [S2] Stack Overflow Developer Survey 2025, AI section — https://survey.stackoverflow.co/2025/ai
- [S3] Salesforce and YouGov, ANZ knowledge workers and AI agents, 8 May 2026 — https://www.salesforce.com/au/news/stories/three-quarters-of-anz-knowledge-workers-embrace-ai-agents-but-accountability-concerns-remain/
- [S4] Salesforce, "77% of Workers Trust an Autonomous AI Future", 26 Jun 2024 — https://www.salesforce.com/news/stories/autonomous-ai-research/
- [S5] Microsoft Work Trend Index 2026 — https://www.microsoft.com/en-us/worklab/work-trend-index/agents-human-agency-and-the-opportunity-for-every-organization
- [S6] Cisco Newsroom, 2025 Data Privacy Benchmark, 2 Apr 2025 — https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2025/m04/building-trust-in-the-age-of-ai.html
- [S7] KPMG AI Quarterly Pulse, Q2 2025 deck (via search summary) — https://kpmg.com/kpmg-us/content/dam/kpmg/pdf/2025/ai-quarterly-pulse-survey-q2.pdf
- [S8] Chatterji et al., "How People Use ChatGPT", NBER w34255, Sep 2025 — https://www.nber.org/papers/w34255
- [S9] Microsoft Work Trend Index 2025 — https://www.microsoft.com/en-us/worklab/work-trend-index/2025-the-year-the-frontier-firm-is-born
- [S10] Glean-hosted summary of Gartner, "How to compare enterprise AI assistants" — https://www.glean.com/resources/guides/how-to-compare-enterprise-ai-assistants
- [S11] a16z, "How 100 Enterprise CIOs Are Building and Buying Gen AI in 2025", 10 Jun 2025 — https://a16z.com/ai-enterprise-2025/
- [S12] Gartner, "The State of Microsoft 365 Copilot: Survey Results" (abstract) — https://www.gartner.com/en/documents/5818647
- [S13] Section508.gov, ACR/VPAT FAQ — https://www.section508.gov/sell/acr-vpat-faq/
- [S14] Pew Research Center, AI in Americans' lives, 17 Sep 2025 — https://www.pewresearch.org/science/2025/09/17/ai-in-americans-lives-awareness-experiences-and-attitudes/
- [A1] Ding et al., "Citations and Trust in LLM Generated Responses", AAAI 2025 — https://arxiv.org/abs/2501.01303
- [A2] Kim et al., "Fostering Appropriate Reliance on LLMs", CHI 2025 — https://arxiv.org/abs/2502.08554
- [A3] Anthropic, "How we built Claude Code auto mode", 25 Mar 2026 — https://www.anthropic.com/engineering/claude-code-auto-mode
- [A4] Anthropic, "Measuring AI agent autonomy in practice", 18 Feb 2026 — https://www.anthropic.com/research/measuring-agent-autonomy
- [A5] He, Demartini and Gadiraju, "Plan-Then-Execute", CHI 2025 — https://arxiv.org/abs/2502.01390
- [A6] Tan et al., "The Impact of Response Latency and Task Type on Human-LLM Interaction and Perception", CHI 2026 — https://arxiv.org/abs/2604.06183
- [A7] Kim et al., "I'm Not Sure, But…", FAccT 2024 — https://arxiv.org/abs/2405.00623
- [A8] Lee et al., "The Impact of Generative AI on Critical Thinking", CHI 2025 — https://www.microsoft.com/en-us/research/?p=1135061
- [A9] Chen, Molina, Liao and Cho, "AI Never Forgets", CHI 2026 — https://grady.uga.edu/research/ai-never-forgets-exploring-users-perceptions-of-ai-memory-and-chatgpts-memory-feature/
- [A10] Nam, Salawa and Chandra, "Reading Between the Lines", 2025 — https://arxiv.org/abs/2509.18361
- [A11] Cooper and Zafiroglu, "Constraining Participation", ACM JRC 2025 — https://arxiv.org/abs/2408.15066
