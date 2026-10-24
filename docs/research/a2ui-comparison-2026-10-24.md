# A2UI compared with this toolkit — 24 October 2026

## Scope and snapshot

A review of [a2ui-project/a2ui](https://github.com/a2ui-project/a2ui)
(formerly `google/A2UI`, which now redirects) at commit `b817d02`
(2026-10-23) and release tag `python/a2ui-adk/v0.1.0` (commit `c68db10`),
Apache-2.0 with no NOTICE, cloned on 24 October 2026 into its own directory
and read, never run. Also read: the `@a2ui/web_core` 0.14.0 npm package, the
ag-ui `integrations/adk-middleware` README, the adk-recipes
`staged-ui-widgets` pins, the `adk web` bundle shipped in google-adk 2.12.0,
and PyPI metadata for `a2ui-adk`, `a2ui-a2a` and `a2ui-agent-sdk`.

**Maintenance.** Active: four package releases on 2026-10-17, commits daily.
The project moved from the `google` organisation to `a2ui-project` and still
calls itself an early-stage public preview; v0.9.1 is the stable protocol,
v1.0 a candidate, v0.8 legacy. Main carries unreleased breaking changes, so
the skills cite released versions only.

**Conclusion.** The memo's "catalog-validated generative UI" holds only on one
of three ADK routes and only when the client enforces it: agent-side
validation exists in `a2ui-adk`'s toolset and checks each payload in
isolation, the AG-UI route skips it, and the web client tolerates unknown
components unless it is given a validation config. The frontend skill now
asks the ticket to declare the route and where the check runs, says `adk web`
2.12.0 shows none of these widgets, and records the `a2a-sdk<0.4` conflict
that `a2ui-adk[a2a]` brings. The conformance YAML is SDK test data with no
published runner, so it is not a project check.

## Method

Facts were read from the released package source at the tag and the npm
package rather than the README where they differ, and re-read before editing
(the toolset's `validate_payload` call, the validator's stateless note, the
web client's default, the `A2uiSubagentMap` error and state key, PyPI
`requires_dist`, and the absence of `render_ui_widgets` in the `adk web`
bundle). One scenario case covers the journey; the fresh-agent trial is in
the [testing record](../testing/a2ui-alignment-2026-10-24.md).

## Drift corrected

- The memo's link and the frontend provenance pointed at `google/A2UI`; the
  repository is `a2ui-project/a2ui`.
- The staged-widgets text cited the recipe's `a2ui-agent-sdk>=0.2.1,<0.3.0`
  pin without saying the SDK is at 0.9.0, `a2ui.adk` moved into `a2ui-adk`,
  and the AG-UI middleware no longer supports 0.2.x.
- The frontend provenance said the A2UI protocol and SDK "were not reviewed
  here"; they now are.
- The AG-UI note left the middleware's A2UI helper for this source; it is
  covered as the third route.

## Imported, by specialist

- **adk-frontend-integration.** "Choose the A2UI route and say where
  validation runs" under widgets: the three routes, `adk web` not rendering
  `render_ui_widgets`, the stateless agent-side check and
  `surface_catalog_ids`, the client's `validationConfig` and
  `STRICT_VALIDATION`, `VALIDATION_FAILED` back to the agent, inline catalogues
  as allowlist widening, orchestrator-set display names, and the pin change
  from the recipe's 0.2.x SDK. Package pins and the `a2a-sdk<0.4` conflict in
  compatibility. A routing-table pointer in `SKILL.md`.
- **adk-agent-interoperability.** `A2uiSubagentMap` for several sub-agents
  drawing surfaces in one client, in topology.

## Routed, not copied

None. The repository's own skills are contributor tooling; the companion
skills named in its AG-UI guide were not read.

## Vendored assets

None.

## Left out, with reasons

- The quickstart's API-key flow, the guide's fixed demo user and its pinned
  model with a non-default thinking budget: weaker than this repository's
  identity, session-ownership and model rules.
- The hosted Composer and Theater tools: they take pasted content into a
  third-party service.
- Unreleased APIs on main (stateless `Parser`, `RendererState`, the Express
  default format).
- The guide's same-origin sandbox for MCP Apps inside A2UI, which the MCP
  Apps specification forbids; the ext-apps review covers the sandbox.
- The conformance YAML as an application gate: it is SDK-internal data.

## Limits

Nothing was installed or executed. `a2ui-adk` 0.1.0 was not exercised with
google-adk 2.12.0; `@a2ui/react` and the AG-UI toolkit's client-side
strictness were not read; newer `adk web` builds were not checked.
