// Calls the FastAPI service with the signed-in user's Identity Platform ID token.
// The browser never sends a user ID; the server takes it from the verified token.
import { getIdToken } from "./auth";

export interface ChatReply {
  session_id: string;
  reply: string;
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
