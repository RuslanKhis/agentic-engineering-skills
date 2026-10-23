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
| `@axe-core/playwright` on the main view | 0 serious or critical | 0 serious or critical in idle, streaming, approval, tool-error and empty states |
| Screenshots at 375, 768 and 1280 px, light and dark, no horizontal overflow | Reviewed by eye | Baselines with `toHaveScreenshot` on a pinned browser |
| Browser journey (sign-in, send, streamed answer with tool progress, approve and reject) against the real API with the model replaced | One journey | Per state, with keyboard-only send, stop, approve and deny |

Automated accessibility checks find only part of WCAG; they are a floor, not
conformance.

`scripts/check_theme.py` reads the theme CSS that `components.json` names (or
`--css PATH`) and exits 1 while shadcn's default token values or default font
stacks remain. So that `make check` works without the skill installed, copy it
into the project (for example `frontend/scripts/`; it is MIT like this skill)
and run it with Python 3.11 or later.

After each `shadcn add`, read the `package.json` diff: in an engineer trial on
23 October 2026, shadcn 4.22.1 added an unrelated `cn` package and imported
`cn` from it instead of the local `@/lib/utils`. Its defaults are recorded from a pinned shadcn version; a newer
shadcn may change them, so update the recorded set when the project's shadcn
version moves.

## Streaming-UI rules

- Abort the fetch on unmount and on Stop (`AbortController`); a disconnect
  does not prove the server-side effect stopped.
- Buffer tokens in a ref or store and render with `useDeferredValue` or
  `startTransition`; never re-render the whole thread for each token.
- Read the stream with `fetch` and a bearer token, never native
  `EventSource` or a token in the URL (SB08). Validate each event at run time
  (for example with zod); a type assertion is not validation.
- Never send a user ID from the browser; the server derives it (SB03).
- Render model output as text or markdown with raw HTML off, a URL-protocol
  allowlist and images only from listed hosts; no `dangerouslySetInnerHTML`
  (SB10).
- No edit or regenerate without a server checkpoint to resume from.
- Never wait for network idle in a browser test of a streaming page; wait for
  the visible state instead.

## Recorded browser stack and the gap

[compatibility.md](compatibility.md) records the exercised manual-browser
recipe (React 18.3.1, Vite 6.4.3) and the move to the current line as an open
version decision.
