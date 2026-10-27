# Stage 1: build the SPA (web/dist)
FROM node:22-slim AS web
WORKDIR /web
COPY web/package.json web/package-lock.json ./
RUN npm ci
COPY web/ ./
RUN npm run build

# Stage 2: Python service. The source stays in /srv because app/helpdesk.py reads
# help/articles.json relative to the repository root and server.py serves web/dist.
FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 HOME=/home/app
RUN useradd --create-home --home-dir /home/app --uid 10001 app
WORKDIR /srv
COPY pyproject.toml ./
# Dependencies only, at the pinned versions; the code is imported from /srv.
RUN python - <<'PY' > /tmp/requirements.txt
import tomllib
print("\n".join(tomllib.load(open("pyproject.toml", "rb"))["project"]["dependencies"]))
PY
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY app/ app/
COPY help/ help/
COPY --from=web /web/dist web/dist
USER app
ENV PYTHONPATH=/srv PORT=8080
# One process per container: no --workers. Sessions are in memory, so the service
# is deployed with max-instances=1 (see deploy/RUNBOOK.md).
CMD ["sh", "-c", "exec fastapi run app/server.py --host 0.0.0.0 --port ${PORT}"]
