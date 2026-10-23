# A house DESIGN.md: warm paper, ink-blue accent, three open fonts

The house design system should be **one Google-format `DESIGN.md`**, linted with `@google/design.md@0.4.0`. Each colour token in it should be named after the shadcn CSS variable it feeds, so the mapping to `:root` and `.dark` is one to one. The look it should describe:

- **Colour:** warm near-neutral greys (hue 85, chroma no more than 0.008) with a single deep ink-blue accent (`oklch(0.40 0.085 250)`, hex `#1F4A73`). The semantic colours (green, amber, brick red) are muted, and there are no gradients or glass. Every text pair below clears 4.5:1 in both light and a designed dark mode, and every control boundary and focus ring clears 3:1.
- **Fonts:** **Inter** for the interface, **Source Serif 4** for headings and long-form answers, and **JetBrains Mono** for code. All three are SIL OFL 1.1 and self-hosted from `@fontsource-variable/*`.
- **Shape and spacing:** a pinned radius scale (4, 6, 8 px) instead of shadcn's 0.625rem default, a 4 px spacing grid, and 32 px controls on shadcn's `nova` style. Elevation is hairlines, with shadows only on floating layers.
- **Motion and copy:** motion runs 100 to 250 ms and switches off under `prefers-reduced-motion`. Copy is in sentence case.
- **What clients may change:** the accent ramp, licensed fonts, the logo and, optionally, the radius step. Everything else is house.

Three findings shape the implementation:

- **shadcn's own defaults fail the house's accessibility floor.** At shadcn 4.22.1 the default focus ring (`ring-ring/50`) measures 1.54:1 against white, `muted-foreground` on `muted` is 4.34:1, and the input border is 1.26:1. A themed app that keeps them fails review, so the checker should look for the exact default values listed below.
- **The DESIGN.md CLI checks less than its spec promises.** Contrast is checked only for `components` pairs, at 4.5:1. Errors the spec calls fatal come out as warnings, and lint exits 0 on warnings. The CI gate must therefore parse the JSON for both errors and warnings.
- **The export is a comparison aid, not the theme.** `export --format css-tailwind` writes Tailwind `@theme` keys in hex. Those are not shadcn's `:root` variables, so the theme file has to come from shadcn's DESIGN.md workflow.

Everything here was read or run on 23 October 2026.

## The DESIGN.md format, as specified and as shipped

### Pin 0.4.0 and read the spec at a commit

- **Version to pin:** [`@google/design.md`](https://registry.npmjs.org/@google/design.md) has `latest` at **0.4.0**, published 27 July 2026. Earlier releases were 0.1.0 and 0.1.1 (21 April), 0.2.0 (26 May) and 0.3.0 (15 June).
- **Where the source is:** the repository [google-labs-code/design.md](https://github.com/google-labs-code/design.md) was read at commit `6e5da53` (16 October 2026, "allow interleaved YAML code blocks"). It has about 28.5k stars.
- **Licence:** Apache-2.0 ([LICENSE](https://github.com/google-labs-code/design.md/blob/6e5da5382f41edbba9d73b2c62f33f32e9971f15/LICENSE)). The npm tarball ships the same LICENSE file, but its `package.json` has no `license` field, so licence scanners that read only that field will report it as unknown.
- **Format status:** the format version is `alpha`, and the README warns that the spec, schema and CLI will change ([README](https://github.com/google-labs-code/design.md/blob/6e5da5382f41edbba9d73b2c62f33f32e9971f15/README.md)).
- **Binaries:** the package exposes two names, `design.md` and `designmd`. The dot-free alias exists because Windows resolves `design.md` as a Markdown file.

### Tokens: five groups, CSS colours, `{path}` references

The [spec](https://github.com/google-labs-code/design.md/blob/6e5da5382f41edbba9d73b2c62f33f32e9971f15/docs/spec.md) defines this schema:

```yaml
version: <string>          # optional, "alpha"
name: <string>
description: <string>      # optional
omitted: <string[] | {section, reason}[]>   # optional, silences missing-section findings
colors:     { <token>: <Color> }
typography: { <token>: <Typography> }
rounded:    { <level>: <Dimension> }
spacing:    { <level>: <Dimension | number> }
components: { <component>: { <property>: <value | {reference}> } }
```

- **Color:** any CSS colour string is allowed: hex, named, `rgb()`/`hsl()`/`hwb()`, `oklch()`/`oklab()`/`lch()`/`lab()` or `color-mix(in srgb, …)`.
  - The linter converts every colour to sRGB for its contrast checks.
  - The spec still recommends hex as the default.
- **Dimension:** a number with `px`, `em` or `rem`.
- **Typography:** an object with these keys:
  - `fontFamily`
  - `fontSize`
  - `fontWeight` (a number)
  - `lineHeight` (a Dimension, or a unitless multiplier)
  - `letterSpacing`
  - `fontFeature` (maps to `font-feature-settings`)
  - `fontVariation` (maps to `font-variation-settings`)
- **References:** `{colors.primary}`.
  - Most groups must point at a single value, not a group.
  - `components` may also reference composite values such as `{typography.label-md}`.
  - A colour may reference another colour. In a test run, `primary: "{colors.brand-700}"` linted clean and exported resolved.
- **Component properties:** only eight are recognised: `backgroundColor`, `textColor`, `typography`, `rounded`, `padding`, `size`, `height` and `width`.
  - Any other property (for example `borderColor`) is accepted with a warning.
  - Hover and pressed states are written as sibling keys, such as `button-primary-hover`.
- **Where tokens go:** in YAML front matter, or (spec text since commit `6e5da53`) in fenced ` ```yaml ` blocks interleaved through the sections. A top-level key may be defined only once across the whole file.
- **Unknown content:** headings and token names the spec does not know are kept. A duplicate section heading or a duplicate top-level key is meant to reject the file.
- **Suggested names (non-normative):**
  - Colours: `primary`, `secondary`, `tertiary`, `neutral`, `surface`, `on-surface`, `error`.
  - Typography: `headline-display`, `headline-lg/md`, `body-lg/md/sm`, `label-lg/md/sm`.
  - Rounded: `none` … `full`.

### Body: eight `##` sections in a fixed order

All sections are optional, but the ones present must appear in this order. An `#` title is allowed and is not parsed as a section ([spec, Sections](https://github.com/google-labs-code/design.md/blob/6e5da5382f41edbba9d73b2c62f33f32e9971f15/docs/spec.md)):

1. `## Overview` (alias "Brand & Style")
2. `## Colors`
3. `## Typography`
4. `## Layout` (alias "Layout & Spacing")
5. `## Elevation & Depth` (alias "Elevation")
6. `## Shapes`
7. `## Components`
8. `## Do's and Don'ts`

The headings keep American spelling (`Colors`) because the linter matches them literally. The token key is likewise `colors`; `colours:` triggers an `unknown-key` warning, shown in the run below.

### The linter: eleven rules, contrast only on component pairs

`design.md spec --rulesOnly` at 0.4.0 lists these rules:

| Rule | Severity | Checks |
|---|---|---|
| `broken-ref` | error | References that do not resolve, circular references, and unknown component sub-tokens (reported as a warning) |
| `missing-primary` | warning | Colours are defined but there is no `primary` |
| `contrast-ratio` | warning | Each component's `backgroundColor`/`textColor` pair below 4.5:1 |
| `orphaned-tokens` | warning | A colour token that no component references, directly or through another colour |
| `token-summary` | info | Token counts |
| `missing-sections` | info | No `spacing` or no `rounded` |
| `missing-typography` | warning | Colours are defined but there is no typography |
| `section-order` | warning | Sections out of the canonical order |
| `unknown-key` | warning | A top-level key that looks like a typo, for example `colours` |
| `token-like-ignored` | warning | An unknown key whose values look like tokens and that export will drop |
| `omitted-rules` | info | Bad entries in `omitted` |

What these rules mean in practice:

- **Contrast checking is narrow.** It sees only `components` pairs, always at 4.5:1. It has no 3:1 rule for large text or non-text elements, and colour tokens that no component uses are never checked.
- **Pair components do two jobs.** The house file should declare one component for every text-on-surface pair (`page`, `card`, `muted-text`, `menu-item-active`, `error-text` and so on, plus their `dark-` twins). That puts every pair under the contrast check and also silences `orphaned-tokens`.
- **Non-text pairs need their own check.** The 3:1 checks for input borders and focus rings fall to the house contrast script. A lazy workaround is a `focus-ring` component whose `textColor` is the ring colour. The linter then holds the ring to 4.5:1, which is stricter than needed but catches regressions.

### CLI 0.4.0, run on 23 October 2026

The commands below were run in a scratch directory. They show where the shipped CLI and the spec differ.

`npx -y @google/design.md@0.4.0 --help` printed:

```
Agent-first CLI for DESIGN.md — the hands and eyes for design system work. (design.md v0.4.0)
USAGE design.md lint|diff|export|spec
    lint    Validate a DESIGN.md file for structural correctness.
    diff    Compare two DESIGN.md files and report changes.
  export    Export DESIGN.md tokens to other formats. css-tailwind emits Tailwind v4 CSS @theme;
            json-tailwind emits Tailwind v3 theme.extend JSON; tailwind is an alias for
            json-tailwind; dtcg emits W3C Design Tokens; css-vars emits CSS custom properties.
    spec    Output the DESIGN.md format specification.
```

Each subcommand's syntax, from its `--help`:

- **lint:** `design.md lint [--format json|text] <FILE|->`
- **diff:** `design.md diff [--format json|text] <BEFORE> <AFTER>`
- **export:** `design.md export <FILE|-> --format css-tailwind|json-tailwind|tailwind|dtcg|css-vars [--prefix <p>]`
- **spec:** `design.md spec [--rules] [--rulesOnly] [--format markdown|json]`

A clean sample (front matter, all eight section types, and two components that reference everything) printed the following and exited with 0:

```json
{
  "findings": [
    { "severity": "info",
      "message": "Design system defines 4 colors, 1 typography scale, 2 rounding levels, 2 spacing tokens, 2 components.",
      "rule": "token-summary" }
  ],
  "summary": { "errors": 0, "warnings": 0, "infos": 1 }
}
```

A deliberately broken sample exited with 1 and produced one error, six warnings and three infos. The broken parts were an undefined `{rounded.md}`, white text on `#9CA3AF`, an unused colour, a `colours:` key, a `borderColor` property and `## Colors` placed before `## Overview`. The findings, in order:

- `broken-ref` error: "Reference {rounded.md} does not resolve to any defined token."
- `broken-ref` warning: "'borderColor' is not a recognized component sub-token…"
- `contrast-ratio` warning: "textColor (#ffffff) on backgroundColor (#9ca3af) has contrast ratio 2.54:1, below WCAG AA minimum of 4.5:1."
- `orphaned-tokens` warning for the unused colour.
- `section-order` warning: "Section 'Colors' appears before 'Overview'…"
- `unknown-key` warning: "Unknown key "colours" — did you mean "colors"?"
- `token-like-ignored` warning for the same key.
- Three infos: the summary, plus "No 'spacing' section defined" and "No 'rounded' section defined".

`diff DESIGN.md BAD.md` printed the README's shape with `"regression": true`, and exited with 1. It listed token keys added, removed and modified for each group (`colors`, `typography`, `rounded`, `spacing`, `components`), and gave before, after and delta finding counts.

`export --format css-tailwind` on the clean sample printed:

```css
@theme {
  --color-primary: #284e7d;
  --color-on-primary: #ffffff;
  --color-neutral: #fafaf9;
  --color-on-surface: #1c1a17;
  --font-body-md: "Inter";
  --text-body-md: 15px;
  --font-weight-body-md: 400;
  --radius-sm: 4px;
  --radius-md: 6px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
}
```

`--format css-vars --prefix house` printed a `:root` block (`--house-color-primary`, `--house-spacing-sm`, `--house-rounded-sm` …) with no typography in it.

Where the 0.4.0 CLI departs from the spec and README:

| Behaviour | Spec or README says | 0.4.0 does |
|---|---|---|
| Duplicate top-level key (front matter and a YAML block) | Error, reject the file | Warning, exit 0 |
| Duplicate `##` heading | Error, reject the file | No finding, exit 0 |
| `lint --format text` | Text output | Still prints JSON |
| Contrast failures | — | Warning, so **exit 0** |
| `export css-tailwind` colours | "Original format is preserved for display and export" | `oklch()` converted to hex |
| Unitless `lineHeight: 1.55` | Allowed and recommended | Dropped from `css-tailwind` output; `24px` is exported as `--leading-*` |
| `fontFeature` | Typography property | Not exported |
| Interleaved YAML blocks | Documented on `main` since `6e5da53`; not in the 0.4.0 bundled `spec.md` | Parsed correctly in a test |
| `css-vars` format, `--prefix` | Missing from the README table | Present |
| Rules-only flag | README: `--rules-only` | Help: `--rulesOnly` |

Consequences for the house:

- **Front matter only.** Keep every token in front matter; interleaved YAML is newer than the pinned release.
- **Pixel line heights.** Give `lineHeight` in px so exports carry it.
- **A gate that reads the JSON.** Gate on `summary.errors == 0 && summary.warnings == 0` from the JSON, not on the exit code.

The export emits Tailwind `@theme` keys (`--color-primary`) rather than shadcn's `:root` variables (`--primary`), and shadcn already defines `--color-primary: var(--primary)` in `@theme inline`. Pasting the export in would therefore define the key twice. This is an inference and was not tested in a built app. The house should hand-map tokens through shadcn's workflow, and use `export` only to diff values.

### A minimal conforming skeleton

The skeleton below linted clean at 0.4.0: zero errors, zero warnings, and one info reading "15 colors, 4 typography scales, 3 rounding levels, 4 spacing tokens, 12 components". It is trimmed here for length, and the full sample covers more pairs. The house file is this pattern with all shadcn roles filled in.

````markdown
---
version: alpha
name: House
description: Restrained enterprise look for agent web apps on shadcn/ui (Base UI) and Tailwind CSS v4.
colors:
  primary: "oklch(0.40 0.085 250)"
  primary-foreground: "oklch(0.985 0.003 85)"
  background: "oklch(0.988 0.003 85)"
  foreground: "oklch(0.205 0.006 85)"
  muted: "oklch(0.962 0.004 85)"
  muted-foreground: "oklch(0.47 0.008 85)"
  ring: "oklch(0.50 0.10 250)"
  dark-background: "oklch(0.185 0.004 85)"
  dark-foreground: "oklch(0.945 0.004 85)"
typography:
  body-md:
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
rounded:
  sm: 4px
  md: 6px
  lg: 8px
spacing:
  base: 4px
  sm: 8px
  md: 16px
components:
  page:
    backgroundColor: "{colors.background}"
    textColor: "{colors.foreground}"
    typography: "{typography.body-md}"
  muted-text:
    backgroundColor: "{colors.muted}"
    textColor: "{colors.muted-foreground}"
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.primary-foreground}"
    rounded: "{rounded.md}"
    height: 32px
  focus-ring:
    backgroundColor: "{colors.background}"
    textColor: "{colors.ring}"
  answer:
    backgroundColor: "{colors.background}"
    textColor: "{colors.foreground}"
    typography: "{typography.answer-md}"
  dark-page:
    backgroundColor: "{colors.dark-background}"
    textColor: "{colors.dark-foreground}"
---

## Overview
## Colors
## Typography
## Layout
## Elevation & Depth
## Shapes
## Components
## Do's and Don'ts
````

Each heading carries prose in the real file. The spec has no concept of dark mode, so the `dark-` prefix is a house convention: tokens named `dark-<shadcn variable>` map to `.dark`. shadcn's own skill also lists "Responsive" and "Known Gaps" sections, which the format preserves as unknown headings. Put them after `Do's and Don'ts`. Whether they trigger `section-order` was not tested.

## From DESIGN.md to a shadcn theme

### The shadcn workflow and its checks

shadcn's skill (repository [shadcn-ui/ui](https://github.com/shadcn-ui/ui), MIT, read at commit `3d98900`, 22 October 2026; CLI `shadcn@4.22.1`) has a dedicated [design-system.md](https://github.com/shadcn-ui/ui/blob/3d98900e9b73c45f035f8109e9d41ba6a51685e7/skills/shadcn/design-system.md) for applying a DESIGN.md. Its steps:

1. **Scaffold.** Run `npx shadcn@latest init --base base --preset <style> --template vite --name <app> --no-monorepo -y`, then `npx shadcn@latest info --json`.
   - Without `--preset` or `--base`, `init` stops at a prompt even with `-y`.
   - Pick the style by geometry. `nova` is described as "32–36px controls, 6–8px radius, hairlines over shadows", which is the house's target.
   - `mira` is for dense data UIs (28–32 px controls). `sera` is editorial, with serif display type.
2. **Install everything.** Run `add --all -y` and count the component files on disk. Wire up `TooltipProvider` and the Base UI `Toaster`. Typecheck with `npx tsc -p tsconfig.app.json --noEmit` on Vite.
3. **Read the DESIGN.md.** Read the front matter, the Do's and Don'ts and the Known Gaps in full, and build an extraction table: canvas, ink, action states, surfaces, lines, focus, fonts, type scale, radius, elevation, control heights and hard rules.
4. **Map tokens to the theme.** Edit only the `tailwindCssFile`.
   - Keep hex as hex; do not convert it to OKLCH.
   - Map roles to variables (table below).
   - Give each token that has no shadcn slot its own variable, registered in `@theme inline`.
   - Pin the radius steps in `@theme inline`. Do not derive them from `--radius`.
   - Override shadows in `@theme`, and set `--shadow-xs: 0 0 #0000` for hairline-only systems.
   - Install fonts from Fontsource and set `--font-sans`, `--font-serif`, `--font-mono` and `--font-heading`.
   - Turn type tokens into `@utility type-*`. Do not use `--text-*`, because `cn()` treats unknown `text-*` classes as colours.
   - Write a designed `.dark`. If you derive it instead, say so.
   - Replace the focus treatment. A solid outline needs an unlayered `:focus-visible` rule that also sets `--tw-ring-shadow: 0 0 #0000`.
5. **Map component recipes to variants.** Edit the `cva` variants, keeping the variant names. Control heights move together across `button`, `input`, `input-group`, `select`, `toggle`, `tabs` and the rest; `h-8` is the 32 px default in `base-nova`. Turn every "Don't" into a check.
6. **Build a design system page** following [design-system-page.md](https://github.com/shadcn-ui/ui/blob/3d98900e9b73c45f035f8109e9d41ba6a51685e7/skills/shadcn/design-system-page.md). Show colours as surface and foreground pairs with measured contrast, and report "any pair below 4.5:1 for body-size text, even when the DESIGN.md specifies it". `scripts/showcase-coverage.mjs` must list no unshowcased components.
7. **Verify in a browser:**
   - The typecheck passes and the console shows no errors.
   - The page loads at `scrollY === 0`.
   - Nothing overflows horizontally at 375 and 1280 px.
   - Take screenshots of the hero, the foundations, a form and a dark band, and compare them against the DESIGN.md.
   - Toggle dark mode once.
   - Report contrast pairs under 4.5:1, every edited file, and every deviation.

The role mapping from that file:

| DESIGN.md role | shadcn variable |
|---|---|
| canvas, surface | `--background` |
| ink | `--foreground`, `--card-foreground`, `--popover-foreground` |
| primary CTA, on-primary | `--primary`, `--primary-foreground` (plus a new `--primary-active` if pressed differs) |
| secondary button | `--secondary`, `--secondary-foreground` |
| soft band | `--muted` |
| descriptive text | `--muted-foreground` |
| ghost hover, active tab, menu highlight | `--accent`, `--accent-foreground` |
| card fill | `--card` |
| menus, dialogs | `--popover` |
| hairline | `--border`, `--input` |
| focus | `--ring` |
| error | `--destructive` |
| data series | `--chart-1` … `--chart-5` |
| nav rail | `--sidebar-*` |

The skill's styling rules ([rules/styling.md](https://github.com/shadcn-ui/ui/blob/3d98900e9b73c45f035f8109e9d41ba6a51685e7/skills/shadcn/rules/styling.md)) add three constraints:

- **Semantic tokens only.** Do not use raw Tailwind colours, even for status: use Badge variants, `text-destructive` or new CSS variables.
- **No colour or typography overrides through `className`.**
- **No manual `dark:` colour overrides.**

### The complete variable list

The default theme in [theming.mdx](https://github.com/shadcn-ui/ui/blob/3d98900e9b73c45f035f8109e9d41ba6a51685e7/apps/v4/content/docs/(root)/theming.mdx), together with the `init` output, defines these variables in `:root` and `.dark`:

- `--background`, `--foreground`
- `--card`, `--card-foreground`
- `--popover`, `--popover-foreground`
- `--primary`, `--primary-foreground`
- `--secondary`, `--secondary-foreground`
- `--muted`, `--muted-foreground`
- `--accent`, `--accent-foreground`
- `--destructive`
- `--border`, `--input`, `--ring`
- `--chart-1` to `--chart-5`
- `--sidebar`, `--sidebar-foreground`, `--sidebar-primary`, `--sidebar-primary-foreground`, `--sidebar-accent`, `--sidebar-accent-foreground`, `--sidebar-border`, `--sidebar-ring`
- `--radius`

`@theme inline` registers each colour as `--color-<name>: var(--<name>)`. It also defines the radius scale `--radius-sm` to `--radius-4xl` as multiples of `--radius`: 0.6, 0.8, 1, 1.4, 1.8, 2.2 and 2.6. In the `init` output it also carries `--font-sans` and `--font-heading`.

The skill's [customization.md](https://github.com/shadcn-ui/ui/blob/3d98900e9b73c45f035f8109e9d41ba6a51685e7/skills/shadcn/customization.md) still lists `--destructive-foreground` and a `--surface`/`--surface-foreground` pair. Neither appears in the default theme or the `init` output, so treat both as optional extras.

### shadcn's defaults, which a checker should flag as leftovers

The values below come from running `npx -y shadcn@4.22.1 init --base base --preset nova --template vite --name probe --no-monorepo -y` in a scratch directory on 23 October 2026. The output matched the `neutral` theme in [apps/v4/registry/themes.ts](https://github.com/shadcn-ui/ui/blob/3d98900e9b73c45f035f8109e9d41ba6a51685e7/apps/v4/registry/themes.ts) at commit `3d98900`.

The run wrote:

- `components.json` with `"style": "base-nova"` and `"baseColor": "neutral"`.
- `@base-ui/react ^1.9.0`, `tailwindcss ^4`, `tw-animate-css ^1.4.0`, `lucide-react ^1.61.0` and `@fontsource-variable/geist ^5.3.0`.

| Variable | Light | Dark |
|---|---|---|
| `--background` | `oklch(1 0 0)` | `oklch(0.145 0 0)` |
| `--foreground` | `oklch(0.145 0 0)` | `oklch(0.985 0 0)` |
| `--card`, `--popover` | `oklch(1 0 0)` | `oklch(0.205 0 0)` |
| `--card-foreground`, `--popover-foreground` | `oklch(0.145 0 0)` | `oklch(0.985 0 0)` |
| `--primary` | `oklch(0.205 0 0)` | `oklch(0.922 0 0)` |
| `--primary-foreground` | `oklch(0.985 0 0)` | `oklch(0.205 0 0)` |
| `--secondary`, `--muted`, `--accent` | `oklch(0.97 0 0)` | `oklch(0.269 0 0)` |
| `--secondary-foreground`, `--accent-foreground` | `oklch(0.205 0 0)` | `oklch(0.985 0 0)` |
| `--muted-foreground` | `oklch(0.556 0 0)` | `oklch(0.708 0 0)` |
| `--destructive` | `oklch(0.577 0.245 27.325)` | `oklch(0.704 0.191 22.216)` |
| `--border` | `oklch(0.922 0 0)` | `oklch(1 0 0 / 10%)` |
| `--input` | `oklch(0.922 0 0)` | `oklch(1 0 0 / 15%)` |
| `--ring` | `oklch(0.708 0 0)` | `oklch(0.556 0 0)` |
| `--chart-1` … `--chart-5` | `oklch(0.87 0 0)`, `oklch(0.556 0 0)`, `oklch(0.439 0 0)`, `oklch(0.371 0 0)`, `oklch(0.269 0 0)` | same |
| `--sidebar` | `oklch(0.985 0 0)` | `oklch(0.205 0 0)` |
| `--sidebar-primary` | `oklch(0.205 0 0)` | `oklch(0.488 0.243 264.376)` |
| `--sidebar-accent` | `oklch(0.97 0 0)` | `oklch(0.269 0 0)` |
| `--sidebar-border`, `--sidebar-ring` | `oklch(0.922 0 0)`, `oklch(0.708 0 0)` | `oklch(1 0 0 / 10%)`, `oklch(0.556 0 0)` |
| `--radius` | `0.625rem` | — |
| Fonts | `--font-sans: 'Geist Variable', sans-serif`; `--font-heading: var(--font-sans)`; `@import "@fontsource-variable/geist"` | — |

Further facts about the defaults:

- **The docs' chart colours differ from the `init` output.** The docs' "Default Theme CSS" uses coloured charts instead of the greys above. Light: `oklch(0.646 0.222 41.116)`, `oklch(0.6 0.118 184.704)`, `oklch(0.398 0.07 227.392)`, `oklch(0.828 0.189 84.429)`, `oklch(0.769 0.188 70.08)`. Dark adds `oklch(0.488 0.243 264.376)` and `oklch(0.627 0.265 303.9)`. A checker should flag both sets.
- **Other base colours exist.** `stone`, `zinc`, `mauve`, `olive`, `mist` and `taupe` are also offered ([base-colors.ts](https://github.com/shadcn-ui/ui/blob/3d98900e9b73c45f035f8109e9d41ba6a51685e7/apps/v4/registry/base-colors.ts)). The robust check is to extract every value from `themes.ts` at the pinned commit.
- **The default font depends on the path taken.** The CLI's `nova` preset uses Geist ([defaults.ts](https://github.com/shadcn-ui/ui/blob/3d98900e9b73c45f035f8109e9d41ba6a51685e7/packages/shadcn/src/preset/defaults.ts)). The website's `DEFAULT_CONFIG` uses Inter and radius "default" ([config.ts](https://github.com/shadcn-ui/ui/blob/3d98900e9b73c45f035f8109e9d41ba6a51685e7/apps/v4/registry/config.ts)), and the site offers radii of `0`, `0.45rem`, `0.625rem` and `0.875rem`.
  - **Inter appearing is not on its own a sign of leftover defaults.** The checker should look for Geist, `0.625rem` and the values above.
- **The generated button keeps the default focus treatment.** `button.tsx` contains `focus-visible:ring-3 focus-visible:ring-ring/50`, and the base layer applies `outline-ring/50` to everything. These classes are default focus treatment to replace.
- **Default dark sidebar-primary sits in the violet band.** `oklch(0.488 0.243 264.376)` is a saturated blue-violet close to the band this house avoids.

The defaults measured against the house floor, using the script in the colour section below:

| Pair (shadcn 4.22.1 defaults) | Ratio | Floor |
|---|---|---|
| `muted-foreground` on `background`, light | 4.73:1 | 4.5 pass |
| `muted-foreground` on `muted`, light (helper text in a muted band) | **4.34:1** | 4.5 fail |
| `ring` on `background`, light | 2.59:1 | 3.0 fail |
| `ring` at 50% (`ring-ring/50`) on `background`, light | **1.54:1** | 3.0 fail |
| `border` or `input` on `background`, light | 1.26:1 | 3.0 fail if it is the only edge of a field |
| `input` (white at 15%) on `background`, dark | 1.47:1 | 3.0 fail |
| `ring` at 50% on `background`, dark | 1.87:1 | 3.0 fail |
| `destructive` on `background`, light | 4.76:1 | pass, though `oklch(0.577 0.245 27.325)` is outside sRGB and the browser clips it |

## Enterprise systems: principles to borrow, assets to leave

The five systems agree on more than they differ:

- **Text sizes.** Product body text is 14/20, with a larger size kept for reading.
- **Spacing.** It sits on a 4 or 8 px grid.
- **Colour.** Tokens are named by role and paired as surface and on-surface.
- **Focus.** It has a dedicated token that is never reused for anything else.
- **Depth.** It comes from surfaces and borders before shadows.
- **Motion.** Interactions take 100–150 ms and overlays take 200–250 ms.

All five protect their typefaces, logos and icons more tightly than their code. Figures below were read from each system's documentation or source on 23 October 2026. Only the principles are borrowed; no values or assets are copied.

| System | Transferable principles | Licence and what not to copy |
|---|---|---|
| **IBM Carbon** | **Type:** 14 px body in two line heights, 18 for compact and 20 for reading; 12/16 labels; headings 20/28, 28/36, 32/40 ([type sets](https://carbondesignsystem.com/elements/typography/type-sets/)). **Spacing:** an 8 px mini-unit grid with steps of 2, 4, 8, 12, 16, 24, 32, 40, 48 … ([spacing](https://carbondesignsystem.com/elements/spacing/overview/), [2x Grid](https://carbondesignsystem.com/elements/2x-grid/overview/)). **Density:** one size ramp across components; table rows are 24/32/40/48/64 ([data table](https://carbondesignsystem.com/components/data-table/style/)). **Colour and depth:** tokens grouped by role, with depth from `layer-01/02/03` rather than shadow ([colour usage](https://carbondesignsystem.com/elements/color/usage/)). **Focus:** a 2 px solid focus outline that turns dotted under `prefers-contrast` ([source](https://github.com/carbon-design-system/carbon/blob/main/packages/styles/scss/utilities/_focus-outline.scss)). **Motion:** durations of 70–700 ms, with separate productive and expressive curves ([motion](https://carbondesignsystem.com/elements/motion/overview/)). | Code is Apache-2.0 ([LICENSE](https://github.com/carbon-design-system/carbon/blob/main/LICENSE)) and `@carbon/icons` is Apache-2.0. **IBM Plex** is OFL-1.1, but "Plex" is a reserved name and the README calls it IBM's corporate, signature face. Do not copy Plex, IBM blue `#0f62fe`, IBM marks, or the AI glow and gradient styling. |
| **Carbon for AI** | **The label's job:** one AI label is the single sign that AI made or shaped content, and the way into an explainability popover. **The popover:** behaves like a toggletip, with overview, supporting details, artefacts and resources, and additional actions. **Limits:** the label is never decoration, never an action button and never disabled. **After an edit:** human edits remove the AI marking and offer a revert ([AI label](https://carbondesignsystem.com/components/ai-label/usage/), [Carbon for AI](https://carbondesignsystem.com/guidelines/carbon-for-ai/)). **Carbon AI Chat** (`@carbon/ai-chat`, Apache-2.0): streams can be stopped and stopped items are marked as such; reasoning steps close when the answer arrives, and a click by the person wins ([docs](https://chat.carbondesignsystem.com/tag/latest/docs/documents/Overview.html)). | Take the behaviour, not the look. The house label is plain text. |
| **Microsoft Fluent 2** | **Spacing:** a 4 px base with 2, 6 and 10 for icon alignment ([layout](https://fluent2.microsoft.design/layout)). **Type:** body 14/20; headings are semibold rather than bold; weights 400–700 ([typography](https://fluent2.microsoft.design/typography)). **Brand colour:** for actions and selection, not large surfaces ([colour](https://fluent2.microsoft.design/color)). **Elevation:** each level is an ambient shadow plus a key shadow, with depth set by the key shadow's size ([shadows source](https://github.com/microsoft/fluentui/blob/master/packages/tokens/src/utils/shadows.ts)). **Focus:** 2 px on `:focus-visible`, switching to `Highlight` in forced-colours mode ([source](https://github.com/microsoft/fluentui/blob/master/packages/react-components/react-tabster/src/focus/createFocusOutlineStyle.ts)). **Motion and radius:** durations 50–500 ms, with buttons at 100 ms; controls have a 4 px radius ([durations](https://github.com/microsoft/fluentui/blob/master/packages/tokens/src/global/durations.ts), [radius](https://github.com/microsoft/fluentui/blob/master/packages/tokens/src/global/borderRadius.ts)). | Code and `@fluentui/react-icons` are MIT ([LICENSE](https://github.com/microsoft/fluentui/blob/master/LICENSE)). **Segoe UI** and the Office icons fall under the revocable [Fabric assets licence](https://aka.ms/fluentui-assets-license), which allows use only in apps that use Microsoft services. Do not copy Segoe, Office icons, or Microsoft colours and logos. |
| **Atlassian Design System** | **Spacing:** an 8 px base with fractional steps of 2 to 80, in three bands: 0–8 for dense UI, 12–24 for components, 32–80 for layout. Token names encode the multiplier, for example `space.150` ([spacing](https://atlassian.design/foundations/spacing)). **Type:** body 14/20, with separate number styles for metrics ([typography](https://atlassian.design/foundations/typography)). **Colour grammar:** property, then role, then emphasis, then state. Selected states need a cue other than colour ([colour](https://atlassian.design/foundations/color)). **Elevation:** each surface is paired with its own shadow, higher surfaces get lighter in dark mode, and a flat card is a border, not a shadow ([elevation](https://atlassian.design/foundations/elevation)). **Radius and focus:** radius by role (4 for tags, 6 for buttons and inputs, 8 for cards and menus, 12 for modals); a 2 px focus ring set 2 px outside the element ([radius](https://atlassian.design/foundations/radius), [border](https://atlassian.design/foundations/border)). **Motion:** 50–150 ms for interactions and 150–400 ms for transitions; menus take 150 and modals 250 ([motion](https://atlassian.design/foundations/motion)). | The [ADS licence](https://atlassian.design/license) is limited to building Atlassian integrations and forbids derivative works. Some `@atlaskit/*` packages declare Apache-2.0 on npm, which conflicts with it; treat that as unresolved. Charlie Sans and Atlassian Sans (an Inter derivative) are proprietary. Do not copy tokens files, icons, fonts or Atlassian blues. |
| **Salesforce SLDS 2** | **Naming:** global hooks follow `--slds-g-[category]-[name]-[n]`, numbered from lightest or smallest to darkest or largest ([guidance](https://v1.lightningdesignsystem.com/platforms/lightning/new-global-styling-hooks-guidance/)). **Colour roles:** surface, then container, then on-surface, which is the closest match to shadcn's pairs. `border-2` is for interactive borders and `border-1` for decorative ones. **Overrides:** consumers read hooks and never reassign them, which is a model for the house override surface. **Spacing and type:** a 4-based spacing scale; a 13 px type base; system fonts. **Motion:** durations have meaning-based names (quickly 100, promptly 200). Values were read from `@salesforce-ux/sds-metadata` 2.264.1, because the site renders client-side. | Code is BSD-3-Clause. Icons and images are CC BY-ND 4.0 ([licence](https://github.com/salesforce-ux/licenses/blob/master/LICENSE-icons-images.txt)), so no altered versions are allowed. Do not copy icons, Salesforce or Agentforce marks, or brand blues. |
| **GOV.UK Design System** | **Reading:** body 19/25, line length of about 75 characters or less, content in a two-thirds column ([type scale](https://design-system.service.gov.uk/styles/type-scale/), [layout](https://design-system.service.gov.uk/styles/layout/)). **Spacing:** a 5 px-step scale ([spacing](https://design-system.service.gov.uk/styles/spacing/)). **Focus:** designed to pass 1.4.11 on any background, with a transparent outline kept for forced-colours mode ([focus states](https://design-system.service.gov.uk/get-started/focus-states/)). **Colour:** functional names, each with one job; the focus colour is used for nothing else ([colour](https://design-system.service.gov.uk/styles/colour/)). **Shape:** flat and square. | Code is MIT, Crown copyright ([LICENSE](https://github.com/alphagov/govuk-frontend/blob/main/LICENSE.txt)). Services outside GOV.UK must not use the crown, the GOV.UK logotype, **GDS Transport** or GOV.UK colours ([service manual](https://www.gov.uk/service-manual/design/making-your-service-look-like-govuk)). The yellow and black focus look is a GOV.UK signature, so take the mechanism and recolour it. |

What the house takes from them:

- **Text sizes:** 14/20 for the interface (Carbon, Fluent, Atlassian) and a separate reading size and measure for answers (GOV.UK).
- **Grid and density:** a 4 px grid and one density ramp (Carbon).
- **Colour tokens:** role-named tokens in surface and on-surface pairs (SLDS, Atlassian).
- **Brand colour:** only on actions and selection (Fluent).
- **Focus:** a single-purpose token drawn as an `outline`, which survives forced-colours mode (Carbon, Fluent, GOV.UK).
- **Depth:** surfaces and borders before shadows, and lighter surfaces in dark mode (Carbon, Atlassian).
- **Motion:** 100–150 ms for interactions and 200–250 ms for overlays (Fluent, Atlassian).
- **AI marking:** one restrained marker with an explanation behind it (Carbon for AI).

## Agent UX: what the guidance agrees on

The shadcn and AI SDK material is read at shadcn commit `3d98900` and AI Elements `ai-elements@1.9.1` (repository [vercel/ai-elements](https://github.com/vercel/ai-elements) at `ca8be60`). Vercel's [README](https://github.com/vercel/ai-elements/blob/ca8be600bfd01b3131f9bf6134b51602a71f4374/README.md) says the package will be deprecated at the end of November 2026 in favour of [AI Elements in shadcn/ui](https://ui.shadcn.com/docs/ai-elements), which are copy-in patterns built on the new `Trace` component ([changelog](https://github.com/shadcn-ui/ui/blob/3d98900e9b73c45f035f8109e9d41ba6a51685e7/apps/v4/content/docs/changelog/2026-10-ai-elements.mdx)). **Build on the shadcn patterns.** Use Vercel's components only for comparison.

The two general frameworks used here:

- **Microsoft's HAX** [18 guidelines](https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/), grouped by phase:
  - Initially: G1–G2.
  - During interaction: G3–G6.
  - When wrong: G7–G11.
  - Over time: G12–G18.
- **Google PAIR's chapters**, in particular [Explainability + Trust](https://pair.withgoogle.com/chapter/explainability-trust/), [Errors + Graceful Failure](https://pair.withgoogle.com/chapter/errors-failing/), [Feedback + Control](https://pair.withgoogle.com/chapter/feedback-controls/) and [Mental Models](https://pair.withgoogle.com/chapter/mental-models/).

| Concern | Guidance | House rule |
|---|---|---|
| **Tool steps** | shadcn [chat.md](https://github.com/shadcn-ui/ui/blob/3d98900e9b73c45f035f8109e9d41ba6a51685e7/skills/shadcn/rules/chat.md): every action is a `TraceLine` in one `Trace` per run of parts. A row becomes collapsible only once output exists. Status is `running`, `error`, `pending` or none (done). Titles agree with the status ("Running…", "Ran…", "Failed to run…") and are sentences, for example "Edited trace.tsx". Never dim a line with opacity. The [Tool pattern](https://github.com/shadcn-ui/ui/blob/3d98900e9b73c45f035f8109e9d41ba6a51685e7/apps/v4/content/docs/ai-elements/base/tool.mdx) maps AI SDK states, and a tool still in `input-*` after the stream stops becomes "Failed to run…", except client-side tools. | Use one line per step with the status in words. Never show status by colour alone ([Trace docs](https://github.com/shadcn-ui/ui/blob/3d98900e9b73c45f035f8109e9d41ba6a51685e7/apps/v4/content/docs/components/base/trace.mdx) say the same). Rows start closed. |
| **Approval before effects** | shadcn [Confirmation](https://github.com/shadcn-ui/ui/blob/3d98900e9b73c45f035f8109e9d41ba6a51685e7/apps/v4/content/docs/ai-elements/base/confirmation.mdx): a pending approval is a question, rendered outside `Trace` as an `Item` with Deny and Approve. Once answered it goes back to being a line ("Running…" or "Denied…"). HAX [G16](https://www.microsoft.com/en-us/haxtoolkit/guideline/convey-the-consequences-of-user-actions/) asks for feedforward before the action; [G9](https://www.microsoft.com/en-us/haxtoolkit/guideline/support-efficient-correction/) asks for undo. | The approval card states the effect in plain words (what, where, reversible or not) before the buttons. Deny is never styled as destructive. Approve uses `primary`; the destructive variant is used only when the effect is destructive. |
| **Citations** | shadcn [Sources](https://github.com/shadcn-ui/ui/blob/3d98900e9b73c45f035f8109e9d41ba6a51685e7/apps/v4/content/docs/ai-elements/base/sources.mdx): one "Used N sources" line after the answer, with duplicates removed by URL, a hostname fallback for missing titles, and new-tab links with a screen-reader-only notice. [Inline Citation](https://github.com/shadcn-ui/ui/blob/3d98900e9b73c45f035f8109e9d41ba6a51685e7/apps/v4/content/docs/ai-elements/base/inline-citation.mdx) puts a `HoverCard` in the sentence it supports. PAIR asks for data scope and limits to be stated. | Cite inline where a claim rests on a source; list the sources after the answer. |
| **Reasoning** | shadcn [Reasoning](https://github.com/shadcn-ui/ui/blob/3d98900e9b73c45f035f8109e9d41ba6a51685e7/apps/v4/content/docs/ai-elements/base/reasoning.mdx): "Thinking" opens while streaming, then becomes "Thought" and closes, and **a click by the person wins**. Measure the duration on the server. Vercel's legacy version auto-closes 1 s after the stream ends. PAIR: explain for understanding, with progressive disclosure. HAX [G11](https://www.microsoft.com/en-us/haxtoolkit/guideline/make-clear-why-the-system-did-what-it-did/) warns that explanations can raise trust past what is warranted. | Collapsed once done; never auto-reopened. |
| **Streaming** | shadcn: use the `shimmer` utility, never custom keyframes. `MessageScroller` follows the live edge until the person scrolls up and has a built-in jump-to-latest button. The AI SDK [chatbot](https://ai-sdk.dev/docs/ai-sdk-ui/chatbot) statuses are `submitted`, `streaming`, `ready` and `error`, with Stop enabled only while submitted or streaming. Carbon AI Chat shows a loader if the first chunk is late ([server communication](https://chat.carbondesignsystem.com/tag/latest/docs/documents/Server_communication.html)). | One shimmer at a time. Stop is always reachable during a run. Under reduced motion the shimmer stops, and shadcn's `tailwind.css` already has a `prefers-reduced-motion` block for it. |
| **Errors after partial output** | AI SDK [error handling](https://ai-sdk.dev/docs/ai-sdk-ui/error-handling): show a generic message and a Retry that calls `regenerate()`, which replaces the last reply. shadcn's Message footer has Retry. PAIR: say what failed, offer a way forward, and hand back control with context. No source says what to do with the partial text. | Keep the partial text, mark it "Incomplete" in words below it, and offer Retry. This rule is the house's own inference. |
| **Empty state** | shadcn [Suggestion](https://github.com/shadcn-ui/ui/blob/3d98900e9b73c45f035f8109e9d41ba6a51685e7/apps/v4/content/docs/ai-elements/base/suggestion.mdx): outline buttons whose label is the exact prompt sent, in a sideways-scrolling row above the input. HAX [G1](https://www.microsoft.com/en-us/haxtoolkit/guideline/make-clear-what-the-system-can-do/): show example inputs and say what the system can do. HAX [G2](https://www.microsoft.com/en-us/haxtoolkit/guideline/make-clear-how-well-the-system-can-do-what-it-can-do/): say how well it does it. PAIR: state limits and lead with the benefit. | A short title, one line on scope and limits, then 3–4 suggestions. |
| **AI-generated label** | Carbon [AI label](https://carbondesignsystem.com/components/ai-label/usage/): marks AI-made or AI-assisted content and opens an explainability popover (overview, supporting details, artefacts and resources, actions). It is never decorative and never an action, and it is replaced by a revert control once the person edits the content. PAIR: say plainly that it is a system and not a person. shadcn and Vercel have no label component. | A house text label ("AI-generated") with a popover showing the model, sources and time. Do not copy Carbon's glow or gradient AI styling. |
| **Feedback and control** | shadcn [Message](https://github.com/shadcn-ui/ui/blob/3d98900e9b73c45f035f8109e9d41ba6a51685e7/apps/v4/content/docs/ai-elements/base/message.mdx) footer: Copy, Good response and Bad response (toggles with `aria-pressed`), Retry, and Edit on the person's own turn. HAX [G15](https://www.microsoft.com/en-us/haxtoolkit/guideline/encourage-granular-feedback/), [G17](https://www.microsoft.com/en-us/haxtoolkit/guideline/provide-global-controls/). PAIR: acknowledge feedback by saying what changes, and do not over-promise tuning. | Ghost icon buttons with tooltips and visible focus. |

## Accessibility floor: WCAG 2.2 AA plus two AAA habits

Sources are [WCAG 2.2](https://www.w3.org/TR/WCAG22/) (W3C Recommendation, 12 December 2024) and its Understanding documents.

| Criterion | Level | Requirement | Effect on the house |
|---|---|---|---|
| [1.4.3 Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) | AA | Text at least 4.5:1. Large text at least 3:1, where large means 18 pt (about 24 px) or 14 pt bold (about 18.5 px). Inactive controls, decoration and logotypes are exempt. | Every text pair is at least 4.5:1, including text at large sizes, so one rule covers all. |
| [1.4.11 Non-text Contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html) | AA | UI components and meaningful graphics at least 3:1 against adjacent colours | `--input` borders, the focus ring, checkbox edges and chart marks at least 3:1. `--border` for decorative hairlines may be lower. |
| [2.4.7 Focus Visible](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html) | AA | Keyboard focus indicator visible | Never remove the outline without a replacement. |
| [2.4.11 Focus Not Obscured (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html) | AA | The focused item is not entirely hidden by author content | Sticky prompt bars and headers need `scroll-padding` so focused items are not covered. |
| [2.4.13 Focus Appearance](https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html) | AAA | Indicator area at least a 2 CSS px perimeter, and at least 3:1 between focused and unfocused pixels | A 2 px solid outline in `--ring` with a 2 px offset meets it. shadcn's `ring-3 ring-ring/50` does not. |
| [2.5.8 Target Size (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) | AA | Pointer targets at least 24×24 CSS px. Exceptions: spacing, an equivalent control, inline text, user-agent controls, essential presentation. | 32 px controls pass; the 24 px `icon-xs` size is the minimum. |
| [2.3.3 Animation from Interactions](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html) | AAA | Motion triggered by interaction can be turned off unless essential | Honour [`prefers-reduced-motion: reduce`](https://www.w3.org/TR/mediaqueries-5/#prefers-reduced-motion) ([MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)): no translate or scale, fades of 100 ms or less, no shimmer. |

## Typography: Inter, Source Serif 4, JetBrains Mono

Licences were checked through the GitHub licence API, and versions from `registry.npmjs.org`. Features and metrics come from the `@fontsource-variable` latin woff2 files, inspected with fontTools. x-height is the OS/2 `sxHeight` divided by units per em. KB is the latin upright woff2.

| Family | Licence, reserved name | Package (latest) | Axes | Latin KB | `tnum` | x-height | Verdict |
|---|---|---|---|---|---|---|---|
| **Inter** | [OFL-1.1](https://github.com/rsms/inter/blob/master/LICENSE.txt), none | [`@fontsource-variable/inter` 5.3.0](https://registry.npmjs.org/@fontsource-variable/inter/latest) | wght 100–900, opsz 14–32, ital | 47 | yes | .546 | **UI sans** |
| **Source Serif 4** | [OFL-1.1](https://github.com/adobe-fonts/source-serif/blob/release/LICENSE.md), "Source" | [`@fontsource-variable/source-serif-4` 5.3.1](https://registry.npmjs.org/@fontsource-variable/source-serif-4/latest) | wght 200–900, **opsz 8–60**, ital | 50 (120 with opsz) | yes (tabular by default) | .475 | **Headings and answers** |
| **JetBrains Mono** | [OFL-1.1](https://github.com/JetBrains/JetBrainsMono/blob/master/OFL.txt), none | [`@fontsource-variable/jetbrains-mono` 5.3.0](https://registry.npmjs.org/@fontsource-variable/jetbrains-mono/latest) | wght 100–800, ital | 40 | monospaced, distinguished zero | .550 | **Code** |
| Source Sans 3 | [OFL-1.1](https://github.com/adobe-fonts/source-sans/blob/release/LICENSE.md), "Source" | [`@fontsource-variable/source-sans-3` 5.3.1](https://registry.npmjs.org/@fontsource-variable/source-sans-3/latest) | wght 200–900, ital | 28 | tabular by default | .478 | Alternate sans |
| Literata | [OFL-1.1](https://github.com/googlefonts/literata/blob/main/OFL.txt), none | `@fontsource-variable/literata` 5.3.0 | wght, opsz 7–72, ital | 51 | yes | .507 | Alternate serif; repo idle since 2023 |
| Newsreader | [OFL-1.1](https://github.com/productiontype/Newsreader/blob/master/OFL.txt) | `@fontsource-variable/newsreader` 5.3.0 | wght, opsz 6–72, ital | 57 | yes | .426 | Small x-height |
| Fraunces | [OFL-1.1](https://github.com/undercasetype/Fraunces/blob/master/OFL.txt) | `@fontsource-variable/fraunces` 5.3.0 | wght, opsz, SOFT, WONK | 36 | **no** | .482 | Too characterful; no tabular figures |
| Spectral | [OFL-1.1](https://github.com/productiontype/Spectral/blob/master/ofl.txt) | `@fontsource/spectral` 5.3.0 (static only) | — | 21 per weight | yes | .450 | No variable build |
| Lora | [OFL-1.1](https://github.com/cyrealtype/Lora-Cyrillic/blob/main/OFL.txt), "Lora" | `@fontsource-variable/lora` 5.3.0 | wght 400–700 only | 37 | yes | .500 | Narrow weight range |
| IBM Plex Sans, Serif, Mono | [OFL-1.1](https://github.com/IBM/plex/blob/master/LICENSE.txt), "Plex" | `@fontsource-variable/ibm-plex-sans` 5.3.0; Serif and Mono static only | Sans: wght 100–700, wdth | 45 | tabular by default | .516 | **Excluded:** the [README](https://github.com/IBM/plex/blob/master/README.md) calls it IBM's corporate signature typeface |
| Geist, Geist Mono | [OFL-1.1](https://github.com/vercel/geist-font/blob/main/LICENSE.txt) | `@fontsource-variable/geist` 5.3.0 | wght 100–900 | 29 | yes | .530 | **Excluded:** Vercel's typeface and shadcn's `nova` default, so it reads as stock output |
| Public Sans | [OFL-1.1 + CC0](https://github.com/uswds/public-sans/blob/develop/LICENSE.md) | `@fontsource-variable/public-sans` 5.3.0 | wght 100–900 | 26 | yes | .517 | **Excluded:** its [README](https://github.com/uswds/public-sans/blob/develop/README.md) says it is not actively maintained |

The reasons for the pairing:

- **Neutrality.** None of the three is another company's identity face.
- **Small-size reading.** Inter has the tallest x-height among the sans candidates, and it was designed for screens ([README](https://github.com/rsms/inter/blob/master/README.md)).
- **One serif file for all sizes.** Source Serif 4's optical-size axis lets that file tighten for display headings and open up at answer sizes.
- **Inline code sits level.** JetBrains Mono's x-height (.550) matches Inter's (.546).
- **Data tables work.** Tabular figures are available in all three.
- **Fontsource already uses it.** shadcn's own font registry wires every font through `@fontsource-variable/*` ([font-definitions.ts](https://github.com/shadcn-ui/ui/blob/3d98900e9b73c45f035f8109e9d41ba6a51685e7/apps/v4/lib/font-definitions.ts)). Fonts are bundled at build time and never fetched from a font CDN at run time.

Practical notes:

- **Set serif answers one step up.** Source Serif 4's x-height (.475) is visibly smaller than Inter's, so set serif answers at 17 px against 14–15 px UI text.
- **Optical sizing needs its own import.** Use `@fontsource-variable/source-serif-4/opsz.css`; the default `index.css` fixes opsz.
- **Budget.** Latin upright is about 206 KB with opsz and about 136 KB without. Other subsets and italics load only through `unicode-range` when used.
- **Some alternates are missing.** The Fontsource builds are Google Fonts builds and drop Inter's `cv*`, `ss*` and `zero` alternates. `tnum` survives, and `font-feature-settings: "cv11"` silently does nothing. Self-host the upstream files only if those alternates are required.
- **Reserved names.** The "Source" reserved font name restricts *modified* copies under that name. Using the npm packages unmodified is fine, but re-subsetting them ourselves would mean renaming the font.
- **Alternate pairing.** Source Sans 3 with Source Serif 4 (one foundry, matching proportions, about 117–187 KB), with UI text at 15 px or more because of the small x-height.

## Colour: warm paper, ink blue, muted signals

### Direction

- **Warm, barely there greys.** The neutrals use hue 85 at chroma 0.003–0.008. Against pure-grey shadcn defaults that reads as paper rather than screen, while staying neutral enough for clients' accents.
- **Ink-blue accent.** The accent uses hue 250. Common "AI purple" sits near hue 277–293, and the accent stays well clear of it: `#6366F1` measures `oklch(0.585 0.204 277.1)`, `#7C3AED` `oklch(0.541 0.247 293.0)` and `#8B5CF6` `oklch(0.606 0.219 292.7)`.
- **Low-chroma semantics.** Success, warning and destructive keep chroma at 0.15 or below, so status reads without shouting.
- **No decoration.** No gradients, glass or glow.

Contrasts were computed with a short Python script kept in the scratch directory, not the repository. It converts OKLCH to OKLab to linear sRGB, applies the WCAG 2.2 relative-luminance formula, and composites alpha in gamma-encoded sRGB. It reproduces the CLI's 2.54:1 for white on `#9CA3AF`. Every value listed is inside the sRGB gamut.

### Accent ramp (hue 250)

| Step | OKLCH | Hex | vs white | vs ink `#181714` |
|---|---|---|---|---|
| 50 | `oklch(0.975 0.012 250)` | `#F1F8FF` | 1.07 | 16.68 |
| 100 | `oklch(0.948 0.022 250)` | `#E3EFFC` | 1.16 | 15.42 |
| 200 | `oklch(0.895 0.042 250)` | `#C8DFF8` | 1.36 | 13.13 |
| 300 | `oklch(0.81 0.065 250)` | `#A2C5EA` | 1.80 | 9.97 |
| 400 | `oklch(0.70 0.085 250)` | `#75A3D2` | 2.66 | 6.74 |
| 500 | `oklch(0.59 0.095 250)` | `#4F81B4` | 4.09 | 4.38 |
| 600 | `oklch(0.50 0.095 250)` | `#356697` | 5.98 | 3.00 |
| **700** (primary) | `oklch(0.40 0.085 250)` | `#1F4A73` | 9.19 | 1.95 |
| 800 | `oklch(0.33 0.07 250)` | `#153758` | 12.20 | 1.47 |
| 900 | `oklch(0.27 0.055 250)` | `#0F2840` | 15.05 | 1.19 |
| 950 | `oklch(0.21 0.04 250)` | `#09192A` | 17.70 | 1.01 |

Steps 600 and darker can carry text on white, and steps 400 and lighter can carry text on ink. Step 500 is for marks only.

### Light theme

| Variable | OKLCH | Hex |
|---|---|---|
| `--background` | `oklch(0.988 0.003 85)` | `#FCFBF9` |
| `--foreground` | `oklch(0.205 0.006 85)` | `#181714` |
| `--card`, `--popover` | `oklch(1 0 0)` | `#FFFFFF` |
| `--muted` | `oklch(0.962 0.004 85)` | `#F4F2EF` |
| `--muted-foreground` | `oklch(0.47 0.008 85)` | `#5D5A56` |
| `--secondary` | `oklch(0.955 0.005 85)` | `#F2F0EC` |
| `--secondary-foreground` | `oklch(0.24 0.008 85)` | `#211F1B` |
| `--accent` | `oklch(0.948 0.012 250)` | `#E8EFF6` |
| `--accent-foreground` | `oklch(0.30 0.07 250)` | `#0D2F4F` |
| `--primary` | `oklch(0.40 0.085 250)` | `#1F4A73` |
| `--primary-foreground` | `oklch(0.985 0.003 85)` | `#FBFAF8` |
| `--border` (decorative hairline) | `oklch(0.905 0.005 85)` | `#E1DFDC` |
| `--input` (field edge) | `oklch(0.64 0.008 85)` | `#8E8C87` |
| `--ring` | `oklch(0.50 0.10 250)` | `#32669A` |
| `--destructive` | `oklch(0.50 0.15 27)` | `#A83630` |
| `--success` (new) | `oklch(0.47 0.09 150)` | `#31693F` |
| `--warning` (new) | `oklch(0.52 0.10 65)` | `#905B20` |
| `--sidebar` | `oklch(0.972 0.004 85)` | `#F7F6F3` |
| `--sidebar-accent` | `oklch(0.935 0.006 85)` | `#EBE9E5` |
| `--chart-1` … `--chart-5` | `oklch(0.50 0.095 250)`, `oklch(0.55 0.085 185)`, `oklch(0.62 0.11 70)`, `oklch(0.50 0.02 85)`, `oklch(0.52 0.13 30)` | `#356697`, `#268278`, `#B07932`, `#686357`, `#A74639` |

`--sidebar-foreground` and `--sidebar-primary` equal `--foreground` and `--primary`.

| Pair, light | Ratio | Floor |
|---|---|---|
| foreground / background | 17.31 | 4.5 |
| foreground / card | 17.91 | 4.5 |
| muted-foreground / background | 6.59 | 4.5 |
| muted-foreground / muted | 6.11 | 4.5 |
| muted-foreground / card | 6.83 | 4.5 |
| muted-foreground / accent | 5.87 | 4.5 |
| muted-foreground / sidebar | 6.30 | 4.5 |
| secondary-foreground / secondary | 14.43 | 4.5 |
| accent-foreground / accent | 11.71 | 4.5 |
| primary-foreground / primary | 8.80 | 4.5 |
| primary (link text) / background | 8.88 | 4.5 |
| primary / accent (selected row) | 7.90 | 4.5 |
| destructive / background | 6.26 | 4.5 |
| destructive-foreground / destructive | 6.20 | 4.5 |
| success / background | 6.32 | 4.5 |
| warning / background | 5.46 | 4.5 |
| sidebar-foreground / sidebar-accent | 14.80 | 4.5 |
| input / background | 3.25 | 3.0 |
| input / card | 3.36 | 3.0 |
| ring / background | 5.78 | 3.0 |
| ring / card | 5.98 | 3.0 |
| ring / accent | 5.14 | 3.0 |
| chart-1 … chart-5 / background | 5.77, 4.49, 3.60, 5.80, 5.67 | 3.0 |
| border / background | 1.28 | decorative only |

### Dark theme, designed rather than inverted

- **Surfaces step up in lightness.** The background is not black, and card, popover and muted step up by about 0.03 L each, so layers read without shadows.
- **The accent flips to a light step on a dark label.** `--primary` becomes `oklch(0.78 0.075 250)` and `--primary-foreground` becomes `oklch(0.20 0.03 250)`.
- **Borders are solid.** Field and divider edges use opaque colours instead of white at 10–15%, so they can be measured and they pass.

| Variable | OKLCH | Hex |
|---|---|---|
| `--background` | `oklch(0.185 0.004 85)` | `#131311` |
| `--foreground` | `oklch(0.945 0.004 85)` | `#EEEDEA` |
| `--card` | `oklch(0.215 0.005 85)` | `#1A1917` |
| `--popover` | `oklch(0.245 0.005 85)` | `#21201E` |
| `--muted` | `oklch(0.255 0.005 85)` | `#242320` |
| `--muted-foreground` | `oklch(0.735 0.008 85)` | `#ABA9A4` |
| `--secondary` | `oklch(0.275 0.006 85)` | `#292724` |
| `--secondary-foreground` | `oklch(0.93 0.004 85)` | `#E9E8E5` |
| `--accent` | `oklch(0.29 0.03 250)` | `#202D3A` |
| `--accent-foreground` | `oklch(0.91 0.025 250)` | `#D5E3F2` |
| `--primary` | `oklch(0.78 0.075 250)` | `#93BCE6` |
| `--primary-foreground` | `oklch(0.20 0.03 250)` | `#0B1723` |
| `--border` | `oklch(0.30 0.005 85)` | `#2F2E2B` |
| `--input` | `oklch(0.53 0.008 85)` | `#6E6B67` |
| `--ring` | `oklch(0.74 0.09 250)` | `#7FAFE2` |
| `--destructive` | `oklch(0.72 0.13 25)` | `#EB827B` |
| `--destructive-foreground` | `oklch(0.20 0.03 25)` | `#22100F` |
| `--success` | `oklch(0.76 0.10 150)` | `#82C38F` |
| `--warning` | `oklch(0.80 0.10 75)` | `#E4B572` |
| `--sidebar` | `oklch(0.205 0.005 85)` | `#181715` |
| `--sidebar-accent` | `oklch(0.27 0.006 85)` | `#282623` |
| `--chart-1` … `--chart-5` | `oklch(0.74 0.09 250)`, `oklch(0.74 0.08 185)`, `oklch(0.80 0.10 75)`, `oklch(0.72 0.015 85)`, `oklch(0.72 0.12 30)` | `#7FAFE2`, `#6CBCB1`, `#E4B572`, `#A9A49A`, `#E68677` |

| Pair, dark | Ratio | Floor |
|---|---|---|
| foreground / background | 15.87 | 4.5 |
| foreground / card | 14.91 | 4.5 |
| foreground / popover | 13.82 | 4.5 |
| muted-foreground / background | 7.94 | 4.5 |
| muted-foreground / muted | 6.71 | 4.5 |
| muted-foreground / card | 7.46 | 4.5 |
| muted-foreground / popover | 6.91 | 4.5 |
| muted-foreground / accent | 6.00 | 4.5 |
| secondary-foreground / secondary | 12.07 | 4.5 |
| accent-foreground / accent | 10.80 | 4.5 |
| primary-foreground / primary | 9.09 | 4.5 |
| primary / background | 9.36 | 4.5 |
| primary / card | 8.80 | 4.5 |
| primary / accent | 7.08 | 4.5 |
| destructive / background | 7.11 | 4.5 |
| destructive-foreground / destructive | 6.95 | 4.5 |
| success / background | 9.03 | 4.5 |
| warning / background | 9.86 | 4.5 |
| sidebar-foreground / sidebar | 14.58 | 4.5 |
| sidebar-foreground / sidebar-accent | 12.26 | 4.5 |
| input / background | 3.53 | 3.0 |
| input / card | 3.32 | 3.0 |
| input / popover | 3.07 | 3.0 |
| ring / background | 8.13 | 3.0 |
| ring / card | 7.64 | 3.0 |
| ring / popover | 7.08 | 3.0 |
| chart-1 … chart-5 / background | 8.13, 8.38, 9.86, 7.51, 7.15 | 3.0 |
| border / background | 1.37 | decorative only |

A first attempt at dark `--input` (`oklch(0.50 …)`) measured 2.92:1 on `--card` and was raised to 0.53. A client accent ramp needs the same pass: run the script on every pair before accepting it.

## Recommendations for the house DESIGN.md

- **File and tooling.**
  - The file lives at `docs/design/DESIGN.md`, as the baseline proposal already names it ([proposal](web-app-baseline-proposal-2026-10-22.md)).
  - Tokens go in front matter only. Colour token names match the shadcn variables (`background`, `muted-foreground`, `sidebar-accent` …), with `dark-` twins for `.dark`.
  - Add one `components` entry per text-on-surface pair, in light and dark.
  - Pin `npx -y @google/design.md@0.4.0 lint docs/design/DESIGN.md`, and fail on any error or warning in `summary`.
  - Back it with the house contrast script for the 3:1 non-text pairs, and with a leftover-defaults grep for the shadcn values listed above, including `ring-ring/50`, `outline-ring/50`, `0.625rem` and Geist.
- **Fonts.**
  - Packages: `@fontsource-variable/inter@5.3.0`, `@fontsource-variable/source-serif-4@5.3.1` (import `opsz.css`) and `@fontsource-variable/jetbrains-mono@5.3.0`.
  - Variables: `--font-sans: "Inter Variable", system-ui, sans-serif`, `--font-serif: "Source Serif 4 Variable", Georgia, serif` and `--font-mono: "JetBrains Mono Variable", ui-monospace, monospace`.
  - Keep `--font-heading` on the sans for small component titles, and use serif `type-*` utilities for page headings and answers.
  - Never load fonts from a font CDN.
- **Type scale (px size / line height).**

  | Token | Font | Size / line height | Weight |
  |---|---|---|---|
  | `display` | serif | 36/44 | 600 |
  | `headline-lg` | serif | 28/36 | 600 |
  | `headline-md` | serif | 22/30 | 600 |
  | `title` | sans | 16/24 | 600 |
  | `body-md` (UI default) | sans | 14/20 | 400 |
  | `body-sm` | sans | 13/18 | 400 |
  | `label` | sans | 13/16 | 500 |
  | `caption` | sans | 12/16 | 400 |
  | `answer-md` | serif | 17/28 | 400, measure about 68ch |
  | `code-sm` | mono | 13/20 | 400 |

  - Tables use `tnum`.
  - Weights are 400, 500 and 600 only.
  - Tracking is `-0.01em` at 22 px and above, otherwise 0.
- **Colour.** Use the light and dark tables above, with primary at accent step 700 in light and step 300-ish (`0.78`) in dark. `--success` and `--warning` are new variables registered in `@theme inline`. Raw Tailwind colours are not allowed.
- **Radius.**
  - Base `--radius: 0.375rem` (6 px).
  - Pin the steps in `@theme inline`: `--radius-sm: 4px`, `--radius-md: 4px` (menu items), `--radius-lg: 6px` (buttons, inputs), `--radius-xl: 8px` (cards, dialogs), `--radius-2xl: 10px`, `--radius-4xl: 9999px` (avatars only; badges use `rounded-sm`).
  - A client may choose 4 or 8 px as the control step. Nothing rounder, and no pill buttons.
- **Spacing and density.**
  - A 4 px grid: Tailwind's `--spacing` stays at `0.25rem`. Layout steps are 4, 8, 12, 16, 24, 32, 48 and 64.
  - Controls are 32 px (`nova`, `h-8`), with table rows at 36 px and a compact mode of 28 px for data-dense screens.
  - No target is smaller than 24 px.
  - Content is at most 1200 px wide. The answer column is about 68ch.
- **Elevation.**
  - Hairlines first, with `--shadow-xs: 0 0 #0000`.
  - Two shadow tiers, for popovers and menus and for dialogs and sheets, both low-alpha and warm-tinted. For example `0 1px 2px rgb(24 23 20 / 0.06), 0 4px 12px rgb(24 23 20 / 0.06)`, with a larger second tier. Exact values are open.
  - Dark mode separates layers by surface lightness, not shadow.
- **Focus.**
  - Use a 2 px solid outline in `--ring` with a 2 px offset on all actions, through shadcn's unlayered `:focus-visible` rule.
  - Fields use a 2 px solid indicator instead of `ring-3 ring-ring/50`. Prefer `outline` to Tailwind's box-shadow `ring`, because box-shadows disappear in forced-colours mode (Fluent and GOV.UK both plan for this).
  - `--ring` is used only for focus.
  - Sticky bars set `scroll-padding`.
- **Motion.**
  - Durations: 100 ms for hover and press, 150 ms for menus and tooltips, 200 ms for collapsibles and Trace rows, and 250 ms at most for sheets and dialogs.
  - Ease out on enter and ease in on exit, using a decelerating `cubic-bezier(0, 0, 0.2, 1)` and an accelerating `cubic-bezier(0.4, 0, 1, 1)`. No bounce or spring.
  - Under `prefers-reduced-motion: reduce`, only opacity changes, within 100 ms, and shimmer stops.
- **Copy.**
  - Sentence case everywhere: buttons, titles, menu items, column headers.
  - Plain verbs on buttons ("Approve", "Retry").
  - Tool lines are past-tense sentences.
  - No exclamation marks, and no first-person claims of feeling.
  - Label AI output "AI-generated" in words.
- **Agent surfaces.** Use shadcn's chat primitives and Trace patterns as described above. Approvals are an `Item` outside the Trace, and the empty state has 3–4 suggested prompts.
- **What clients may change** (the defined override surface):
  1. The accent ramp (steps 50–950), which drives `primary`, `accent`, `ring`, `sidebar-primary` and `chart-1`. Every pair must pass the same script; if one fails, adjust the step, never the floor.
  2. Font families, only if the client holds a web licence, with the same three roles and the house fallbacks.
  3. The logo, as an SVG or image in the header slot.
  4. Optionally, one radius step.

  Neutrals, semantic colours, spacing, motion, focus, density and copy rules stay fixed.

## What this research could not verify

- **The DESIGN.md runs were small.**
  - The CLI was run only on hand-written samples in a scratch directory. The full house file has not been written or linted.
  - Whether extra "Responsive" or "Known Gaps" sections after Do's and Don'ts trigger `section-order` was not tested.
  - The collision between `export --format css-tailwind` and shadcn's `@theme inline` is inferred, not observed in a built app.
- **The shadcn probe was partial.**
  - Its scaffold was not built or opened in a browser, so the house theme's rendered appearance, its focus rings and screenshots against the DESIGN.md are untested.
  - Only `base-nova` with `neutral` was scaffolded. Other styles and base colours were read from source.
- **Contrast figures are computed, not measured.** They come from computed sRGB values. Browser gamut mapping, font smoothing and translucent overlays could shift them slightly. Chart colour separation for colour-blind readers was not simulated.
- **Font checks were by file inspection only.**
  - Readability judgements rest on metrics, not rendered tests at 14–17 px.
  - `api.fontsource.org` was unreachable (TLS interception), so metadata came from the npm tarballs.
  - Whether Adobe has explicitly approved Fontsource redistributing subsets under the "Source" reserved name was not checked.
- **Agent UX sources were partly unreadable.**
  - The PAIR guidebook's landing page renders client-side. Its guidance was read from the chapter pages, which appear to be the 2021 edition.
  - Five HAX phase labels were inferred from numbering.
  - Carbon AI Chat's feedback, citation and reasoning-step behaviour was seen only in its type index.
  - No source says what an interface should do with partial text after a stream error, so the house rule above is an inference.
- **Enterprise system details were partly unverified.**
  - Carbon's explainability popover fields, its `$shadow` value and its radius pixel values (inferred from token names) were not confirmed.
  - Atlassian's colour and shadow values were not retrieved, and the Atlassian Sans licence was not found.
  - The SLDS 2 site would not render, so its values come from `@salesforce-ux/sds-metadata`. The Salesforce Sans licence was not checked.
  - The GDS Transport licence text was not read.
  - Fluent's density modes beyond button sizes were not checked.
  - GOV.UK's documented 1020 px page width disagrees with the Sass default of 960 px on `main`.
- **Untested choices.** The shadow values, the 36 px row height and the client override surface are proposals, not tested choices.
