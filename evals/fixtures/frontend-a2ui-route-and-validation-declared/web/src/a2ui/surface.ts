// A2UI surface for product cards and comparison tables beside the chat reply.
import { MessageProcessor } from "@a2ui/web_core";

export const processor = new MessageProcessor();

// Feed A2UI messages from the agent into the processor; the React renderer
// subscribes to the processor's surfaces.
export function applyA2uiMessages(messages: unknown[]): void {
  for (const message of messages) {
    processor.processMessages([message as never]);
  }
}
