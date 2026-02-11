# ---------- Base image ----------
FROM python:3.11-slim

# ---------- Metadata ----------
LABEL maintainer="nikhilmahesh89@gmail.com"

ENV PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1

# ---------- System deps ----------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    ca-certificates \
    libgl1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# ---------- Create app dir ----------
WORKDIR /app

# ---------- Copy dependency manifests ----------
COPY pyproject.toml uv.lock ./

# ---------- Install uv ----------
RUN pip install --no-cache-dir uv

# ---------- Install dependencies ----------
RUN uv sync --frozen --no-dev

# ---------- Copy project files ----------
COPY . .

# ---------- Render requires this ----------
ENV PORT=10000
EXPOSE 10000

# ---------- Start app ----------
CMD ["sh", "-c", "python -m src.app --port=$PORT"]
