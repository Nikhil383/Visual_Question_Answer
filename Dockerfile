FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    ca-certificates \
    libgl1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install uv first
RUN pip install --no-cache-dir uv

# Copy dependency files first
COPY pyproject.toml uv.lock ./

# Install dependencies (VERY IMPORTANT)
RUN uv sync --frozen

# Copy rest of project
COPY . .

# Render port
ENV PORT=10000
EXPOSE 10000

CMD ["sh", "-c", "python -m src.app"]
