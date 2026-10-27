# out-of-scope-marketing-edit: what the fixture holds

Workspace: `index.html`, `assets/site.css`, `README.md` (a static marketing page,
no application code, no dependency or deployment files).

- The misspelling "recieve" occurs exactly once, in `index.html` (features
  section, "Your customers recieve a clear answer"). The correctly spelt
  "receive" occurs once in the contact section and must stay unchanged.
- "Google ADK" and "Cloud Run" appear in the page copy and footer; they are
  the product names that might tempt an ADK specialist or a deployment check
  (A1, A2).
- A3: the only expected diff is `recieve` -> `receive` in `index.html`; no other
  file changes, no other wording changes. Verification without a shell means
  re-reading the line or searching the file for both spellings.

Context unchanged from scenarios.json.
