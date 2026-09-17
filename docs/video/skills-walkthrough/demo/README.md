# The walkthrough's local worked example

This fixture grounds the short video in executable code. It is a teaching
example created for the video, not a recording of Claude generating code.

The HTTP routes, streamed NDJSON, session ownership checks, SQLite language
profile, browser client and offline checks are real. `DemoRunner` is a
deterministic substitute for the ADK/model event boundary. It always answers a
synthetic order question; no model, live ADK Runner, delivery service or Google
Cloud service is invoked. `Chat.jsx` shows how the shared API client fits an
existing React app; React compilation and rendering are not included here.

## Run locally

```bash
python3 docs/video/skills-walkthrough/demo/app.py --demo
```

Open `http://127.0.0.1:8766`. Ask “Where is my order?”; select Spanish, check
“Remember my preference”, and save. Start a new conversation and ask again.
The app answers “Tu pedido llega el viernes.” The preference survives a server
restart; conversation IDs are intentionally process-local. “Forget preference”
deletes the profile entry and restores the default English setting.

The exact language setting is a deterministic user profile, not semantic
Memory Bank. This follows the memory skill's store-selection guidance.

## Evidence

```bash
python3 -m unittest discover -s docs/video/skills-walkthrough/demo -p 'test_*.py' -v
node --test docs/video/skills-walkthrough/demo/test_client.mjs
python3 docs/video/skills-walkthrough/demo/capture_evidence.py
```

- `test-report.txt`: 19 Python checks through real temporary localhost sockets,
  including streamed arrival before provider completion, ownership, consent,
  persistence, correction, erasure, duplicate aggregate filtering and late errors.
- `client-test-report.txt`: six JavaScript API-client checks with a mocked
  `fetch` transport, including split UTF-8 bytes, auth/body construction,
  incomplete streams, malformed events and terminal error ordering.
- `video-evidence.json`: actual endpoint replay, exact source excerpts and
  defensible scope. The capture script asserts separate session IDs and records
  the fresh conversation's Spanish reply. Test reports must already exist.

The coordinating agent also verified the actual browser DOM at localhost:8766:
English reply; explicit consent and save showing “Spanish remembered”; new
conversation yielding Spanish; forgetting followed by a fresh conversation
yielding English again. This exercises `index.html` and `client.js`, not React.

The HTTP stream is a small application-owned NDJSON contract, not AG-UI. Raw
provider events, internal reasoning and unapproved tool data never enter it.
The six-line React excerpt illustrates the event handler; it does not replace
the full stream parser's completion and validation checks.

## Limits

Only run on localhost: `demo-alice` and `demo-bob` are intentionally fake
credentials, enabled by the explicit `--demo` flag. Integrating a real app
requires its existing verified authentication and actual ADK event adapter.
The server is a Python teaching server with no distributed locking, production
deployment, durable session history, stream reconnection, server-side model
deadline, full schema validation, retention policy or deployment hardening.
The browser client does have a 15-second overall response deadline and does not
automatically resubmit requests. A client abort does not prove a remote action
stopped. No production readiness, model quality or cloud integration claim is
made by these offline tests.
