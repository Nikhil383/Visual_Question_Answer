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

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies (creates .venv)
RUN uv sync --frozen

# Copy rest of project
COPY . .

# Render dynamic port
ENV PORT=10000
EXPOSE 10000

# 🚨 IMPORTANT: Use uv run
CMD ["sh", "-c", "uv run python -m src.app"]
