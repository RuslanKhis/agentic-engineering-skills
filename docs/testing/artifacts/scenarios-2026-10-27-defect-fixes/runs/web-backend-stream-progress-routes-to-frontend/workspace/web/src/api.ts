// Calls the FastAPI service with the signed-in user's Identity Platform ID token.
// The browser never sends a user ID; the server takes it from the verified token.
import { getIdToken } from "./auth";

export interface ChatReply {
  session_id: string;
  reply: string;
}

export type StreamFrame =
  | { type: "session"; session_id: string }
  | { type: "tool_start"; id: string; title: string }
  | { type: "tool_end"; id: string; title: string; ok: boolean }
  | { type: "text"; text: string }
  | { type: "done" }
  | { type: "error"; message: string };

function parseFrame(line: string): StreamFrame | null {
  let raw: unknown;
  try {
    raw = JSON.parse(line);
  } catch {
    return null;
  }
  const f = raw as Record<string, unknown>;
  switch (f?.type) {
    case "session": return typeof f.session_id === "string" ? (f as StreamFrame) : null;
    case "tool_start": return typeof f.id === "string" && typeof f.title === "string" ? (f as StreamFrame) : null;
    case "tool_end":
      return typeof f.id === "string" && typeof f.title === "string" && typeof f.ok === "boolean"
        ? (f as StreamFrame) : null;
    case "text": return typeof f.text === "string" ? (f as StreamFrame) : null;
    case "done": return f as StreamFrame;
    case "error": return typeof f.message === "string" ? (f as StreamFrame) : null;
    default: return null;
  }
}

/**
 * Streams one turn, calling onFrame per frame as it arrives. Resolves when the
 * stream ends; rejects if the request fails or the connection drops. The caller
 * keeps whatever it already rendered either way.
 */
export async function streamMessage(
  message: string,
  sessionId: string | null,
  onFrame: (frame: StreamFrame) => void,
  signal?: AbortSignal,
): Promise<void> {
  const token = await getIdToken();
  const resp = await fetch("/api/chat/stream", {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify({ message, session_id: sessionId }),
    signal,
  });
  if (!resp.ok || !resp.body) {
    throw new Error(`chat request failed: ${resp.status}`);
  }
  const reader = resp.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    let nl: number;
    while ((nl = buffer.indexOf("\n")) >= 0) {
      const frame = parseFrame(buffer.slice(0, nl));
      buffer = buffer.slice(nl + 1);
      if (frame) onFrame(frame);
    }
  }
}

export async function sendMessage(message: string, sessionId: string | null): Promise<ChatReply> {
  const token = await getIdToken();
  const resp = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify({ message, session_id: sessionId }),
  });
  if (!resp.ok) {
    throw new Error(`chat request failed: ${resp.status}`);
  }
  return (await resp.json()) as ChatReply;
}
