import os
import base64
import io
import logging
from flask import Flask, render_template, request, jsonify
from PIL import Image
from PIL import ImageFile
from PIL import UnidentifiedImageError
from src.model import VQAEngine

app = Flask(__name__)

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("multimodal_ai")

# Limit request size (bytes). Defaults to 10MB.
app.config["MAX_CONTENT_LENGTH"] = int(
    os.getenv("MAX_CONTENT_LENGTH", str(10 * 1024 * 1024))
)

ALLOWED_IMAGE_MIMES = {"image/jpeg", "image/png", "image/webp"}
MAX_IMAGE_PIXELS = int(os.getenv("MAX_IMAGE_PIXELS", str(20_000_000)))

# PIL safety: protect against decompression bombs.
Image.MAX_IMAGE_PIXELS = MAX_IMAGE_PIXELS
ImageFile.LOAD_TRUNCATED_IMAGES = False

# Initialize the VQA engine
_engine: VQAEngine | None = None


def get_engine() -> VQAEngine:
    global _engine
    if _engine is None:
        logger.info("Loading VQA Engine...")
        _engine = VQAEngine(model_name=os.getenv("MODEL_NAME", "gemini-2.5-flash"))
        logger.info("VQA Engine ready.")
    return _engine


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image part"}), 400

    file = request.files["image"]
    text = request.form.get("question", "")

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not text:
        return jsonify({"error": "No question provided"}), 400

    try:
        if file.mimetype not in ALLOWED_IMAGE_MIMES:
            return jsonify({"error": f"Unsupported image type: {file.mimetype}"}), 415

        # --- App Controller logic: Base64 Encoding ---
        # Read image and convert to RGB
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        image.verify()  # validates headers without decoding full image
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Convert to Base64 JSON-compatible string
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        # --- Engine logic: Chain Execution ---
        answer = get_engine().predict(img_b64, text)

        return jsonify({"answer": answer})

    except UnidentifiedImageError:
        return jsonify({"error": "Invalid or corrupted image"}), 400
    except Image.DecompressionBombError:
        return jsonify({"error": "Image too large"}), 413
    except Exception as e:
        logger.exception("Controller error")
        debug = os.getenv("FLASK_DEBUG", "").lower() in {"1", "true", "yes", "on"}
        return jsonify({"error": str(e) if debug else "Internal server error"}), 500


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "").lower() in {"1", "true", "yes", "on"}
    app.run(host=host, port=port, debug=debug)
