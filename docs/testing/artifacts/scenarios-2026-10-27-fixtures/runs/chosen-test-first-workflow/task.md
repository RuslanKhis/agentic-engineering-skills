Using the test-first workflow I picked, fix our refund adapter: if the provider times out after it has already accepted a refund, our retry refunds the customer again. Show the duplicate in a test first, then fix it, and keep the success response the same.

---
Situation (from the person asking): The user explicitly selected the installed test-first development skill before this request. The repository has an existing refund adapter, durable operation store, provider replay-key contract and deterministic provider double. No live payments or external model calls are authorized.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.