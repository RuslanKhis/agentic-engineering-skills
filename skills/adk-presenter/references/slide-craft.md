# Slide craft: from the outline to slides a reader gets in three seconds

Read before rendering an outline into slides, and when writing a slide body
that will be rendered. The shape with a controlled comparison behind it is
the assertion-evidence slide: a full-sentence headline stating the claim and,
under it, one piece of visual evidence the headline is about, and almost
nothing else. The multimedia-learning findings predict the same (extraneous
material removed, cues that signal structure, no on-screen text that
duplicates the speech), and the chart-design studies add: declutter, then
point at the pattern with one colour and one annotation. Sources and dates
are in the repository's research note `docs/research/slide-craft.md`.

## The slide

- **Headline:** the action title verbatim, a complete sentence of at most
  two lines (about 20 words), 28 to 30 point. "Not measured" goes in the
  headline when the record lacks the number; no placeholder figures.
- **Body:** one visual (chart, diagram, table, screenshot, quoted test
  result), at most two call-outs, no bullets on body slides; a list that
  cannot be avoided has at most four items of two lines. About 40 words in
  total, at least 20 point; caption at least 14 point; no all-caps.
- **Caption:** source, sample, repeats, interval, dates, who measured.
  Projections say "estimate"; untested claims say "hypothesis".
- **What the audience must recall exactly** (a threshold, a cost, a date,
  the decision asked) is written on the slide as a call-out; that is the one
  thing text-heavy slides did better in the comparison.
- **Nothing decorative:** logo on the title and closing slides only; no
  stock images, transitions, 3D, shadows or plot backgrounds.
- **Notes carry the argument;** the linked document carries the detail. A
  sentence from the notes never appears on the slide.

## Charts for agent results

- Grey by default; the bar or series carrying the claim is the one coloured
  element; the takeaway is written on the chart beside it in the headline's
  words.
- Before and after against the baseline: two bars on one scale, or a line
  with the baseline drawn flat on the same chart. Never a chart of the
  result without its baseline.
- Uncertainty: the interval drawn as a light range and named ("95 percent
  interval"); with a small sample show the points, not a bar.
- Cost per unit and volume over a pilot: two stacked panels on one time
  axis, never a secondary axis.
- A funnel: left-aligned horizontal bars in stage order, the step
  conversion written between them, never a centred funnel shape.
- Refused forms: pie, donut, dual axis, 3D.
- Generated from recorded project data, never typed by hand; captioned with
  sample, method and date.

## Diagrams for technical audiences

At most three, in layers: context (users, agent, external systems),
container (agent, model, tools, session and memory stores, with the identity
on each arrow and trust boundaries as dotted regions), and a component view
only where a contract is being asked for. Every diagram has a title, a
legend, every arrow labelled with protocol and identity, every container
with its technology, consistent shapes and colours across the set. The
design document is linked, not redrawn.

## Colour and contrast

Text and marks at a contrast of at least 4.5 to 1. The emphasis colour from
a colour-blind-safe palette (Okabe and Ito: orange, sky blue, bluish green,
vermilion, blue) or the brand's accessible equivalent; never red against
green for baseline against agent; readable in greyscale; alt text on every
image where the host allows it.

## Two renderings, one outline

The projected deck shows the headline, the visual and the caption. The
leave-behind is the same slides with the notes laid out beside the visual,
so it reads without a presenter. Never one deck that tries to be both. The
one-slide version is the executive summary alone and must pass the checklist
below. The appendix holds the criteria table, evaluation excerpts, cost
workings and the answers to expected questions.

## Checklist per body slide

1. Headline is a complete sentence that could be contradicted, at most two
   lines.
2. One message; the slide supports that sentence and nothing else.
3. Evidence is visible on the slide, not described in bullets.
4. The takeaway is annotated on the chart in the headline's words; one
   emphasis colour; the rest grey.
5. Method and sample in the caption; estimate and hypothesis labelled.
6. "Not measured" in the headline where the record lacks the number.
7. Headline at most 20 words; body at most 40 words; no list beyond four
   items of two lines.
8. Headline 28 to 30 point, body at least 20, caption at least 14; no
   all-caps.
9. Contrast 4.5 to 1; colour-blind-safe; readable in greyscale; alt text.
10. One currency, one time unit, one definition of "conversation" or "case",
    stated on the axis.
11. Bars or lines on a shared baseline with the baseline drawn; no pie,
    donut, dual axis or 3D.
12. Diagram has title, legend, labelled arrows, trust boundaries, and the
    shared notation.
13. Nothing decorative.
14. A reader who sees only this slide gets the claim in three seconds.

The deck check warns when a title or a body runs over its word budget; the
rest of the checklist is applied by reading.
