// Reads the agent's SSE stream and keeps the text parts and MCP App widgets of each event.
export type McpWidget = {
  id: string;
  provider: 'mcp';
  resource_uri: string; // page to fetch from /api/mcp_app/view?uri=...
  tool: unknown; // backend sends a name; ADK's own widget carries a tool dump with meta/_meta
  tool_args: Record<string, unknown>;
};
export type ChatItem =
  | { role: 'user' | 'agent'; text: string }
  | { role: 'widget'; widget: McpWidget };

export async function* agentStream(body: object): AsyncGenerator<ChatItem> {
  const res = await fetch('/api/run_sse', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  const reader = res.body!.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  for (;;) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const chunks = buffer.split('\n\n');
    buffer = chunks.pop() ?? '';
    for (const chunk of chunks) {
      const event = JSON.parse(chunk.replace(/^data: /, ''));
      if (event.mcp_widget) yield { role: 'widget', widget: event.mcp_widget };
      // Widgets ADK itself attaches (if the partner lists UI tools to ADK's session too).
      // ADK 2.12.0 attaches them even for isError results; those are not shown.
      const failed = (event.content?.parts ?? []).some((p: any) => p.functionResponse?.response?.isError);
      for (const w of event.actions?.renderUiWidgets ?? event.actions?.render_ui_widgets ?? []) {
        if (w.provider === 'mcp' && !failed) yield { role: 'widget', widget: { id: w.id, provider: 'mcp', ...w.payload } };
      }
      for (const part of event.content?.parts ?? []) {
        if (part.text) yield { role: 'agent', text: part.text };
      }
    }
  }
}
