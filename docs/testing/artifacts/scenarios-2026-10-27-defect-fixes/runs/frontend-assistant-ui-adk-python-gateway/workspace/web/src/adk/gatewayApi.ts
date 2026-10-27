// Browser side of the /api/adk gateway. IAP supplies the caller's identity; nothing here sends a
// user ID. Events are validated at run time before they reach the assistant-ui accumulator.

export interface PublicPart {
  text?: string;
  functionCall?: { id: string; name: string; args: Record<string, unknown> };
  functionResponse?: { id: string; name: string; response: Record<string, unknown> };
}

export interface PublicEvent {
  id?: string;
  invocationId?: string;
  author?: string;
  partial?: boolean;
  longRunningToolIds?: string[];
  content?: { role?: string; parts: PublicPart[] };
  errorCode?: string;
  errorMessage?: string;
}

export const SAFE_ERROR = "Something went wrong. Please try again.";

function isRecord(v: unknown): v is Record<string, unknown> {
  return typeof v === "object" && v !== null && !Array.isArray(v);
}

export function parseEvent(raw: unknown): PublicEvent {
  if (!isRecord(raw)) throw new Error("malformed event");
  if (typeof raw.errorCode === "string") {
    return { errorCode: raw.errorCode, errorMessage: SAFE_ERROR, invocationId: String(raw.invocationId ?? "") };
  }
  const content = raw.content;
  if (!isRecord(content) || !Array.isArray(content.parts)) throw new Error("malformed event");
  for (const p of content.parts) {
    if (!isRecord(p)) throw new Error("malformed part");
    const call = p.functionCall;
    if (call !== undefined && !(isRecord(call) && typeof call.id === "string" && typeof call.name === "string")) {
      throw new Error("malformed function call");
    }
    if (p.text !== undefined && typeof p.text !== "string") throw new Error("malformed text");
  }
  return raw as PublicEvent;
}

export async function createSession(): Promise<string> {
  const resp = await fetch("/api/adk/sessions", { method: "POST", credentials: "same-origin" });
  if (!resp.ok) throw new Error(`create session failed: ${resp.status}`);
  const body: unknown = await resp.json();
  if (!isRecord(body) || typeof body.sessionId !== "string") throw new Error("malformed session");
  return body.sessionId;
}

/** POST a turn and yield validated public events. `fetch` with a stream, never EventSource. */
export async function* runTurn(
  body: Record<string, unknown>,
  signal?: AbortSignal,
): AsyncGenerator<PublicEvent> {
  const resp = await fetch("/api/adk/run", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    body: JSON.stringify(body),
    signal,
  });
  if (!resp.ok || !resp.body) throw new Error(`run failed: ${resp.status}`);
  const reader = resp.body.pipeThrough(new TextDecoderStream()).getReader();
  let buffer = "";
  try {
    for (;;) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += value;
      let end: number;
      while ((end = buffer.indexOf("\n\n")) >= 0) {
        const frame = buffer.slice(0, end);
        buffer = buffer.slice(end + 2);
        if (frame.startsWith("data: ")) yield parseEvent(JSON.parse(frame.slice(6)));
      }
    }
  } finally {
    await reader.cancel().catch(() => undefined);
  }
}

/**
 * Checkpoint for an edit or regenerate: the state after the last assistant message among the
 * messages that stay (`parents`), or "start" when none stays. `null` hides the buttons.
 * Messages are assumed to carry the ADK invocation id as `<invocationId>` or `<invocationId>:<n>`
 * (the package derives ids from it); confirm that against the installed 0.0.40 source.
 */
export function checkpointAfter(parents: { id: string; role: string }[]): string | null {
  if (parents.length === 0) return "start";
  const last = [...parents].reverse().find((m) => m.role === "assistant");
  const invocationId = last?.id.split(":")[0];
  return invocationId ? `after:${invocationId}` : null;
}
