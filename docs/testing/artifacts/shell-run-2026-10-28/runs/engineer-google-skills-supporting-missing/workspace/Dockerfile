FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /srv

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY help ./help

# Non-root user with a writable home (the SDK writes config under $HOME) and a writable
# SQLite directory; the container filesystem is ephemeral on Cloud Run.
RUN useradd --create-home --uid 10001 agent && mkdir -p /tmp/support && chown agent /tmp/support
USER agent
ENV HOME=/home/agent SUPPORT_DB_PATH=/tmp/support/support.db

ENV PORT=8080
CMD exec uvicorn app.server:app --host 0.0.0.0 --port ${PORT}
