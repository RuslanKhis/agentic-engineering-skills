# Harbour Outfitters support chat: design system

## Brand

Calm, practical, outdoor. Plain words; no exclamation marks in system copy.

## Tokens

| Token | Value | Use |
| --- | --- | --- |
| color-bg | #f7f5f0 | page background |
| color-surface | #ffffff | chat panel, cards |
| color-text | #1f2a2e | body text |
| color-muted | #5b6b70 | secondary text, borders |
| color-primary | #1d5c63 | buttons, links, focus ring |
| color-error | #b3261e | error text and badges |
| radius | 10px | panels, inputs, buttons |
| space | 8px | base spacing unit |
| font | Inter, system-ui | all text |

## Components

- Message: user messages right-aligned, assistant left-aligned; a failed reply keeps its text
  and shows a "Failed" badge in color-error.
- Secondary lines inside the chat log use color-muted at 0.85em.
- Buttons: color-primary fill, white text; disabled at 50 % opacity.

## Accessibility

Contrast at least 4.5:1 for text; every state is said in words, not colour alone; the chat log
is an ordered list with an accessible name.
