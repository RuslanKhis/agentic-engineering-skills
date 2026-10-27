// A2UI surface for product cards and comparison tables beside the chat reply.
import { MessageProcessor, STRICT_VALIDATION } from "@a2ui/web_core";

// Components our catalogue defines; keep in step with ALLOWED_COMPONENTS in app/tools/a2ui.py.
export const ALLOWED_COMPONENTS = new Set(["Column", "Row", "Card", "Text", "Image"]);

// UNVERIFIED: the option shape below follows the 0.14.0 notes (validationConfig beside the
// catalogues and the outbound listener); no package is installed here, so run `tsc` and the
// rejection test in a checkout with dependencies. Without validationConfig, 0.14.0 tolerates
// unknown components, which is why the explicit guard below also runs.
export const processor = new MessageProcessor([], undefined, { validationConfig: STRICT_VALIDATION } as never);

export class WidgetRejected extends Error {}

// Refuse a batch whose components are not all in the catalogue (or lack a root) before it
// reaches the processor, so nothing renders silently or half-rendered.
export function guardMessages(messages: unknown[]): void {
  for (const raw of messages) {
    const update = (raw as { updateComponents?: { surfaceId: string; components: { id: string; component: string }[] } })
      .updateComponents;
    if (!update) continue;
    if (!update.components.some((c) => c.id === "root")) {
      throw new WidgetRejected(`surface ${update.surfaceId}: missing root`);
    }
    for (const c of update.components) {
      if (!ALLOWED_COMPONENTS.has(c.component)) {
        throw new WidgetRejected(`component "${c.component}" (${c.id}) is not in the catalogue`);
      }
    }
  }
}

// Feed A2UI messages into the processor. Throws WidgetRejected (or the processor's own
// validation error) on bad input; the caller shows a visible fallback and logs it.
export function applyA2uiMessages(messages: unknown[]): void {
  guardMessages(messages);
  for (const message of messages) {
    processor.processMessages([message as never]);
  }
}
