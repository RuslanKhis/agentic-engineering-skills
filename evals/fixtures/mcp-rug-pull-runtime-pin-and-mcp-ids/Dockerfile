FROM python:3.12-slim
WORKDIR /srv
COPY pyproject.toml ./
COPY app ./app
RUN pip install --no-cache-dir .
# The PDF extraction MCP server runs as a stdio subprocess of the agent in this container.
ENV PORT=8080
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8080"]
