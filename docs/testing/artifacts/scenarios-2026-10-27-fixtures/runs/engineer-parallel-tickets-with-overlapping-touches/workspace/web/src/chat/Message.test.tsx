import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { Message, type ChatMessage } from "./Message";

const render = (state: ChatMessage["state"], text = "Your refund of") =>
  renderToStaticMarkup(<Message message={{ role: "assistant", text, state }} />);

describe("Message", () => {
  it("keeps partial text and shows the failed badge when the stream failed", () => {
    const html = render("failed");
    expect(html).toContain("Your refund of");
    expect(html).toContain('data-badge="failed"');
    expect(html).toContain('data-state="failed"');
    expect(html).not.toContain('data-state="completed"');
  });

  it("does not show the completed state while a stream is open", () => {
    const html = render("streaming");
    expect(html).toContain('data-state="streaming"');
    expect(html).not.toContain('data-state="completed"');
    expect(html).not.toContain('data-badge="failed"');
  });

  it("shows no badge on a completed reply", () => {
    expect(render("completed")).not.toContain("data-badge");
  });
});
