# assistant-ui compared with this toolkit — 26 October 2026

## Scope and snapshot

A review of [assistant-ui/assistant-ui](https://github.com/assistant-ui/assistant-ui)
at commit `86040b7` (2026-10-25), cloned on 26 October 2026 and read; the
published `@assistant-ui/react-google-adk` 0.0.40 was downloaded with
`npm pack --ignore-scripts` and read, never run. Its AG-UI adapter's
approval contract was checked against ag-ui-protocol/ag-ui commit `85a427d`
(main, 2026-10-21).

**Licence.** MIT for every published package; no NOTICE file. Assistant
Cloud is a proprietary, paid hosted service, and self-hosting it is an
Enterprise offering.

**Maintenance.** Active (`react-google-adk` 0.0.40 on 2026-10-19,
`react-ag-ui` 0.1.0 on 2026-10-22).

**Conclusion.** assistant-ui can front a Python ADK agent, but only through
a FastAPI route the team writes: its server helper runs an ADK JS runner.
Its documentation agrees with the frontend skill on session ownership, but
its defaults do not (a browser-generated thread id, a hard-coded user, a
route that creates any session it is handed), and its stock stream forwards
raw ADK events (thought parts, every state key, raw exception text). Choosing
it over CopilotKit therefore adds gateway work the skill now names: filter
the stream and history, validate inbound parts and batched approvals,
rewind for edit and regenerate, use `{approved: bool}` on AG-UI, and keep
Assistant Cloud off for client data.

## Method

The event stream conversion, request parsing, the server helper's runner
type, the cloud option and dependency range, `Runner.rewind_async` in
google-adk 2.12.0 and the AG-UI middleware's resume handling were confirmed
in source before editing. One scenario case covers the journey; the
fresh-agent trial is in the
[testing record](../testing/assistant-ui-alignment-2026-10-26.md).

## Drift corrected

- None in the skills. The FastAPI and React research note's "edit and
  regenerate hidden without `getCheckpointId`" omits the rewind; that note
  belongs to separate work and is not edited here, but the frontend skill
  now requires `rewind_async` before an edited message runs.

## Imported, by specialist

- **adk-frontend-integration.** In `json-api.md`: the Python route shape and
  server-allocated ids. In `production.md`: filtering raw ADK events in
  stream and history, inbound part and batched-approval validation, and
  hosted persistence as a data boundary. In `frontend-quality.md`: edit and
  regenerate need `rewind_async`. In `ag-ui.md`: assistant-ui on the
  interrupt contract and the non-decision payload that approves.

After the trial: ADK 2.12 rejects a message holding both function
responses and text, so a batched approval is split into ordered runs;
`rewind_async` checks no ownership, only appends a marker and undoes no
side effect; how assistant-ui's edit, regenerate and checkpoint ids behave;
which proxy fields to ignore, refuse or define; which event fields the
filter must keep; its thread-list adapter's browser-chosen user id; a
routing row; and a compatibility row.

## Routed, not copied

None.

## Vendored assets

None.

## Left out, with reasons

- Direct mode beyond local demos; Assistant Cloud for client data; any
  component code.

## Limits

No browser or model ran; whether ADK 2.12 accepts an approval and new text
in one message was not exercised.
