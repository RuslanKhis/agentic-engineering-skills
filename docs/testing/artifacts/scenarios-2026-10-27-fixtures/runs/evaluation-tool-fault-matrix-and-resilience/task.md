Our ADK travel agent breaks badly when the flight API is flaky. Add tests where tools time out, return empty or garbage results, or error, and tell us how to score whether the agent recovers and is honest about it.

---
Situation (from the person asking): Python ADK 2.12.0. Tools: search_flights, book_flight (write, idempotency key), send_confirmation. Scripted-model Runner harness exists; one Environment Simulation 503 test. Live Gemini runs need approval.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.