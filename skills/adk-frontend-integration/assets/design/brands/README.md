# Demo brands

Four invented companies for showing what a client's own branded app could look like before the client's brand arrives. Each brand is made only of what the house [DESIGN.md](../DESIGN.md) "Brand override" section allows: the accent ramp, licensed font families, a logo and one optional control radius. Neutrals, semantic colours, spacing, density, elevation, motion, focus treatment and copy rules stay the house ones.

They are not a client, a partner or anyone's real brand.

| Brand | Industry | Accent (light / dark primary) | Interface / headings / code | Mark | Controls |
|---|---|---|---|---|---|
| [Kelderwick Bank](kelderwick-bank/brand.yaml) | Retail and private bank | Claret, hue 350: #712A50 / #DDA4BE | Instrument Sans / Newsreader / JetBrains Mono | Lucide `landmark` | 4 px |
| [Marrowby](marrowby/brand.yaml) | Grocery and home retailer | Moss, hue 120: #48531C / #B6C781 | Figtree / Fraunces / JetBrains Mono | Lucide `sprout` | 8 px |
| [Veldmark Industrial](veldmark-industrial/brand.yaml) | Engineering manufacturer | Petrol, hue 192: #0D5957 / #77C8C4 | Geologica / Source Serif 4 / JetBrains Mono | Lucide `hexagon` with a "V" | 4 px |
| [Avenhale Health](avenhale-health/brand.yaml) | Health insurer | Cobalt, hue 266 (dark 262): #26449D / #7CA7F6 | Atkinson Hyperlegible Next / Literata / JetBrains Mono | Lucide `shield-plus` | 6 px (house) |

Each folder holds `brand.yaml` (the override), `logo.svg` (mark and wordmark) and `mark.svg` (mark alone, for the collapsed sidebar or an app icon).

## Usage rule

- **Label it.** Every demo built on a demo brand says "Demo: fictional company" in the footer or the about panel, and in any deck that presents it.
- **Use `.example` domains only**, such as `kelderwick.example` or `support@marrowby.example`, and invented people. Never use the `.com` or `.co.uk`: some are registered by strangers. [RFC 2606](https://www.rfc-editor.org/rfc/rfc2606) reserves `.example` for this.
- **Never imply endorsement.** Do not put a real client's or vendor's name, logo, colour or product beside a demo brand in a way that suggests a link, and never present a demo brand as a past or current client. Do not use vendors' sample companies (Contoso, Fabrikam, Northwind, Cymbal and the like) instead.
- **Do not register, trade under, or build anything lasting on these names or logos.** They had only a quick collision check (web search and UK Companies House, 23 October 2026), not a trademark clearance. Ask legal before showing one at a public event or in marketing.
- **Swap for the real brand as soon as you can.** When the client gives you its brand and confirms its font licence covers self-hosting on the web, write the client's own `brand.yaml` and apply it with the same helper. If a pair fails, adjust the client's step, never the floor.
- **Avenhale Health:** never draw the mark as a red cross on white or white on red; the Red Cross emblem is protected.

## Apply a brand

From the skill root (`skills/adk-frontend-integration`), with Python 3.11 or newer and no packages:

```sh
# Read-only JSON report: every contrast pair, the CSS to paste, font imports, npm install line
python scripts/apply_brand.py --brand kelderwick-bank

# Only the paste-ready CSS block (:root, .dark, @fontsource-variable imports, @theme inline fonts and radius)
python scripts/apply_brand.py --brand kelderwick-bank --format css

# Write the merged DESIGN.md into the project (only when every check passes), then lint it (needs npx and network)
python scripts/apply_brand.py --brand kelderwick-bank --out ../my-app/docs/design/DESIGN.md --lint
```

`--brand` takes a shipped slug, a brand folder or a `brand.yaml` path. `--dry-run` reports what `--out` would write and never writes or runs npx. Exit codes: 0 every pair passes; 1 a contrast pair, the sRGB gamut check or the lint fails (the failing pair is named on stderr and in `checks.failing`); 2 invalid input, including any key outside the override surface (the key is named).

The helper recomputes WCAG 2.x contrast for every pair the override touches, against the house neutrals in the DESIGN.md it reads: every `components` pair at 4.5:1 (as the linter checks them), primary as link text on each surface at 4.5:1, and ring, the `input` edge and `chart-1` marks at 3:1 on the surfaces they sit on. It reads token and component names from the file, so tokens the house adds later are handled. Then paste the CSS block into the project's theme file over the matching house values, run `npm install` with the printed pinned packages, and put the logo in the header slot.

The radius lines follow the house Tailwind mapping, in which `rounded.md` is Tailwind's `rounded-lg`: a 4 px or 8 px brand sets `--radius-lg` to that value and keeps the other house radius pins.

## Brand file format

`brand.yaml` is a small YAML subset so the helper can parse it with the standard library: `key: value` lines, `#` comment lines, and one level of two-space nesting. Quote any value that starts with `@` or contains `#` or `:`. Flow mappings, lists, anchors and deeper nesting are refused.

| Key | Allowed values |
|---|---|
| `name` | The brand name (required). |
| `fictional` | `true` for a demo brand; `false` or absent for a real client. |
| `colors.<token>` | Only `primary`, `primary-hover`, `primary-active`, `primary-foreground`, `accent`, `accent-foreground`, `ring`, `chart-1` and their `dark-` twins, each as `oklch(L C h)` or `#rrggbb`. Tokens left out keep the house value. |
| `fonts.<role>`, `fonts.<role>-package`, `fonts.<role>-css` | Roles `sans`, `serif`, `mono`: the family name, a pinned `@fontsource-variable/<name>@x.y.z` package, and optionally the CSS file to import (`opsz.css`). A role left out keeps the house font. |
| `logo.logo`, `logo.mark`, `logo.alt` | Paths relative to the brand folder (`.svg`, `.png` or `.webp`) and the alternative text. |
| `rounded.md` | `4px`, `6px` or `8px`: the control radius. |

## Logos

Each logo is a Lucide icon followed by the brand name set in the brand's open font. The icon paths are copied unchanged from `lucide-static@1.61.0` (stroke width 2 in `mark.svg`, 1.75 at logo size). The wordmark, and the "V" in Veldmark's hexagon, are outlines made with fontTools from the `@fontsource-variable` latin `wght` file at weight 600 with the font's own pair kerning, so no font has to load to render them.

- The mark is drawn in `var(--primary)` and the wordmark in `currentColor`. Inline the SVG (or import it as a component, for example with SVGR) and give the header `color: var(--foreground)`; both then follow light and dark mode. The files hold no fixed colours.
- Loaded through `<img>`, the theme variables do not reach inside the file and it draws in black, which disappears on a dark background. For a favicon, export a copy of `mark.svg` with the brand's primary hex filled in.
- Each file has a `<title>` "<Name> (fictional demo brand)" for its accessible name, and carries the Lucide ISC notice and the font credit in a comment.
- Checked by rendering both files on the house light and dark backgrounds with `rsvg-convert`, not in a browser.

## Licences

| Material | Licence | Notes |
|---|---|---|
| Lucide icons `landmark`, `sprout`, `hexagon`, `shield-plus` (`lucide-static@1.61.0`) | ISC, Copyright (c) 2026 Lucide Icons and Contributors | ISC allows use, change and distribution for any purpose if the notice stays with every copy; it is in each SVG. None of the four is on Lucide's list of Feather-derived (MIT) icons. |
| Newsreader, Fraunces, Geologica, Atkinson Hyperlegible Next (outlined in the wordmarks) | SIL Open Font License 1.1 | Copyright 2020 The Newsreader Project Authors; 2020 The Fraunces Project Authors; 2020 The Geologica Project Authors; 2020-2024 The Atkinson Hyperlegible Next Project Authors. The OFL FAQ allows fonts in logos and says the artwork is not itself under the OFL. None of these fonts declares a Reserved Font Name. |
| Interface and heading fonts in `brand.yaml` (Instrument Sans, Newsreader, Figtree, Fraunces, Geologica, Source Serif 4, Atkinson Hyperlegible Next, Literata, JetBrains Mono) | SIL Open Font License 1.1 (npm `license: OFL-1.1`) | Self-host from `@fontsource-variable` at the pinned versions; never load from a font CDN. |

Never use Tabler's `brand-*` icons (real companies' logos), Remix Icon (its licence forbids logo use from 4.9.0), Logoipsum logos as they are, or any real company's logo.

## Checks recorded on 23 October 2026

Run against the working copy of the house DESIGN.md on branch `demo-polish`, which already had another change in progress (new tokens, components and a 12 px `rounded.xl` step); the Brand override surface was unchanged.

- **Helper tests:** `python -m unittest discover -s tests -p 'test_apply_brand.py'`: 13 tests, all passing.
- **Contrast:** 44 pairs per brand, all passing. Every text pair is at least 4.73:1 (floor 4.5) and every 3:1 pair at least 3.11:1. As in the house, the tightest pair is the house `input` edge on the brand's `accent` fill.
- **Lint:** each brand was applied with `--out` to a scratch copy and `npx -y @google/design.md@0.4.0 lint` reported 0 errors and 0 warnings for all four, with exit code 0. The one info finding was the token summary: 82 colours, 11 typography scales, 5 rounding levels, 13 spacing tokens and 94 components.

| Pair | Floor | Kelderwick | Marrowby | Veldmark | Avenhale |
|---|---|---|---|---|---|
| primary-foreground on primary / hover / active | 4.5 | 9.37 / 12.30 / 14.94 | 7.96 / 10.61 / 13.42 | 7.79 / 10.53 / 13.23 | 8.40 / 11.10 / 13.78 |
| primary as link on background / card / muted | 4.5 | 9.45 / 9.68 / 8.74 | 8.03 / 8.23 / 7.43 | 7.86 / 8.05 / 7.27 | 8.47 / 8.68 / 7.84 |
| primary on accent (selected row) | 4.5 | 8.34 | 7.16 | 7.03 | 7.53 |
| accent-foreground on accent | 4.5 | 12.12 | 11.63 | 11.50 | 12.01 |
| chart-1 on muted / card | 4.5 / 3 | 6.52 / 7.22 | 5.66 / 6.26 | 5.37 / 5.95 | 5.52 / 6.12 |
| ring on background / muted / accent / sidebar-accent | 3 (4.5 where a component pairs them) | 6.19 / 5.72 / 5.46 / 5.28 | 5.67 / 5.25 / 5.06 / 4.84 | 5.55 / 5.14 / 4.97 / 4.73 | 5.97 / 5.53 / 5.30 / 5.09 |
| input edge (house) on brand accent | 3 | 3.11 | 3.14 | 3.15 | 3.12 |
| dark primary-foreground on primary / hover / active | 4.5 | 8.82 / 10.94 / 7.09 | 9.86 / 11.99 / 7.99 | 9.30 / 11.34 / 7.56 | 7.51 / 9.32 / 5.99 |
| dark primary as link on background / card / muted | 4.5 | 8.97 / 8.47 / 7.58 | 10.16 / 9.60 / 8.59 | 9.60 / 9.07 / 8.11 | 7.72 / 7.29 / 6.52 |
| dark primary on accent (selected row) | 4.5 | 6.91 | 7.64 | 7.19 | 5.88 |
| dark accent-foreground on accent | 4.5 | 10.91 | 10.79 | 10.75 | 10.86 |
| dark chart-1 on muted / card | 4.5 / 3 | 6.47 / 7.24 | 7.47 / 8.35 | 6.83 / 7.64 | 6.31 / 7.05 |
| dark ring on background / muted / accent / sidebar-accent | 3 (4.5 where a component pairs them) | 7.73 / 6.53 / 5.95 / 6.27 | 8.85 / 7.48 / 6.65 / 7.18 | 8.34 / 7.04 / 6.24 / 6.76 | 7.46 / 6.31 / 5.68 / 6.05 |
| dark input edge (house) on brand accent | 3 | 3.20 | 3.12 | 3.11 | 3.17 |

**Separation** (OKLab distance, higher is more distinct; the helper reports these for information only):

| | Kelderwick | Marrowby | Veldmark | Avenhale |
|---|---|---|---|---|
| primary from the house primary, light / dark | 0.150 / 0.115 | 0.151 / 0.156 | 0.078 / 0.075 | 0.075 / 0.074 |
| primary from the nearest semantic colour, light / dark | 0.135 / 0.101 (destructive) | 0.067 / 0.065 (success) | 0.069 / 0.043 (info) | 0.128 / 0.092 (info) |
| chart-1 from the nearest other series, light / dark | 0.108 / 0.100 | 0.098 / 0.092 | 0.095 / 0.092 (house chart-1) | 0.159 / 0.138 |

## Watch items

- **Avenhale is blue by the maintainer's decision**, replacing the heather first proposed in `docs/research/demo-brands-2026-10-23.md`. It is a cobalt at hue 266: more saturated (chroma 0.15 against 0.085) and cooler than the house ink blue at hue 250, and well clear of `info` at hue 220. Lighter azures (hue 232–244) were rejected: sRGB limits them to about 0.10 chroma at a lightness that carries white text, and they came within 0.05 of NHS blue (#005EB8) and of the bright azures (around #0079C8) common in UK health care. A fictional health insurer should not look like the NHS or a real insurer. The cobalt is 0.076 from NHS blue and 0.15 from #0079C8. Hue 266 is 11° short of indigo-500 (277) at three-quarters of its chroma; in a render it reads as cobalt, not violet. Its distance from the house primary (0.075) is the smallest of the four, similar to Veldmark's; the difference is mainly chroma and hue, so it is clearest side by side.
- **Marrowby's moss sits nearest to `success`.** The house rule that status is always given in words and an icon covers this.
- **Veldmark's dark primary is 0.043 from `dark-info`**, the same as the house's own primary, and its `chart-1` stays the house blue because a petrol series looked like the teal `chart-2`.
- **Kelderwick's claret is nearest to `destructive`.** The house already keeps Deny as an outline button, so a claret Approve never sits beside a red Deny.

## Not verified

- No colour was measured in a rendered app with axe, and no colour-blind simulation was run.
- The fonts and logos were not seen in a browser at header size; the logos were rendered only with `rsvg-convert`.
- Nobody has checked whether the four marks, as drawn, resemble a real company's logo.
- The names had only a quick collision check; no trademark register was searched. Nothing here is legal advice.
- Whether each `@fontsource-variable` version is at least two weeks old was not checked.
- NHS blue (#005EB8) was taken from memory of the NHS identity colours, not re-read for this note. Whether cobalt hue 266 reads as blue rather than violet is a judgement from one render.
