# A2UI alignment — 24 October 2026

Source note: [A2UI comparison](../research/a2ui-comparison-2026-10-24.md).

## Changed journey

`adk-frontend-integration`, the widgets path: a ticket now declares the A2UI
route and where the catalogue check runs before staged emission, and the
dependency decision hands the A2A pin to `adk-agent-interoperability`.

## Fresh-agent trial

A fresh agent with only the skill package planned an ADK 2.12.0 shopping
agent rendering a three-component custom catalogue in a React app, with a
designer's rule that invented components never reach the screen, an
`adk web` demo request for Friday and a later A2A exposure on a2a-sdk 1.x.

Result: it chose the staged-converter route, rejected the toolset route
(model-written JSON, stateless check, `a2a-sdk<0.4` through the `[a2a]`
extra) and the AG-UI route (no strict agent-side check), built a stateful
agent-side registry and specified `STRICT_VALIDATION` on the client, kept
both pins and declined the `a2ui-adk[a2a]` extra, and said the demo surface
is the app. 22 offline tests passed on Python 3.12, including a model-free
`InMemoryRunner` test on google-adk 2.12.0 that confirmed both ADK facts the
staged route rests on (a render-only callback with no state change emits no
event; the staged callback emits the widget once). A TypeScript test was
sketched and not run.

Ease: 3 of 5. The route split, both validation gaps and the dependency
conflict were what the task needed; the demo and wire-format facts had to be
dug out of the bundle.

## Frictions and fixes (same day)

1. The skill did not say the `adk web` renderer speaks A2UI v0.8 with the
   standard catalogue only, so no route shows custom widgets there. Fixed,
   after checking the 2.12.0 bundle (`beginRendering` and `surfaceUpdate`
   present, `createSurface` absent, "Unknown component type").
2. Whether the toolset route's output shows in `adk web`. Fixed in the same
   sentence: it is a function response and does not.
3. No schema location for converter tests. Fixed: `specification/v0_9/json/`
   and the catalogues directory.
4. What a staged widget becomes over A2A. Fixed: ADK metadata under
   `adk_actions` only (`from_adk_event.py`, 2.12.0), so a non-ADK partner
   renders nothing.
5. Whether `a2ui-agent-sdk` 0.9.0 alone constrains A2A. Fixed: its
   dependencies from PyPI, none on A2A.
6. and 7. The client constructor and the React renderer. Partly fixed: the
   options object carries `validationConfig` beside the catalogues, and the
   renderer is `@a2ui/react`; its component registration was not reviewed and
   the reference says so.
8. No recipe for confirming the ADK facts on the pinned version. Fixed: the
   model-free `InMemoryRunner` test is named.
9. Demo-readiness weight for an internal widgets demo and the helper's Python
   floor. Not changed: demo readiness belongs to its own guide, and the
   Python floor applies to the helpers as stated.
10. No template for the route declaration. Fixed: a one-line example.

## Limits

Nothing from A2UI was installed; the TypeScript client was read, not run;
`@a2ui/react` was not reviewed.
