# What makes AI product interfaces look premium, and what the house theme should change

The best AI and enterprise products of 2025–2026 do not look premium because of decoration. They look premium because **the product has a shape**, **the chrome is calm while the content is loud**, and **the agent's work becomes objects people can handle**. On shape: a quiet sidebar of past work, a composer that is clearly the main object on the screen, and a side panel for whatever is being made or checked. On calm chrome: few borders, a dimmed sidebar, one accent kept for rare moments. On objects: sources as chips with previews, steps folded into one honest summary line, approvals as decision cards that show exactly what will happen. Linear's 2026 refresh puts the principle in two lines: don't compete for attention you haven't earned, and structure should be felt rather than seen. The house theme already gets the hard parts right: accessible tokens, an editorial serif for answers, status in words, an honest approval and error model. It is "tidy rather than memorable" because it has no app shell, it wraps every secondary element in a hairline box, its composer is a form field, and its sources and steps are lists of text rather than objects. Fix those four things and keep the tokens: that is what moves a client from "clean" to "I can see this in production".

Everything here was read on 23 October 2026. The source list is at the end. Statements about how specific products look come from product use up to mid-2026 unless a source is cited. This research did not capture live screenshots of them (see the last section).

## 1. Fifteen transferable patterns

1. **A real app shell with a quiet sidebar.** *Seen in:* Claude, ChatGPT, Gemini and Gemini Enterprise (conversation list plus an Agents entry), Microsoft 365 Copilot (a collapsible navigation pane, pinning and session recall [M2]), and Linear (its 2026 refresh dimmed the sidebars so the work area wins [L2, L3]). *Why it reads as premium:* history and navigation say "this is a product people live in", not a demo page. *Apply:* use the shadcn `Sidebar` with `collapsible="icon"` (block sidebar-07) or the inset variant (sidebar-08) [S1]. Put New conversation at the top and conversations under date groups (Today, Previous 7 days), as 32 px rows with titles truncated. The workspace or client logo and the user go in the footer. No borders between items; the `sidebar` surface stays one step darker than the canvas.

2. **An empty state built around the composer.** *Seen in:* Claude, ChatGPT and Gemini all centre a greeting and the composer on a new conversation, with suggestions next to it. *Why:* the first screen a client sees is a confident invitation rather than a blank thread. *Apply:* put a serif `display` line ("Procurement assistant" or "Good afternoon, Priya") at about 38% of the viewport height, with the composer directly under it. Suggestions go below as a 2 × 2 grid of small cards (icon, prompt, one muted line). After the first send, the composer moves to the bottom.

3. **The composer as the hero object.** *Seen in:* Microsoft turned the prompt line into a "task-aware workspace", with room for longer requests and tools beneath it [M2]. Claude and ChatGPT use a raised, rounder, two-row composer with a tool row. *Why:* it is the one control used every turn, so craft there is noticed every turn. *Apply:* build it as a card surface with a textarea at least 56 px tall and a toolbar row underneath. The toolbar holds ghost icon buttons on the left (Attach, Sources or connectors) and a 32 px primary icon Send on the right, which Stop replaces while a run is going. Use a 12 px radius and the floating shadow. Cmd/Ctrl+Enter or Enter to send, as the Vercel guidelines describe for textareas [V1].

4. **Calm chrome, loud content.** *Seen in:* Linear ("don't compete for attention you haven't earned"; fewer, softer separators; smaller and fewer icons [L2]) and Microsoft's "clarity and calm" [M1]. Refactoring UI says to use fewer borders and to group with space or a background change instead [R1]. *Why:* when every region is boxed, the eye has nowhere to rest, and the screen looks like a form. *Apply:* draw a hairline only between major regions (sidebar, header, side panel). Inside the thread, use space (24 to 32 px between turns) and surface steps.

5. **Editorial answer typography.** *Seen in:* Claude sets answers in a serif. Microsoft calls output quality, meaning tone, structure and readability, "the core experience" [M2]. Refactoring UI asks for a limited line length and a type scale [R1]. *Why:* the answer is the product, and well-set prose reads as considered. *Apply:* keep `answer-md` (17/28 serif, 68ch). Add prose rules for headings, lists, tables and code inside answers. Use `text-wrap: pretty`, curly quotes and the ellipsis character [V1].

6. **Work shown, but folded.** *Seen in:* Perplexity's collapsible research steps ("Completed 2 steps", per a third-party teardown [P3]) and Claude's collapsed tool and thinking rows. Granola's agent post says to expose the steps *and* how much was reviewed [G2]. *Why:* the steps prove diligence without burying the answer. *Apply:* once the answer starts, collapse a finished Trace into one summary line: "Worked for 4 s · 3 steps · 1 failed · searched 42 contracts". Expanding it shows the current TraceLines.

7. **Sources as objects.** *Seen in:* Perplexity's numbered citations on every answer [P1, P2], Claude's linked citations with excerpts [C2], and AI Elements' inline citation: a badge with the host name that opens a card showing title, URL, description and quote, with a "1/5" stepper [S3]. *Why:* a chip with an icon and a domain looks like evidence, and a link list looks like a footnote. *Apply:* render each citation as a small `rounded-sm` chip in `muted` holding a number or host name, with a `HoverCard` preview (Popover on touch). Below the answer goes one row of source chips (document-type icon or favicon, title, host). "View all" opens the side panel.

8. **A side panel for what is being made or checked.** *Seen in:* Claude Artifacts, a separate window beside the chat [C1]; ChatGPT canvas; and Microsoft's dynamic windowing, where chat sits beside the document [M1, M2]. *Why:* real work (drafts, tables, sources) needs more than a chat column, and the split screen is what enterprise buyers picture. *Apply:* a resizable right panel (shadcn `Resizable`, 360–480 px) with tabs for Sources, Drafts and Data. Below 1024 px it becomes a `Sheet`. Keep its open state in the URL [V1].

9. **Approvals as decision cards with a preview.** *Seen in:* AI Elements Confirmation (requested, accepted and rejected states [S4]) and the confirmation steps in Gemini Enterprise and ChatGPT agent mode. *Why:* a well-structured card says the system is safe to let loose. *Apply:* the header row has a Lucide icon, the title "Send 3 emails" and a "Waiting for approval" badge on the warning surface. Under it, a two-column definition list with muted labels (Action, Affects, Consequence), then a collapsible "Preview emails". The footer has Deny (outline) and Approve (primary), aligned right. After the decision it collapses to a Trace line, as now.

10. **Human and AI output told apart.** *Seen in:* Granola (the person's text in black, everything else in grey, and "Zoom In" to the transcript quotes behind a note [G1]). *Why:* clear provenance looks like an enterprise feature, not a disclaimer. *Apply:* keep the sans user bubble against the serif answer and the "AI-generated" label. Add "where this came from" links from claims to sources.

11. **Tinted semantic surfaces on a disciplined ramp.** *Seen in:* Stripe's perceptual colour levels, where any two steps far enough apart pass contrast, and badges shift background and text together [ST1]. Vercel Geist gives every colour ten steps by role: 100–300 backgrounds, 400–600 borders, 700–800 solid fills, 900–1000 text [V2]. Linear generates themes in LCH from base, accent and contrast [L1]. *Why:* status on grey reads drab, while a faint tint with a dark same-hue label reads designed. *Apply:* add `success-subtle`, `warning-subtle`, `destructive-subtle` and `info-subtle` surfaces (L about 0.96, chroma about 0.02–0.03, same hue), each with its existing text colour, and lint the pairs.

12. **Fast, purposeful motion.** *Seen in:* Emil Kowalski: under 300 ms, ease-out, popovers opening from their trigger, never animating from `scale(0)`, no motion on actions repeated all day [E1, E2]. Rauno Freiberg: fast keyboard and mouse actions can skip animation, and feedback belongs near the trigger [RF1, RF2]. Vercel: animate only transform and opacity, never `transition: all` [V1]. Granola: animating height cost real CPU [G3]. *Apply:* new turns enter with opacity and a 4 px rise over 150 ms. Popovers use the Base UI transform-origin variable. Text that is streaming in gets no fade per token. Sidebar and panel toggles are instant or 150 ms.

13. **Loading states that keep their shape.** *Seen in:* the Vercel guidelines: wait 150–300 ms before showing a loader, then keep it up for 300–500 ms, and make skeletons match the final layout [V1]. *Apply:* skeleton rows for the conversation list and for restoring a session. The status line in the thread keeps its shimmer.

14. **Small details that add up.** *Seen in:* the Vercel guidelines (nested radii, optical alignment, balanced icon and text pairs, layered shadows on floating layers [V1]) and Linear's alignment pass, "felt after a few minutes" [L1]. *Apply:* a chip inside the composer gets the composer's radius minus its padding, and Lucide strokes match the text weight.

15. **Honest endings with next steps.** *Seen in:* Granola (mark partial answers, offer "go further" or "open sources" [G2]) and Microsoft's layered output [M2]. *Apply:* two or three follow-up chips after a finished answer.

## 2. Critique of the current screens

**Conversation screen** (`house-conversation-1280-light.png`, `-375-dark.png`):

- *Keep:* the serif answers, status in words with timings on Trace lines, the approval content, the partial answer kept with Retry, the "AI-generated" label, the warm canvas, the ink-blue accent and the dark mode.
- *No shell.* A logo tile, a product name and a "New conversation" outline button make it read as a demo page. There is no conversation history, title, user or workspace, and no panel toggle.
- *The empty state sits beside a full thread* at 1280 px. It serves as a specimen, but a client sees two states at once. Show it as its own screen.
- *Box soup.* Sources, the error notice, the approval card and the composer are all hairline boxes of similar weight. Nothing is clearly most important.
- *The composer is a form field:* one 1 px rectangle, a greyed square Stop and a hairline above it that spans the column. Nothing marks it as the main object.
- *Steps sit open above the answer:* four lines (thought, ran, searched, failed) before the first sentence, every turn.
- *Sources are a text list* with underlined links in a box. Citation markers are bracketed superscripts in blue, which work but read academic rather than product.
- *The approval card's bold "Action:" and "Affects:"* labels read like a form printout. The buttons float to the right of the text at desktop width, with no header or status.
- *The accent appears only on the logo tile, links and Approve.* That restraint is right, but the screen has no single designed "moment".
- *At 375 px*, the header wraps the product name onto two lines next to a large button.

**Design-system page** (`house-design-system-1280-light.png`): an accurate specification sheet (roles, type scale, buttons, inputs), but it shows parts, not products. It has no app shell, conversation patterns, source chips, approval card, empty state, loading state or motion, so it cannot sell the system to a client. The colour section shows a few filled tiles rather than the ramp and its roles, and the "Disabled" button's washed blue is the weakest swatch on the page.

## 3. Prioritised changes

**Must**

1. **App shell:** shadcn `Sidebar` (icon-collapsible) with New conversation, date-grouped history and a workspace and user footer. The header shows the conversation title (editable), the agent name and a panel toggle. Below 768 px the sidebar becomes a `Sheet`, and the header keeps one line: menu, title, new-conversation icon.
2. **Empty state as a separate screen:** a centred serif greeting, the composer directly below it, then 2 × 2 suggestion cards. After the first send the composer docks at the bottom. Drop the "idle state" side card from the conversation screen.
3. **Composer:** a two-row card (textarea, then a tool row with Attach, a sources or connector toggle, and Send/Stop). Remove the hairline that spans the column. The thread scrolls under the composer, with a short fade in the canvas colour behind it. State in DESIGN.md that this fade is not a decorative gradient.
4. **Collapse finished steps:** one summary line per turn, with scope counts, which expands to the TraceLines. Reasoning stays as it is.
5. **Sources as chips:** inline numbered chips with a hover-card preview (title, host, date, quote), a row of source chips after the answer, and "View all sources" opening the side panel. Keep the "Source 1: title" accessible names and the deduplication.
6. **Fewer boxes:** the sources row and the error notice lose their outer boxes. The approval card is the only bordered card in the thread.
7. **Demo realism:** a seeded history of six to ten plausible conversations, a client logo slot, real-looking source titles and dates (the procurement data is already good).

**Should**

1. **Radius:** add `rounded.xl: 12px` for the composer, side panel, sheets and dialogs only, which matches Geist's 12 px for raised and menu materials [V3]. Controls stay at 6 px, and there are still no pills.
2. **Elevation:** add the composer to the list of floating layers that get the one shadow. Optionally use a two-layer shadow with a slightly stronger close layer [V1, R1].
3. **Subtle semantic surfaces:** `*-subtle` tokens plus their `dark-` twins, used by status badges, the waiting-for-approval badge and the incomplete-answer notice. Recompute the contrast table.
4. **Approval card layout:** a header with icon, title and status badge; a definition list; "Preview emails" behind a collapsible; footer actions; a 3 px left border in `warning` while pending.
5. **Side panel component:** resizable, with tabs for Sources, Drafts and Data, and the open state kept in the URL.
6. **Prose rules for answers:** h3 and h4 in sans 600, list spacing, tables in `data-md` with hairline rows, code blocks with a copy button, `text-wrap: pretty`.
7. **Icon rules:** Lucide at 16 px in controls, 14 px in Trace lines and chips. Choose one stroke width (1.5 or 1.75) to match Inter at 400–500 and set it globally. Use fewer icons in navigation [L2].
8. **Motion additions:** turn enter at 150 ms (opacity and a 4 px rise), origin-aware popovers, and no animation on frequent keyboard actions.
9. **Design-system page:** add a "Patterns" section that renders the shell, the empty state, a turn with folded steps and source chips, the approval card, the side panel and skeletons, in light and dark side by side.

**Could**

1. **Follow-up chips** after a finished answer.
2. **Press feedback:** `active:scale-[0.98]` on primary buttons only, which Emil Kowalski recommends [E2]. The house currently forbids it, so decide deliberately.
3. **A signature moment:** the composer's focus state draws its edge in `ring` while focused, or the active conversation in the sidebar carries a 2 px accent bar. Pick one and use it nowhere else.
4. **Keyboard layer:** a Cmd+K command menu for "new conversation", "search conversations" and "toggle sources".
5. **A "Thought for 4 s" style summary for the whole run,** with a duration in tabular figures.

## 4. What to avoid

- Purple-to-blue gradients, glows, glass, sparkles and animated "AI" backgrounds (already house rules). OpenAI's app guidelines also reject custom gradients and brand-tinted backgrounds [O1].
- A bot avatar on every message, typing dots, emoji and chatty greetings ("Hi! I'm your AI assistant").
- Boxes inside boxes, with every region bordered at the same weight.
- Bubbles on both sides, and full-width sans answers.
- Pill-shaped everything and large shadows on static cards.
- Stock shadcn neutral with Geist and the default 10 px radius: the "generic template" look clients recognise.
- Icons whose meaning needs a tooltip, and toolbars crowded with ghost buttons.
- Loaders that flicker on fast responses, skeletons that do not match the final layout, and animated height.
- Errors as toasts only, and sources hidden behind a tooltip.
- Lorem ipsum, "Acme" data or empty history in a client demo.

## 5. What this research could not verify

- **Live product layouts:** no live screenshots of Claude, ChatGPT or ChatGPT Enterprise, Gemini Enterprise, Microsoft 365 Copilot, Glean, Notion AI, Raycast, Dia, Granola, the Stripe dashboard or v0 were captured. Layout statements without a citation come from product use up to mid-2026 and may have changed.
- **OpenAI's own pages:** openai.com and help.openai.com returned HTTP 403, so ChatGPT's sources sidebar and canvas are described from use, not from documentation.
- **Perplexity:** no official design rationale was found. The collapsible steps and source panel come from third-party write-ups [P3].
- **Claude's typefaces:** third-party sites disagree about which typefaces Claude.ai uses, and Anthropic does not document them.
- **Glean and Notion:** the product pages describe "cited" answers but not how citations are drawn [GL1, N1].
- **Gemini Enterprise:** documentation confirms grounded answers with citations and an Agent Gallery [GE1], not the visual treatment.
- **Untested changes:** none of the recommended changes has been prototyped, linted or contrast-checked. The new radius step, the subtle surfaces and the composer shadow need a DESIGN.md lint run and a recomputed contrast table.
- **Untested reaction:** "Clients will find this production-ready" is a judgement, not tested with clients.

## Sources (all read 23 October 2026)

- [V1] Vercel, Web Interface Guidelines — https://vercel.com/design/guidelines
- [V2] Vercel Geist, Colors — https://vercel.com/geist/colors
- [V3] Vercel Geist, Materials — https://vercel.com/geist/materials (and Typography, https://vercel.com/geist/typography)
- [L1] Linear, "How we redesigned the Linear UI (part II)", Karri Saarinen, 28 Mar 2024 — https://linear.app/blog/how-we-redesigned-the-linear-ui
- [L2] Linear, "Behind the latest design refresh", 2026 — https://linear.app/blog/behind-the-latest-design-refresh
- [L3] Linear changelog, UI refresh, 12 Mar 2026 — https://linear.app/changelog/2026-03-12-ui-refresh
- [M1] Microsoft Design, "Designs for the frontier future", Jon Friedman, 30 May 2025 — https://microsoft.design/articles/designs-for-the-frontier-future/
- [M2] Microsoft 365 blog, new design for Microsoft 365 Copilot, Jon Friedman, 28 May 2026 — https://www.microsoft.com/en-us/microsoft-365/blog/?p=281377
- [G1] Granola, "Introducing Granola", Chris Pedregal, 22 May 2024 — https://granola.ai/blog/announcement
- [G2] Granola, "How Granola thinks about designing agents", 6 May 2026 — https://www.granola.ai/blog/how-granola-thinks-about-designing-agents
- [G3] Granola, "Don't animate height!", Jim Fisher, 29 Jan 2025 — https://www.granola.ai/blog/dont-animate-height
- [G4] Granola, "Meet the new look Granola", Sam Stephenson, 2 Feb 2026 — https://www.granola.ai/blog/a-new-look-for-granola
- [ST1] Stripe, "Designing accessible color systems", Koopersmith and Miner, 15 Oct 2019 — https://stripe.com/blog/accessible-color-systems
- [E1] Emil Kowalski, "Great animations" — https://emilkowal.ski/ui/great-animations
- [E2] Emil Kowalski, "7 practical animation tips" — https://emilkowal.ski/ui/7-practical-animation-tips
- [RF1] Rauno Freiberg, "Invisible details of interaction design", Jul 2023 — https://rauno.me/craft/interaction-design
- [RF2] Rauno Freiberg, "Designing depth", Jul 2024, and "Contrasting aesthetics", Jan 2024 — https://rauno.me/craft/depth, https://rauno.me/craft/contrasting-aesthetics
- [R1] Refactoring UI (Wathan and Schoger) — https://www.refactoringui.com/
- [O1] OpenAI Apps SDK design guidelines — https://developers.openai.com/apps-sdk/concepts/design-guidelines
- [C1] Anthropic, Claude 3.5 Sonnet announcement (Artifacts), 21 Jun 2024 — https://www.anthropic.com/news/claude-3-5-sonnet
- [C2] Claude Help Center, web search citations — https://support.claude.com/en/articles/10684626-enabling-and-using-web-search
- [P1] Perplexity Help Center, "How does Perplexity work?" — https://www.perplexity.ai/help-center/en/articles/10352895-how-does-perplexity-work
- [P2] Perplexity, "Getting started with Perplexity", 1 Oct 2024 — https://www.perplexity.ai/hub/blog/getting-started-with-perplexity
- [P3] Third-party Perplexity teardown (secondary; seen as a search-result summary, not opened) — https://aiuxplayground.com/teardowns/perplexity/output
- [S1] shadcn/ui, Sidebar blocks — https://ui.shadcn.com/blocks/sidebar
- [S2] AI Elements component index (the page says AI Elements is moving into shadcn/ui and will be deprecated at the end of November 2026) — https://elements.ai-sdk.dev/
- [S3] AI Elements, Inline citation — https://elements.ai-sdk.dev/components/inline-citation
- [S4] AI Elements, Confirmation — https://elements.ai-sdk.dev/components/confirmation
- [GE1] Gemini Enterprise concepts and Agent Gallery — https://docs.cloud.google.com/gemini/enterprise/docs/concepts, https://docs.cloud.google.com/agentspace/docs/agents-gallery
- [GL1] Glean Assistant product page — https://www.glean.com/product/assistant
- [N1] Notion AI product page — https://www.notion.com/product/ai
