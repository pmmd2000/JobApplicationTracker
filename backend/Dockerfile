# Stage 1: Builder
FROM python:3.12 AS builder

WORKDIR /app

# Install Python dependencies to a temporary location
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy installed dependencies from builder
COPY --from=builder /root/.local /root/.local

# Ensure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# Expose backend port
EXPOSE 5000

# Run with Gunicorn
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]
