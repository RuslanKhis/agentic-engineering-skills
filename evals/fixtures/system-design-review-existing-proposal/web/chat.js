// Minimal chat client for the travel desk assistant.
const profile = JSON.parse(localStorage.getItem("tw_profile") || "{}");
let sessionId = null;

export async function send(message) {
  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      tenant_id: profile.tenant_id,
      traveller_id: profile.traveller_id,
      message,
      session_id: sessionId,
    }),
  });
  const data = await res.json();
  sessionId = data.session_id;
  return data.reply;
}
