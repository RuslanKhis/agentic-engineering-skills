// Shared browser API: can be used unchanged inside a React component.
export async function streamReply({message, sessionId, token, onEvent}) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 15000);
  let reader;
  try {
    const response = await fetch('/api/chat', {
      method: 'POST', signal: controller.signal,
      headers: {'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`},
      body: JSON.stringify({message, session_id: sessionId}),
    });
    if (!response.ok) throw Error('Unable to open this conversation.');
    reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '', terminal = false;
    while (true) {
      const {value, done} = await reader.read();
      buffer += decoder.decode(value, {stream: !done});
      let newline;
      while ((newline = buffer.indexOf('\n')) >= 0) {
        const event = JSON.parse(buffer.slice(0, newline));
        buffer = buffer.slice(newline + 1);
        const field = {session:'session_id', text:'text', tool:'label', error:'message'}[event.type];
        if (terminal || (event.type !== 'done' && (!field || typeof event[field] !== 'string')))
          throw Error('Invalid reply stream.');
        if (field && event[field].length > 10000) throw Error('Reply too large.');
        terminal = event.type === 'done' || event.type === 'error';
        onEvent(event);
      }
      if (done) break;
      if (buffer.length > 16384) throw Error('Reply too large.');
    }
    if (!terminal || buffer.trim()) throw Error('The reply was interrupted.');
  } finally {
    clearTimeout(timer);
    await reader?.cancel();
  }
}
