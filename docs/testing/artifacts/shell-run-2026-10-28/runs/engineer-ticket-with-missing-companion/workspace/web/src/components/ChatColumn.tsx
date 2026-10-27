import { useCallback, useEffect, useRef, useState } from "react";
import { applyEvent, endStream, startMessage, type AssistantMessage } from "../lib/message";
import { readEvents } from "../lib/sse";
import { SafeText } from "./SafeText";

interface Turn {
  question: string;
  answer: AssistantMessage;
}

// The browser sends the conversation ID and the question only; identity comes from IAP on the server.
export function ChatColumn({ conversationId }: { conversationId: string }) {
  const [turns, setTurns] = useState<Turn[]>([]);
  const [draft, setDraft] = useState("");
  const abort = useRef<AbortController | null>(null);
  useEffect(() => () => abort.current?.abort(), []);

  const update = (fn: (m: AssistantMessage) => AssistantMessage) =>
    setTurns((all) => all.map((t, i) => (i === all.length - 1 ? { ...t, answer: fn(t.answer) } : t)));

  const send = useCallback(async () => {
    const question = draft.trim();
    if (!question) return;
    setDraft("");
    setTurns((all) => [...all, { question, answer: startMessage() }]);
    const controller = (abort.current = new AbortController());
    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: conversationId, message: question }),
        signal: controller.signal,
      });
      if (!response.ok || !response.body) throw new Error("request failed");
      for await (const event of readEvents(response.body)) update((m) => applyEvent(m, event));
    } catch {
      /* fall through: an unfinished message becomes failed below */
    }
    if (!controller.signal.aborted) update(endStream);
  }, [draft, conversationId]);

  return (
    <section aria-label="Conversation" style={{ maxWidth: 720, margin: "0 auto" }}>
      {turns.map((turn, i) => (
        <article key={i}>
          <p>{turn.question}</p>
          <div>
            <SafeText source={turn.answer.text} />
          </div>
          {turn.answer.status === "streaming" && <p role="status">Working…</p>}
          {turn.answer.status === "failed" && (
            <p role="status">
              <strong>Failed</strong> {turn.answer.error}
            </p>
          )}
        </article>
      ))}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          void send();
        }}
      >
        <label>
          Ask about a policy
          <textarea value={draft} onChange={(e) => setDraft(e.target.value)} />
        </label>
        <button type="submit">Send</button>
      </form>
    </section>
  );
}
