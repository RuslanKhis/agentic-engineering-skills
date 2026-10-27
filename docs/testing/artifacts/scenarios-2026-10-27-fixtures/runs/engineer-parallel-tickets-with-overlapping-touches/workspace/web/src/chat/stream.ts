export type StreamEnd = "completed" | "failed" | "interrupted";

export type StreamHandlers = {
  onSession: (sessionId: string) => void;
  onText: (text: string) => void;
};

// Reads POST /api/chat/stream (SSE) with fetch so the IAP session cookie goes along.
// Always resolves with how the stream ended: a network error or a stream that closes
// without a terminal event is "failed", never "completed".
export async function streamMessage(
  message: string,
  sessionId: string | undefined,
  handlers: StreamHandlers,
  signal?: AbortSignal,
): Promise<StreamEnd> {
  let end: StreamEnd = "failed";
  try {
    const res = await fetch("/api/chat/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "same-origin",
      body: JSON.stringify({ message, session_id: sessionId ?? null }),
      signal,
    });
    if (!res.ok || !res.body) return "failed";
    const id = res.headers.get("X-Session-Id");
    if (id) handlers.onSession(id);

    const reader = res.body.pipeThrough(new TextDecoderStream()).getReader();
    let buffer = "";
    for (;;) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += value;
      let sep = buffer.indexOf("\n\n");
      while (sep !== -1) {
        const frame = buffer.slice(0, sep);
        buffer = buffer.slice(sep + 2);
        const parsed = parseFrame(frame);
        if (parsed?.event === "text") handlers.onText(parsed.data.text as string);
        else if (parsed && isEnd(parsed.event)) end = parsed.event;
        sep = buffer.indexOf("\n\n");
      }
    }
  } catch {
    return signal?.aborted ? "interrupted" : "failed";
  }
  return end;
}

function isEnd(event: string): event is StreamEnd {
  return event === "completed" || event === "failed" || event === "interrupted";
}

function parseFrame(frame: string): { event: string; data: Record<string, unknown> } | null {
  let event = "";
  let data = "";
  for (const line of frame.split("\n")) {
    if (line.startsWith("event: ")) event = line.slice(7);
    else if (line.startsWith("data: ")) data += line.slice(6);
  }
  if (!event) return null;
  return { event, data: data ? (JSON.parse(data) as Record<string, unknown>) : {} };
}
