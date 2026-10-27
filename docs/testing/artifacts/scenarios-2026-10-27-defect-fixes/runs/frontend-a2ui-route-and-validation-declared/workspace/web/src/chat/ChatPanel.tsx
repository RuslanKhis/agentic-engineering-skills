import { useState } from "react";
import { sendMessage } from "../api";
import { applyA2uiMessages } from "../a2ui/surface";
import { Message, type ChatMessage } from "./Message";

export function ChatPanel() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    const text = draft.trim();
    if (!text || busy) return;
    setDraft("");
    setBusy(true);
    setMessages((m) => [...m, { role: "user", text, state: "completed" }]);
    try {
      const reply = await sendMessage(text, sessionId);
      setSessionId(reply.session_id);
      let notice = "";
      if (reply.a2ui?.length) {
        try {
          applyA2uiMessages(reply.a2ui);
        } catch (err) {
          console.error("A2UI widget rejected", err);
          notice = "\n(The product display could not be shown.)";
        }
      }
      setMessages((m) => [...m, { role: "assistant", text: reply.reply + notice, state: "completed" }]);
    } catch {
      setMessages((m) => [
        ...m,
        { role: "assistant", text: "Sorry, something went wrong. Please try again.", state: "failed" },
      ]);
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="chat-panel" aria-label="Support chat">
      <ol className="chat-log">
        {messages.map((m, i) => (
          <Message key={i} message={m} />
        ))}
      </ol>
      <form className="chat-input" onSubmit={submit}>
        <input
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          placeholder="Ask about an order, delivery or refund"
          aria-label="Message"
        />
        <button type="submit" disabled={busy}>
          Send
        </button>
      </form>
    </section>
  );
}
