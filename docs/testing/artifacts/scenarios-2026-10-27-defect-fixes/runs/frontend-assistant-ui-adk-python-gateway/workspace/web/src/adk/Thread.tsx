// Conversation view built from assistant-ui primitives (unstyled; classes reuse theme.css).
// The Edit button shows only where getCheckpointId returned a checkpoint, i.e. where the server
// can rewind. Text is rendered as plain text.
import {
  ActionBarPrimitive,
  ComposerPrimitive,
  MessagePrimitive,
  ThreadPrimitive,
} from "@assistant-ui/react";
import { RefundApproval } from "./RefundApproval";

function UserMessage() {
  return (
    <MessagePrimitive.Root className="message message--user">
      <MessagePrimitive.Content />
      <ActionBarPrimitive.Root>
        <ActionBarPrimitive.Edit asChild>
          <button type="button" aria-label="Edit message">Edit</button>
        </ActionBarPrimitive.Edit>
      </ActionBarPrimitive.Root>
    </MessagePrimitive.Root>
  );
}

function EditComposer() {
  return (
    <ComposerPrimitive.Root className="chat-input">
      <ComposerPrimitive.Input aria-label="Edit message" />
      <ComposerPrimitive.Cancel asChild><button type="button">Cancel</button></ComposerPrimitive.Cancel>
      <ComposerPrimitive.Send asChild><button type="submit">Save and resend</button></ComposerPrimitive.Send>
    </ComposerPrimitive.Root>
  );
}

function AssistantMessage() {
  return (
    <MessagePrimitive.Root className="message message--assistant">
      <MessagePrimitive.Content />
      <MessagePrimitive.Error>
        <span className="badge badge--error" role="alert">Something went wrong. Please try again.</span>
      </MessagePrimitive.Error>
    </MessagePrimitive.Root>
  );
}

export function Thread() {
  return (
    <ThreadPrimitive.Root className="chat-panel" aria-label="Support chat">
      <RefundApproval />
      <ThreadPrimitive.Viewport className="chat-log">
        <ThreadPrimitive.Messages
          components={{ UserMessage, EditComposer, AssistantMessage }}
        />
      </ThreadPrimitive.Viewport>
      <ComposerPrimitive.Root className="chat-input">
        <ComposerPrimitive.Input placeholder="Ask about an order, delivery or refund" aria-label="Message" />
        <ComposerPrimitive.Send asChild><button type="submit">Send</button></ComposerPrimitive.Send>
      </ComposerPrimitive.Root>
    </ThreadPrimitive.Root>
  );
}
