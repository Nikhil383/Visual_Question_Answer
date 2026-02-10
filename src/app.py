import os
import base64
import io
from flask import Flask, render_template, request, jsonify
from PIL import Image
from src.model import VQAEngine

app = Flask(__name__)

# Initialize the VQA engine
print("Loading VQA Engine...")
engine = VQAEngine()
print("VQA Engine ready.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    
    file = request.files['image']
    text = request.form.get('question', '')
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if not text:
        return jsonify({'error': 'No question provided'}), 400

    try:
        # --- App Controller logic: Base64 Encoding ---
        # Read image and convert to RGB
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # Convert to Base64 JSON-compatible string
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        # --- Engine logic: Chain Execution ---
        answer = engine.predict(img_b64, text)
        
        return jsonify({'answer': answer})
        
    except Exception as e:
        print(f"Controller Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
