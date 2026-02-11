FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    ca-certificates \
    libgl1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files first
COPY pyproject.toml uv.lock ./

# 🚨 Install into system Python (CRITICAL)
RUN uv sync --frozen --system

# Copy rest of app
COPY . .

# Render dynamic port
ENV PORT=10000
EXPOSE 10000

CMD ["sh", "-c", "uv run py -m src.app"]
