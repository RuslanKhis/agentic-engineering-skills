import { useEffect, useRef, useState, type FormEvent } from "react";
import { useParams } from "react-router";
import { applyEvent, citations, endWithoutTerminal, startReply, type AssistantMessage } from "./lib/chat";
import { parseInline } from "./lib/safe";
import { readEvents } from "./lib/stream";

interface Turn {
  question: string;
  reply: AssistantMessage;
}

function Answer({ text }: { text: string }) {
  // React renders these as text nodes and attributes; no HTML is ever interpreted.
  return (
    <p className="answer">
      {parseInline(text).map((part, i) =>
        part.kind === "link" ? (
          <a key={i} href={part.href} rel="noopener noreferrer" target="_blank">
            {part.label}
          </a>
        ) : part.kind === "image" ? (
          <img key={i} src={part.src} alt={part.alt} referrerPolicy="no-referrer" />
        ) : (
          <span key={i}>{part.text}</span>
        ),
      )}
    </p>
  );
}

function Reply({ reply }: { reply: AssistantMessage }) {
  const sources = reply.state === "completed" ? citations(reply.text) : [];
  return (
    <div data-state={reply.state}>
      <Answer text={reply.text} />
      {reply.state === "streaming" && <p role="status">Working…</p>}
      {reply.state === "failed" && (
        <p role="status">
          <strong>Failed</strong> {reply.failure}
        </p>
      )}
      {sources.length > 0 && (
        <ul aria-label="Sources">
          {sources.map((source) => (
            <li key={source}>{source}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

export function Chat() {
  const { conversationId } = useParams();
  const [turns, setTurns] = useState<Turn[]>([]);
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);
  const abort = useRef<AbortController | null>(null);

  useEffect(() => () => abort.current?.abort(), []);

  function update(index: number, change: (reply: AssistantMessage) => AssistantMessage) {
    setTurns((all) => all.map((t, i) => (i === index ? { ...t, reply: change(t.reply) } : t)));
  }

  async function send(event: FormEvent) {
    event.preventDefault();
    const question = draft.trim();
    if (!question || busy) return;
    const index = turns.length;
    setDraft("");
    setBusy(true);
    setTurns((all) => [...all, { question, reply: startReply() }]);
    const controller = new AbortController();
    abort.current = controller;
    try {
      // No user ID: the server derives identity from the IAP principal.
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: conversationId ?? "new", message: question }),
        signal: controller.signal,
      });
      if (!response.ok || !response.body) throw new Error(String(response.status));
      for await (const streamEvent of readEvents(response.body)) {
        update(index, (reply) => applyEvent(reply, streamEvent));
      }
      update(index, endWithoutTerminal);
    } catch {
      if (!controller.signal.aborted) update(index, endWithoutTerminal);
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="chat">
      <h1>Doc assistant</h1>
      {turns.length === 0 && <p>Ask a question about our policies.</p>}
      {turns.map((turn, i) => (
        <section key={i}>
          <p className="question">{turn.question}</p>
          <Reply reply={turn.reply} />
        </section>
      ))}
      <form onSubmit={send}>
        <label htmlFor="question">Your question</label>
        <textarea id="question" value={draft} onChange={(e) => setDraft(e.target.value)} />
        <button type="submit" disabled={busy}>
          Send
        </button>
      </form>
    </main>
  );
}
