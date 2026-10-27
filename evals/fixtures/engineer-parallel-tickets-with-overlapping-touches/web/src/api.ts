export type ChatReply = { session_id: string; reply: string };

export async function sendMessage(message: string, sessionId?: string): Promise<ChatReply> {
  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    body: JSON.stringify({ message, session_id: sessionId ?? null }),
  });
  if (!res.ok) throw new Error(`chat failed: ${res.status}`);
  return (await res.json()) as ChatReply;
}
