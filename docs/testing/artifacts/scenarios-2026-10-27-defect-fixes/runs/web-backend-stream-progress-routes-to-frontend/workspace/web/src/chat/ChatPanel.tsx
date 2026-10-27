import { useState } from "react";
import { streamMessage, type StreamFrame } from "../api";
import { Message, type ChatMessage } from "./Message";

// Applies one frame to the in-progress assistant message (always the last one).
function applyFrame(m: ChatMessage, frame: StreamFrame): ChatMessage {
  const steps = m.steps ?? [];
  switch (frame.type) {
    case "tool_start":
      return { ...m, steps: [...steps, { id: frame.id, title: frame.title, status: "running" }] };
    case "tool_end":
      return {
        ...m,
        steps: steps.map((s) => (s.id === frame.id ? { ...s, status: frame.ok ? "done" : "failed" } : s)),
      };
    case "text":
      return { ...m, text: m.text ? `${m.text}\n\n${frame.text}` : frame.text };
    case "done":
      return { ...m, state: "completed" };
    case "error":
      return failTurn(m);
    default:
      return m;
  }
}

// A failed turn keeps its text; steps still running can no longer finish.
function failTurn(m: ChatMessage): ChatMessage {
  const steps = m.steps?.map((s) => (s.status === "running" ? { ...s, status: "failed" as const } : s));
  return { ...m, steps, state: "failed" };
}

export function ChatPanel() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);

  function updateLast(fn: (m: ChatMessage) => ChatMessage) {
    setMessages((all) => [...all.slice(0, -1), fn(all[all.length - 1])]);
  }

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    const text = draft.trim();
    if (!text || busy) return;
    setDraft("");
    setBusy(true);
    setMessages((m) => [
      ...m,
      { role: "user", text, state: "completed" },
      { role: "assistant", text: "", state: "streaming", steps: [] },
    ]);
    let finished = false;
    try {
      await streamMessage(text, sessionId, (frame) => {
        if (frame.type === "session") setSessionId(frame.session_id);
        if (frame.type === "done" || frame.type === "error") finished = true;
        updateLast((m) => applyFrame(m, frame));
      });
    } catch {
      // Network failure or HTTP error: keep anything already shown.
    } finally {
      // A stream that ended without done/error was cut off.
      if (!finished) updateLast(failTurn);
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
      <div role="status" className="visually-hidden">
        {!busy && messages.length > 0 && messages[messages.length - 1].state === "failed" && "The reply failed."}
      </div>
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
