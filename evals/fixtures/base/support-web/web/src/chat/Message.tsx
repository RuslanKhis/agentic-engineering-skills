export type MessageState = "streaming" | "completed" | "failed";

export interface ChatMessage {
  role: "user" | "assistant";
  text: string;
  state: MessageState;
}

export function Message({ message }: { message: ChatMessage }) {
  return (
    <li className={`message message--${message.role} message--${message.state}`}>
      <p>{message.text}</p>
      {message.state === "failed" && <span className="badge badge--error">Failed</span>}
    </li>
  );
}
