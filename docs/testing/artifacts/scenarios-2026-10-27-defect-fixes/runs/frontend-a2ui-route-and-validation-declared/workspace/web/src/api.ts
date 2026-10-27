// Calls the FastAPI service on the same origin. IAP adds the signed-in user's
// assertion; the browser never sends a user ID.

export interface ChatReply {
  session_id: string;
  reply: string;
  a2ui?: unknown[];
}

export async function sendMessage(message: string, sessionId: string | null): Promise<ChatReply> {
  const resp = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    body: JSON.stringify({ message, session_id: sessionId }),
  });
  if (!resp.ok) {
    throw new Error(`chat request failed: ${resp.status}`);
  }
  return (await resp.json()) as ChatReply;
}
