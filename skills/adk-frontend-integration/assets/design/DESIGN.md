---
version: alpha
name: House
description: Restrained enterprise theme for ADK agent web apps on shadcn/ui (Base UI) and Tailwind CSS v4. Warm paper greys, one ink-blue accent, Inter, Source Serif 4 and JetBrains Mono.
colors:
  background: "oklch(0.988 0.003 85)"
  foreground: "oklch(0.205 0.006 85)"
  card: "oklch(0.997 0.0015 85)"
  card-foreground: "{colors.foreground}"
  popover: "{colors.card}"
  popover-foreground: "{colors.foreground}"
  primary: "oklch(0.40 0.085 250)"
  primary-hover: "oklch(0.33 0.07 250)"
  primary-active: "oklch(0.27 0.055 250)"
  primary-foreground: "oklch(0.985 0.003 85)"
  secondary: "oklch(0.955 0.005 85)"
  secondary-foreground: "oklch(0.24 0.008 85)"
  muted: "oklch(0.962 0.004 85)"
  muted-foreground: "oklch(0.47 0.008 85)"
  accent: "oklch(0.948 0.012 250)"
  accent-foreground: "oklch(0.30 0.07 250)"
  destructive: "oklch(0.50 0.15 27)"
  destructive-foreground: "{colors.primary-foreground}"
  success: "oklch(0.47 0.09 150)"
  warning: "oklch(0.50 0.10 65)"
  info: "oklch(0.48 0.07 220)"
  border: "oklch(0.905 0.005 85)"
  input: "oklch(0.62 0.008 85)"
  ring: "oklch(0.50 0.10 250)"
  chart-1: "oklch(0.50 0.095 250)"
  chart-2: "oklch(0.50 0.08 185)"
  chart-3: "oklch(0.52 0.10 70)"
  chart-4: "oklch(0.50 0.02 85)"
  chart-5: "oklch(0.52 0.13 30)"
  sidebar: "oklch(0.972 0.004 85)"
  sidebar-foreground: "{colors.foreground}"
  sidebar-primary: "{colors.primary}"
  sidebar-primary-foreground: "{colors.primary-foreground}"
  sidebar-accent: "oklch(0.935 0.006 85)"
  sidebar-accent-foreground: "{colors.foreground}"
  sidebar-border: "{colors.border}"
  sidebar-ring: "{colors.ring}"
  dark-background: "oklch(0.185 0.004 85)"
  dark-foreground: "oklch(0.945 0.004 85)"
  dark-card: "oklch(0.215 0.005 85)"
  dark-card-foreground: "{colors.dark-foreground}"
  dark-popover: "oklch(0.245 0.005 85)"
  dark-popover-foreground: "{colors.dark-foreground}"
  dark-primary: "oklch(0.78 0.075 250)"
  dark-primary-hover: "oklch(0.84 0.06 250)"
  dark-primary-active: "oklch(0.72 0.08 250)"
  dark-primary-foreground: "oklch(0.20 0.03 250)"
  dark-secondary: "oklch(0.275 0.006 85)"
  dark-secondary-foreground: "oklch(0.93 0.004 85)"
  dark-muted: "oklch(0.255 0.005 85)"
  dark-muted-foreground: "oklch(0.735 0.008 85)"
  dark-accent: "oklch(0.29 0.03 250)"
  dark-accent-foreground: "oklch(0.91 0.025 250)"
  dark-destructive: "oklch(0.72 0.13 25)"
  dark-destructive-foreground: "oklch(0.20 0.03 25)"
  dark-success: "oklch(0.76 0.10 150)"
  dark-warning: "oklch(0.80 0.10 75)"
  dark-info: "oklch(0.76 0.07 220)"
  dark-border: "oklch(0.30 0.005 85)"
  dark-input: "oklch(0.57 0.008 85)"
  dark-ring: "oklch(0.74 0.09 250)"
  dark-chart-1: "oklch(0.74 0.09 250)"
  dark-chart-2: "oklch(0.74 0.08 185)"
  dark-chart-3: "oklch(0.80 0.10 75)"
  dark-chart-4: "oklch(0.72 0.015 85)"
  dark-chart-5: "oklch(0.72 0.12 30)"
  dark-sidebar: "oklch(0.205 0.005 85)"
  dark-sidebar-foreground: "{colors.dark-foreground}"
  dark-sidebar-primary: "{colors.dark-primary}"
  dark-sidebar-primary-foreground: "{colors.dark-primary-foreground}"
  dark-sidebar-accent: "oklch(0.27 0.006 85)"
  dark-sidebar-accent-foreground: "{colors.dark-foreground}"
  dark-sidebar-border: "{colors.dark-border}"
  dark-sidebar-ring: "{colors.dark-ring}"
typography:
  display:
    fontFamily: Source Serif 4
    fontSize: 36px
    fontWeight: 600
    lineHeight: 44px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Source Serif 4
    fontSize: 28px
    fontWeight: 600
    lineHeight: 36px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Source Serif 4
    fontSize: 22px
    fontWeight: 600
    lineHeight: 30px
    letterSpacing: -0.01em
  title-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 600
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: 400
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: 400
    lineHeight: 18px
  label-md:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: 500
    lineHeight: 16px
  caption:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 400
    lineHeight: 16px
  data-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: 400
    lineHeight: 20px
    fontFeature: '"tnum" 1'
  answer-md:
    fontFamily: Source Serif 4
    fontSize: 17px
    fontWeight: 400
    lineHeight: 28px
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: 400
    lineHeight: 20px
rounded:
  sm: 4px
  md: 6px
  lg: 8px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 24px
  2xl: 32px
  3xl: 48px
  4xl: 64px
  control: 32px
  control-compact: 28px
  row: 36px
  row-compact: 28px
  content-max: 1200px
components:
  page:
    backgroundColor: "{colors.background}"
    textColor: "{colors.foreground}"
    typography: "{typography.body-md}"
  card:
    backgroundColor: "{colors.card}"
    textColor: "{colors.card-foreground}"
    rounded: "{rounded.lg}"
    padding: 16px
  popover:
    backgroundColor: "{colors.popover}"
    textColor: "{colors.popover-foreground}"
    rounded: "{rounded.lg}"
  helper-text:
    backgroundColor: "{colors.background}"
    textColor: "{colors.muted-foreground}"
    typography: "{typography.body-sm}"
  helper-text-on-card:
    backgroundColor: "{colors.card}"
    textColor: "{colors.muted-foreground}"
  muted-band:
    backgroundColor: "{colors.muted}"
    textColor: "{colors.muted-foreground}"
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.primary-foreground}"
    typography: "{typography.label-md}"
    rounded: "{rounded.md}"
    height: 32px
    padding: 12px
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
    textColor: "{colors.primary-foreground}"
  button-primary-active:
    backgroundColor: "{colors.primary-active}"
    textColor: "{colors.primary-foreground}"
  button-secondary:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.secondary-foreground}"
    rounded: "{rounded.md}"
    height: 32px
  button-destructive:
    backgroundColor: "{colors.destructive}"
    textColor: "{colors.destructive-foreground}"
    rounded: "{rounded.md}"
    height: 32px
  input:
    backgroundColor: "{colors.card}"
    textColor: "{colors.foreground}"
    rounded: "{rounded.md}"
    height: 32px
  input-edge:
    backgroundColor: "{colors.input}"
  divider:
    backgroundColor: "{colors.border}"
  menu-item-active:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.accent-foreground}"
    rounded: "{rounded.sm}"
  selected-row:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.primary}"
  link:
    backgroundColor: "{colors.background}"
    textColor: "{colors.primary}"
  focus-ring:
    backgroundColor: "{colors.muted}"
    textColor: "{colors.ring}"
  badge:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.secondary-foreground}"
    typography: "{typography.caption}"
    rounded: "{rounded.sm}"
  status-success:
    backgroundColor: "{colors.muted}"
    textColor: "{colors.success}"
  status-warning:
    backgroundColor: "{colors.muted}"
    textColor: "{colors.warning}"
  status-danger:
    backgroundColor: "{colors.muted}"
    textColor: "{colors.destructive}"
  status-info:
    backgroundColor: "{colors.muted}"
    textColor: "{colors.info}"
  user-message:
    backgroundColor: "{colors.muted}"
    textColor: "{colors.foreground}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 12px
  assistant-answer:
    backgroundColor: "{colors.background}"
    textColor: "{colors.foreground}"
    typography: "{typography.answer-md}"
  code:
    backgroundColor: "{colors.muted}"
    textColor: "{colors.foreground}"
    typography: "{typography.code-sm}"
    rounded: "{rounded.sm}"
  data-cell:
    backgroundColor: "{colors.card}"
    textColor: "{colors.foreground}"
    typography: "{typography.data-md}"
    height: 36px
  trace-line:
    backgroundColor: "{colors.background}"
    textColor: "{colors.muted-foreground}"
    typography: "{typography.body-sm}"
  ai-label:
    backgroundColor: "{colors.background}"
    textColor: "{colors.muted-foreground}"
    typography: "{typography.caption}"
  chart-series-1:
    backgroundColor: "{colors.muted}"
    textColor: "{colors.chart-1}"
  chart-series-2:
    backgroundColor: "{colors.muted}"
    textColor: "{colors.chart-2}"
  chart-series-3:
    backgroundColor: "{colors.muted}"
    textColor: "{colors.chart-3}"
  chart-series-4:
    backgroundColor: "{colors.muted}"
    textColor: "{colors.chart-4}"
  chart-series-5:
    backgroundColor: "{colors.muted}"
    textColor: "{colors.chart-5}"
  sidebar:
    backgroundColor: "{colors.sidebar}"
    textColor: "{colors.sidebar-foreground}"
  sidebar-item-active:
    backgroundColor: "{colors.sidebar-accent}"
    textColor: "{colors.sidebar-accent-foreground}"
  sidebar-primary-item:
    backgroundColor: "{colors.sidebar-primary}"
    textColor: "{colors.sidebar-primary-foreground}"
  sidebar-focus-ring:
    backgroundColor: "{colors.sidebar-accent}"
    textColor: "{colors.sidebar-ring}"
  sidebar-divider:
    backgroundColor: "{colors.sidebar-border}"
  dark-page:
    backgroundColor: "{colors.dark-background}"
    textColor: "{colors.dark-foreground}"
  dark-card:
    backgroundColor: "{colors.dark-card}"
    textColor: "{colors.dark-card-foreground}"
  dark-popover:
    backgroundColor: "{colors.dark-popover}"
    textColor: "{colors.dark-popover-foreground}"
  dark-helper-text:
    backgroundColor: "{colors.dark-background}"
    textColor: "{colors.dark-muted-foreground}"
  dark-helper-text-on-popover:
    backgroundColor: "{colors.dark-popover}"
    textColor: "{colors.dark-muted-foreground}"
  dark-muted-band:
    backgroundColor: "{colors.dark-muted}"
    textColor: "{colors.dark-muted-foreground}"
  dark-button-primary:
    backgroundColor: "{colors.dark-primary}"
    textColor: "{colors.dark-primary-foreground}"
  dark-button-primary-hover:
    backgroundColor: "{colors.dark-primary-hover}"
    textColor: "{colors.dark-primary-foreground}"
  dark-button-primary-active:
    backgroundColor: "{colors.dark-primary-active}"
    textColor: "{colors.dark-primary-foreground}"
  dark-button-secondary:
    backgroundColor: "{colors.dark-secondary}"
    textColor: "{colors.dark-secondary-foreground}"
  dark-button-destructive:
    backgroundColor: "{colors.dark-destructive}"
    textColor: "{colors.dark-destructive-foreground}"
  dark-input-edge:
    backgroundColor: "{colors.dark-input}"
  dark-divider:
    backgroundColor: "{colors.dark-border}"
  dark-menu-item-active:
    backgroundColor: "{colors.dark-accent}"
    textColor: "{colors.dark-accent-foreground}"
  dark-selected-row:
    backgroundColor: "{colors.dark-accent}"
    textColor: "{colors.dark-primary}"
  dark-focus-ring:
    backgroundColor: "{colors.dark-muted}"
    textColor: "{colors.dark-ring}"
  dark-status-success:
    backgroundColor: "{colors.dark-muted}"
    textColor: "{colors.dark-success}"
  dark-status-warning:
    backgroundColor: "{colors.dark-muted}"
    textColor: "{colors.dark-warning}"
  dark-status-danger:
    backgroundColor: "{colors.dark-muted}"
    textColor: "{colors.dark-destructive}"
  dark-status-info:
    backgroundColor: "{colors.dark-muted}"
    textColor: "{colors.dark-info}"
  dark-chart-series-1:
    backgroundColor: "{colors.dark-muted}"
    textColor: "{colors.dark-chart-1}"
  dark-chart-series-2:
    backgroundColor: "{colors.dark-muted}"
    textColor: "{colors.dark-chart-2}"
  dark-chart-series-3:
    backgroundColor: "{colors.dark-muted}"
    textColor: "{colors.dark-chart-3}"
  dark-chart-series-4:
    backgroundColor: "{colors.dark-muted}"
    textColor: "{colors.dark-chart-4}"
  dark-chart-series-5:
    backgroundColor: "{colors.dark-muted}"
    textColor: "{colors.dark-chart-5}"
  dark-sidebar:
    backgroundColor: "{colors.dark-sidebar}"
    textColor: "{colors.dark-sidebar-foreground}"
  dark-sidebar-item-active:
    backgroundColor: "{colors.dark-sidebar-accent}"
    textColor: "{colors.dark-sidebar-accent-foreground}"
  dark-sidebar-primary-item:
    backgroundColor: "{colors.dark-sidebar-primary}"
    textColor: "{colors.dark-sidebar-primary-foreground}"
  dark-sidebar-focus-ring:
    backgroundColor: "{colors.dark-sidebar-accent}"
    textColor: "{colors.dark-sidebar-ring}"
  dark-sidebar-divider:
    backgroundColor: "{colors.dark-sidebar-border}"
---

# House design system

The house theme for web interfaces in front of ADK agents. Copy this file to `docs/design/DESIGN.md` in the target project, map it to the shadcn theme file as described under Colors, and keep the two in step. The format is Google's DESIGN.md (`version: alpha`); lint it with `npx -y @google/design.md@0.4.0 lint docs/design/DESIGN.md` and treat any error **or warning** in the JSON `summary` as a failure, because 0.4.0 reports contrast failures as warnings and exits 0 on them.

## Overview

A quiet working tool for people who read, check and approve what an agent did. It should feel like good paper and ink: warm near-neutral greys, one deep ink-blue accent kept for actions, selection and focus, and type chosen for long reading. It is not a marketing page and it does not look "AI": no gradients, glass, glow, neon or purple, no sparkle icons and no animated backgrounds.

- **Density:** comfortable by default (32 px controls, 36 px table rows); compact mode (28 px controls and rows) for data-dense screens only.
- **Copy:** sentence case everywhere — buttons, titles, menu items, column headers, tabs. Plain verbs on buttons ("Approve", "Retry"). No exclamation marks and no first-person claims of feeling. This is a house choice: some companion skills and client brand guides use title case for buttons and headings; inside a house app, sentence case wins unless a client brand override says otherwise in writing.
- **Accessibility floor:** WCAG 2.2 AA. Every text pair, at any size, is at least 4.5:1. Field edges, focus indicators, checkbox and radio edges and chart marks are at least 3:1 against what they sit on. Pointer targets are at least 24 × 24 px.
- **Two sections follow the eight spec sections:** Motion and Brand override. The linter keeps them as unknown headings.

## Colors

Colour token names are the shadcn CSS variable names; tokens prefixed `dark-` are the same variables under `.dark`. Map them one to one into the project's `tailwind.css` file (the `tailwind.css` field of `components.json`): `colors.muted-foreground` becomes `--muted-foreground` in `:root`, and `colors.dark-muted-foreground` becomes `--muted-foreground` in `.dark`. Keep the `oklch()` values exactly as written. `primary-hover`, `primary-active`, `destructive-foreground`, `success`, `warning` and `info` are house additions: declare them in both scopes and register each in `@theme inline` as `--color-<name>: var(--<name>)`. Never use raw Tailwind palette colours (`text-green-600`) or `dark:` colour overrides; use the tokens.

- **Neutrals:** hue 85, chroma at most 0.008 — paper, not screen grey. `background` is the canvas, `card` and `popover` one step lighter, `muted` and `secondary` one step darker for bands and quiet buttons.
- **Accent ramp (ink blue, hue 250):** `primary` (#1F4A73) for the one main action per view, links and selected items; `primary-hover` (#153758) and `primary-active` (#0F2840) for pointer states; `accent` (#E8EFF6) is the subtle step for hover rows, menu highlights and the selected-row fill; `ring` (#32669A) is the focus colour and is used for nothing else. Hue 250 is kept well away from the 277–293 band of generic "AI purple".
- **Semantic colours, muted:** `success` (#31693F), `warning` (#8A5619), `destructive` (#A83630) and `info` (#276779) are text and icon colours at chroma 0.15 or less. Status is always also said in words or an icon; never by colour alone.
- **Lines:** `border` (#E1DFDC) is a decorative hairline between regions and may be below 3:1. `input` (#888681) is the edge of a field, checkbox or control that has no other boundary and must stay at 3:1 or more.
- **Dark mode is designed, not inverted:** surfaces step up in lightness (background #131311, card #1A1917, popover #21201E, muted #242320) so layers read without shadows; the accent flips to a light step (#93BCE6) carrying a dark label; edges are opaque (`dark-input` #797772), never white at 10–15%.

Measured contrast (WCAG 2.x, sRGB, worst surface each colour sits on):

| Pair | Light | Dark | Floor |
|---|---|---|---|
| foreground on background / card / popover | 17.3 / 17.8 / 17.8 | 15.9 / 15.0 / 13.9 | 4.5 |
| muted-foreground on muted (worst surface) | 6.1 | 6.7 | 4.5 |
| primary-foreground on primary / hover / active | 8.8 / 11.7 / 14.4 | 9.1 / 11.1 / 7.3 | 4.5 |
| primary as link text on background | 8.9 | 9.4 | 4.5 |
| accent-foreground on accent | 11.8 | 10.8 | 4.5 |
| success, warning, destructive, info on muted | 5.8, 5.5, 5.8, 5.7 | 7.6, 8.3, 6.0, 7.5 | 4.5 |
| chart-1 … chart-5 on muted | 5.4, 5.1, 5.1, 5.4, 5.3 | 6.8, 7.1, 8.4, 6.3, 6.0 | 3.0 (4.5 met) |
| input edge on background / card / muted / accent | 3.5 / 3.6 / 3.25 / 3.1 | 4.2 / 3.9 / 3.5 / 3.1 | 3.0 |
| ring on muted (worst surface) | 5.4 | 6.8 | 3.0 |
| border on background | 1.3 | 1.4 | decorative only |

The `components` block holds one entry per text-on-surface pair so the linter checks each one at 4.5:1. The linter does not check 3:1 non-text pairs; recompute the `input` and `ring` rows after any change.

## Typography

Three open families (SIL OFL 1.1), self-hosted from npm and bundled at build time. Never load fonts from a font CDN at run time.

| Role | Package (tested) | CSS variable and stack |
|---|---|---|
| Interface | `@fontsource-variable/inter@5.3.0` | `--font-sans: "Inter Variable", ui-sans-serif, system-ui, sans-serif` |
| Headings and assistant answers | `@fontsource-variable/source-serif-4@5.3.1` (import `opsz.css` for optical sizing) | `--font-serif: "Source Serif 4 Variable", Georgia, "Times New Roman", serif` |
| Code, identifiers, tool arguments | `@fontsource-variable/jetbrains-mono@5.3.0` | `--font-mono: "JetBrains Mono Variable", ui-monospace, SFMono-Regular, Menlo, monospace` |

- **Scale:** the typography tokens above, px size / line height: display 36/44, headline-lg 28/36, headline-md 22/30 (serif, 600); title-md 16/24 (sans, 600); body-md 14/20 is the interface default; body-sm 13/18; label-md 13/16 (500); caption 12/16; answer-md 17/28 (serif, 400); code-sm 13/20.
- **Weights:** 400, 500 and 600 only. Tracking −0.01em at 22 px and above, otherwise 0.
- **Answers:** assistant answers are set in `answer-md` with a measure of about 68ch. The serif is one step larger than the interface text because its x-height is smaller.
- **Numbers:** tables, metrics, timestamps, token counts and durations use tabular figures (`data-md`, Tailwind `tabular-nums`).
- **Default size:** set `body` to body-md (14/20); Tailwind's preflight leaves it at 16 px.
- **Implementation:** turn each token into an `@utility type-<token>` in the theme file. Do not register `--text-*` keys for them, because shadcn's `cn()` treats unknown `text-*` classes as colours. Keep `--font-heading` on the sans for small component titles (card and dialog titles); page headings use the serif utilities.

## Layout

- **Grid:** an 8-point rhythm with 4 px half-steps. Tailwind's `--spacing` stays `0.25rem`; use the steps 4, 8, 12, 16, 24, 32, 48 and 64 px (`spacing` tokens). Other values need a reason.
- **Density:** comfortable — controls 32 px (`h-8`, the `base-nova` default), table rows 36 px, card padding 16 px. Compact — controls and rows 28 px, card padding 12 px, for data-dense screens only, switched per screen and never mixed in one view. No target below 24 px.
- **Page:** content at most 1200 px wide; 16 px side gutter below 768 px, 24 px from 768 px, 32 px from 1280 px. No horizontal page scroll at 375 px; wide tables and code scroll inside their own container.
- **Conversation column:** one centred column at most 768 px wide; answer prose at about 68ch. The composer is sticky at the bottom with `scroll-padding-bottom` equal to its height so focused items are never hidden behind it.

## Elevation & Depth

Depth comes from surface lightness and hairlines, not shadows.

- **Flat by default:** cards, panels, tables, messages and the composer are separated by a 1 px `border` hairline or a surface step. Set `--shadow-xs: 0 0 #0000` and remove shadows from cards and inputs.
- **One elevation, for floating layers only:** popovers, menus, tooltips, dialogs and sheets use `0 1px 2px rgb(24 23 20 / 0.06), 0 8px 24px rgb(24 23 20 / 0.08)` plus their hairline. Nothing else casts a shadow.
- **Dark mode:** separate layers by surface lightness (`dark-popover` is lighter than `dark-card`); keep the hairline, drop the shadow.
- **Scrims:** dialogs dim the page with `foreground` at 40% opacity; no blur.

## Shapes

- **Radius steps:** 4 px (`rounded.sm`: badges, menu items, inline code, checkboxes), 6 px (`rounded.md`: buttons, inputs, selects, tabs) and 8 px (`rounded.lg`: cards, popovers, dialogs, message bubbles). `full` is for avatars and status dots only. Nothing else is rounder: no pill buttons.
- **Tailwind mapping:** set `--radius: 0.375rem` and pin the steps in `@theme inline` instead of deriving them: `--radius-sm: 4px`, `--radius-md: 4px`, `--radius-lg: 6px`, `--radius-xl: 8px`, and `--radius-2xl`, `--radius-3xl`, `--radius-4xl` all `8px`, so shadcn's larger classes cannot exceed the scale. Give badges `rounded-sm`.
- **Lines:** 1 px hairlines. Focus is a 2 px solid `ring` outline with a 2 px offset, drawn with `outline` (it survives forced-colours mode), replacing shadcn's `ring-3 ring-ring/50` box-shadow. Implement it as an unlayered `:focus-visible` rule that also sets `--tw-ring-shadow: 0 0 #0000`, and remove `outline-ring/50` from the base layer.
- **Icons:** Lucide, 16 px in controls, 1.5–2 px stroke, `currentColor`. No filled or multicolour icons.

## Components

Use shadcn/ui (Base UI) components first; edit their `cva` variants to these rules rather than overriding with `className`. Control heights move together across button, input, select, toggle and tabs.

- **Buttons:** primary for the single main action in a region; secondary or outline for the rest; ghost for icon buttons in toolbars and message footers (with a tooltip and an `aria-label`); destructive only when the effect destroys something. Hover darkens to `primary-hover`, press to `primary-active`; no translate, scale or opacity-dimmed hover.
- **Inputs and selects:** `card` fill, `input` edge, 6 px radius, 32 px tall; the error state adds a `destructive` edge and a message in words below the field.
- **Badges:** 4 px radius, caption type, `secondary` fill or outline; status badges add an icon or word, never colour alone.
- **Cards and panels:** hairline border, 8 px radius, no shadow.

Agent conversation patterns (build on shadcn's AI Elements patterns and `Trace`; hand-build only where shadcn has no component):

- **Messages:** assistant answers are full-width prose in the column, no bubble, set in `answer-md`; user messages are compact `user-message` bubbles aligned to the end, `body-md`, at most 80% of the column. Each assistant turn has a quiet footer of ghost icon buttons: Copy, Good response, Bad response (toggles with `aria-pressed`) and Retry.
- **AI-generated label:** every assistant answer carries the words "AI-generated" in `ai-label` style (caption, `muted-foreground`, no icon glow or gradient). It opens a popover with the model, the sources used and the time of the answer. It is never decoration, never an action and never disabled; once a person edits the content, replace it with an "Edited" note and a revert control.
- **Streaming:** one subtle indicator at a time — shadcn's `shimmer` on the live status line ("Writing answer…"), or a 6 px `muted-foreground` caret at the end of the text. No spinners in the prose, no custom keyframes. Stop is reachable for the whole run. Announce completion, not each token: the transcript is an `aria-live="polite"` log, `aria-busy="true"` while streaming.
- **Tool steps:** one quiet `Trace` per run of steps, one `TraceLine` per step, `trace-line` style in `muted-foreground`. The title states the status in words and tense — "Running query…", "Ran query", "Failed to run query" — with an icon as a second cue; failures use `destructive` text plus the word "Failed". Rows are collapsed by default and become collapsible only once they have output; never dim a line with opacity. shadcn 4.22.1's `TraceDescription` ships `text-muted-foreground/70`, which axe measured at 3.3:1 on the house background (2.7:1 on stock tokens); change it to `text-muted-foreground`.
- **Reasoning:** collapsed by default behind a "Thought for 4 s" trigger; open while streaming only if the person opened it, and never reopen automatically. A person's click always wins.
- **Approval card:** a pending approval is a `card` (shadcn `Item`, outline) outside the Trace. Above the buttons it states, in plain words, the action ("Send 3 emails"), what it affects ("to the finance-approvers list") and the consequence ("Recipients see them immediately; this cannot be undone"). Buttons are "Deny" (outline, never destructive) and "Approve" (primary; destructive variant only when the effect is destructive). It is a labelled `role="group"`, keyboard-operable in tab order with visible focus, and focus moves to it when it appears without trapping. Once answered it collapses back to a Trace line ("Approved: sent 3 emails" or "Denied: send 3 emails").
- **Citations:** a claim that rests on a source carries a numbered footnote marker (`[1]`, superscript, `link` colour, a real link with an accessible name "Source 1: <title>"). After the answer a "Sources" panel lists the numbered sources with title, host name and date, deduplicated by URL, opening in a new tab with a screen-reader notice.
- **Error after a partial answer:** keep the text already shown. Mark the turn failed below it in words with an icon — "Answer incomplete: the connection to the agent was lost." — in `destructive`, and offer "Retry" (secondary) that regenerates the turn. Never erase the partial text or replace it with a generic error.
- **Empty state:** a short serif title ("What can I help with?"), one line on what the agent can do and its limits, then three or four suggested prompts as outline buttons whose label is the exact prompt sent. On narrow screens they stack or scroll sideways inside their row.
- **Composer:** a textarea with a visible label (may be visually hidden), Send as a primary icon button with an accessible name, Stop replacing Send while running.

## Do's and Don'ts

- Do keep one primary action per region; don't put two primary buttons side by side.
- Do say status in words ("Ran", "Failed", "Incomplete"); don't rely on colour, opacity or an icon alone.
- Do keep the partial answer and offer Retry after a stream error; don't erase visible text or show only a toast.
- Do put the action, what it affects and the consequence in the approval card before its buttons; don't ask "Are you sure?" without saying what happens.
- Do style Deny as outline; don't style Deny or Cancel as destructive.
- Do keep reasoning and tool output collapsed by default; don't auto-expand them or reopen them after the person closed them.
- Do use one subtle streaming indicator; don't stack spinners, typing dots and shimmer.
- Do number citations and list sources after the answer; don't hide sources in a tooltip only.
- Do label assistant output "AI-generated" in words; don't use sparkles, glows, gradients or purple to mean AI.
- Do set answers in the serif at 17/28 with a 68ch measure; don't set long answers in 14 px sans across the full width.
- Do use tokens through shadcn variables; don't use raw Tailwind palette colours, `dark:` colour overrides, hex in components or shadows on cards.
- Do use a 2 px solid focus outline in `ring`; don't keep shadcn's `ring-ring/50` or remove outlines.
- Do keep secondary text at full `muted-foreground`; don't dim text with opacity modifiers such as `/70`.
- Do self-host fonts from `@fontsource-variable`; don't link a font CDN.
- Do write sentence case; don't use title case, all caps labels or exclamation marks.
- Don't leave shadcn defaults in the theme file (Geist, `--radius: 0.625rem`, the stock neutral values); run `scripts/check_theme.py` from this skill.

## Motion

Motion explains a change of state; it is never decoration.

- **Durations:** 150 ms for hover, press, menus and tooltips; 200 ms for collapsibles, Trace rows, dialogs and sheets. Nothing longer.
- **Easing:** enter with `cubic-bezier(0, 0, 0.2, 1)`, exit with `cubic-bezier(0.4, 0, 1, 1)`. No bounce, spring, parallax or looping motion other than the single streaming indicator.
- **Reduced motion:** under `prefers-reduced-motion: reduce`, remove translate and scale, keep only opacity changes of 100 ms or less, and stop the shimmer (shadcn's `tailwind.css` already stops it; keep `motion-reduce:shimmer-none`).

## Brand override

A client brand may change only these tokens; everything else is fixed.

1. **Accent ramp:** `primary`, `primary-hover`, `primary-active`, `primary-foreground`, `accent`, `accent-foreground`, `ring`, `chart-1`, and their `dark-` twins (the `sidebar-primary*` and `sidebar-ring` tokens follow by reference). Keep the ramp's roles: primary carries white-ish text, accent is the subtle step, ring is focus only.
2. **Font families:** the three `fontFamily` values and the matching `--font-sans`, `--font-serif` and `--font-mono` stacks, only if the client holds a web licence for self-hosting, keeping the three roles and the house fallbacks. Sizes, weights and line heights stay.
3. **Logo:** an SVG or image in the header slot, with alternative text.
4. **Radius (optional):** one step for controls, 4 px or 8 px instead of 6 px. Nothing rounder.

Neutrals, semantic colours, borders, spacing, density, elevation, motion, focus treatment and copy rules do not change. After any override, `npx -y @google/design.md@0.4.0 lint` must report zero errors and zero warnings, and every 3:1 pair in the Colors table must be recomputed and still pass. If a pair fails, adjust the client step, never the floor.
