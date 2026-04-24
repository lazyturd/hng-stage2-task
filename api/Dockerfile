# Stage 1: Build
FROM python:3.11-slim-bookworm AS builder
WORKDIR /app
COPY requirements.txt .
# FIX: Upgrade core Python packaging tools to patch known CVEs
RUN pip install --upgrade pip setuptools wheel
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Production
FROM python:3.11-slim-bookworm
# FIX: Use dist-upgrade to catch packages that standard upgrade holds back
RUN apt-get update && apt-get dist-upgrade -y && rm -rf /var/lib/apt/lists/*
RUN groupadd -r devops && useradd -r -g devops appuser
WORKDIR /app
COPY --from=builder /root/.local /home/appuser/.local
COPY . .
RUN chown -R appuser:devops /app
USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/docs')" || exit 1
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
