# Doc assistant design system

Base: the house theme of the Agentic Engineering frontend skill (warm paper greys, Inter,
Source Serif 4 for answers, JetBrains Mono), unchanged except for the client overrides
below. Agreed with Nordlicht Insurance's brand team on 2026-10-16.

## Client overrides

| Token | Value | Why |
| --- | --- | --- |
| primary | `oklch(0.42 0.08 200)` (Nordlicht petrol) | brand colour; must keep 4.5:1 on background |
| primary-hover | `oklch(0.35 0.07 200)` | |
| ring | `oklch(0.52 0.09 200)` | |
| dark-primary | `oklch(0.78 0.07 200)` | |
| display font | Source Serif 4 | unchanged |
| logo | `web/public/nordlicht-mark.svg` (to be supplied by the brand team) | |

## Copy

- Sentence case for every label and button.
- Answers cite policy ID and section, e.g. "HR-04 §2.3".
- Errors say what happened and what to do, in one sentence, never raw error text.

## Layout

A single chat column, max width 720 px, sources listed under each answer; a sidebar of
recent conversations from 1024 px.
