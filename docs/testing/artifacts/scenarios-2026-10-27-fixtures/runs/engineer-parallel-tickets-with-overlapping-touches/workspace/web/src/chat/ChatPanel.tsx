import { useState } from "react";
import { Message, type ChatMessage } from "./Message";
import { streamMessage } from "./stream";

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
    setMessages((m) => [...m, { role: "assistant", text: "", state: "streaming" }]);
    const patchReply = (patch: (reply: ChatMessage) => ChatMessage) =>
      setMessages((m) => [...m.slice(0, -1), patch(m[m.length - 1])]);
    try {
      const end = await streamMessage(text, sessionId, {
        onSession: setSessionId,
        onText: (chunk) => patchReply((r) => ({ ...r, text: r.text + chunk })),
      });
      patchReply((r) => ({ ...r, state: end }));
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
