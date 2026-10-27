FROM python:3.12-slim
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ app/
COPY help/ help/
ENV PORT=8080
CMD ["python", "-m", "app.http_server"]
