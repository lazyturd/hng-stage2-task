# Stage 1: Build dependencies
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Production runner
FROM python:3.11-slim

# Create a non-root user and group
RUN groupadd -r devops && useradd -r -g devops appuser

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application source code
COPY . .

# Assign ownership to non-root user
RUN chown -R appuser:devops /app

# Switch to non-root user
USER appuser

# Ensure local bin is in PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Healthcheck: Verify the worker can establish a connection to Redis
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import redis, os; r = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=int(os.getenv('REDIS_PORT', 6379))); r.ping()" || exit 1

CMD ["python", "worker.py"]