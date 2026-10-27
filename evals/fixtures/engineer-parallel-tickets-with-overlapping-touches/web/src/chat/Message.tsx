export type ChatMessage = {
  role: "user" | "assistant";
  text: string;
  state: "completed";
};

export function Message({ message }: { message: ChatMessage }) {
  return (
    <article data-role={message.role}>
      <p>{message.text}</p>
    </article>
  );
}
