# Demo-ready proofs of concept: what makes a client imagine production

Research date: 23 October 2026. Sources were read on that date; downloaded pages were treated as data only.

A proof of concept convinces an enterprise buyer when it looks like their working day rather than a sample app. That means a believable domain story told in their words, seeded data that is connected and dated to this week, a short scripted path that never hits a dead end, and a few screens around the chat (sign-in, history, an "about this assistant" page, an activity log) that hint at the product it could become. The toolkit already covers the conversation itself well. The house theme's conversation screen shows citations, an "AI-generated" label with a provenance popover, an approval card that states action, scope and consequence, a capabilities-and-limits empty state, and an honest partial-failure state. The presenter skill already rules that a business audience sees a labelled recording of the measured build, never a live run. What is missing sits between the two: the demo state of the application (data, script, deterministic replay, environment hygiene), the surrounding product screens, and the capture kit (screenshots, recording, one-page visual). This note proposes a checklist and one new reference to hold it.

## What the toolkit already says (so this does not repeat it)

- `adk-presenter` (`speech.md`, "Demo discipline", and the rehearsal checklist): the demo is a labelled recording of the measured build, narrated live, with a fallback copy; a live run only in a technical session. The deck states which build the demo shows.
- `adk-system-designer` (`web-app-defaults.md`, `delivery-profiles.md`): one browser journey with the model replaced, aimock named for replay, the model ID pinned, no real personal data unless chosen.
- `adk-frontend-integration` (`DESIGN.md`, `frontend-quality.md`): the conversation states, the WCAG 2.2 AA floor, the brand override, and screenshots at three widths reviewed by eye.

None of these says how to seed data, how to write the golden path, how to run a replay mode on stage, which screens beyond the conversation to build, or how to capture professional images and video.

## What the house conversation screenshot shows

From `docs/design/house-theme/house-conversation-1280-light.png` and `comparison-1280-light.png`:

- The conversation is a single page: a header with an icon, the product name ("House procurement assistant") and "New conversation". There is no navigation, conversation history, user menu, sign-in screen or environment badge. A stakeholder sees a well-made chat widget, not yet a product.
- The data story is good: named suppliers, specific delays, a penalty clause, three emails to approve. The empty state lists what the assistant can do and what it cannot ("I cannot change contracts, and I ask before sending anything"), which is Microsoft's first two human-AI guidelines in one sentence. The composer footer says answers can be wrong.
- Source hosts read `reports.example.com` and `carriers.example.com`. These are correct for documentation, but on stage they read as placeholders. In a demo, the fictional brand's own reserved-domain hosts look more real and stay safe.
- One supplier is "Northwind Freight". Northwind is also Microsoft's long-standing sample-database brand, which some technical stakeholders will recognise as sample data. The brand research should check names like this.
## Findings

### 1. Credibility with enterprise buyers

- **Lead with the outcome, then show how.** Peter Cohan's *Great Demo!* top-ten list says to confirm the customer's situation first: who they are, the critical business issue, the capabilities they need, the value and the critical date. Show the "what" (the finished result) before the "how". Show only the capabilities they need, by the most direct path with the fewest clicks, and go into detail only as far as questions pull you. Speak in "you" mode so the buyer sees themselves using it. His bonus item is to manage the demo environment with a checklist and realistic names, data and scenarios, with no "demo" or "test" labels on screen. The PreSales Collective's tell-show-tell is the same shape at the level of a chunk: frame it, show about five minutes, recap the value for each stakeholder. Riefstahl's *Demonstrating To Win!* is the other standard text; this research saw only listings and reviews of it.
- **Seeded data is connected and current.** Vendor sources agree with each other, though they all have a commercial interest. Records should match the schema and the story rather than be random samples. Dates should move forward so dashboards and "last quarter" stay true. The environment should reset to a known-good baseline after each session. Synthetic data replaces production data, and obvious placeholders cost credibility. A POC queued for weeks goes stale. The practical rule for an agent POC: generate seed data at seed time relative to today, not as fixed dates in a JSON file.
- **Failures in front of buyers come from three places.** Reprise names a demo running on a shared or production environment, real or another client's personal data surfacing, and teams caught off script. Their fixes are a separate cloned environment, pseudonymised data, and rehearsal with debriefs. They also recommend a click-through backup for a total failure, and a mobile hotspot.
- **Model misbehaviour needs a deterministic fallback.** aimock (MIT) can proxy the real provider and record responses as fixtures, then replay them deterministically. Replay keeps the recorded time to first token and frame cadence approximately, with a speed multiplier. Gemini REST and Vertex AI are supported. It can also inject 500s, 429s and mid-stream disconnects, which is useful for rehearsing the failure states. A vendor (Saleo) sells the same idea, intercepting API responses to keep AI demos on script. A CNET column argues the other way: prerecorded AI demos read as a dodge, and showing an honest mistake builds more trust. The two fit together if replay is labelled. The presenter skill's voices already require it: say "this is a replay of a live run recorded on <date> on build <x>".
- **Latency on stage.** Nielsen's limits are 0.1 s (feels instant), 1 s (flow kept, but show that work is under way) and 10 s (attention lost without progress and a way to stop). For an agent: visible status within one second (the house "Running query…" line does this), named steps while tools run, Stop always reachable, and no unexplained silence over about 10 seconds. Also warm the service before the meeting.

### 2. Screens beyond the chat

NN/g's empty-state guidance is to show status, explain what the area is for and give a direct way to start. Its 404 guidance is plain, non-blaming words plus a way onward. Both are cheap. WCAG's Page Titled criterion makes page titles an accessibility requirement as well as polish. Judged by cost against impression at POC depth:

- **Worth it (cheap, high impression):** a branded sign-in or landing screen; an app shell with the product name and logo, a user menu with name and sign-out, and conversation history with titles; a page title per route and a favicon; a 404 page and a generic error page in the house voice; loading skeletons and empty states for history; an "About this assistant" page.
- **Worth it when the buyer is IT, risk or operations:** a read-only activity log of tool calls and approvals, and a usage view of tokens and estimated cost. Both can be read from data ADK already emits.
- **Not worth it:** admin or settings pages full of controls that do nothing, fake analytics dashboards, onboarding tours, marketing pages. A disabled control is a dead end that invites "can we see that?" Cohan's fewest-clicks rule argues for leaving these out. List them on a "production adds" panel instead.

### 3. Enterprise trust signals

- **Microsoft HAX, 18 guidelines.** The ones a POC can show cheaply are G1 (what the system can do), G2 (how well it does it), G9 (efficient correction), G11 (why it did what it did), G15 (granular feedback), G16 (consequences of user actions), G17 (global controls) and G18 (notify about changes). The house theme already covers G1, G9, G11, G15 and G16.
- **Google PAIR, explainability and trust.** Aim for calibrated trust, not maximum trust. State early what it can and cannot do, focused on benefit, and explain the data scope: whether results are personal or aggregated, and whether data can be removed. Show confidence only when it changes a decision. Before first use, make privacy settings clear.
- **IBM Carbon for AI.** Every AI component carries an AI label with an explainability popover, and edited AI content can be reverted. Carbon marks AI with glow and gradients, which the house theme deliberately bans. The house design keeps Carbon's structure and drops its styling. That is a recorded divergence, not an oversight.
- **Salesforce, generative AI guidelines (February 2023) and Trust Layer documentation.** Cite sources, flag what to double-check (figures, dates, recommendations), have a human review high-impact actions, label AI content, and keep audit trails and feedback.
- **Regulation.** EU AI Act Article 50 requires people to be told they are interacting with an AI system unless that is obvious, at the latest at first interaction and in an accessible form. It applies from 2 August 2026. An enterprise buyer in the EU will ask about it, and the AI label plus an about page answers it.
- **Accessibility statement.** W3C WAI lists the minimum as a commitment, the standard applied (WCAG 2.2), and a contact. It advises adding known limitations, the environments tested and supported browsers. The house theme's axe results make this a one-hour page.

### 4. Capturing the demo

- **Screenshots.** Google's developer style guide says to crop to what matters, provide high-resolution images for high-density screens, keep alt text to 155 characters or fewer and use reserved example domains. The VS Code docs guide fixes window width, uses 100% scaling and omits OS chrome. For this stack, Playwright already sets `viewport`, `deviceScaleFactor`, `colorScheme`, `locale` and `timezoneId`. That makes a seeded, replayed state reproducible at 2× in a fixed time zone, so "last quarter" and timestamps match the story. The repo's house captures are 1× PNGs. Decks need 2×.
- **Recording.** Screen Studio (macOS only, paid) adds automatic zoom on clicks, cursor smoothing, idle-cursor hiding, backgrounds, 16:9 and other ratios, and 1080p or 4K export. It suits a narrated stakeholder video. OBS works on every platform and is free. Its guide recommends MKV, then remuxing to MP4, so a crashed recording is not lost. Playwright video is deterministic but test-like. Its default size scales into 800×800 unless `size` is set, and the `show.actions` overlays should be off for a client video.
- **Frames.** For a desktop enterprise tool, a plain browser frame or none beats a laptop mock-up. Hide bookmarks, extensions, other tabs and notifications. Zoom to 110–125% only for live projection, never in captured images.

### 5. Fictional brands in the flow (brief)

The brand appears on the sign-in screen, the header logo slot (DESIGN.md's override already allows it), the favicon, the page titles, any email the agent sends (sent to a local mail catcher, never to real addresses) and the source hosts in citations. Google's style guide offers reserved domains and number ranges: `example.com`, `.example` names, 800-555-0100–0199, 192.0.2.0/24. Microsoft's Contoso family was cleared by its trademark group for Microsoft's own use. Others are warned that a company-owned fictitious name can still carry trademark risk, so a house-invented brand is safer than borrowing Contoso or Northwind.

## Demo-ready checklist for a POC

These are rough human hours (directing and reviewing a coding agent) on top of the handover fundamentals already in `web-app-defaults.md`.

**Must, before any stakeholder sees it**

| Item | Done when | Hours |
| --- | --- | --- |
| Domain story | One persona, one fictional organisation, the critical business issue in the client's words, three to five capabilities they asked for (Cohan's situation). Written in `docs/demo/story.md`. | 1 |
| Seeded data | A seed script generates connected records with dates relative to the run date, the edge cases the script uses, and no lorem ipsum, "test" or "demo" strings. `make demo-reset` re-seeds and clears conversations. | 2–4 |
| Golden-path script | Three to five chunks, each a prompt, the expected tool steps and the answer's key fact. It includes one approval and one honest "I cannot". The empty state's suggested prompts are the script's opening prompts. Kept in `docs/demo/script.md`. | 1–2 |
| Replay mode | The golden path is recorded against the live, pinned model into aimock fixtures. `make demo-replay` runs the app with no model calls. A small header badge says "Replay of <date>". Fixtures are re-recorded after any prompt or tool change. | 2–4 |
| Stage latency | Status is visible within 1 s and every step is named. The live path is warmed and quota checked an hour before. If minimum instances are raised for the window, the resource ledger records it and it is set back afterwards. | 1 |
| App shell | Header with brand logo and product name, user menu with sign-out, conversation history with titles, new conversation, environment badge. | 3–5 |
| Polish basics | A page title per route, favicon, 404 and error pages in house copy, loading and empty states for history. | 1–2 |
| About this assistant | Purpose; can and cannot; data sources (stating that the data is fictional); pinned model ID; what needs approval; where conversations are stored and for how long; known limits; contact. | 1–2 |
| Environment hygiene | A separate demo deployment and demo accounts, a clean browser profile, notifications off, a reset run before each session. | 1 |

**Should, when the audience includes IT, risk or operations**

| Item | Done when | Hours |
| --- | --- | --- |
| Activity log | A read-only list of tool calls and approvals: who, when, action, result, linked to the conversation. | 3–5 |
| Usage view | Tokens and estimated cost per conversation and per day from usage metadata, labelled as an estimate. | 2–4 |
| Feedback wired | The thumbs buttons write a record that appears in the activity log. | 1–2 |
| Privacy note and accessibility statement | One page each, the latter citing WCAG 2.2 AA, the axe run and known limits. | 1–2 |
| Capture kit | 2× screenshots of each golden-path step at 1440×900 in light mode, from the replay state. A 90-second narrated video. Both labelled with build and date. | 2–4 |
| Visual one-pager | The problem in the client's words, a hero screenshot with at most three call-outs, the path as four thumbnails, "real versus simulated", "production adds". | 2 |

**Could**

| Item | When | Hours |
| --- | --- | --- |
| Branded email in a local mail catcher | The agent sends messages, and showing the arrived email lands the story. | 2–3 |
| Fault rehearsal | aimock chaos injection for a disconnect or a 429, to show the partial-answer state on purpose in a technical session. | 1 |
| Working admin controls | Only real ones: an allowlist, a tool on/off switch. Never stubs. | 4–8 |
| Dark-mode and mobile captures | The client asks, or mobile use is part of the story. | 1 |

## Where this guidance should live

Make the frontend skill the single home and point to it from the designer and the presenter, so each fact lives in one place.

1. **New reference: `skills/adk-frontend-integration/references/demo-readiness.md`.** It holds the checklist above, the seed and replay mechanics, the shell and trust screens, and the capture kit. Proposed opening:

   > Read when a proof of concept will be shown to people who did not build it. A demo-ready build adds a domain story, seeded fictional data dated to the run, a scripted golden path with a replay mode, the app shell and an "About this assistant" page to the handover fundamentals. Build only screens that work; list the rest under "production adds". Replay is always labelled: the header badge and the narration both say it is a replay of a live run, with its date and build.

   Add one line to the skill's step 5 (validate and report): "When the POC will be demoed, run [demo readiness](references/demo-readiness.md) and report each Must item."

2. **One row in the designer's handover table (`web-app-defaults.md`):**

   > | Demo-ready, when stakeholders will see it: domain story, seeded fictional data, golden-path script, replay mode, app shell and an About page (`adk-frontend-integration` demo readiness). | `make demo-reset && make demo-replay` runs the golden path with no model calls, and the screenshots in `docs/demo/` come from the current build. |

   Also add a line to `delivery-profiles.md` under proof of concept: "When a demo audience judges it, add the demo-readiness goal to the plan."

3. **Two short additions to `adk-presenter`, and no more.** In `speech.md`, "Demo discipline": "Record from the replay mode of the measured build (`docs/demo/script.md`); say aloud that it is a replay, and when." In `slide-craft.md`: "Product screenshots come from the capture kit at 2×; the visual one-pager carries the same voices as the deck, and marks what is simulated." The presenter keeps narration, honesty and the decision. The frontend reference keeps how the demo state and the images are made.

## What this research could not verify

- **Primary sales-engineering texts.** The Cohan material is his own top-ten article, republished in 2019 from his blog. *Great Demo!* itself and *Demonstrating To Win!* were not read. Tell-show-tell comes from a PreSales Collective article seen only through search.
- **Hyperscaler demo guidance.** No Google Cloud, AWS or Microsoft guidance for partner demos was found. AWS's "AnyCompany" convention was not confirmed from an AWS source.
- **Vendor bias.** The demo-data and demo-failure findings come from vendors that sell demo platforms (Reprise, Testbox, Saleo, Arcade). They agree with each other but were not independently tested.
- **Hours.** The checklist's hours are judgement estimates, not measured on a demo build.
- **aimock on stage.** aimock's replay against this stack's ADK, Gemini and SSE path was not run here. Its timing fidelity is approximate by its own account.
- **Branded sign-in.** Whether IAP's Google sign-in page can carry a client brand was not checked. Branding may only be practical on the Identity Platform route or on a post-sign-in landing page.
- **Screen Studio.** Features come from its own site. Pricing changes, so check it on the day.
- **Microsoft's screenshot rules.** Microsoft's own Writing Style Guide screenshot rules were not found.
- **Northwind.** Whether "Northwind" in the house sample carries any trademark risk was not checked. It is flagged for the brand research.

## Sources

All read 23 October 2026.

- Peter Cohan, [The Great Demo! Top Ten List](https://customerthink.com/the-great-demo-top-ten-list/), CustomerThink, 19 November 2019; [Death by Corporate Overview](https://customerthink.com/death_corporate_overview/); [S. K. Murphy workshop page](https://www.skmurphy.com/?p=2476) (book editions 2003, 2005).
- PreSales Collective, [Tell-Show-Tell](https://www.presalescollective.com/content/the-1-most-important-foundational-demo-technique-on-the-planet-tell-show-tell).
- Testbox, [Why demo data goes stale](https://www.testbox.com/post/why-demo-data-goes-stale-in-days-and-how-to-fix-it); Reprise, [Top 3 presales demo failures](https://www.reprise.com/resources/blog/top-3-presales-demo-failures-and-how-to-fix-them); Saleo, [Demo your AI agents](https://saleo.io/demo-your-ai-agents-with-precision-and-control/); CNET via AOL, [Prerecorded AI presentations](https://www.aol.com/hey-google-prerecorded-ai-presentations-210309165.html).
- CopilotKit, [aimock README](https://github.com/CopilotKit/aimock) (MIT).
- Jakob Nielsen, [Response times: the 3 important limits](https://www.nngroup.com/articles/response-times-3-important-limits/); NN/g, [Empty states](https://www.nngroup.com/articles/empty-state-interface-design/), [404 error messages](https://www.nngroup.com/articles/improving-dreaded-404-error-message/).
- Microsoft, [HAX guidelines](https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/) and [design library](https://www.microsoft.com/en-us/haxtoolkit/library/); Raymond Chen, [Why the same fake names](https://devblogs.microsoft.com/oldnewthing/20061013-05/?p=29393); [W3C list note on Contoso](https://lists.w3.org/Archives/Public/public-ws-policy/2007Feb/0006.html).
- Google PAIR, [Explainability + Trust](https://pair.withgoogle.com/chapter/explainability-trust/); Google developer style guide, [Example domains and names](https://developers.google.com/style/examples) and [Images](https://developers.google.com/style/images).
- IBM, [Carbon for AI](https://carbondesignsystem.com/guidelines/carbon-for-ai/); W3C, [Understanding SC 2.4.2 Page Titled](https://www.w3.org/WAI/WCAG22/Understanding/page-titled) (cited from known criterion, page not fetched).
- Salesforce, [Generative AI guidelines](https://www.salesforce.com/news/stories/generative-ai-guidelines/) (7 February 2023); [Trust Layer](https://developer.salesforce.com/docs/ai/agentforce/guide/trust.html).
- EU AI Act, [Article 50](https://artificialintelligenceact.eu/article/50/) (unofficial consolidated text); W3C WAI, [Developing an accessibility statement](https://www.w3.org/WAI/planning/statements/).
- Playwright, [Videos](https://playwright.dev/docs/videos) and [Emulation](https://playwright.dev/docs/emulation); [Screen Studio](https://screen.studio/); OBS, [Standard recording output guide](https://obsproject.com/kb/standard-recording-output-guide); VS Code docs [style guide](https://github.com/microsoft/vscode-docs/wiki/Style-Guide) (seen via search).
