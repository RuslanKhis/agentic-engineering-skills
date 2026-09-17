// Integration excerpt for an EXISTING React app. Not part of the offline build.
import {useState} from 'react';
import {streamReply} from './client.js';

export function Chat({token}) {
  const [sessionId, setSession] = useState(null);
  const [reply, setReply] = useState('');
  const [status, setStatus] = useState('Ready');
  const [busy, setBusy] = useState(false);
  async function send(event) {
    event.preventDefault();
    const message = new FormData(event.currentTarget).get('message');
    setBusy(true); setReply(''); setStatus('Working…');
    try {
      await streamReply({message, sessionId, token, onEvent(e) {
        if (e.type === 'session') setSession(e.session_id);
        if (e.type === 'text')
          setReply(text => text + e.text);
        if (e.type === 'tool')
          setStatus(e.label);
        if (e.type === 'done')
          setStatus('Complete');
        if (e.type === 'error') setStatus(e.message);
      }});
    } catch { setStatus('The reply could not finish.'); }
    finally { setBusy(false); }
  }
  return <section>
    <p aria-live="polite">{reply}</p><small>{status}</small>
    <form onSubmit={send}><input name="message" required maxLength={2000}/>
      <button disabled={busy}>Send</button></form>
  </section>;
}
