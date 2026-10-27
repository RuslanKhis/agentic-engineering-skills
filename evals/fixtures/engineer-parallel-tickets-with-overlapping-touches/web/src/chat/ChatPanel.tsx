import { useState } from "react";
import { sendMessage } from "../api";
import { Message, type ChatMessage } from "./Message";

export function ChatPanel() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [sessionId, setSessionId] = useState<string | undefined>();
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit() {
    const text = draft.trim();
    if (!text || busy) return;
    setDraft("");
    setBusy(true);
    setMessages((m) => [...m, { role: "user", text, state: "completed" }]);
    try {
      const reply = await sendMessage(text, sessionId);
      setSessionId(reply.session_id);
      setMessages((m) => [...m, { role: "assistant", text: reply.reply, state: "completed" }]);
    } catch {
      setMessages((m) => [...m, { role: "assistant", text: "Something went wrong.", state: "completed" }]);
    } finally {
      setBusy(false);
    }
  }

  return (
    <section aria-label="Chat">
      <ol>
        {messages.map((m, i) => (
          <li key={i}>
            <Message message={m} />
          </li>
        ))}
      </ol>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          void submit();
        }}
      >
        <label htmlFor="draft">Message</label>
        <input id="draft" value={draft} onChange={(e) => setDraft(e.target.value)} />
        <button type="submit" disabled={busy}>
          Send
        </button>
      </form>
    </section>
  );
}
