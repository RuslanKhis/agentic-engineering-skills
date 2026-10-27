Our agent reads from memory with PreloadMemoryTool, but nothing ever gets saved to it. Can you design and build the saving side: what gets saved and when, who agreed to it, how people correct or delete it, and what happens when the memory service is down? Engineers share sites, and one engineer's preferences must never show up for another. Offline tests only.

---
Situation (from the person asking): google-adk==2.8.0 project with Memory Bank in deploy and InMemoryMemoryService in tests, a DatabaseSessionService, two tools and no consent or erasure code. No network or credentials.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.