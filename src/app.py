
import os
from flask import Flask, render_template, request, jsonify
from PIL import Image
import io
from src.model import VQAEngine

app = Flask(__name__)

# Initialize the VQA engine
# We do this at module level so it loads once when the app starts
print("Loading model...")
engine = VQAEngine()
print("Model loaded.")

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
        # Read image into PIL format
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # Get prediction
        answer = engine.predict(image, text)
        
        return jsonify({'answer': answer})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
