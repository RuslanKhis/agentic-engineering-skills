# CopilotKit v2 implementation recipe

Use these pieces when wiring a CopilotKit frontend or its AG-UI HTTP boundary. They target `@copilotkit/react-core` / `@copilotkit/runtime` **1.69.0**, their **`/v2` APIs**, `@ag-ui/client` 0.0.57 and Zod 3.25.76. Check the target's versions against [compatibility.md](compatibility.md); these examples do not authorise changing pins. The recorded Next.js app requires Node >=22.12. Snippets assume the usual `@/*` → `src/*` TypeScript alias; adapt paths to the existing app.

## Connect the runtime, client and renderer

Keep a public identifier in `src/lib/agent-config.ts`; it contains no credentials. Use it as the runtime registry key, chat `agentId`, renderer scope and `useAgent` selector. The Python endpoint URL and its internal ADK application name are separate settings.

```ts
export const AGENT_ID = "support_triage";
```

In `src/app/api/copilotkit/[[...slug]]/route.ts`, the optional catch-all handles the base path and the v2 runtime's subpaths. Preserve every required method when wrapping this handler with the application's authentication.

```ts
import { HttpAgent } from "@ag-ui/client";
import { CopilotRuntime, createCopilotRuntimeHandler } from "@copilotkit/runtime/v2";
import { AGENT_ID } from "@/lib/agent-config";

let handler: ReturnType<typeof createCopilotRuntimeHandler> | undefined;

async function handle(request: Request) {
  // Resolve configuration on invocation so missing credentials do not prevent an offline build.
  const backendUrl = process.env.AGENT_BACKEND_URL;
  const serviceToken = process.env.AGENT_BACKEND_TOKEN;
  if (!backendUrl || !serviceToken) {
    return Response.json({ error: "Agent service is unavailable" }, { status: 503 });
  }
  if (!handler) {
    const runtime = new CopilotRuntime({
      agents: {
        [AGENT_ID]: new HttpAgent({
          url: backendUrl,
          headers: { Authorization: `Bearer ${serviceToken}` },
        }),
      },
      forwardHeaders: { deny: ["authorization"], denyPrefixes: ["x-"] },
    });
    handler = createCopilotRuntimeHandler({ runtime, basePath: "/api/copilotkit" });
  }
  return handler(request);
}

// Transport wiring: the application's browser authentication must cover all methods.
export const dynamic = "force-dynamic";
export const GET = handle;
export const POST = handle;
export const PATCH = handle;
export const DELETE = handle;
```

This variant assumes a private backend using a shared service token and requires both settings. For an existing workload-identity mechanism, adapt credential acquisition explicitly rather than forwarding an unauthenticated request. Restart the server when its cached backend configuration changes. These environment values belong only to the server; never prefix the token with `NEXT_PUBLIC_`. A shared service token identifies the BFF, not a browser user. The companion's unauthenticated browser route is a loopback-only demonstration. Before exposing this route, apply the existing verifier to every exported method and propagate separately verified user identity. The forwarding policy above strips browser-supplied authorization and `x-*` assertions; add only the separately verified assertions required by the backend. Construct request-scoped headers/client state for that identity; never mutate the module-level agent's headers with a caller's token. Authentication alone does not authorise runtime thread/history/stop operations.

Import the v2 stylesheet once in the existing root layout. Keep the layout's metadata and other providers; the small layout below just shows the required placement.

```tsx
import type { ReactNode } from "react";
import "@copilotkit/react-core/v2/styles.css";

export default function RootLayout({ children }: { children: ReactNode }) {
  return <html lang="en"><body>{children}</body></html>;
}
```

## Validate completed tool results

The renderer's `parameters` schema describes tool arguments. It does not validate the result, and the hook's `status: "complete"` does not mean a successful business outcome. In this pinned API the completed hook result is a string; the helper also accepts already-decoded objects for other entry points.

This complete helper can live beside the renderer as `src/lib/tool-result.ts`. It is new defensive guidance: the companion's historical `parseResult` cast arbitrary objects/JSON to a TypeScript type. Its successful tool-card observations do not validate malformed-result handling.

```ts
import { z } from "zod";

const MAX_RESULT_BYTES = 4096;
const RoutingResultSchema = z.object({
  status: z.enum(["routed", "success"]),
  queue: z.enum(["billing", "technical_support", "general_support"]),
  reason: z.string().trim().min(1).max(500),
}).strict();
type RoutingResult = z.infer<typeof RoutingResultSchema>;
export type ResultView =
  | { kind: "pending" }
  | { kind: "invalid" }
  | { kind: "valid"; value: RoutingResult };

export function parseRoutingResult(result: unknown, status: string): ResultView {
  if (status === "inProgress" || status === "executing") return { kind: "pending" };
  if (status !== "complete") return { kind: "invalid" };

  let candidate: unknown = result;
  if (typeof candidate === "string") {
    // Check character count first to bound the UTF-8 allocation and JSON parsing.
    if (candidate.length > MAX_RESULT_BYTES ||
        new TextEncoder().encode(candidate).byteLength > MAX_RESULT_BYTES) {
      return { kind: "invalid" };
    }
    try { candidate = JSON.parse(candidate); }
    catch { return { kind: "invalid" }; }
  }
  if (candidate === null || typeof candidate !== "object" || Array.isArray(candidate)) {
    return { kind: "invalid" };
  }
  const prototype = Object.getPrototypeOf(candidate);
  if ((prototype !== Object.prototype && prototype !== null) ||
      Object.keys(candidate).length !== 3) return { kind: "invalid" };

  const parsed = RoutingResultSchema.safeParse(candidate);
  if (!parsed.success) return { kind: "invalid" };
  // Only the three schema-bounded scalar fields reach serialization/rendering.
  if (new TextEncoder().encode(JSON.stringify(parsed.data)).byteLength > MAX_RESULT_BYTES) {
    return { kind: "invalid" };
  }
  return { kind: "valid", value: parsed.data };
}
```

The byte limit is an example for this small result; enforce response/event byte limits before decoding large network payloads too. This parser expects decoded transport data, not arbitrary executable objects/getters. Its strict schema rejects unknown fields; the Python public projection should remove private fields before transmission. If an existing contract deliberately permits extra keys, explicitly project only the three public fields before applying this schema. Frontend projection can prevent display, but cannot undo disclosure of fields already sent to the browser. For another tool, choose its actual fields and success/error variants instead of copying the support queues.

| Input and hook status | Outcome |
| --- | --- |
| `undefined`, `executing` | Pending; keep a loading display |
| `null`, `complete` | Invalid; do not keep waiting indefinitely |
| `"{bad json"`, `complete` | Invalid |
| `"null"`, `"[]"`, or `"42"`, `complete` | Invalid |
| Object with `reason: {text: "…"}`, unknown status/queue, missing or extra fields | Invalid |
| Result beyond the byte bound or reason beyond 500 characters | Invalid |
| Valid string/object with one of the two documented statuses | Valid; render only the validated projection |

Register a backend-tool **renderer**, not a frontend function that executes the tool again. For `src/app/tool-renderers.tsx`:

```tsx
"use client";
import { useRenderTool } from "@copilotkit/react-core/v2";
import { z } from "zod";
import { AGENT_ID } from "@/lib/agent-config";
import { parseRoutingResult } from "@/lib/tool-result";

export function ToolRenderers() {
  useRenderTool({
    agentId: AGENT_ID,
    name: "route_support_ticket",
    parameters: z.object({ ticket_text: z.string().min(1).max(8000) }),
    render: ({ result, status }) => {
      const view = parseRoutingResult(result, status);
      if (view.kind === "pending") return <p role="status">Choosing a queue…</p>;
      if (view.kind === "invalid") return <p role="alert">The routing result is unavailable.</p>;
      return <section aria-live="polite">
        <h3>{view.value.queue.replaceAll("_", " ")}</h3>
        <p>{view.value.reason}</p>
      </section>;
    },
  }, []);
  return null;
}
```

Mount the renderer under the provider, alongside the chat. For the client portion of `src/app/page.tsx`:

```tsx
"use client";
import { CopilotChat, CopilotKit } from "@copilotkit/react-core/v2";
import { AGENT_ID } from "@/lib/agent-config";
import { ToolRenderers } from "./tool-renderers";
import { ActivityMonitor } from "./activity-monitor";

export default function Page() {
  return <CopilotKit runtimeUrl="/api/copilotkit">
    <ToolRenderers />
    <CopilotChat agentId={AGENT_ID} />
    <ActivityMonitor />
  </CopilotKit>;
}
```

An optional `src/app/activity-monitor.tsx` observes the same agent. Unsubscribe whenever the agent changes or the component unmounts. `TOOL_CALL_END` means its arguments have arrived; it does not prove execution success.

```tsx
"use client";
import { useEffect, useState } from "react";
import { useAgent } from "@copilotkit/react-core/v2";
import { AGENT_ID } from "@/lib/agent-config";

export function ActivityMonitor() {
  const { agent } = useAgent({ agentId: AGENT_ID });
  const [entries, setEntries] = useState<string[]>([]);
  useEffect(() => {
    const add = (message: string) => setEntries((current) => [message, ...current].slice(0, 50));
    const subscription = agent.subscribe({
      onRunStartedEvent: () => add("Agent run started"),
      onToolCallEndEvent: () => add("Tool arguments received"),
      onRunErrorEvent: () => add("Agent run failed"),
      onRunFinishedEvent: () => add("Agent run finished"),
    });
    return () => subscription.unsubscribe();
  }, [agent]);
  return <aside aria-label="Agent activity">{entries.map((entry, index) =>
    <p key={index}>{entry}</p>)}</aside>;
}
```

Fixed event labels avoid displaying arbitrary provider errors or tool names. Fifty short monitor entries bound this component only, not CopilotKit's message store or a server queue.

## Admit a fresh turn before starting work

For a bridge supporting only ordinary new text turns, run the following profile after trusted authentication and before session creation, provider invocation or returning a streaming response. Its explicit restrictions are **new guidance**, not a claim that the companion enforces them. The companion searches backwards for a user message; a trailing tool-result continuation can therefore select an earlier user turn.

```python
import re
from ag_ui.core import RunAgentInput
from fastapi import HTTPException

def admit_fresh_turn(input_data: RunAgentInput) -> str:
    def reject() -> None:
        raise HTTPException(status_code=422, detail="Unsupported agent request")

    if not all(re.fullmatch(r"[A-Za-z0-9_-]{1,128}", value)
               for value in (input_data.thread_id, input_data.run_id)):
        reject()
    if (input_data.tools or input_data.state != {} or input_data.context
            or input_data.forwarded_props not in ({}, None)
            or input_data.resume is not None or input_data.parent_run_id is not None
            or input_data.model_extra):
        reject()
    if not 1 <= len(input_data.messages) <= 200:
        reject()
    latest = input_data.messages[-1]
    if (latest.role != "user" or latest.model_extra
            or not isinstance(latest.content, str)
            or not latest.content.strip() or len(latest.content) > 8000):
        reject()
    return latest.content
```

Treat prior browser history as display data; send only this admitted text with the server-derived user and authorised conversation. Check request bytes before model parsing. This profile deliberately disables client state, context extensions, browser-defined tools, multimodal input and continuation. A product that needs any of them must define and validate that separate contract. In particular, a frontend that echoes projected server state needs an explicit permitted projection or must omit it; do not relax the check to arbitrary state merely to make a request pass.

Test each rejected form at the actual route with a counted provider/session boundary and assert **zero invocations**. Include a trailing tool message after an earlier user message, resume/parent-run payloads, shadowing browser tools and writable identity state. A renderer registration alone is not authority to accept a browser-executed tool.

## Encode the public stream at the HTTP boundary

After admission and conversation authorisation succeed, give the HTTP boundary an owned async generator of **public** AG-UI events. The generator must consume the upstream outcome before emitting `RUN_FINISHED`, enforce result correlation and suppress repeated aggregates as described in [ag-ui.md](ag-ui.md). It owns run/text/tool lifecycle construction; this wrapper owns encoding, closure and safe error delivery. Hold a proposed successful terminal until the generator has exhausted and closed: an exception during closure must not follow an already emitted success.

```python
import asyncio
from contextlib import aclosing
from typing import AsyncGenerator
from ag_ui.core import (
    BaseEvent, EventType, RunAgentInput, RunErrorEvent, RunStartedEvent, TextMessageEndEvent,
)
from ag_ui.encoder import EventEncoder
from fastapi import Request
from fastapi.responses import StreamingResponse

def public_stream_response(
    request: Request, input_data: RunAgentInput, events: AsyncGenerator[BaseEvent, None],
):
    encoder = EventEncoder(accept=request.headers.get("accept"))

    async def encoded():
        open_text: set[str] = set()
        started = False
        pending_finish = None
        try:
            async with aclosing(events):
                async for event in events:
                    if await request.is_disconnected():
                        raise asyncio.CancelledError
                    if pending_finish is not None:
                        raise RuntimeError("Event after declared completion")
                    if event.type == EventType.RUN_STARTED:
                        if (started or event.thread_id != input_data.thread_id
                                or event.run_id != input_data.run_id):
                            raise RuntimeError("Invalid run start")
                        started = True
                    elif not started:
                        raise RuntimeError("Run start missing")
                    if event.type == EventType.RUN_FINISHED:
                        if (event.thread_id != input_data.thread_id
                                or event.run_id != input_data.run_id or open_text):
                            raise RuntimeError("Invalid run completion")
                        pending_finish = event
                        continue
                    if event.type == EventType.RUN_ERROR:
                        raise RuntimeError("Reported run failure")
                    if event.type == EventType.TEXT_MESSAGE_START:
                        open_text.add(event.message_id)
                    elif event.type == EventType.TEXT_MESSAGE_END:
                        open_text.discard(event.message_id)
                    yield encoder.encode(event)
            if pending_finish is None:
                raise RuntimeError("Run completion missing")
            yield encoder.encode(pending_finish)
        except asyncio.CancelledError:
            raise
        except Exception:
            if not started:
                yield encoder.encode(RunStartedEvent(
                    type=EventType.RUN_STARTED, thread_id=input_data.thread_id,
                    run_id=input_data.run_id))
            for message_id in sorted(open_text):
                yield encoder.encode(TextMessageEndEvent(
                    type=EventType.TEXT_MESSAGE_END, message_id=message_id))
            yield encoder.encode(RunErrorEvent(
                type=EventType.RUN_ERROR, message="The agent could not complete the request"))

    return StreamingResponse(encoded(), media_type=encoder.get_content_type(), headers={
        "Cache-Control": "no-cache", "X-Accel-Buffering": "no",
    })
```

Apply the overall deadline around preparation and iterator consumption, including admission/lock waiting and owned closure; this framing snippet does not implement a deadline manager or translator. Keep its generator lazy until the route's auth/admission checks pass. Preserve cancellation while applying the installed client's supported bounded shutdown. The disconnect check above runs between yielded events; prompt cancellation while a producer is stalled requires the serving framework's disconnect handling or an explicitly tested concurrent watcher. A cancelled connection does not prove that remote effects stopped.

Auth/input rejection before streaming uses the application's HTTP 401/403/422 policy. Once headers/content have started, an execution failure travels in-band as `RUN_ERROR`; HTTP 200 alone does not mean a successful run. The encoder supplies the supported content type, aliases and framing. Python field names and the trace checker's NDJSON are not substitutes for SSE wire encoding. Anti-buffering headers are hints, not proof of deployed proxy behaviour.

For managed text streaming, the recorded ADK call passed `run_config=RunConfig(streaming_mode=StreamingMode.SSE).model_dump(mode="json", exclude_unset=True)`, producing `{"streaming_mode":"sse"}`. Choosing an SSE HTTP response alone did not request model partials.

## Check the connected pieces

Typecheck the snippets with the target's installed pinned dependencies. Test the result helper against both valid statuses plus malformed JSON, null, arrays/scalars, extra fields, wrong field types, invalid status/queue, and string/object size limits. Exercise pending and completed-invalid states separately.

An HTTP test that reads the entire `response.text` proves the final wire sequence, not progressive delivery. Add a test that receives a text frame before upstream completion; cancel while waiting for the next frame and assert iterator closure and absence of successful completion. Run an actual browser through the BFF to verify one matching tool card, incremental text, a safe failure/timeout and a subsequent successful submission. Use a model-boundary substitute that requests the real application tool and derives its final answer from the actual result.

When invoking `createCopilotRuntimeHandler` directly in a Node Fetch test, inspect the returned stream's chunk type if `response.text()` reports `Received non-Uint8Array chunk`. The pinned runtime produced string chunks in one offline direct-handler evaluation, even though its synthetic upstream returned byte chunks. This did not establish a Next.js hosting defect; the historical Next browser path worked. If the selected host requires bytes, apply a streaming string-to-UTF-8 transform while preserving byte chunks, status, headers and cancellation, then test that host. Avoid collecting the entire response merely to satisfy a test consumer.

Evidence limits: the companion's pinned wiring, encoder use, partial/aggregate suppression and successful cards have source/tests and historical offline/live-browser evidence. The strict result parser, lazy required configuration and fresh-turn admission here are additional implementation guidance. A typecheck or local helper test is not a fresh BFF/browser, identity-provider or cloud test; report those evidence classes separately.
