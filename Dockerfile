# ---------- Base image ----------
FROM python:3.11-slim

# ---------- Metadata ----------
LABEL maintainer="nikhilmahesh89@gmail.com"
ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    FLASK_PORT=5000

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

# ---------- Copy dependency manifests first (for layer caching) ----------
COPY pyproject.toml uv.lock /app/

# ---------- Install uv and sync dependencies ----------
RUN pip install --no-cache-dir uv \
    && uv sync --non-interactive || true

# ---------- Copy project files ----------
COPY . /app

# ---------- Expose port ----------
EXPOSE ${FLASK_PORT}

# ---------- Default command ----------
CMD ["python", "-m", "src.app"]
