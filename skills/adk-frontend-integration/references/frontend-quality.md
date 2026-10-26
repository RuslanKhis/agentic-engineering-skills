# Frontend quality gates and streaming-UI rules

Read when building or reviewing the browser app of an ADK interface, or when
a ticket names a design system. Gates run in the project's `make check` at the
profile's depth.

## Start from the house theme

Copy [the house DESIGN.md](../assets/design/DESIGN.md) to
`docs/design/DESIGN.md` unless the client brings its own design system. A
client brand overrides only the surface that file names. Map its tokens to the
shadcn theme variables with the `shadcn` companion's DESIGN.md workflow; never
ship shadcn's default theme, because the generic look comes from its default
tokens. The DESIGN.md file itself states its lint gate (the CLI pinned
exactly; fail on any error or warning, read from the JSON output, because at
0.4.0 contrast failures arrive as warnings while the exit code stays 0).

## Gates by depth

| Gate | POC | Internal tool and above |
| --- | --- | --- |
| `eslint-plugin-react-hooks` `recommended` preset (7.x includes the compiler-derived rules) and `tsc --noEmit` in strict mode | 0 errors | 0 errors |
| Generated-client drift: regenerate from the offline OpenAPI dump, `git diff --exit-code` (`adk-fastapi-backend`) | When handed over | Always |
| DESIGN.md lint and `scripts/check_theme.py --project frontend` (no shadcn default tokens or fonts left) | When handed over | Always |
| No raw colour values outside the theme file (grep for hex, `rgb(`, `oklch(` and palette classes such as `bg-blue-500`) | When handed over | Always |
| `@axe-core/playwright` on the main view, with the `target-size` rule enabled by ID (axe-core 4.14.0 ships it switched off) | 0 serious or critical | 0 serious or critical in idle, streaming, approval, tool-error and empty states |
| Screenshots at 375, 768 and 1280 px, light and dark, no horizontal overflow | Reviewed by eye | Baselines with `toHaveScreenshot` on a pinned browser |
| Browser journey (sign-in, send, streamed answer with tool progress, approve and reject) against the real API with the model replaced | One journey | Per state, with keyboard-only send, stop, approve and deny |
| Lab vitals: a pinned `npx lighthouse` run on the FastAPI-served build with the model replaced (never Lighthouse CI's public temporary storage) | Recorded before a demo: LCP, CLS, initial JavaScript size, time to first token | LCP ≤ 2.5 s and CLS ≤ 0.1 |
| First frame in dark mode and a reduced-motion run | Reviewed by eye | Screenshot baselines |

Automated accessibility checks find only part of WCAG; they are a floor, not
conformance.

`scripts/check_theme.py` reads the theme CSS that `components.json` names (or
`--css PATH`) and exits 1 while shadcn's default token values or default font
stacks remain. So that `make check` works without the skill installed, copy it
into the project (for example `frontend/scripts/`; it is MIT like this skill)
and run it with Python 3.11 or later. Its defaults are recorded from a pinned
shadcn version; update the recorded set when the project's shadcn version
moves.

After each `shadcn add`, read the `package.json` diff. shadcn now publishes its
own `cn` package (`shadcn-ui/cn`), which registry items such as the
`message-scroller` list as a dependency; an engineer trial on 23 October 2026
saw components switch to importing `cn` from it instead of the local
`@/lib/utils`. Keep one source and make the imports agree.

## Streaming-UI rules

- Abort the fetch on unmount and on Stop (`AbortController`); a disconnect
  does not prove the server-side effect stopped.
- Show the person's message and the status line before the first network
  byte arrives.
- Buffer deltas in a ref or store and publish them at most once per animation
  frame; earlier message rows must not re-render during a stream (check with
  the React Profiler; `useDeferredValue` helps only with memoised rows).
- Follow the stream only while the reader is at the bottom and release on any
  upward scroll: shadcn's Message Scroller (`@shadcn/react`, pinned exactly,
  React 19 or later) or `use-stick-to-bottom`. Under reduced motion, scroll
  instantly; neither library checks it.
- Read the stream with `fetch` and a bearer token, never native
  `EventSource` or a token in the URL (SB08). Validate each event at run time
  (for example with zod); a type assertion is not validation.
- Never send a user ID from the browser; the server derives it (SB03).
- Render model output as text or markdown with raw HTML off, a URL-protocol
  allowlist and images only from listed hosts; no `dangerouslySetInnerHTML`
  (SB10). Streamdown 2.7.1, used by shadcn's chat components, enables raw HTML
  (`rehype-raw`) and allows every link, image and protocol by default: pass
  `skipHtml`, replace `rehypePlugins` without the raw plugin, and set its
  harden prefixes to the SB10 allowlist.
- No edit or regenerate without a server checkpoint to resume from. Showing the buttons is not rewinding: the gateway calls `Runner.rewind_async(user_id=, session_id=, rewind_before_invocation_id=)` (google-adk 2.12.0; `adk api_server` has no rewind route) before running the edited message, and a scripted-model test asserts the removed turn is absent from the next model request. Three facts shape the gateway (2.12.0 `runners.py` and `sessions/_rewind_utils.py`, read 2026-10-26): `rewind_async` loads the session through `_get_or_create_session`, so check ownership before calling it; it only appends a rewind marker event, so stored history keeps the discarded turns and a history endpoint must apply the markers itself; and it undoes no side effect, so refuse a rewind past a completed write rather than let the user re-issue it. In assistant-ui the buttons appear only when `getCheckpointId` is supplied, a regenerate arrives as an empty text part (re-send the user text stored on the server), and a null checkpoint sends the edit as a new message, leaving the server's history and the screen out of step.
- Never wait for network idle in a browser test of a streaming page; wait for
  the visible state instead.

## First paint

- Put an inline theme script and the `color-scheme` meta tag in `index.html`;
  shadcn's Vite theme provider applies the dark class only after first paint,
  so a dark-mode user sees a light flash.
- Preload only the interface font's latin file, and give the three font
  stacks metric-matched fallbacks (for example with `fontaine`) so swapping
  fonts does not shift the layout.
- Lazy-load every route and any highlighter, diagram or maths renderer;
  treat a Vite chunk-size warning as a failure.

Sources for this section and the streaming rules, read 23 October 2026, are
in the toolkit repository's `docs/research/frontend-craft-2026-10-23.md`.

## Recorded browser stack and the gap

[compatibility.md](compatibility.md) records the exercised manual-browser
recipe (React 18.3.1, Vite 6.4.3) and the move to the current line as an open
version decision.
