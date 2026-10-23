# Fast-feeling agent demos: answer in one frame, stream calmly, never fight the reader

A proof of concept feels production-grade in a live demo when four things hold. **The person's message and a status line appear in the same frame as Send.** **Tokens arrive in batches of about one per frame, not one render per token.** **The view follows the answer only while the reader is at the bottom.** **The first paint is already in the right theme and font metrics.** Most of this is cheap if the agent knows it before writing code. The house DESIGN.md already fixes the look: durations, easing, the streaming indicator, the `aria-live` log and self-hosted fonts. What the toolkit lacks are behaviour rules that a test can check: scroll-follow, render batching, markdown hardening, no theme flash, IME-safe Enter, Stop focus and lab vitals.

Four findings change existing advice:

- **shadcn now ships a Message Scroller** (`@shadcn/react` 0.3.1). It does the scroll-following that people otherwise hand-build.
- **Streamdown's defaults are permissive.** They allow raw HTML and accept any link, image or protocol, so used as shipped they break SB10.
- **shadcn's Vite theme provider applies the dark class after first paint.**
- **axe-core leaves its target-size rule switched off by default.**

All pages were read and all registry entries checked on 23 October 2026.

## Checklist

Each rule names its source and a way to test it. "House" means a toolkit choice, not a sourced fact.

### Send, wait and stream

1. **Optimistic send.** On submit, append the person's message and clear the composer in the same task, before any network response. Below 0.1 s, a response feels instant ([NN/g response times](https://www.nngroup.com/articles/response-times-3-important-limits/)). `useOptimistic` must be called inside a transition or Action; when the Action throws, it reverts ([React](https://react.dev/reference/react/useOptimistic)). *Test:* with the stream route delayed 2 s, the message is visible within 100 ms of the click.
2. **A status line from the first frame, no answer skeleton.** Show the house status line ("Working…") until the first event arrives. Use skeletons only for loading a whole view (for example, opening a thread's history) that takes more than 1 s. Under 1 s, a skeleton only flickers, and frame-only skeletons read as a stalled page ([NN/g skeletons](https://www.nngroup.com/articles/skeleton-screens/)). *Test:* no skeleton element is present during a turn.
3. **Batch token renders.** Keep the deltas in a ref or store, and publish at most once per animation frame or about every 50 ms. The AI SDK's `throttle: 50` is the published precedent ([AI SDK chatbot](https://ai-sdk.dev/docs/ai-sdk-ui/chatbot)). `useDeferredValue` helps only when the slow child is memoised. An object built during render defeats it ([React](https://react.dev/reference/react/useDeferredValue)). *Test:* React Profiler shows zero commits of earlier message rows while a turn streams.
4. **Append, don't re-parse.** Re-parsing the whole message into `innerHTML` on every chunk repeats work and is an XSS path. Sanitise the accumulated output, not single chunks ([Chrome](https://developer.chrome.com/docs/ai/render-llm-responses)). Streamdown 2.7.1 memoises per block and closes unterminated markdown with `remend`. However, its default rehype plugins include `rehype-raw`, and `rehype-harden` with `allowedLinkPrefixes`, `allowedImagePrefixes` and `allowedProtocols` all set to `["*"]` (package `dist`, 2.7.1). *Test:* a fixture answer with `<img src=x onerror>`, a `javascript:` link and an off-list image host renders all three inert.
5. **Stop feels immediate.** Stop aborts the fetch ([AI SDK](https://ai-sdk.dev/docs/ai-sdk-ui/chatbot)). The button swaps back to Send in the same frame, and the partial text stays, marked "Stopped". *Test:* after Stop, no further text is appended and the turn reads "Stopped".
6. **Measure time to first visible token.** Put `performance.mark` on Send and on the first painted delta, and record the gap in the demo run (house).

### Scroll

7. **Follow only at the live edge.** Keep the view pinned while the reader is within about 70 px of the bottom (`STICK_TO_BOTTOM_OFFSET_PX` in use-stick-to-bottom 1.1.6). Release on any upward wheel, touch, scroll key or scrollbar drag ([shadcn Message Scroller](https://ui.shadcn.com/docs/components/base/message-scroller), [use-stick-to-bottom](https://github.com/stackblitz-labs/use-stick-to-bottom)). *Test:* scroll up 300 px mid-stream, and `scrollTop` is unchanged 2 s later.
8. **Offer a jump-to-latest button** only when the reader is away from the bottom. It re-engages following, and it is `inert` otherwise. Message Scroller and AI Elements' `ConversationScrollButton` both do this ([AI Elements](https://elements.ai-sdk.dev/components/conversation)).
9. **Scroll instantly under reduced motion.** use-stick-to-bottom springs by default (damping 0.7, stiffness 0.05, mass 1.25) and never reads `prefers-reduced-motion`. Pass `resize="instant"` and `initial="instant"` when the query matches (source, 1.1.6). *Test:* with `reducedMotion: 'reduce'` emulated, the view reaches the bottom within one frame.

### Motion

10. **Use the house curves through Tailwind's names.** The house enter and exit curves are exactly Tailwind 4.3.3's `ease-out` (`0, 0, 0.2, 1`) and `ease-in` (`0.4, 0, 1, 1`) (`theme.css`). They are also Material's "legacy" decelerate and accelerate curves ([Flutter `motion.dart`](https://github.com/flutter/flutter/blob/master/packages/flutter/lib/src/material/motion.dart)). The house 150 and 200 ms match Material's short3 and short4 ([Flutter Durations](https://api.flutter.dev/flutter/material/Durations-class.html)) and sit under Kowalski's 300 ms ceiling ([great animations](https://emilkowal.ski/ui/great-animations)). *Test:* grep finds no `transition-all` and no `duration-` above 200 ([Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines/blob/main/command.md)).
11. **Animate state changes, not repetition.** Leave unanimated: anything triggered from the keyboard, Send, every token and trace-line text changes ([Kowalski](https://emilkowal.ski/ui/great-animations)). Animate: the approval card's entry (opacity with a small translate), a trace row's expansion, and the jump button. Keep Streamdown's per-word `animated` off.
12. **CSS transitions first; Motion only for layout animation.** Transitions can be interrupted, and only `transform` and `opacity` should move (Kowalski, Web Interface Guidelines). If Motion is needed, use `m` with `LazyMotion` (about 5 kB, plus 24 kB for `domAnimation`) instead of `motion` (about 43 kB) ([Motion bundle size](https://motion.dev/docs/react-reduce-bundle-size)), and use `MotionConfig reducedMotion="user"` ([Motion accessibility](https://motion.dev/docs/react-accessibility)).
13. **View Transitions only between routes.** Same-document view transitions became Baseline on 14 October 2025 (Firefox 144). Cross-document transitions are not Baseline (web-features 3.44.0). The page is frozen while the update callback runs ([Chrome](https://developer.chrome.com/docs/web-platform/view-transitions/same-document)), so never wrap streaming updates in one.

### Fonts and first paint

14. **Fontsource is already subset and set to swap.** Each `@fontsource-variable` package declares `font-display: swap` with `unicode-range` subsets, so only the subsets a page uses are downloaded. Latin files: Inter 48 KB, JetBrains Mono 40 KB, Source Serif 4 51 KB with `wght` but 122 KB with `opsz`. *Test:* the network log of the empty state shows at most three woff2 requests.
15. **Preload one face.** Preload the Inter latin woff2 with `crossorigin`, using a `?url` import so the hashed name resolves ([Fontsource](https://fontsource.org/docs/getting-started/preload)). Use preload sparingly ([web.dev fonts](https://web.dev/articles/font-best-practices)). In an SPA, text paints only after the JavaScript runs, so a preload lets the font download in parallel (inference).
16. **Metric-matched fallbacks.** fontaine 1.0.3 generates a `"<family> fallback"` face with `size-adjust` and the override descriptors, but only if that name is added to the CSS variable stack ([fontaine](https://github.com/unjs/fontaine)). `size-adjust` has been Baseline widely available since March 2026. `ascent-override` has no Safari support (web-features 3.44.0). *Test:* CLS ≤ 0.1 on a throttled cold load.

### Vitals and bundle

17. **Vitals targets.** LCP ≤ 2.5 s, INP ≤ 200 ms and CLS ≤ 0.1 at the 75th percentile ([web.dev](https://web.dev/articles/vitals)). By default, web-vitals 6.2.3 measures hard loads only, and its `web-vitals/attribution` build splits INP into input delay, processing and presentation ([web-vitals](https://github.com/GoogleChrome/web-vitals)). Keep the DOM small and yield after visible feedback ([optimise INP](https://web.dev/articles/optimize-inp)).
18. **One lazy chunk per route; heavy renderers on demand.** Load each route through React Router's `lazy` ([route object](https://reactrouter.com/start/data/route-object)), and keep Shiki, Mermaid and KaTeX out of the entry chunk. Vite warns at 500 kB per chunk, uncompressed ([build options](https://vite.dev/config/build-options)). Rolldown's `codeSplitting.groups` pull dependencies in recursively, so check the lazy chunks after configuring them ([Rolldown](https://rolldown.rs/in-depth/manual-code-splitting)). *Test:* the build emits no chunk-size warning.
19. **React Compiler on, and proven.** Enable it with `@rolldown/plugin-babel` and `reactCompilerPreset` ([React](https://react.dev/learn/react-compiler/installation)). *Test:* the built JavaScript imports `react/compiler-runtime`.

### Theme

20. **No flash.** shadcn's Vite `ThemeProvider` sets the class in `useEffect`, has no inline script and does not listen for OS changes ([shadcn](https://ui.shadcn.com/docs/dark-mode/vite)). Add a blocking inline script at the top of `<head>` that reads the stored choice or `matchMedia` and sets `.dark` and `style.colorScheme`. Add `<meta name="color-scheme" content="light dark">` ([web.dev](https://web.dev/articles/color-scheme)) and a `theme-color` matching the background (Web Interface Guidelines). *Test:* with `colorScheme: 'dark'`, `<html>` has `.dark` before the app's script runs.
21. **Instant switch.** Suppress transitions for one frame while the theme changes, as next-themes' `disableTransitionOnChange` does ([next-themes](https://github.com/pacocoursey/next-themes)), and follow OS changes while the stored choice is "system".

### Keyboard, focus and announcements

22. **IME-safe Enter.** Enter sends and Shift+Enter adds a new line. Ignore Enter while `isComposing` is true (or `keyCode` is 229), because Enter confirms the IME candidate ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/isComposing)). *Test:* Enter during a composition does not send.
23. **Shortcuts with modifiers, scoped.** Escape stops a run only while focus is in the thread or composer and no popover or dialog is open. Use Cmd/Ctrl+K only for a palette or a new chat. Never use single-character shortcuts ([WCAG 2.1.4](https://www.w3.org/WAI/WCAG22/Understanding/character-key-shortcuts.html)). Avoid the conflicts the APG lists, and show each key on its control ([APG](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/)).
24. **Focus never drops to `body`.** When Stop becomes Send, keep it the same element or move focus to the composer. Do not move focus when an answer completes ([APG](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/)). *Test:* after a keyboard-triggered Stop, `document.activeElement` is not `body`.
25. **Announce additions and outcomes, not tokens.** `role="log"` defaults to polite and non-atomic ([MDN log](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/log_role)). Message Scroller adds `aria-relevant="additions"` and suggests `aria-busy` while a row streams. `aria-busy` asks assistive technology to wait, but it is a hint ([MDN aria-busy](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-busy)). Announce "Stopped", "Failed" and "Approval needed" through a separate `role="status"`.
26. **Touch is not hover.** Tailwind 4's `hover:` variant applies only under `(hover: hover)` (4.3.3 source), so message-footer actions must be visible without hover on touch. Use `touch-action: manipulation` and `overscroll-behavior: contain` in sheets (Web Interface Guidelines).
27. **URLs hold state.** Put the thread ID in the path and open panels in the query string. Format dates, numbers and durations with `Intl`, and use "…" rather than three dots (Web Interface Guidelines).

### Visual QA

28. **The gates are realistic for a POC.** axe-core 4.14.0 ships `target-size` (tag `wcag22aa`) with `enabled: false`, so turn it on explicitly. `toHaveScreenshot` already defaults to `animations: "disabled"` and `caret: "hide"`. Baselines vary with the operating system and hardware, so capture and compare them in one environment ([Playwright](https://playwright.dev/docs/test-snapshots), [assertions](https://playwright.dev/docs/api/class-pageassertions)). Add `reducedMotion: 'reduce'` to the screenshot project ([`emulateMedia`](https://playwright.dev/docs/api/class-page#page-emulate-media)). For Lighthouse, record one run for the POC rather than gating on it (see below).

## What to add to frontend-quality.md and agent-ui-states.md

To keep each fact in one place, the numbers stay in DESIGN.md (durations, easing, the indicator, the live log, fonts). The two references point to those numbers and add only behaviour and tests.

**frontend-quality.md, "Streaming-UI rules":**

- *Must:* "Publish buffered deltas at most once per animation frame. Earlier message rows must not re-render during a stream; check with the React Profiler." This replaces the current `useDeferredValue` bullet, which needs `memo` to work.
- *Must:* "A markdown renderer must not enable raw HTML or wildcard link, image or protocol prefixes. Streamdown 2.7.1 enables all of these by default: pass `skipHtml`, replace `rehypePlugins` without `raw`, and set the `harden` prefixes to the SB10 allowlist."
- *Must:* "Follow the stream only at the live edge, and release on any upward scroll. Use shadcn's `message-scroller`, or use-stick-to-bottom where AI Elements is used. Under reduced motion, scroll instantly."
- *Should:* "Show the person's message and the status line before the first network byte."

**frontend-quality.md, new "First paint" bullets:**

- *Must:* "Add an inline theme script and the `color-scheme` meta tag to `index.html`; shadcn's Vite provider applies the theme after first paint."
- *Should:* "Preload only Inter latin, and add fontaine fallbacks to the three font stacks."
- *Should:* "Lazy-load every route and every highlighter, diagram or maths renderer; treat a Vite chunk-size warning as a failure."
- *Could:* "Before a demo, record LCP, CLS, initial JavaScript size and time to first token from one run."

**frontend-quality.md, gate table:**

- Extend the axe row: "with `target-size` enabled".
- Add a row "Lab vitals (`lighthouse` pinned, FastAPI-served build, model replaced)": recorded for POC; LCP ≤ 2.5 s and CLS ≤ 0.1 for internal tools and above.
- Add a row "Theme first frame and reduced-motion screenshots": reviewed by eye for POC; baselines for internal tools and above.

**frontend-quality.md, correction:** the npm `cn` package is published by the `shadcn` account (repository `shadcn-ui/cn`, 0.5.0, 16 October 2026). The base-nova `message-scroller` registry item lists it as a dependency. Reword "unrelated `cn` package" to say that shadcn now imports its own `cn` package, and keep the rule to read the `package.json` diff. That item also ships a 400 ms exit transition, so add it to the DESIGN.md list of stock classes that break house rules.

**agent-ui-states.md, two new table rows:**

- "Request sent, no event yet" (any source): the person's message shown, the status line "Working…", Stop enabled.
- "Stopped by the person" (client abort): keep the text, mark the turn "Stopped" in words, offer Retry only under the checkpoint rule, and return focus to the composer.

**agent-ui-states.md, new rules:**

- *Must:* "Announce the outcome of each turn (finished, stopped, failed, approval needed) once, in a status region. Never announce individual deltas."
- *Must:* "Enter sends, except during IME composition. Shift+Enter adds a new line. Escape stops a run only when focus is in the conversation and no overlay is open."
- *Should:* "An approval card that appears while the reader is scrolled up must not pull the view down. Show it through the jump control's badge, and announce it."

**DESIGN.md, one aside:** importing `opsz.css` adds about 71 KB to the latin serif. Either justify optical sizing for answers at 17 px, or switch to `wght.css`.

## Versions found (npm registry, 23 October 2026)

| Package | Latest | Published | Licence | Note |
|---|---|---|---|---|
| `@shadcn/react` | 0.3.1 | 2026-08-31 | MIT | Message Scroller; React ≥ 19; 0.x, so pin exactly |
| `use-stick-to-bottom` | 1.1.6 | 2026-06-04 | MIT | No dependencies; React 16.8–19 |
| `streamdown` | 2.7.1 | 2026-10-19 | Apache-2.0 | Override the defaults (rule 4) |
| `motion` | 14.6.0 | 2026-10-22 | MIT | Wraps `framer-motion` 14.6.0 |
| `fontaine` | 1.0.3 | 2026-10-22 | MIT | Uses capsize metrics |
| `@fontsource-variable/inter` / `jetbrains-mono` / `source-serif-4` | 5.3.0 / 5.3.0 / 5.3.1 | July–October 2026 | OFL-1.1 | Match DESIGN.md |
| `web-vitals` | 6.2.3 | 2026-10-05 | Apache-2.0 | |
| `@axe-core/playwright` (`axe-core`) | 4.14.0 (4.14.0) | 2026-10-15 | MPL-2.0 | `target-size` off by default |
| `@playwright/test` | 1.64.1 | 2026-10-14 | Apache-2.0 | |
| `lighthouse` | 13.5.0 | 2026-09-18 | Apache-2.0 | Prefer pinned `npx lighthouse` |
| `@lhci/cli` | 0.15.1 | 2025-06-25 | Apache-2.0 | Bundles Lighthouse 12.6.1; `temporary-public-storage` is public, never for client data |
| `vite` / `@vitejs/plugin-react` / `@rolldown/plugin-babel` / `babel-plugin-react-compiler` | 8.3.5 / 6.1.2 / 0.2.4 / 1.0.0 | | MIT | |
| `react` / `react-router` / `@tanstack/react-query` / `tailwindcss` | 19.3.1 / 8.5.0 / 5.104.5 / 4.3.3 | | MIT | React Router 8 is current; the toolkit names no major |

Lighthouse's navigation mode measures load but cannot capture SPA transitions. Its timespan mode reports CLS but not LCP ([user flows](https://github.com/GoogleChrome/lighthouse/blob/main/docs/user-flows.md)). Neither measures INP during streaming, so check INP with web-vitals attribution in development.

## What this research could not verify

- **Pages that would not load:** the Material 3 and Apple HIG motion pages render with JavaScript and returned no text. The Material values above come from Flutter's published constants, and Apple's guidance was not read.
- **Missing vendor guidance:** no OpenAI or Anthropic interface-writing guidance on streaming was found.
- **Untested components and techniques:** none of the following was run in a browser: Message Scroller, use-stick-to-bottom, Streamdown with hardened options, the inline theme script, Fontsource preload through `?url` in a Vite `index.html`, and fontaine with CSS variables.
- **Screen readers:** support for `aria-busy` and `aria-relevant` is not established. Test with VoiceOver and NVDA before relying on them.
- **IME behaviour:** the Safari ordering of `compositionend` before the Enter keydown comes from a secondary summary, not a primary specification.
- **axe tag selection:** whether running axe by the `wcag22aa` tag switches on rules that are disabled by default was not checked, so enable `target-size` by rule ID.
- **Budgets:** no authoritative per-SPA bundle budget exists. The chunk-warning rule is a house choice, and the 70 px follow threshold is a library constant, not a standard.
- **Versions:** React Router 8.5.0 and React 19.3.1 are newer than anything the toolkit records. Whether the data-mode guidance changed between majors was not checked.
