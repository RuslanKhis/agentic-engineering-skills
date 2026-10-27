// Reads the agent's SSE stream and keeps the text parts of each event.
export type ChatItem = { role: 'user' | 'agent'; text: string };

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
      for (const part of event.content?.parts ?? []) {
        if (part.text) yield { role: 'agent', text: part.text };
      }
    }
  }
}
