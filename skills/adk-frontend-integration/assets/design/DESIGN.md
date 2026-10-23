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
  destructive-foreground: "oklch(0.985 0.003 85)"
  success: "oklch(0.47 0.09 150)"
  warning: "oklch(0.50 0.10 65)"
  info: "oklch(0.48 0.07 220)"
  success-subtle: "oklch(0.955 0.025 150)"
  warning-subtle: "oklch(0.955 0.03 75)"
  destructive-subtle: "oklch(0.955 0.022 27)"
  info-subtle: "oklch(0.955 0.02 220)"
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
  dark-success-subtle: "oklch(0.27 0.03 150)"
  dark-warning-subtle: "oklch(0.27 0.03 70)"
  dark-destructive-subtle: "oklch(0.27 0.035 27)"
  dark-info-subtle: "oklch(0.27 0.025 220)"
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
  xl: 12px
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
  status-success-subtle:
    backgroundColor: "{colors.success-subtle}"
    textColor: "{colors.success}"
    typography: "{typography.caption}"
    rounded: "{rounded.sm}"
  status-warning-subtle:
    backgroundColor: "{colors.warning-subtle}"
    textColor: "{colors.warning}"
    typography: "{typography.caption}"
    rounded: "{rounded.sm}"
  status-danger-subtle:
    backgroundColor: "{colors.destructive-subtle}"
    textColor: "{colors.destructive}"
    rounded: "{rounded.lg}"
  status-info-subtle:
    backgroundColor: "{colors.info-subtle}"
    textColor: "{colors.info}"
    typography: "{typography.caption}"
    rounded: "{rounded.sm}"
  text-on-status-subtle:
    backgroundColor: "{colors.destructive-subtle}"
    textColor: "{colors.foreground}"
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
  composer:
    backgroundColor: "{colors.popover}"
    textColor: "{colors.popover-foreground}"
    typography: "{typography.body-md}"
    rounded: "{rounded.xl}"
    padding: 8px
  composer-placeholder:
    backgroundColor: "{colors.popover}"
    textColor: "{colors.muted-foreground}"
  side-panel:
    backgroundColor: "{colors.card}"
    textColor: "{colors.card-foreground}"
    rounded: "{rounded.xl}"
  approval-card:
    backgroundColor: "{colors.card}"
    textColor: "{colors.card-foreground}"
    rounded: "{rounded.lg}"
    padding: 16px
  citation-chip:
    backgroundColor: "{colors.muted}"
    textColor: "{colors.muted-foreground}"
    typography: "{typography.caption}"
    rounded: "{rounded.sm}"
  citation-chip-hover:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.accent-foreground}"
  source-chip:
    backgroundColor: "{colors.muted}"
    textColor: "{colors.foreground}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.md}"
  suggestion-card:
    backgroundColor: "{colors.card}"
    textColor: "{colors.card-foreground}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 12px
  greeting:
    backgroundColor: "{colors.background}"
    textColor: "{colors.foreground}"
    typography: "{typography.display}"
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
  sidebar-group-label:
    backgroundColor: "{colors.sidebar}"
    textColor: "{colors.muted-foreground}"
    typography: "{typography.caption}"
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
  dark-status-success-subtle:
    backgroundColor: "{colors.dark-success-subtle}"
    textColor: "{colors.dark-success}"
  dark-status-warning-subtle:
    backgroundColor: "{colors.dark-warning-subtle}"
    textColor: "{colors.dark-warning}"
  dark-status-danger-subtle:
    backgroundColor: "{colors.dark-destructive-subtle}"
    textColor: "{colors.dark-destructive}"
  dark-status-info-subtle:
    backgroundColor: "{colors.dark-info-subtle}"
    textColor: "{colors.dark-info}"
  dark-text-on-status-subtle:
    backgroundColor: "{colors.dark-destructive-subtle}"
    textColor: "{colors.dark-foreground}"
  dark-composer:
    backgroundColor: "{colors.dark-popover}"
    textColor: "{colors.dark-popover-foreground}"
  dark-citation-chip:
    backgroundColor: "{colors.dark-muted}"
    textColor: "{colors.dark-muted-foreground}"
  dark-citation-chip-hover:
    backgroundColor: "{colors.dark-accent}"
    textColor: "{colors.dark-accent-foreground}"
  dark-source-chip:
    backgroundColor: "{colors.dark-muted}"
    textColor: "{colors.dark-foreground}"
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
  dark-sidebar-group-label:
    backgroundColor: "{colors.dark-sidebar}"
    textColor: "{colors.dark-muted-foreground}"
---

# House design system

The house theme for web interfaces in front of ADK agents. Copy this file to `docs/design/DESIGN.md` in the target project, map it to the shadcn theme file as described under Colors, and keep the two in step. The format is Google's DESIGN.md (`version: alpha`); lint it with `npx -y @google/design.md@0.4.0 lint docs/design/DESIGN.md` and treat any error **or warning** in the JSON `summary` as a failure, because 0.4.0 reports contrast failures as warnings and exits 0 on them.

## Overview

A quiet working tool for people who read, check and approve what an agent did. It should feel like good paper and ink: warm near-neutral greys, one deep ink-blue accent kept for actions, selection and focus, and type chosen for long reading. It is not a marketing page and it does not look "AI": no gradients, glass, glow, neon or purple, no sparkle icons and no animated backgrounds. The chrome stays calm so the content can be loud: few borders, a dimmed sidebar, and the agent's work shown as things people can check (claims linked to passages, steps folded into one honest line, approvals that show exactly what will happen).

- **Density:** comfortable by default (32 px controls, 36 px table rows); compact mode (28 px controls and rows) for data-dense screens only.
- **Copy:** sentence case everywhere — buttons, titles, menu items, column headers, tabs. Plain verbs on buttons ("Approve", "Retry"). No exclamation marks and no first-person claims of feeling. This is a house choice: some companion skills and client brand guides use title case for buttons and headings; inside a house app, sentence case wins unless a client brand override says otherwise in writing.
- **Accessibility floor:** WCAG 2.2 AA. Every text pair, at any size, is at least 4.5:1. Field edges, focus indicators, checkbox and radio edges, chart marks and the check-before-use underline are at least 3:1 against what they sit on. Pointer targets are at least 24 × 24 px; run axe with the `target-size` rule switched on, because axe-core 4.14.0 ships it disabled.
- **Two sections follow the eight spec sections:** Motion and Brand override. The linter keeps them as unknown headings.

## Colors

Colour token names are the shadcn CSS variable names; tokens prefixed `dark-` are the same variables under `.dark`. Map them one to one into the project's `tailwind.css` file (the `tailwind.css` field of `components.json`): `colors.muted-foreground` becomes `--muted-foreground` in `:root`, and `colors.dark-muted-foreground` becomes `--muted-foreground` in `.dark`. Keep the `oklch()` values exactly as written. `primary-hover`, `primary-active`, `destructive-foreground`, `success`, `warning`, `info` and the four `*-subtle` surfaces are house additions: declare them in both scopes and register each in `@theme inline` as `--color-<name>: var(--<name>)`. Never use raw Tailwind palette colours (`text-green-600`) or `dark:` colour overrides; use the tokens.

- **Neutrals:** hue 85, chroma at most 0.008 — paper, not screen grey. `background` is the canvas, `card` and `popover` one step lighter, `muted` and `secondary` one step darker for bands and quiet buttons. `sidebar` sits one step darker than the canvas.
- **Accent ramp (ink blue, hue 250):** `primary` (#1F4A73) for the one main action per view, links and selected items; `primary-hover` (#153758) and `primary-active` (#0F2840) for pointer states; `accent` (#E8EFF6) is the subtle step for hover rows, menu highlights, the selected-row fill and a pressed toggle; `ring` (#32669A) is the focus colour and is used for nothing else. Hue 250 is kept well away from the 277–293 band of generic "AI purple".
- **Semantic colours, muted:** `success` (#31693F), `warning` (#8A5619), `destructive` (#A83630) and `info` (#276779) are text and icon colours at chroma 0.15 or less. Status is always also said in words or an icon; never by colour alone.
- **Status surfaces (tinted, subtle):** `success-subtle` (#E5F5E7), `warning-subtle` (#FCEEDB), `destructive-subtle` (#FFEBE8) and `info-subtle` (#E2F4FA) sit at L 0.955 with chroma 0.02–0.03 in the same hue as their colour; in dark mode they sit at L 0.27 (#1C2B1F, #302416, #36201D, #18292F). Each carries its own semantic colour as text, plus `foreground` and `muted-foreground`. Use them for status badges ("Waiting for approval", "Approved"), the environment badge and the incomplete-answer notice. They are fills, never borders, and never a whole region or page.
- **Lines:** `border` (#E1DFDC) is a decorative hairline between regions and may be below 3:1. `input` (#888681) is the edge of a field, checkbox or control that has no other boundary, including the composer card, and must stay at 3:1 or more.
- **Dark mode is designed, not inverted:** surfaces step up in lightness (background #131311, card #1A1917, popover #21201E, muted #242320) so layers read without shadows; the accent flips to a light step (#93BCE6) carrying a dark label; edges are opaque (`dark-input` #797772), never white at 10–15%.

Measured contrast (WCAG 2.x, sRGB, worst surface each colour sits on):

| Pair | Light | Dark | Floor |
|---|---|---|---|
| foreground on background / card / popover | 17.3 / 17.8 / 17.8 | 15.9 / 15.0 / 13.9 | 4.5 |
| muted-foreground on muted (worst surface) | 6.1 | 6.7 | 4.5 |
| muted-foreground on popover (composer placeholder) / sidebar | 6.8 / 6.4 | 6.9 / 7.6 | 4.5 |
| primary-foreground on primary / hover / active | 8.8 / 11.7 / 14.4 | 9.1 / 11.1 / 7.3 | 4.5 |
| primary as link text on background | 8.9 | 9.4 | 4.5 |
| accent-foreground on accent (pressed toggle, citation chip hover) | 11.8 | 10.8 | 4.5 |
| success, warning, destructive, info on muted | 5.8, 5.5, 5.8, 5.7 | 7.6, 8.3, 6.0, 7.5 | 4.5 |
| success, warning, destructive, info on their own `*-subtle` | 5.75, 5.37, 5.66, 5.62 | 7.18, 8.02, 5.80, 7.15 | 4.5 |
| foreground / muted-foreground on any `*-subtle` (worst) | 15.6 / 6.0 | 12.7 / 6.3 | 4.5 |
| chart-1 … chart-5 on muted | 5.4, 5.1, 5.1, 5.4, 5.3 | 6.8, 7.1, 8.4, 6.3, 6.0 | 3.0 (4.5 met) |
| input edge on background / card / popover / muted / accent | 3.5 / 3.6 / 3.6 / 3.25 / 3.1 | 4.2 / 3.9 / 3.6 / 3.5 / 3.1 | 3.0 |
| ring on muted / popover / worst `*-subtle` | 5.4 / 5.9 / 5.2 | 6.8 / 7.1 / 6.5 | 3.0 |
| warning (check-before-use underline) on background | 5.9 | 9.9 | 3.0 |
| border on background | 1.3 | 1.4 | decorative only |

The `components` block holds one entry per text-on-surface pair so the linter checks each one at 4.5:1. The linter does not check 3:1 non-text pairs; recompute the `input`, `ring` and underline rows after any change. On 23 October 2026, 224 pairs were recomputed from these tokens with an OKLCH-to-sRGB script; the smallest margins were warning on `sidebar-accent` (5.06, light) and `input` on `accent` (3.13, dark).

## Typography

Three open families (SIL OFL 1.1), self-hosted from npm and bundled at build time. Never load fonts from a font CDN at run time.

| Role | Package (tested) | CSS variable and stack |
|---|---|---|
| Interface | `@fontsource-variable/inter@5.3.0` | `--font-sans: "Inter Variable", ui-sans-serif, system-ui, sans-serif` |
| Headings and assistant answers | `@fontsource-variable/source-serif-4@5.3.1` (import `wght.css`) | `--font-serif: "Source Serif 4 Variable", Georgia, "Times New Roman", serif` |
| Code, identifiers, tool arguments | `@fontsource-variable/jetbrains-mono@5.3.0` | `--font-mono: "JetBrains Mono Variable", ui-monospace, SFMono-Regular, Menlo, monospace` |

- **Serif file:** import `wght.css`, not `opsz.css`. The latin `opsz` file is 122 KB against 51 KB for `wght` (5.3.1, measured 23 October 2026). Answers are set at 17 px, close to the text optical size the `wght` file is drawn at, so optical sizing would change only the 28 and 36 px headings, and slightly. That gain does not justify 71 KB on every first load.
- **Scale:** the typography tokens above, px size / line height: display 36/44, headline-lg 28/36, headline-md 22/30 (serif, 600); title-md 16/24 (sans, 600); body-md 14/20 is the interface default; body-sm 13/18; label-md 13/16 (500); caption 12/16; answer-md 17/28 (serif, 400); code-sm 13/20.
- **Weights:** 400, 500 and 600 only. Tracking −0.01em at 22 px and above, otherwise 0.
- **Answers:** assistant answers are set in `answer-md` with a measure of about 68ch, `text-wrap: pretty`, curly quotes and the ellipsis character. The serif is one step larger than the interface text because its x-height is smaller.
- **Answer formatting:** the first sentence answers the question directly; paragraphs run to three sentences at most; detail, tables and lists come after. No greeting, no praise of the question, and any limit ("I could not find…") is said plainly where it applies. Inside an answer: `h3` in title-md and `h4` in body-md at 600 (both sans); lists keep the serif with a `muted-foreground` marker and 4 px between items; tables in `data-md` with tabular figures, hairline rows, `label-md` headers in `muted-foreground` and right-aligned numbers, scrolling inside their own focusable region on narrow screens; inline code in the mono at 0.82 em on `muted`; code blocks in `code-sm` on `muted` with a 6 px radius, a language label and a Copy button. The wording belongs in the agent instruction; this file fixes how it is set.
- **Numbers:** tables, metrics, timestamps, token counts and durations use tabular figures (`data-md`, Tailwind `tabular-nums`).
- **Default size:** set `body` to body-md (14/20); Tailwind's preflight leaves it at 16 px.
- **Implementation:** turn each token into an `@utility type-<token>` in the theme file. Do not register `--text-*` keys for them, because shadcn's `cn()` treats unknown `text-*` classes as colours. Keep `--font-heading` on the sans for small component titles (card and dialog titles); page headings use the serif utilities. Declare `--font-*` in a plain `@theme` block (not `inline`) so a brand can override them at run time.

## Layout

- **Grid:** an 8-point rhythm with 4 px half-steps. Tailwind's `--spacing` stays `0.25rem`; use the steps 4, 8, 12, 16, 24, 32, 48 and 64 px (`spacing` tokens). Other values need a reason.
- **Density:** comfortable — controls 32 px (`h-8`, the default of shadcn's Base UI `nova` style: `shadcn init -b base -p nova`), table rows 36 px, card padding 16 px. Compact — controls and rows 28 px, card padding 12 px, for data-dense screens only, switched per screen and never mixed in one view. No target below 24 px.
- **Page:** content at most 1200 px wide; 16 px side gutter below 768 px, 24 px from 768 px, 32 px from 1280 px. No horizontal page scroll at 375 px; wide tables and code scroll inside their own container.
- **App shell:** shadcn `Sidebar` with `collapsible="icon"`, then a `SidebarInset` holding a 48 px header and the work area. The sidebar is expanded (256 px) from 1024 px, an icon rail (48 px) from 768 px, and a `Sheet` below 768 px. The header keeps one line at every width: sidebar toggle, conversation title (truncated), environment badge, side-panel toggle, and a new-conversation icon below 768 px.
- **Conversation column:** one centred column at most 768 px wide; answer prose at about 68ch; 32 px between turns. The thread scrolls inside its own region; the composer floats over its bottom edge with a 24 px fade above it, and the thread has bottom padding and `scroll-padding-bottom` at least the composer's height so the last line and focused items are never hidden behind it.
- **Side panel:** at 1024 px and wider, a shadcn `Resizable` panel beside the conversation, 400 px by default, 360–480 px, inset 8 px from the edges. Below 1024 px the same content opens in a right-hand `Sheet`. Its open state lives in the URL (`?panel=sources`).
- **Empty state:** its own screen, never beside a thread. The greeting sits at about 38% of the viewport height, the composer directly under it, the suggestions under that, in a column at most 720 px wide.

## Elevation & Depth

Depth comes from surface lightness and hairlines, not shadows.

- **Flat by default:** cards, panels, tables and messages are separated by a 1 px `border` hairline or a surface step. Set `--shadow-xs: 0 0 #0000` and remove shadows from cards and inputs.
- **One elevation, for floating layers only:** popovers, menus, tooltips, hover cards, dialogs, sheets and the composer use `0 1px 2px rgb(24 23 20 / 0.06), 0 8px 24px rgb(24 23 20 / 0.08)` plus their hairline. The composer is the only in-flow element with it, because it floats over the thread. Nothing else casts a shadow.
- **Scroll fade:** the thread fades into the canvas over 24 px above the composer (`linear-gradient` from transparent to `background`). It shows that text continues underneath; it is not a decorative gradient, and no other gradient is allowed.
- **Dark mode:** separate layers by surface lightness (`dark-popover` is lighter than `dark-card`; the composer uses `popover`); keep the hairline, drop every shadow by setting `--shadow-md` and `--shadow-lg` to `0 0 #0000` under `.dark`.
- **Scrims:** dialogs and sheets dim the page with the light-mode `foreground` value (`oklch(0.205 0.006 85 / 0.4)`) in both modes, so the scrim darkens in dark mode too; no blur.

## Shapes

- **Radius steps:** 4 px (`rounded.sm`: badges, menu items, sidebar rows, inline code, citation chips, checkboxes), 6 px (`rounded.md`: buttons, inputs, selects, tabs, follow-up chips, code blocks), 8 px (`rounded.lg`: cards, the approval card, popovers, hover cards, message bubbles, suggestion cards, the incomplete-answer notice) and 12 px (`rounded.xl`: the composer, the side panel, sheets and dialogs only). `full` is for avatars and status dots only. Nothing else is rounder: no pill buttons, and controls never take the 12 px step.
- **Tailwind mapping:** set `--radius: 0.375rem` and pin the steps instead of deriving them: `--radius-sm: 4px`, `--radius-md: 4px`, `--radius-lg: 6px`, `--radius-xl: 8px`, `--radius-2xl: 12px`, and `--radius-3xl` and `--radius-4xl` both `8px`, so stock classes such as the badge's `rounded-4xl` cannot become pills. The names do not line up: `rounded.md` (6 px) is Tailwind's `rounded-lg`, which `base-nova` buttons and inputs already use; `rounded.lg` (8 px) is `rounded-xl`, which its cards use; `rounded.xl` (12 px) is `rounded-2xl`. Write `rounded-xl`, not `rounded-lg`, for a card. Give badges `rounded-sm` (they ship as `rounded-4xl`). Declare the radius steps in a plain `@theme` block so the brand's control radius can override `--radius-lg` at run time.
- **Lines:** 1 px hairlines. Focus is a 2 px solid `ring` outline with a 2 px offset, drawn with `outline` (it survives forced-colours mode), replacing shadcn's `ring-3 ring-ring/50` box-shadow. Implement it as an unlayered `:focus-visible` rule that also sets `--tw-ring-shadow: 0 0 #0000`, and remove `outline-ring/50` from the base layer. The composer draws the outline on its whole card while its text area has focus (`:has(textarea:focus-visible)`), not inside the field.
- **Icons:** Lucide, 16 px in controls and 14 px in chips and source rows, 1.5–2 px stroke, `currentColor`. No filled or multicolour icons, and few icons in navigation: conversation rows carry none.

## Components

Use shadcn/ui (Base UI) components first; edit their `cva` variants to these rules rather than overriding with `className`. Control heights move together across button, input, select, toggle and tabs.

- **Buttons:** primary for the single main action in a region; secondary or outline for the rest; ghost for icon buttons in toolbars and message footers (with a tooltip and an `aria-label`); destructive only when the effect destroys something. Hover darkens to `primary-hover`, press to `primary-active`; no translate, scale or opacity-dimmed hover.
- **Inputs and selects:** `card` fill, `input` edge, 6 px radius, 32 px tall; the error state adds a `destructive` edge and a message in words below the field.
- **Badges:** 4 px radius, caption type, `secondary` fill or outline; status badges use the matching `*-subtle` fill with the semantic colour as text and add an icon or word, never colour alone.
- **Cards and panels:** hairline border, 8 px radius, no shadow. In the conversation thread, the approval card is the only bordered card.
- **Tabs:** the `line` variant in panels; inactive tabs in full `muted-foreground`, the active tab in `foreground` with the 2 px underline.

App shell and screens around the conversation:

- **Sidebar:** `sidebar` surface, one step darker than the canvas, with a hairline to the work area and no borders between items. Header: the workspace or client logo slot (logo image, workspace name in `label-md`, product name in `caption`), then "New conversation" and "About this assistant". Content: conversation history grouped by date ("Today", "Yesterday", "Previous 7 days", "Previous 30 days"), group labels in `caption` and full `muted-foreground`, 32 px rows with titles truncated, the current conversation marked with `sidebar-accent` and `aria-current="page"`. Footer: the user (initials avatar, name, role) opening a menu with theme and sign out. In icon mode the history hides and the remaining items show tooltips.
- **Header:** conversation title (`body-md`, 500, truncated) as the page `h1`, the environment badge, then the side-panel toggle (`aria-pressed`). Nothing else.
- **Environment badge:** an `info-subtle` badge naming the environment ("Pilot"; in replay mode, the replay label that demo readiness defines), with a visually hidden "Environment:" prefix. Never "Demo" or "Test".
- **Empty state:** a serif greeting in `display` (`headline-lg` below 640 px), one line on what the assistant can and cannot do ("I can read delivery and contract records and draft supplier emails. I cannot change contracts, and I ask before sending anything."), the composer, then a 2 × 2 grid of suggestion cards (one column below 640 px). Each card is a button on `card` with a hairline and 8 px radius: an icon in `muted-foreground`, the exact prompt it sends in `body-md` 500, and one muted line on the data it uses.

Agent conversation patterns (build on shadcn's AI Elements patterns and `Trace`; hand-build only where shadcn has no component):

- **Messages:** assistant answers are full-width prose in the column, no bubble, set in `answer-md`; user messages are compact `user-message` bubbles aligned to the end, `body-md`, at most 80% of the column. New turns enter with the turn entrance under Motion.
- **Per-answer actions:** a quiet footer of ghost icon buttons after each answer: Copy (keeps formatting and tables), Copy with sources (appends the numbered source list), Good response and Bad response (toggles with `aria-pressed`) and Retry.
- **Follow-ups:** after a finished answer, two or three follow-up prompts as small outline buttons (6 px radius) whose label is the exact prompt sent. None after a failed or running turn.
- **AI-generated label:** every assistant answer carries the words "AI-generated" in `ai-label` style (caption, `muted-foreground`, no icon glow or gradient). It opens a popover with the model, the sources used and the time of the answer. It is never decoration, never an action and never disabled; once a person edits the content, replace it with an "Edited" note and a revert control.
- **Streaming:** one subtle indicator at a time — shadcn's `shimmer` on the live status line ("Writing answer…"), or a 6 px `muted-foreground` caret at the end of the text. No spinners in the prose, no custom keyframes. Stop is reachable for the whole run. Announce completion, not each token: the transcript is an `aria-live="polite"` log, `aria-busy="true"` while streaming.
- **Tool steps while running:** one quiet `Trace` per run of steps, one `TraceLine` per step, `trace-line` style in `muted-foreground`. The title states the status in words and tense — "Running query…", "Ran query", "Failed to run query" — with an icon as a second cue; failures use `destructive` text plus the word "Failed". Running and finished steps stay visible while the turn is working. Rows become collapsible only once they have output; never dim a line with opacity. shadcn 4.22.1's `TraceDescription` ships `text-muted-foreground/70`, which axe measured at 3.3:1 on the house background (2.7:1 on stock tokens); change it to `text-muted-foreground`.
- **Folded steps:** once a turn finishes, its Trace folds into one summary line above the answer: duration, step count, failures in `destructive`, then scope or effects ("Worked for 4 s · 3 steps · 1 failed · searched 42 contracts", "Worked for 6 s · 2 steps · sent 3 emails after approval by Priya Shah at 14:02"), in `body-sm` `muted-foreground` with tabular figures and a chevron. It expands to the TraceLines. The separators are hidden from screen readers and replaced by commas.
- **No reasoning display:** do not show model reasoning text or a "Thought for 4 s" line. Show only real tool steps; reasoning text reads as proof and can be a rationalisation after the fact.
- **Citations:** a claim that rests on a source carries a numbered chip right after that claim, not at the end of the paragraph: `citation-chip` (caption, `muted` fill, `muted-foreground`, 4 px radius, 18 px tall), turning `accent` on hover. It is a real link with an accessible name that describes the source and place ("Source 1: Q3 delivery performance report, page 4"). Hover or focus opens a `HoverCard` (a `Popover` on touch) that quotes the supporting passage, says where it sits (page, clause, paragraph), gives host and date, and links "Open at passage". Do not put a row or block of source chips after the answer; end with a "View all 4 sources" ghost button that opens the side panel. Keep sources deduplicated by URL.
- **Check before use:** a figure, date or amount the model derived (calculated, converted or summed) rather than quoted gets a dotted 2 px `warning` underline, a tooltip that starts "Check before use." and says how it was derived, and visually hidden text with the same words. Quoted figures carry a citation instead. The line under the composer says "Check figures against the source before acting."
- **Side panel:** a `side-panel` (card surface, hairline, 12 px radius) with `line` tabs for Sources and Drafts and a Close button. Each source lists its number, title, document-type icon, host and date, what it was cited for, and the cited passage with its location, separated by hairlines rather than boxes. Drafts list each item waiting for approval with its status badge.
- **Approval card:** ask for approval only when an action has an effect; never for reads, and approve several similar effects as one batch. A pending approval is the one bordered `approval-card` in the thread, outside the Trace. Header: a Lucide icon for the action, the title ("Send 3 emails") in `title-md` and a "Waiting for approval" badge on `warning-subtle`. Body: a definition list with `label-md` `muted-foreground` labels — Action, Affects ("Brackwater Freight, Harbour Metals and Lindqvist Packaging (3 external recipients)"), Consequence ("Recipients see the emails immediately. Sent email cannot be recalled.") — then the exact item being approved (recipients, subject and full email text, or the ticket fields) on a `muted` band, in a collapsible that is open by default. Footer, aligned to the end: "Deny" (outline, never destructive) and "Approve" (primary; destructive variant only when the effect is destructive). It is a labelled `role="group"`, keyboard-operable in tab order with visible focus. When it appears while the reader is at the live edge, focus moves to it without trapping; when the reader has scrolled up, the view stays put, the jump-to-latest control shows a badge and the status region announces it. Once answered it collapses back to a Trace line ("Approved: sent 3 emails" or "Denied: send 3 emails") and the folded summary names the effect.
- **Error after a partial answer:** keep the text already shown. Below it, an unbordered notice on `destructive-subtle` (8 px radius) with an icon and the words in `destructive` — "Answer incomplete: the connection to the agent was lost. The text above is partial." — and "Retry" (outline, so it stands out from the tinted surface) that regenerates the turn. Never erase the partial text or replace it with a generic error.
- **Composer:** a two-row `composer` card: a text area at least 56 px tall above, a tool row below with ghost icon buttons on the left (Attach, and a sources toggle that names the sources in use, "Contract library, Delivery records", shown pressed on `accent`) and a 32 px primary icon button on the right — Send, replaced by Stop (a filled square) while a run is going. `popover` surface, `input` edge, 12 px radius, the floating shadow, no hairline across the column above it. The text area has a visible or visually hidden label. Enter sends, Shift+Enter adds a line, and Enter during IME composition does not send.
- **Data line:** one caption line under the composer, centred, in `muted-foreground`: where data is kept and how it is used, then what to check ("Data stays in the UK (europe-west2) and is not used for training. Check figures against the source before acting."). Use the deployment's real region and retention; in a demo, the fictional values must still be plausible for the stated region.

## Do's and Don'ts

- Do keep one primary action per region; don't put two primary buttons side by side.
- Do say status in words ("Ran", "Failed", "Incomplete"); don't rely on colour, opacity or an icon alone.
- Do keep the partial answer and offer Retry after a stream error; don't erase visible text or show only a toast.
- Do put the action, what it affects, the consequence and the exact item in the approval card before its buttons; don't ask "Are you sure?" without saying what happens, and don't hide the email text behind a closed preview.
- Do ask for approval only for actions with effects; don't gate reads or ask once per item in a batch.
- Do style Deny as outline; don't style Deny or Cancel as destructive.
- Do fold finished steps into one summary line and keep tool output collapsed; don't auto-expand them, reopen them after the person closed them, or show model reasoning text.
- Do use one subtle streaming indicator; don't stack spinners, typing dots and shimmer.
- Do put a numbered chip next to each claim, with the quoted passage in its preview; don't add a row of source chips after the answer or hide sources in a tooltip only.
- Do mark derived figures "check before use"; don't present a calculated amount as if it were quoted.
- Do answer in the first sentence; don't open with a greeting, praise of the question or a restatement.
- Do label assistant output "AI-generated" in words; don't use sparkles, glows, gradients or purple to mean AI.
- Do set answers in the serif at 17/28 with a 68ch measure; don't set long answers in 14 px sans across the full width.
- Do keep the approval card as the only bordered card in the thread; don't box sources, notices or steps in hairlines.
- Do use the `*-subtle` surfaces for status badges and notices; don't tint whole regions or use them as borders.
- Do keep the 12 px radius for the composer, side panel, sheets and dialogs; don't round controls, cards or chips to 12 px.
- Do give the composer the floating shadow and the canvas fade; don't add other gradients or shadows on static cards.
- Do show the empty state as its own screen; don't show it beside a running thread.
- Do use tokens through shadcn variables; don't use raw Tailwind palette colours, `dark:` colour overrides, hex in components or shadows on cards.
- Do use a 2 px solid focus outline in `ring`; don't keep shadcn's `ring-ring/50` or remove outlines.
- Do keep secondary text at full `muted-foreground`; don't dim text with opacity modifiers such as `/70`.
- Do self-host fonts from `@fontsource-variable`; don't link a font CDN.
- Do set the theme class before first paint with an inline script and `<meta name="color-scheme" content="light dark">`; don't rely on shadcn's Vite `ThemeProvider`, which applies it after first paint.
- Do write sentence case; don't use title case, all caps labels or exclamation marks.
- Do use invented brands and reserved `.example` hosts in demo data (`reports.tollmere.example`); don't use `example.com` placeholders on stage or borrowed sample brands such as Northwind or Contoso.
- Don't leave shadcn defaults in the theme file (Geist, `--radius: 0.625rem`, the stock neutral values); run `scripts/check_theme.py` from this skill.
- Don't keep the stock component classes that break these rules after `shadcn add`. Seen in shadcn 4.22.1 `base-nova` components on 23 October 2026:
  - `dark:` colour overrides (button outline and ghost, badge, tabs, input and textarea `dark:bg-input/30`);
  - text dimmed with opacity: `TraceDescription` `/70`, `SidebarGroupLabel` `text-sidebar-foreground/70`, `TabsTrigger` `text-foreground/60`;
  - the `ring-ring/50` focus shadow in place of the 2 px outline (button, badge, tabs, trace, input, textarea);
  - the press `translate-y-px` and `hover:bg-primary/80` on the primary button (use `primary-hover` and `primary-active`);
  - `transition-all` (button, badge, tabs, `SidebarRail`) and `ease-linear` on the sidebar width (use named properties and `ease-out`);
  - the sheet scrim `bg-black/10` with `backdrop-blur-xs` (use the scrim above, no blur);
  - the `message-scroller` jump button's 400 ms exit (`data-[active=false]:duration-400` with a custom ease-in curve); cap it at 200 ms.

## Motion

Motion explains a change of state; it is never decoration.

- **Durations:** 150 ms for hover, press, menus, tooltips and a new turn's entrance; 200 ms for collapsibles, Trace rows, the folded-steps line, the sidebar collapse, the side panel, dialogs and sheets. Nothing longer.
- **Easing:** enter with `cubic-bezier(0, 0, 0.2, 1)`, exit with `cubic-bezier(0.4, 0, 1, 1)` (Tailwind 4.3.3's `ease-out` and `ease-in`). No bounce, spring, parallax or looping motion other than the single streaming indicator.
- **Turn entrance:** a new turn fades in and rises 4 px over 150 ms (opacity and transform only). Streaming text, each token, trace-line text changes and anything the person triggered from the keyboard get no animation. Popovers and hover cards grow from their trigger using Base UI's `--transform-origin`, never from `scale(0)`.
- **Scrolling:** follow the stream only while the reader is at the bottom and release on any upward scroll. If shadcn's `message-scroller` (`@shadcn/react` 0.3.1) does this, cap its jump button's exit at 200 ms and scroll instantly under reduced motion.
- **Theme switch:** suppress transitions for one frame while the theme class changes.
- **Reduced motion:** under `prefers-reduced-motion: reduce`, remove translate and scale, keep only opacity changes of 100 ms or less, scroll instantly, and stop the shimmer (shadcn's `tailwind.css` already stops it; keep `motion-reduce:shimmer-none`).

## Brand override

A client brand may change only these tokens; everything else is fixed.

1. **Accent ramp:** `primary`, `primary-hover`, `primary-active`, `primary-foreground`, `accent`, `accent-foreground`, `ring`, `chart-1`, and their `dark-` twins (the `sidebar-primary*` and `sidebar-ring` tokens follow by reference). Keep the ramp's roles: primary carries white-ish text, accent is the subtle step, ring is focus only.
2. **Font families:** the three `fontFamily` values and the matching `--font-sans`, `--font-serif` and `--font-mono` stacks, only if the client holds a web licence for self-hosting, keeping the three roles and the house fallbacks. Sizes, weights and line heights stay. The skill's `apply_brand.py` takes Fontsource packages; a licensed commercial font is self-hosted and mapped to the same three variables by hand, and the client's brand otherwise applies with the house fonts.
3. **Logo:** an SVG or image in the sidebar's workspace slot and as the favicon, with alternative text (empty when the workspace name sits next to it).
4. **Radius (optional):** one step for controls, 4 px or 8 px instead of 6 px. Nothing rounder. The 8 px card step and the 12 px step for the composer, side panel, sheets and dialogs do not change.

Neutrals, semantic colours, the `*-subtle` status surfaces, borders, spacing, density, elevation (including the composer shadow and the scroll fade), motion, focus treatment, the conversation patterns and copy rules do not change. After any override, `npx -y @google/design.md@0.4.0 lint` must report zero errors and zero warnings, and every 3:1 pair in the Colors table must be recomputed and still pass. If a pair fails, adjust the client step, never the floor.
