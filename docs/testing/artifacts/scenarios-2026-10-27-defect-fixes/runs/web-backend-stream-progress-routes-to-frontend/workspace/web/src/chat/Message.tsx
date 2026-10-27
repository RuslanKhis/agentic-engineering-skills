export type MessageState = "streaming" | "completed" | "failed";

export interface ToolStep {
  id: string;
  title: string;
  status: "running" | "done" | "failed";
}

export interface ChatMessage {
  role: "user" | "assistant";
  text: string;
  state: MessageState;
  steps?: ToolStep[];
}

const STEP_LABEL: Record<ToolStep["status"], (title: string) => string> = {
  running: (t) => `Running ${t}…`,
  done: (t) => `Ran ${t}`,
  failed: (t) => `Failed to run ${t}`,
};

export function Message({ message }: { message: ChatMessage }) {
  return (
    <li className={`message message--${message.role} message--${message.state}`}>
      {message.steps && message.steps.length > 0 && (
        <ul className="trace" aria-label="Steps">
          {message.steps.map((s) => (
            <li key={s.id} className={`trace__step trace__step--${s.status}`}>
              {STEP_LABEL[s.status](s.title)}
            </li>
          ))}
        </ul>
      )}
      {message.state === "streaming" && !message.text && !message.steps?.length && (
        <p className="status">Working…</p>
      )}
      {message.text && <p>{message.text}</p>}
      {message.state === "failed" && (
        <span className="badge badge--error">
          {message.text ? "Failed — the answer above is incomplete" : "Failed"}
        </span>
      )}
    </li>
  );
}
