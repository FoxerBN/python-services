# ---------- Builder ----------
FROM python:3.12-slim AS builder
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt

# ---------- Runtime ----------
FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_MODULE=app.main:app \
    PORT=9990 \
    WORKERS=2 \
    LOG_LEVEL=info
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY --from=builder /install /usr/local
COPY app ./app
RUN useradd -m -u 1001 fastapiuser && mkdir -p /app/logs /app/db && chown -R fastapiuser:fastapiuser /app
USER fastapiuser
EXPOSE 9990
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl --fail http://127.0.0.1:${PORT}/healthz || exit 1
CMD gunicorn ${APP_MODULE} \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:${PORT} \
  --workers ${WORKERS} \
  --log-level ${LOG_LEVEL} \
  --access-logfile - \
  --error-logfile -
