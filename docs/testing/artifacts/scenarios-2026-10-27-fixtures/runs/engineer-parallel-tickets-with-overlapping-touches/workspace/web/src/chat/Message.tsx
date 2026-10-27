export type ChatMessage = {
  role: "user" | "assistant";
  text: string;
  state: "streaming" | "completed" | "failed" | "interrupted";
};

const BADGES: Partial<Record<ChatMessage["state"], string>> = {
  streaming: "Writing…",
  failed: "Failed",
  interrupted: "Stopped",
};

export function Message({ message }: { message: ChatMessage }) {
  const badge = message.role === "assistant" ? BADGES[message.state] : undefined;
  return (
    <article data-role={message.role} data-state={message.state}>
      <p>{message.text}</p>
      {badge && (
        <p role={message.state === "failed" ? "alert" : "status"} data-badge={message.state}>
          {badge}
        </p>
      )}
    </article>
  );
}
