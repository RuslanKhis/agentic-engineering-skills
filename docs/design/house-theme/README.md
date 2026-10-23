# House theme: rendered check, 23 October 2026

These images show the house theme from [`skills/adk-frontend-integration/assets/design/DESIGN.md`](../../../skills/adk-frontend-integration/assets/design/DESIGN.md) rendered in a real shadcn/ui (Base UI) app. The checks behind them: no horizontal overflow, and zero serious or critical axe findings at every size, in light and dark.

## What the images are

| File | Content |
|---|---|
| `house-design-system-{375,768,1280}-{light,dark}.png` | Design-system page: colour roles as surface and text pairs, semantic colours, lines and chart marks, the type scale, buttons (including hover, pressed and disabled), a keyboard-focused button, inputs with an error, badges, a hairline card and a floating layer |
| `house-conversation-{375,768,1280}-{light,dark}.png` | Agent conversation screen with these parts:<br>• the empty state with suggested prompts, shown as a side panel at 1280 and above the thread when narrower<br>• user messages<br>• reasoning, collapsed<br>• a Trace with ran, failed and running lines<br>• an answer with numbered citations and a sources panel<br>• "AI-generated" labels<br>• a partial answer marked incomplete, with Retry<br>• an approval card, with keyboard focus on Approve<br>• a streaming answer with a running shimmer line and a caret<br>• the composer with Stop |
| `comparison-1280-light.png` | The same conversation markup. House theme on the left; shadcn 4.22.1's stock theme on the right (neutral tokens, Geist, default focus ring) |

Images are 1× PNGs. Captures stop at 2600 px tall: the 375 px design-system page is 3700 px tall, so its last sections are cut off in the image. Axe and the overflow check still ran on the whole page. The 13 images total about 2.8 MB.

## Versions

| Package | Version |
|---|---|
| shadcn CLI | 4.22.1 (`init --base base --preset nova --template vite`; style `base-nova`, base colour `neutral`) |
| @base-ui/react | 1.9.0 |
| react, react-dom | 19.3.1 |
| vite | 8.3.5 (@vitejs/plugin-react 6.1.2) |
| tailwindcss, @tailwindcss/vite | 4.3.3 |
| typescript | 6.0.3 |
| tw-animate-css | 1.4.0 |
| lucide-react | 1.61.0 |
| @fontsource-variable/inter | 5.3.0 |
| @fontsource-variable/source-serif-4 | 5.3.1 (`opsz.css`) |
| @fontsource-variable/jetbrains-mono | 5.3.0 |
| @fontsource-variable/geist (stock render only) | 5.3.0 |
| playwright | 1.64.1 with `channel: "chrome"` (Google Chrome 155.0.8059.86, headless) |
| @axe-core/playwright, axe-core | 4.14.0 |
| @google/design.md | 0.4.0 |
| Node | 22.23.2 |

shadcn components used: button, card, badge, collapsible, input, textarea, label, separator, item, tooltip, popover and trace. The empty state, user message, citation marker, sources panel, AI label and error notice are hand-built from tokens.

## How it was produced

The preview app was built in a scratch directory and is not part of the repository.

1. Scaffold the app and add the components:

   ```
   npx -y shadcn@4.22.1 init --base base --preset nova --template vite --name preview --no-monorepo -y
   npx -y shadcn@4.22.1 add card badge collapsible input textarea separator item tooltip popover label trace -y
   ```

2. Generate the house theme CSS from the DESIGN.md front matter with a scratch script. It maps each colour token to its shadcn variable: `X` goes to `:root` and `dark-X` to `.dark`, and each one is registered in `@theme inline`. It also writes the fonts, the pinned radius steps, the `type-*` utilities, flat shadows, the 2 px `:focus-visible` outline and reduced-motion rules.
3. Add two small preview-only CSS overrides. Badges get `rounded-sm`, and `[data-slot=trace-description]` gets full `muted-foreground` instead of shadcn's `/70` opacity (see the findings).
4. Leave the component files exactly as shadcn wrote them.
5. Build the default-theme page from the stock `index.css`, untouched, plus a shim that gives the `type-*` utilities the same sizes so the two layouts line up. The shim sets no colours or fonts.
6. Build, serve and render:

   ```
   npx vite build && npx vite preview --port 4317
   node render.mjs http://localhost:4317 <out> results.json
   ```

   For each page, `render.mjs` does the following:
   - Waits for `document.fonts.ready`.
   - Presses Tab, then focuses the sample button and checks that it matches `:focus-visible`.
   - Checks overflow (`scrollWidth <= clientWidth`).
   - Runs `new AxeBuilder({ page }).withTags(["wcag2a","wcag2aa","wcag21a","wcag21aa","wcag22aa"])`.
   - Pins the sticky composer in normal flow, then takes the screenshot, because full-page captures position sticky elements unreliably.
7. Compose `comparison-1280-light.png` from a local HTML page holding both screenshots.

Lint: `npx -y @google/design.md@0.4.0 lint skills/adk-frontend-integration/assets/design/DESIGN.md` gave 0 errors, 0 warnings and 1 info ("74 colors, 11 typography scales, 4 rounding levels, 13 spacing tokens, 69 components"), and exited with 0. The contrast pairs, including the 3:1 non-text pairs the linter does not check, were also recomputed from the DESIGN.md tokens with a scratch OKLCH-to-sRGB script. No pair fell below its floor, and every colour is inside the sRGB gamut.

## Results

Axe counts are violating nodes by impact (critical / serious / moderate / minor).

| Image | Overflow (scrollWidth / clientWidth) | Axe | Focus visible | Fonts loaded |
|---|---|---|---|---|
| house-design-system-375-light | none (375 / 375) | 0 / 0 / 0 / 0 | yes | Inter, Source Serif 4, JetBrains Mono |
| house-design-system-768-light | none (768 / 768) | 0 / 0 / 0 / 0 | yes | same |
| house-design-system-1280-light | none (1280 / 1280) | 0 / 0 / 0 / 0 | yes | same |
| house-design-system-375-dark | none (375 / 375) | 0 / 0 / 0 / 0 | yes | same |
| house-design-system-768-dark | none (768 / 768) | 0 / 0 / 0 / 0 | yes | same |
| house-design-system-1280-dark | none (1280 / 1280) | 0 / 0 / 0 / 0 | yes | same |
| house-conversation-375-light | none (375 / 375) | 0 / 0 / 0 / 0 | yes | Inter, Source Serif 4 |
| house-conversation-768-light | none (768 / 768) | 0 / 0 / 0 / 0 | yes | same |
| house-conversation-1280-light | none (1280 / 1280) | 0 / 0 / 0 / 0 | yes | same |
| house-conversation-375-dark | none (375 / 375) | 0 / 0 / 0 / 0 | yes | same |
| house-conversation-768-dark | none (768 / 768) | 0 / 0 / 0 / 0 | yes | same |
| house-conversation-1280-dark | none (1280 / 1280) | 0 / 0 / 0 / 0 | yes | same |
| stock default, conversation 1280 light | none (1280 / 1280) | **0 / 3 / 0 / 0** | yes, but see below | Geist |

- **Incomplete results.** Axe marked one item "incomplete" (it needs a human check) on every conversation render: the running Trace title. Its shimmer is a gradient text fill, so axe cannot measure its contrast.
- **Console errors.** None on any page.

### House against default

- **Contrast.** The stock theme has 3 serious `color-contrast` violations: the Trace durations (`text-muted-foreground/70`) measure 2.71:1 on white. With house tokens the same stock class measured 3.28:1, which is still a failure. That is why the house theme sets full `muted-foreground`. DESIGN.md now says to make the same change in `trace.tsx`.
- **Focus.** Computed styles of the focused Approve button:
  - **House:** a 2 px solid outline, colour `oklch(0.5 0.1 250)` light and `oklch(0.74 0.09 250)` dark, with a 2 px offset and no box-shadow ring. That is 5.8:1 against the light background and 8.1:1 against the dark one.
  - **Stock:** no outline. The ring is a 3 px box-shadow in `oklab(0.708 0 0 / 0.5)`, which measures 1.54:1 against white.
- **Field edges.** The stock `--input` is 1.26:1 against white. The house `input` edge is 3.5:1 in light and 4.2:1 in dark.
- **Why axe passes the stock focus ring and borders.** axe-core does not test 1.4.11 non-text contrast, so the ring and border failures appear only in the computed figures above, not in the axe counts. That matches the research note's prediction.

## Not verified

- **Visual judgement.**
  - The screenshots were looked at by an agent, not reviewed by a designer.
  - No other browsers were tried (Firefox, Safari), and no device pixel ratio other than 1.
  - Forced-colours mode and Windows font rendering were not tried.
- **Interaction.**
  - Hover, pressed and disabled states are shown with static classes, not real pointer states.
  - Tooltip and popover contents were not opened, so the AI-label popover and the floating-layer shadow on a real popover were not captured.
  - Reduced-motion behaviour was not rendered: the CSS rules exist but were not run under `prefers-reduced-motion: reduce`.
  - No screen-reader run was done; live-region announcements are untested.
- **Component edits.** The house treatments for focus, badge radius and Trace descriptions are applied as unlayered CSS in the preview, so the stock component files could be shared with the default render. A real project should edit the `cva` classes as DESIGN.md says. Those edits were not exercised here.
- **Chart marks and colour blindness.** Chart marks were shown only as swatches. Separation for colour-blind readers was not simulated.
- **Brand overrides.** The override procedure in DESIGN.md (accent ramp, fonts, logo, radius) was not exercised with a real client brand.
