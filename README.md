# Multimodal_AI(Visual Question Answering)

A lightweight, fast, and interactive Multimodal AI system that answers questions about images using the ViLT-B/32 Visual Question Answering model.

Upload an image → Ask any question → Get instant answers.

## Problem Statement

Traditional AI systems process text and images separately, making it hard to build applications that jointly understand visual and textual input.
This project solves the problem of enabling machines to:

- View an image

- Understand a natural-language question

- Answer with meaningful context and reasoning

This is widely used in assistive tech, search engines, ecommerce, surveillance, and intelligent tutoring systems.

## Tech Stack

### Languages:

- Python 3.10+

### Libraries & Frameworks:

#### HuggingFace Transformers

-ViLT (dandelin/vilt-b32-finetuned-vqa)
- PyTorch
- Gradio
- Pillow

### Tools:

- uv (dependency manager)
- Docker
- Git / GitHub
- Hugging Face Spaces (deployment)

## To run Locally

1. Install uv
2. Sync all dependencies 
- uv sync
3. Run the applications
-uv run main.py
4. Open Gradio in Browser
  -run on http://127.0.0.1:7860

## How it runs
1. Upload an image
2. Enter a question
3. Model processes image patches + text tokens
4. Returns the best possible answer

## Key Learnings & Challenges
### Key Learnings
- Gained hands-on experience with Vision-Language Transformers (ViLT).
- Learned how multimodal fusion works by embedding both images and text.
- Improved understanding of model loading, tokenization, and image preprocessing.
- Practiced designing a clean, user-friendly Gradio interface.
### Challenges
- Handling slow inference on CPU — optimized preprocessing to reduce latency.
- Managing large dependencies using uv, ensuring reproducible environments.
- Deploying on Hugging Face Spaces and ensuring the model runs within resource limits.
- Keeping the UI responsive while maintaining accurate predictions.

## Future Improvements
- Add image captioning
- Add OCR-based multimodal QA
- Build an API endpoint (FastAPI / Flask)
- Deploy on HuggingFace Spaces
- Add more ViLT variants


