# Single Cloud Run service: FastAPI (Runner in process) + built SPA. See docs/deploy/cloud-run-iap.md.
FROM node:22-slim AS web
WORKDIR /web
COPY web/package.json web/package-lock.json ./
RUN npm ci
COPY web/ ./
RUN npm run build

FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /srv
COPY pyproject.toml ./
COPY app/ app/
COPY help/ help/
RUN pip install . \
 && useradd --create-home --uid 10001 appuser
COPY --from=web /web/dist web/dist
USER appuser
ENV HOME=/home/appuser
# One process per container: scale with instances/concurrency, not workers.
CMD ["sh", "-c", "exec uvicorn app.server:app --host 0.0.0.0 --port ${PORT:-8080}"]
