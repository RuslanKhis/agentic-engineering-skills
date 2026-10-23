# Agent UI states

Read when the conversation UI shows tool steps, approvals, reasoning,
citations or a failed turn. This maps ADK and AG-UI events to what the user
sees. It is an inference from shadcn's chat rules and Trace pattern (shadcn
commit `3d98900`, read 23 October 2026), not a prototyped recipe; the house
[DESIGN.md](../assets/design/DESIGN.md) gives the look. Map SDK states
yourself and never pass a raw event through: the application-owned event
schema in [json-api.md](json-api.md) and [ag-ui.md](ag-ui.md) is the input.

| Event | ADK source | AG-UI source | UI state |
| --- | --- | --- | --- |
| Tool call starts | `Event` with a `function_call` part | `TOOL_CALL_START` (and args) | One running trace line, status in words: "Running <tool title>…" |
| Tool result, validated | `function_response` part that passes the result schema | `TOOL_CALL_RESULT` | The same line becomes "Ran <tool title>", collapsible to show the validated result |
| Tool error or malformed result | `function_response` with an error status, or one that fails validation | `TOOL_CALL_RESULT` with an error payload | "Failed to run <tool title>", with a plain reason; never only a red colour |
| A tool still running when the stream ends | no matching `function_response` | no `TOOL_CALL_RESULT` | "Failed to run…" (the run ended without it) |
| Pending confirmation | `adk_request_confirmation` long-running call | the interrupt outcome or confirmation tool call (see [ag-ui.md](ag-ui.md)) | An approval prompt outside the trace: what the action does, what it affects, whether it can be undone, then Deny and Approve. Once answered it returns to the trace as "Running…" or "Denied…" |
| Text deltas | partial text parts | `TEXT_MESSAGE_CONTENT` | Buffered and rendered as prose with a subtle streaming indicator |
| Run error after visible text | an error event after text events | `RUN_ERROR` after content | Keep the text, mark the turn failed and offer retry; never replace the partial answer |
| Thought parts | parts with `thought=True` | reasoning events | Nothing, or an application-approved summary collapsed by default |
| Citations | grounding metadata or a validated sources result | a validated tool result or state | Numbered footnotes in the answer and a source panel; links follow SB10 |
| Run finished | final response after all events consumed | `RUN_FINISHED` | Indicator removed; the composer is enabled again |

Rules that follow from the mapping:

- One trace per assistant turn, one line per step. Rows start collapsed and
  become collapsible only once they have output.
- An approval is its own prompt, never a trace line, and is
  keyboard-operable. The backend gate (`adk-operational-guardrails`) owns the
  effect; the UI only asks.
- A failed turn is a state of that turn, not a toast that disappears.
- Edit or regenerate appears only when the server can resume from a
  checkpoint; otherwise hide it.
- Label AI-generated content plainly, as the house DESIGN.md describes.
