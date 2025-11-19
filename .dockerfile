# ---------- Base image ----------
FROM python:3.11-slim

# ---------- Metadata ----------
LABEL maintainer="nikhilmahesh89@gmail.com"
ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    # set a default port for Gradio apps; change if your app uses another port
    GRADIO_PORT=7860

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
# We assume you are using pyproject.toml and uv.lock
COPY pyproject.toml uv.lock /app/

# ---------- Install uv and sync dependencies ----------
# Install uv itself with pip, then use uv to install project deps (uv.sync)
RUN pip install --no-cache-dir uv \
 && uv sync --non-interactive || true
# note: `uv sync` may fail in certain environments; the image will still continue so you can debug

# ---------- Copy project files ----------
COPY . /app

# If your project requires additional setup (downloads, model caches), do it here:
# e.g. to pre-cache transformers models, uncomment and adapt:
# RUN python -c "from transformers import AutoModel; AutoModel.from_pretrained('dandelin/vilt-b32-finetuned-vqa')"

# ---------- Expose port ----------
EXPOSE ${GRADIO_PORT}

# ---------- Default command ----------
# Prefer `python main.py` because `uv run` may require environment-specific options.
# Make sure main.py starts your gradio / app server and binds to 0.0.0.0:${GRADIO_PORT}.
CMD ["python", "main.py"]
