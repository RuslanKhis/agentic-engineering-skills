FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /srv

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY help ./help

RUN useradd --create-home --uid 10001 app && chown app /srv
USER app

ENV PORT=8080
CMD exec uvicorn app.server:app --host 0.0.0.0 --port ${PORT}
