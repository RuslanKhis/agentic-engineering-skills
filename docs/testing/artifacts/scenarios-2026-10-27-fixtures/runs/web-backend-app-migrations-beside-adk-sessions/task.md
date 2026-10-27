We added a table for saved answers. Set up migrations; the agent's sessions already live in the same Postgres.

---
Situation (from the person asking): An ADK 2.12 FastAPI app using DatabaseSessionService on Cloud SQL for PostgreSQL; no Alembic yet; tests run against SQLite locally.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.