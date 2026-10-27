Our local policy retriever returns results but misses some answers. Diagnose the retained extraction and query observations, and add checks that expose missing evidence. Keep the existing retrieval and output limits; use offline fixtures only.

---
Situation (from the person asking): Use the memory skill's document-coverage fixture to supply main-policy-only, contents-only, incomplete table and empty image-page observations, along with an honest complete-text control. Keep expected sections with the grader, not the retriever. No real PDF parsing or visual review is available in this fixture.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.