# Demo brands: four fictional clients for the house design system

Consultants want proof-of-concept apps that look like a real client's production app without using a real company's marks. This note proposes **four invented demo brands**, each built only from what the house [DESIGN.md](../../skills/adk-frontend-integration/assets/design/DESIGN.md) "Brand override" section allows: the accent ramp, licensed fonts, a logo and one optional radius step.

| Brand | Industry | Accent | Interface / heading font | Logo mark (Lucide) | Control radius |
|---|---|---|---|---|---|
| **Kelderwick Bank** | Retail and private bank | Claret, hue 350 (`#712A50`) | Instrument Sans / Newsreader | `landmark` | 4 px |
| **Marrowby** | Grocery and home retailer | Moss, hue 120 (`#48531C`) | Figtree / Fraunces | `sprout` | 8 px |
| **Veldmark Industrial** | Engineering manufacturer | Petrol, hue 192 (`#0D5957`) | Geologica / Source Serif 4 (house) | `hexagon` with a "V" | 4 px |
| **Avenhale Health** | Health insurer | Heather, hue 325 (`#643C66`) | Atkinson Hyperlegible Next / Literata | `shield-plus` | 6 px (house) |

The main findings:

- **Do not use the vendors' fictional companies.** Contoso, Fabrikam, Northwind, Tailspin and Woodgrove are Microsoft's. Its trademark group cleared them for Microsoft's own samples, and Microsoft holds the matching domains. The only permission to outsiders on record is informal non-objection to W3C. Cymbal Bank and Cymbal Retail are Google's sample companies, and Google's content licence excludes its brand features. Using any of these in a client demo would suggest a link to that vendor. "Acme" is used by many real companies. Inventing our own names is the safer route.
- **The four invented names had no exact matches** in a quick web search and a UK Companies House name search. This is not a legal clearance. Some of the matching `.com` domains are registered by other people, so demo email addresses and URLs must use the reserved `.example` domain.
- **Build logos from an open icon and a wordmark set in an OFL font.** Lucide (ISC), Tabler, Phosphor, Heroicons and Iconoir (all MIT) and Material Symbols (Apache-2.0) contain nothing that forbids using an icon as a logo. **Remix Icon has forbidden logo use since 4.9.0** (January 2026), although its npm metadata still says Apache-2.0. Logoipsum logos are placeholders only, and its licence forbids using them unaltered as a brand identity or redistributing them as they are.
- **Every pair passes, and every override lints clean.** All 16 ramp tokens per brand were checked, in light and dark. Every text pair is at least 5.4:1 (floor 4.5) and every 3:1 pair is at least 3.10:1. The tightest 3:1 pair is the house input edge on the brand's accent fill, as it is for the house itself. Each brand applied to a copy of the house DESIGN.md gives `@google/design.md@0.4.0 lint` a summary of 0 errors and 0 warnings. A deliberately broken copy produced 4 warnings, so the check does fire.
- **Two pitfalls shaped the colours.** The brand's `chart-1` must stay distinct from the fixed `chart-2`…`chart-5`; Veldmark's teal would have duplicated `chart-2`, so it keeps the house blue for `chart-1`. The primary must also stay away from the semantic colours; Marrowby's moss sits nearest to `success`, and it is flagged below.

Everything here was read or run on 23 October 2026. Nothing here is legal advice.

## 1. Vendors' fictional companies

| Name | Owner and evidence | Usage terms for third parties | Verdict |
|---|---|---|---|
| Contoso, Fabrikam, Litware and the rest of Microsoft's set | Microsoft's legal Trademark Group "performed background checks on these names and cleared them for use as fictitious entities by Microsoft samples and documentation" ([Raymond Chen, The Old New Thing, 2006](https://devblogs.microsoft.com/oldnewthing/20061013-05/?p=29393)). Microsoft's trademark guidelines use Contoso as "the fictitious partner brand" ([Microsoft trademark guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general)). | No public licence was found. Microsoft told W3C it "does not object to the W3C use" of Fabrikam ([Jonathan Marsh, 16 Aug 2005](https://lists.w3.org/Archives/Public/public-ws-addressing/2005Aug/0049.html)) and of "Contoso, Ltd" ([Asir Vedamuthu, 5 Feb 2007](https://lists.w3.org/Archives/Public/public-ws-policy/2007Feb/0006.html)). Both were informal statements to one standards body. The same 2007 thread relays W3C legal advice "not to use company names and rather 'example Ltd' UNLESS we have a written permission from the name and trademark owner". | Avoid |
| Northwind (Traders), Tailspin (Toys), Woodgrove (Bank) | Also Microsoft sample companies. `whois` on 23 October 2026: `contoso.com` has registrant organisation **Microsoft Corporation** (created 1998). `fabrikam.com`, `northwindtraders.com`, `tailspintoys.com` and `woodgrovebank.com` are all held through MarkMonitor, the registrar that holds `contoso.com`. Their registrant was not shown. | As above. | Avoid |
| Cymbal Bank, Cymbal Retail (Google) | Google's GKE learning path says "Cymbal Bank is just an example application" ([Google Cloud docs](https://docs.cloud.google.com/kubernetes-engine/docs/learn/scalable-apps)). Cymbal Retail is the company in a Professional Cloud Architect [case study](https://services.google.com/fh/files/misc/cymbal_retail_case_study_english.pdf). The sample code ([bank-of-anthos](https://github.com/GoogleCloudPlatform/bank-of-anthos)) is Apache-2.0 and links a live demo at `cymbal-bank.fsi.cymbal.dev`. | Page text is CC BY 4.0 and code is Apache-2.0, but "Google's trademarks and other brand features are not included in this license" ([Google Developers site policies](https://developers.google.com/site-policies)). Apache-2.0 §6 also grants no trademark rights. "Cymbal" is not on Google's public [trademark list](https://about.google/brand-resource-center/trademark-list/), but Google calls that list "non-exhaustive". | Avoid. To an engineer at a Google Cloud client, a Cymbal demo reads as Google material. |
| Northern Trail Outfitters, Universal Containers, Cloud Kicks (Salesforce) | Seen only in unofficial exam-practice pages. No Salesforce primary source was found in this pass. | Unknown. | Avoid, for the same reason as the others. |
| Acme | A common real company name (Acme Markets, Acme Brick and others) and the Looney Tunes joke ([Straight Dope](https://www.straightdope.com/columns/read/2224/whats-up-with-the-acme-company/); [99% Invisible](https://99percentinvisible.org/article/acme-morley-real-stories-behind-famous-fictional-film-tv-brands/)). | Not one owner. The name is shared by real companies across many classes of goods. | Avoid in client demos. It reads as a joke and it collides with real companies. |

**Why invent our own names.** Each vendor's set either belongs to a vendor (Microsoft, Google) or collides with real companies (Acme). A consultancy demo for one vendor's client that uses another vendor's sample company also blurs who made what. Invented names avoid all three problems. Made-up words also collide less than real-word compounds: "Larkspur Savings", "Wrenfield", "Penhallow", "Ashcombe" and "Quenby" each returned between 4 and 20 registered UK companies.

**Quick collision check of the proposed names.** This was not a legal clearance. No USPTO, EUIPO or UKIPO trademark search was run, because their search tools render client-side.

| Name | Web search (exact phrase) | UK Companies House name search | `.com` / `.co.uk` |
|---|---|---|---|
| Kelderwick | No pages for the word. Near matches are the places Keckwick and Kildwick. | 0 companies containing the stem | `.com` and `.co.uk` both unregistered |
| Marrowby | No pages. Near matches are the places Garrowby, Moorby and Barrowby. | 0 | `.com` registered 8 Oct 2025 and showing a default Apache page |
| Veldmark | No pages. Near matches are "Feldmark" (ecology) and "Veld". | 0 | `.com` registered since 2001, with no content served |
| Avenhale | No pages. Near matches are Avenhorn and Avenel. | 0 | `.com` unregistered |

Rejected on the way: Sallowfield (one letter from the real village of Swallowfield), Torvane (a soil-testing instrument name), and Larkmoor, Wellmoor, Elmsworth, Mirelle, Corvale and Orbury (all existing UK companies).

**Domains in demo data.** Use only names under the reserved `.example` top-level domain, such as `kelderwick.example` or `support@marrowby.example`. Never use the `.com`, which a stranger may own; two of the four already belong to someone else. [RFC 2606](https://www.rfc-editor.org/rfc/rfc2606) reserves `.example`, `.test` and `example.com/.net/.org` for exactly this use.

## 2. Logos: placeholder sets, icon licences, wordmarks

| Source | Licence (read at) | Logo use | Notes |
|---|---|---|---|
| [Logoipsum](https://logoipsum.com/license) | Its own licence: free, with no attribution needed | **Placeholder only.** You may not "use unaltered logos as final logos, trademarks, service marks, or brand identities", "resell, redistribute, or package the logo 'as is'", or register them. Modified logos may go into products you sell. The [FAQ](https://logoipsum.com/faq) suggests labelling them as placeholders. | Not suitable for the toolkit. Shipping its SVGs in our repository would be redistributing them as they are, and a recurring demo brand is closer to a brand identity than a placeholder. |
| [Lucide](https://github.com/lucide-icons/lucide/blob/main/LICENSE) (`lucide-static@1.61.0`, ISC) | ISC. Icons derived from Feather are MIT (Cole Bemis); the LICENSE lists them, and none of the four marks below is on the list. | Not restricted. ISC permits use, modification and distribution "for any purpose" if the notice is kept "in all copies". | Already the house icon set. Keep the ISC notice in a comment in the logo SVG or a NOTICE file next to it. |
| [Tabler Icons](https://github.com/tabler/tabler-icons/blob/main/LICENSE) (`@tabler/icons@3.49.0`) | MIT | Not restricted | It also ships `brand-*` icons of real companies. Never use those as a mark. |
| [Phosphor](https://github.com/phosphor-icons/core/blob/main/LICENSE) (`@phosphor-icons/core@2.1.1`) | MIT | Not restricted | — |
| [Heroicons](https://github.com/tailwindlabs/heroicons/blob/master/LICENSE) (`@heroicons/react@2.2.0`) | MIT | Not restricted | — |
| [Iconoir](https://github.com/iconoir-icons/iconoir/blob/main/LICENSE) (`iconoir@7.12.1`) | MIT | Not restricted | — |
| [Material Symbols](https://developers.google.com/fonts/docs/material_symbols) (`@material-symbols/svg-400@0.48.1`) | Apache-2.0 ([LICENSE](https://github.com/google/material-design-icons/blob/master/LICENSE)) | Not restricted by the licence. Apache-2.0 §6 withholds Google's trademarks, which concern the Material name, not the icon shapes. | Apache-2.0 needs the licence text to travel with redistributed copies. The icons look like Google's, which works against a neutral demo. |
| [Remix Icon](https://github.com/Remix-Design/RemixIcon/blob/master/License) (`remixicon@4.9.1`) | **Remix Icon License v1.0** (January 2026) | **Forbidden.** §3.3: you may not use the icons "as a logo, trademark, or brand identifier", including "creating a logo by applying simple modifications such as color changes, rotation, combination, or layout". | `remixicon@4.8.0` shipped Apache-2.0, and 4.9.0 shipped the new licence. The npm `license` field still says `Apache-2.0` at 4.9.1, so licence scanners will miss the change. |

**Wordmarks in an OFL font.** The [OFL FAQ](https://openfontlicense.org/ofl-faq/) lists logos among permitted uses: "No additional license or permission is required". Artwork made with the font "does not make the resulting artwork subject to the OFL", and its author keeps copyright. The FAQ also says the OFL "does not grant any rights under trademark law". Google Fonts' FAQ says its fonts can be used in logos (as quoted by a search engine; the [FAQ page](https://fonts.google.com/faq) renders client-side and could not be read directly). None of the font notices checked for the demo brands declares a Reserved Font Name. The checked notices were Instrument Sans, Newsreader, Figtree, Fraunces, Geologica, Atkinson Hyperlegible Next, Literata, Public Sans and Spectral, all from [google/fonts](https://github.com/google/fonts/tree/main/ofl).

**Recommended logo construction.**

- Make one SVG per brand: a Lucide icon at 24 units, stroke 1.75, drawn in `currentColor`, followed by the brand name set in the brand's OFL font.
- Convert the wordmark to outlines (for example with fontTools' SVG path pen), so the file does not depend on a font loading.
- Put the Lucide ISC notice and the font credit in an SVG comment.
- In the header, draw the mark in `--primary`, or `--dark-primary` in dark mode, and the wordmark in `--foreground`.
- Give it the alternative text "<Name> (fictional demo brand)".
- WCAG 2.2 exempts logotypes from the contrast criteria 1.4.3 and 1.4.11, but these colours pass anyway.

## 3. Open fonts for brand roles

The house roles stay fixed: interface sans, a serif for headings and answers, and mono for code (JetBrains Mono for every brand). Each candidate's `@fontsource-variable` latin `wght` file was inspected with fontTools 4.25.0 for a `tnum` feature. Tabular figures are required for the sans, because the sans sets `data-md`. They are optional for the serif, which sets prose. The versions are npm `latest` on 23 October 2026, and every package's npm `license` is `OFL-1.1`.

| Font | Package | `tnum` | Axes in the default file | Use |
|---|---|---|---|---|
| Instrument Sans | `@fontsource-variable/instrument-sans@5.3.0` | yes | wght 400–700 (the package also has `wdth`) | **Kelderwick interface.** Narrow, precise and quietly formal. |
| Figtree | `@fontsource-variable/figtree@5.3.0` | yes | wght 300–900 | **Marrowby interface.** Friendly geometric. |
| Geologica | `@fontsource-variable/geologica@5.3.0` | yes | wght 100–900 (package also has `slnt`, `CRSV`, `SHRP`) | **Veldmark interface.** Engineered, slightly technical. |
| Atkinson Hyperlegible Next | `@fontsource-variable/atkinson-hyperlegible-next@5.3.0` | yes | wght 200–800 | **Avenhale interface.** Designed by the Braille Institute for legibility. Suits a health insurer. |
| Newsreader | `@fontsource-variable/newsreader@5.3.0` (has `opsz.css`) | yes | wght 200–800, opsz | **Kelderwick serif.** Editorial and established. |
| Fraunces | `@fontsource-variable/fraunces@5.3.0` (has `opsz.css`; `SOFT`, `WONK` axes) | **no**, also absent upstream | wght 100–900, opsz | **Marrowby serif.** Warm and soft. Prose only; tables stay in the sans. |
| Literata | `@fontsource-variable/literata@5.3.0` (has `opsz.css`) | yes | wght 200–900, opsz | **Avenhale serif.** Made for long reading. |
| Source Serif 4 | `@fontsource-variable/source-serif-4@5.3.1` | yes | wght, opsz | Veldmark keeps the house serif. |
| Public Sans | `@fontsource-variable/public-sans@5.3.0` | yes | wght 100–900 | Reserve for a public-sector demo (see the end of section 4). |
| Manrope, Plus Jakarta Sans, Outfit, Onest (`5.3.1`), Bricolage Grotesque, Work Sans, Schibsted Grotesk | `@fontsource-variable/*@5.3.0` | yes | wght | Usable alternatives. Not chosen, either because they are widely seen in start-up sites (Plus Jakarta, Outfit, Manrope) or because they are display-leaning (Bricolage). |
| DM Sans, Libre Franklin, Lexend | `@fontsource-variable/*@5.3.0` | **no** (DM Sans also checked upstream in [google/fonts](https://github.com/google/fonts/tree/main/ofl/dmsans): none) | wght | **Not suitable for the interface role.** Without `tnum`, `tabular-nums` does nothing and table digits misalign. |
| Spectral | `@fontsource/spectral@5.3.0` (no variable package) | yes | static | Elegant, but static files only. Newsreader does the same job as one variable file. |
| IBM Plex, Inter | — | — | — | Excluded. IBM Plex is IBM's signature face, and Inter is the house face. |

CSS stacks keep the house fallbacks. For example, `--font-sans: "Figtree Variable", ui-sans-serif, system-ui, sans-serif` and `--font-serif: "Fraunces Variable", Georgia, "Times New Roman", serif`. The fontsource family names were read from each package's `index.css`. Import `opsz.css` for Newsreader, Fraunces and Literata, as the house does for Source Serif 4.

## 4. The four demo brands

### Method

- **Script and floors.** A small script (`colour.py`, `final2.py` in the scratch directory) converts OKLCH to sRGB. It clips to gamut, rounds to 8-bit, and computes WCAG 2.x contrast. Before it was used, it was checked against the house table: it gives 17.33 for foreground on background (house 17.3), 8.81 for primary-foreground on primary (8.8), 3.25 for input on muted (3.25) and 9.11 for dark primary-foreground on primary (9.1). The floors are the house ones: text pairs at 4.5:1 (chart-1 included, because the linter checks `chart-series-*` at 4.5) and ring at 3:1 on every surface it sits on.
- **Neutrals.** These are read from DESIGN.md. The brief's figures differ slightly; the file is authoritative. Light: background `oklch(0.988 0.003 85)`, card `oklch(0.997 0.0015 85)`, muted `oklch(0.962 0.004 85)` (not 0.966), sidebar-accent `oklch(0.935 0.006 85)`. Dark: background `oklch(0.185 0.004 85)` (#131311), card `oklch(0.215 0.005 85)` (#1A1917), popover `oklch(0.245 0.005 85)`, muted `oklch(0.255 0.005 85)`, sidebar-accent `oklch(0.27 0.006 85)`.
- **The ramp shape copies the house.**
  - Light: primary at L ≈ 0.40–0.42, hover −0.07, active −0.13, accent at L 0.948 with low chroma, accent-foreground at L 0.30, ring and chart-1 at L ≈ 0.50.
  - Dark: primary at 0.78–0.80, hover +0.06, active −0.06, a dark label at L 0.20, accent at 0.29, ring and chart-1 at 0.74–0.76.
  - `primary-foreground` stays the house `oklch(0.985 0.003 85)`.
  - Every value is inside the sRGB gamut.
- **Two extra separations, with the house as the yardstick.** Both are measured as OKLab ΔE.
  - **chart-1 against the fixed chart-2…5.** The house's own closest pair is 0.092 (dark chart-1 against chart-2). No brand goes below that.
  - **primary against the semantic text colours.** The house's closest pair is 0.043 (dark primary against dark info). No brand goes below that either.
- **No "AI purple", neon or gradients.** In OKLCH, Tailwind's indigo-500 `#6366F1` sits at hue 277, violet-500 at 293 and purple-500 at 304. Every brand hue is at least 21° clear of 304. Chroma stays at or below 0.12, against 0.20–0.26 for those references. There are no gradients, and none are possible: the override surface holds only flat tokens.

### Kelderwick Bank: claret, hue 350

A long-established retail and private bank: steady, formal, quietly confident. Interface in **Instrument Sans**, headings and answers in **Newsreader**, controls at **4 px**. Logo: Lucide `landmark` (a columned building) in claret, followed by "Kelderwick" in Newsreader 600, outlined.

| Token | Light | Dark |
|---|---|---|
| primary | `oklch(0.40 0.11 350)` #712A50 | `oklch(0.78 0.075 350)` #DDA4BE |
| primary-hover | `oklch(0.33 0.095 350)` #571C3C | `oklch(0.84 0.058 350)` #E9BCD0 |
| primary-active | `oklch(0.27 0.08 350)` #41122C | `oklch(0.72 0.085 350)` #CE8FAC |
| primary-foreground | house `oklch(0.985 0.003 85)` | `oklch(0.20 0.03 350)` #201018 |
| accent (subtle) | `oklch(0.948 0.014 350)` #F6EAEF | `oklch(0.29 0.03 350)` #37252D |
| accent-foreground | `oklch(0.30 0.09 350)` #4D1634 | `oklch(0.91 0.022 350)` #EEDCE3 |
| ring | `oklch(0.50 0.12 350)` #94436D | `oklch(0.74 0.10 350)` #DB91B4 |
| chart-1 | `oklch(0.47 0.12 345)` #883B6A | `oklch(0.74 0.11 340)` #D98FC1 |

The chart hue is turned 5–10° away from the primary hue to keep it clear of `chart-5` (brick, hue 30): ΔE 0.108 in light and 0.100 in dark. Its closest semantic colour is `destructive`, at ΔE 0.135 in light and 0.101 in dark. That is wider than the house's own closest pair, and the house already forbids destructive styling for Deny, so the claret Approve button does not sit next to a red Deny.

### Marrowby: moss, hue 120

A grocery and home retailer: warm, friendly, practical. Interface in **Figtree**, headings and answers in **Fraunces** (use `opsz.css`), controls at **8 px**. Logo: Lucide `sprout` in moss, followed by "Marrowby" in Fraunces 600, outlined.

| Token | Light | Dark |
|---|---|---|
| primary | `oklch(0.42 0.08 120)` #48531C | `oklch(0.80 0.095 120)` #B6C781 |
| primary-hover | `oklch(0.35 0.07 120)` #364010 | `oklch(0.86 0.075 120)` #CAD9A2 |
| primary-active | `oklch(0.29 0.06 120)` #282F08 | `oklch(0.74 0.10 120)` #A3B46B |
| primary-foreground | house | `oklch(0.20 0.03 120)` #141808 |
| accent | `oklch(0.948 0.022 120)` #ECF0E0 | `oklch(0.29 0.03 120)` #292E1D |
| accent-foreground | `oklch(0.30 0.065 120)` #2A3206 | `oklch(0.91 0.03 120)` #DEE5CF |
| ring | `oklch(0.50 0.10 120)` #5C6B21 | `oklch(0.76 0.105 120)` #A8BB6D |
| chart-1 | `oklch(0.48 0.11 125)` #4F6815 | `oklch(0.76 0.12 118)` #AABB5F |

**Watch item.** The primary is closest to `success`, at ΔE 0.067 in light and 0.065 in dark. That clears the house's 0.043 yardstick, but a moss link and a green "Ran" line are both greenish. The house rule that status is always given in words and an icon covers this. Leaning the hue further towards olive (110–115) moves it closer to `warning` instead. `chart-1` against `chart-3` (amber) is ΔE 0.105 in light and 0.092 in dark, equal to the house's closest chart pair.

### Veldmark Industrial: petrol, hue 192

An engineering manufacturer: exact, sturdy, technical. Interface in **Geologica**, headings and answers in the house **Source Serif 4**, controls at **4 px**. Logo: Lucide `hexagon` with a "V" in Geologica 600 inside it, followed by "Veldmark" in Geologica 600, outlined.

| Token | Light | Dark |
|---|---|---|
| primary | `oklch(0.42 0.068 192)` #0D5957 | `oklch(0.78 0.08 192)` #77C8C4 |
| primary-hover | `oklch(0.35 0.058 192)` #054442 | `oklch(0.84 0.065 192)` #98D9D5 |
| primary-active | `oklch(0.29 0.048 192)` #033331 | `oklch(0.72 0.085 192)` #5EB6B2 |
| primary-foreground | house | `oklch(0.20 0.03 192)` #031A19 |
| accent | `oklch(0.948 0.018 192)` #E1F2F1 | `oklch(0.29 0.028 192)` #1A302F |
| accent-foreground | `oklch(0.30 0.05 192)` #023634 | `oklch(0.91 0.025 192)` #CFE7E5 |
| ring | `oklch(0.50 0.082 192)` #10726F | `oklch(0.74 0.08 192)` #6ABBB8 |
| chart-1 | **house** `oklch(0.50 0.095 250)` | **house** `oklch(0.74 0.09 250)` |

- **chart-1 stays the house blue.** A petrol `chart-1` was within ΔE 0.024–0.045 of the fixed teal `chart-2` (hue 185), which makes two series look alike. Keeping the house value is within the override rules, since changing a token is allowed but not required. The brand teal still shows up in charts through `chart-2`.
- **The hue was moved from 200 to 192** to keep the dark primary clear of `dark-info` (hue 220): ΔE 0.043 at 192, the same as the house's own primary against info, and 0.034 at 200.
- **Gamut limits the chroma.** Teal at L 0.42 has room for only about 0.072 chroma in sRGB, so this is the quietest of the four ramps.

### Avenhale Health: heather, hue 325

A health insurer: calm, caring, plain-spoken. Interface in **Atkinson Hyperlegible Next**, headings and answers in **Literata** (use `opsz.css`), with the house's 6 px controls. Logo: Lucide `shield-plus` in heather, followed by "Avenhale" in Atkinson Hyperlegible Next 600, outlined. Never draw the mark as a red cross on white or white on red, because the Red Cross emblem is protected.

| Token | Light | Dark |
|---|---|---|
| primary | `oklch(0.42 0.085 325)` #643C66 | `oklch(0.78 0.075 325)` #D0A7D2 |
| primary-hover | `oklch(0.35 0.072 325)` #4D2C4F | `oklch(0.84 0.06 325)` #DFBEE0 |
| primary-active | `oklch(0.29 0.06 325)` #3A203C | `oklch(0.72 0.085 325)` #C092C2 |
| primary-foreground | house | `oklch(0.20 0.03 325)` #1D111E |
| accent | `oklch(0.948 0.016 325)` #F4EAF4 | `oklch(0.29 0.032 325)` #342634 |
| accent-foreground | `oklch(0.30 0.072 325)` #3F2041 | `oklch(0.91 0.024 325)` #EADCEA |
| ring | `oklch(0.50 0.11 325)` #824B85 | `oklch(0.74 0.10 325)` #CB95CE |
| chart-1 | `oklch(0.50 0.11 325)` #824B85 | `oklch(0.74 0.10 325)` #CB95CE |

**The maintainer's call.** This is the brand closest to the purple family. Hue 325 is 48° from indigo-500, 32° from violet-500 and 21° from purple-500, at less than half their chroma. It reads as a muted heather or plum, not as a violet. If the maintainer still reads it as purple, the next free zone that passes every check above is blue, which would sit too close to the house look.

### Contrast results (all pass)

Each cell lists the ratios against the surfaces in the order given in the row heading.

| Pair | Floor | Kelderwick | Marrowby | Veldmark | Avenhale |
|---|---|---|---|---|---|
| primary-foreground on primary / hover / active | 4.5 | 9.4 / 12.3 / 14.9 | 8.0 / 10.6 / 13.4 | 7.8 / 10.5 / 13.2 | 8.5 / 11.3 / 13.9 |
| primary as link on background / card / muted | 4.5 | 9.4 / 9.7 / 8.7 | 8.0 / 8.2 / 7.4 | 7.9 / 8.1 / 7.3 | 8.5 / 8.7 / 7.9 |
| primary on accent (selected row) | 4.5 | 8.3 | 7.2 | 7.0 | 7.5 |
| accent-foreground on accent | 4.5 | 12.1 | 11.6 | 11.5 | 12.0 |
| chart-1 on muted / card | 4.5 | 6.5 / 7.2 | 5.7 / 6.3 | 5.4 / 5.9 | 5.7 / 6.3 |
| ring on background / card / muted / accent / sidebar-accent | 3.0 | 6.2 / 6.3 / 5.7 / 5.5 / 5.3 | 5.7 / 5.8 / 5.2 / 5.1 / 4.8 | 5.6 / 5.7 / 5.1 / 5.0 / 4.7 | 6.2 / 6.3 / 5.7 / 5.4 / 5.3 |
| input edge (house) on brand accent | 3.0 | 3.11 | 3.14 | 3.15 | 3.10 |
| dark-primary-foreground on dark-primary / hover / active | 4.5 | 8.8 / 10.9 / 7.1 | 9.9 / 12.0 / 8.0 | 9.3 / 11.3 / 7.6 | 8.8 / 10.9 / 7.1 |
| dark-primary as link on background / card / popover / muted | 4.5 | 9.0 / 8.5 / 7.9 / 7.6 | 10.2 / 9.6 / 8.9 / 8.6 | 9.6 / 9.1 / 8.4 / 8.1 | 9.0 / 8.5 / 7.9 / 7.6 |
| dark-primary on dark-accent | 4.5 | 6.9 | 7.6 | 7.2 | 6.9 |
| dark-accent-foreground on dark-accent | 4.5 | 10.9 | 10.8 | 10.8 | 10.8 |
| dark-chart-1 on dark-muted / dark-card | 4.5 | 6.5 / 7.2 | 7.5 / 8.4 | 6.8 / 7.6 | 6.5 / 7.3 |
| dark-ring on background / card / muted / accent / sidebar-accent | 3.0 | 7.7 / 7.3 / 6.5 / 6.0 / 6.3 | 8.9 / 8.4 / 7.5 / 6.7 / 7.2 | 8.3 / 7.9 / 7.0 / 6.2 / 6.8 | 7.7 / 7.3 / 6.5 / 5.9 / 6.3 |
| dark-input edge (house) on brand dark-accent | 3.0 | 3.20 | 3.12 | 3.11 | 3.19 |

**Input edges are the tightest pairs**, as they are for the house (3.14 light, 3.13 dark), because the brand changes the accent fill that the input edge sits on. Any future tweak to an accent step must recompute this row.

**Separation (OKLab ΔE; higher is more distinct):**

| | House | Kelderwick | Marrowby | Veldmark | Avenhale |
|---|---|---|---|---|---|
| Closest chart-2…5, light / dark | 0.095 / 0.092 | 0.108 / 0.100 | 0.098 / 0.092 | 0.095 / 0.092 (house chart-1) | 0.121 / 0.110 |
| Closest semantic colour, light / dark | 0.091 / 0.043 (info) | 0.135 / 0.101 (destructive) | 0.067 / 0.065 (success) | 0.069 / 0.043 (info) | 0.117 / 0.117 (info) |
| Distance from the house primary, light / dark | — | 0.150 / 0.115 | 0.151 / 0.156 | 0.078 / 0.075 | 0.105 / 0.091 |

### Lint run

- **Method.** For each brand, the house DESIGN.md was copied to the scratch directory. The 16 ramp tokens, the `fontFamily` values for the changed roles and `rounded.md` (4 px for Kelderwick and Veldmark, 8 px for Marrowby) were replaced, and `npx -y @google/design.md@0.4.0 lint <file>` was run on the copy.
- **Results.** The house and all four brands gave `{"errors": 0, "warnings": 0, "infos": 1}`, with exit code 0. The info finding is the token summary: 74 colours, 11 typography scales, 4 rounding levels, 13 spacing tokens and 69 components.
- **Negative control.** Moving Kelderwick's primary to L 0.70 gave 4 warnings, for example "textColor (#fbfaf8) on backgroundColor (#d281a8) has contrast ratio 2.70:1". The gate therefore catches a bad override. The exit code was still 0, which matches the house note that the JSON summary must be parsed.
- **What the lint does not check.** It checks only the 4.5:1 component pairs. The 3:1 rows above come from the script.

### Not proposed: a public-sector brand

A fictional "agency" is more likely to be mistaken for a real government body, and the GOV.UK look is reserved. The GOV.UK Design System says that services on `service.gov.uk` must use GDS Transport, and that services elsewhere should "use an alternative typeface" ([GOV.UK typeface](https://design-system.service.gov.uk/styles/typeface/)). For a public-sector demo, use the house theme unchanged. Optionally use Public Sans as the interface font, with a plainly fictional authority name and no crest, flag or coat of arms.

## 5. Where the brands should live, and the usage rule

Proposed layout. None of these files has been created yet.

```
skills/adk-frontend-integration/assets/design/brands/
  README.md                    # the usage rule below and the summary table
  kelderwick-bank/
    brand.yaml                 # only the override surface (see below)
    logo.svg                   # mark + outlined wordmark, ISC/OFL credit in a comment
    mark.svg                   # mark alone, for favicons and the collapsed sidebar
  marrowby/ …
  veldmark-industrial/ …
  avenhale-health/ …
skills/adk-frontend-integration/scripts/apply_brand.py
```

`brand.yaml` uses DESIGN.md front-matter keys, so it reads like a fragment of the house file. For example:

```yaml
name: Kelderwick Bank
fictional: true
colors:
  primary: "oklch(0.40 0.11 350)"
  primary-hover: "oklch(0.33 0.095 350)"
  primary-active: "oklch(0.27 0.08 350)"
  accent: "oklch(0.948 0.014 350)"
  accent-foreground: "oklch(0.30 0.09 350)"
  ring: "oklch(0.50 0.12 350)"
  chart-1: "oklch(0.47 0.12 345)"
  dark-primary: "oklch(0.78 0.075 350)"
  dark-primary-hover: "oklch(0.84 0.058 350)"
  dark-primary-active: "oklch(0.72 0.085 350)"
  dark-primary-foreground: "oklch(0.20 0.03 350)"
  dark-accent: "oklch(0.29 0.03 350)"
  dark-accent-foreground: "oklch(0.91 0.022 350)"
  dark-ring: "oklch(0.74 0.10 350)"
  dark-chart-1: "oklch(0.74 0.11 340)"
fonts:
  sans: { family: Instrument Sans, package: "@fontsource-variable/instrument-sans@5.3.0" }
  serif: { family: Newsreader, package: "@fontsource-variable/newsreader@5.3.0", import: opsz.css }
rounded:
  md: 4px
logo:
  file: logo.svg
  alt: "Kelderwick Bank (fictional demo brand)"
```

`apply_brand.py` should:

1. Copy the house DESIGN.md to the target project's `docs/design/DESIGN.md`.
2. Refuse any key outside the Brand override list, so neutrals, semantic colours, spacing and so on cannot drift.
3. Replace the listed tokens, `fontFamily` values and `rounded.md`.
4. Run the pinned lint and fail on any error or warning.
5. Recompute the 3:1 rows (ring on every surface, and input on accent).
6. Print the `:root` and `.dark` variable block, the `@fontsource-variable` imports and the matching `@theme inline` radius pins:
   - 4 px controls: `--radius-lg: 4px`, keeping `--radius-xl: 8px` for cards.
   - 8 px controls: `--radius-lg: 8px`.

   These follow the house mapping, in which `rounded.md` is Tailwind's `rounded-lg`.

The demo brands are then one command away. They stay one source of truth, and the result passes `scripts/check_theme.py` unchanged, since that script checks only for shadcn defaults and Geist. The `.yaml` values in this note and the scratch copies used for the lint run are the same.

**Usage rule for consultants.** The demo brands (Kelderwick Bank, Marrowby, Veldmark Industrial and Avenhale Health) are invented companies for showing what a client's own branded app could look like. They are not a client, a partner or anyone's real brand.

- Label every demo built on them "Demo: fictional company" in the footer or the about panel, and in the deck that presents it.
- Use only `.example` domains and invented people in their data.
- Never put a real client's name, logo, colour or product beside a demo brand in a way that implies endorsement, and never present a demo brand as a past or current client.
- Do not use Microsoft, Google, Salesforce or other vendors' sample companies instead.
- As soon as the client provides its brand and confirms its font licence for web self-hosting, replace the demo brand with the client's own override. Run the same lint and contrast checks, and adjust the client step, never the floor.
- Do not register, trade under, or build anything lasting on a demo brand name or logo. They were checked only for obvious collisions, not cleared as trademarks.

## Sources (all read on 23 October 2026)

- Microsoft: [The Old New Thing, 13 Oct 2006](https://devblogs.microsoft.com/oldnewthing/20061013-05/?p=29393); [trademark and brand guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general); W3C list posts of [16 Aug 2005](https://lists.w3.org/Archives/Public/public-ws-addressing/2005Aug/0049.html) and [5 Feb 2007](https://lists.w3.org/Archives/Public/public-ws-policy/2007Feb/0006.html); `whois` for `contoso.com`, `fabrikam.com`, `northwindtraders.com`, `tailspintoys.com` and `woodgrovebank.com`.
- Google: [GKE scalable apps learning path](https://docs.cloud.google.com/kubernetes-engine/docs/learn/scalable-apps); [Cymbal Retail case study (PDF)](https://services.google.com/fh/files/misc/cymbal_retail_case_study_english.pdf), seen in search results only; [bank-of-anthos](https://github.com/GoogleCloudPlatform/bank-of-anthos); [site policies](https://developers.google.com/site-policies); [trademark list](https://about.google/brand-resource-center/trademark-list/).
- Acme: [Straight Dope](https://www.straightdope.com/columns/read/2224/whats-up-with-the-acme-company/); [99% Invisible](https://99percentinvisible.org/article/acme-morley-real-stories-behind-famous-fictional-film-tv-brands/).
- Name checks: [Companies House search](https://find-and-update.company-information.service.gov.uk/search/companies); web searches for each exact name; `whois` (Verisign, Nominet).
- [RFC 2606](https://www.rfc-editor.org/rfc/rfc2606) (reserved domain names).
- Logos: [Logoipsum licence](https://logoipsum.com/license) and [FAQ](https://logoipsum.com/faq); LICENSE files on the default branch of [Lucide](https://github.com/lucide-icons/lucide/blob/main/LICENSE), [Tabler](https://github.com/tabler/tabler-icons/blob/main/LICENSE), [Phosphor](https://github.com/phosphor-icons/core/blob/main/LICENSE), [Heroicons](https://github.com/tailwindlabs/heroicons/blob/master/LICENSE), [Material Design Icons](https://github.com/google/material-design-icons/blob/master/LICENSE), [Remix Icon](https://github.com/Remix-Design/RemixIcon/blob/master/License) and [Iconoir](https://github.com/iconoir-icons/iconoir/blob/main/LICENSE); `remixicon` 4.8.0, 4.9.0 and 4.9.1 `License` files from jsDelivr; [Material Symbols guide](https://developers.google.com/fonts/docs/material_symbols); npm registry for icon package versions.
- Fonts: [OFL FAQ](https://openfontlicense.org/ofl-faq/); `OFL.txt` files in [google/fonts](https://github.com/google/fonts/tree/main/ofl); npm registry `latest` for every `@fontsource(-variable)` package named; font files from jsDelivr, inspected with fontTools 4.25.0.
- [GOV.UK Design System: typeface](https://design-system.service.gov.uk/styles/typeface/).
- Tooling: `@google/design.md@0.4.0` (npm); house [DESIGN.md](../../skills/adk-frontend-integration/assets/design/DESIGN.md) at commit `dff9ce0`.

## What this research could not verify

- **Nothing here is legal advice.** The trademark, licence and naming findings come from reading public pages. They have not been reviewed by a lawyer. Before a demo brand is shown outside the firm in a way that matters, such as a public conference or marketing material, ask legal to confirm.
- **No trademark registers were searched.** The USPTO, EUIPO, UKIPO and WIPO search tools render client-side and were not used. "No collision" means only no exact hits in a web search and Companies House. Registrations in other countries, unregistered marks, and names that sound alike were not checked.
- **Microsoft's and Google's positions are inferred.** No current written policy on third-party use of Contoso or Cymbal was found. Only `contoso.com` showed Microsoft as registrant; the others are inferred from the shared registrar. Whether Microsoft or Google hold registered marks for these names was not checked. The Salesforce company names were seen only in unofficial pages.
- **The Google Fonts FAQ wording on logos** was seen in a search summary, not on the page, because the page renders client-side.
- **The logos have not been drawn.** The marks and wordmarks are concepts. No SVG was produced, outlined or reviewed at header size, and nobody has checked whether the Lucide shapes alone resemble a real company's logo.
- **The colours were computed, not seen.**
  - Ratios come from the sRGB conversion. They were not measured with axe in a rendered app.
  - Hover and active states were checked only for text contrast.
  - Colour-blind simulation was not run. In particular, Marrowby's moss and the `success` green may merge for some readers, and Kelderwick's claret and `destructive` may too.
  - Whether heather reads as "purple" is a judgement for the maintainer.
- **The fonts were not rendered.** `tnum` was checked in the latin `wght` file as shipped. Other subsets and the extra-axis files were not checked, except Fraunces' full file. Fitness at 13–17 px, and Geologica and Instrument Sans at the house's 500 weight, were not tested in a browser. Whether the fontsource packages are at least two weeks old was not checked.
- **The proposed `apply_brand.py` and the folder layout are unbuilt.** The lint run used a throwaway script in the scratch directory, not repository code.
