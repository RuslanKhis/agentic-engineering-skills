# Demo polish: research, redesign and checks, 23 October 2026

*What changed to make the house design demo-ready, and what was checked.*

## Research behind it

Five dated notes in `docs/research/`: premium AI product UI, demo brands,
frontend craft, demo-ready proofs of concept, and what enterprise users and
buyers expect from AI interfaces. Where user research contradicted vendor
practice, the user research won: claim-level citations that quote the
supporting passage instead of a block of references, real tool steps
instead of shown reasoning, the exact email inside the approval card, and an
activity view for any agent that acts.

## Visual checks

Rendered with Playwright 1.64.1 in Chrome 155 against a scratch preview
(Vite 8.3.5, React 19.3.1, shadcn 4.22.1 on Base UI, Tailwind 4.3.3), axe
4.14.0 with the WCAG 2.0–2.2 A and AA tags and `target-size` enabled.

| Set | Result |
| --- | --- |
| House design-system, empty-state and conversation screens at 375, 768 and 1280 px, light and dark (18 images) | No horizontal overflow; 0 axe violations of any impact |
| Four demo brands: conversation at 1280 light and empty state at 1280 dark (8 images) | No overflow; 0 axe violations; two contrast items axe could not measure on each conversation screen |
| The same conversation markup with stock shadcn tokens and Geist | 4 serious contrast violations; no focus outline |

`DESIGN.md` lints with `@google/design.md@0.4.0`: 0 errors, 0 warnings (82
colours, 94 components); 224 contrast pairs recomputed. Every demo brand
passes its 43 pairs and lints clean when merged.

The images were judged by the session that made them, not by a designer or a
client. Not exercised: hover cards, menus, mobile sheets, panel resizing, the
composer's keyboard behaviour and screen readers; brands only at 1280.

## Independent review

A reviewer who did not write the changes found 18 issues. The most serious
were in `apply_brand.py`: wrong theme block in its CSS output, `--out`
overwriting any file, a lint failure exiting 2 after writing, and tests that
checked the maths only against itself. All four were fixed, with
known-answer tests. Consistency fixes covered the approval card's focus rule,
the "Fictional company" label (no "demo" on screen), when Stop appears, the
client-font path, and facts restated across files. Kept as they are: a few
visual rules appear both in `DESIGN.md`, which is copied into projects and must
stand alone, and in the skill's references; the reserved phone and IP ranges
in the brands README were written from memory and not re-read against Ofcom
and the RFCs.

## Repository checks

`scripts/check_repo.py`: 23 packages valid, 753 unittest tests passed with
59 optional SDK checks skipped (729 before this branch). `git diff --check`
clean. No implementation trial has exercised `demo-readiness.md` yet; it is
guidance written from the research, to be tried on the first client demo.
