## Multimodal AI – Visual Question Answering Demo

This repository contains a simple **multimodal AI web app** built with **Gradio** and **Hugging Face Transformers**.  
The app loads a pre‑trained **ViLT** (Vision-and-Language Transformer) model (`dandelin/vilt-b32-finetuned-vqa`) that can answer natural‑language questions about an uploaded image.

---

### Problem Statement

Modern applications increasingly need to **understand both images and text together**, not just one modality at a time.  
For example, users may want to:

- ask questions about product photos,
- get quick insights from charts or infographics,
- interact with screenshots or real‑world scenes using natural language.

Building such systems from scratch is complex and requires expertise in computer vision, natural language processing, and model deployment.  
This project demonstrates a **minimal, end‑to‑end visual question answering (VQA) app** that:

- accepts an image and a free‑form text question,
- uses a pretrained multimodal transformer (ViLT),
- returns the most likely answer, all through an easy‑to‑use web interface.

The project is ready to be used as a **GitHub README**, so you can push this repo to GitHub and this file will appear as the main project description.

---

### Features

- **Image + Text input**: Upload an image and ask any question about it.
- **Pretrained ViLT model**: Uses `ViltForQuestionAnswering` with `ViltProcessor`.
- **Gradio UI**: Clean web interface for quick experimentation.
- **Python 3.11+**: Managed via `pyproject.toml` (compatible with tools like `uv` or `pip`).

---

### Project Structure

- `main.py` – Gradio app that:
  - loads the ViLT processor and model,
  - defines `answer_question(image, text)`,
  - exposes a web interface with image and text inputs.
- `pyproject.toml` – Project metadata and Python dependencies.

---

### Installation

1. **Clone the repository from GitHub**

   ```bash
   git clone https://github.com/<your-username>/multimodal-ai.git
   cd multimodal-ai
   ```

2. **Create and activate a virtual environment** (recommended)

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # source .venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**

   Using `pip` (if you export requirements):

   ```bash
   pip install -r requirements.txt
   ```

   Or, if you are using `uv` with `pyproject.toml`:

   ```bash
   uv sync
   ```

   > Make sure you have a recent version of PyTorch installed that matches your system and GPU/CPU setup.  
   > See the official installation instructions at the PyTorch website.

---

### Running the App

Once dependencies are installed and your virtual environment is active:

```bash
python main.py
```

The Gradio interface will start, and the terminal will show a **local URL** (and an optional public `share` URL if enabled).  
Open the URL in your browser, upload an image, type a question, and you’ll see the model’s answer.

---

### Model Details

- **Model**: `dandelin/vilt-b32-finetuned-vqa`
- **Library**: `transformers` (Hugging Face)
- **Task**: Visual Question Answering (VQA)

`main.py`:
- uses `ViltProcessor` to prepare the image + text inputs,
- runs `ViltForQuestionAnswering`,
- selects the highest‑probability answer from `model.config.id2label`.

---

### Using This on GitHub

After you push this project to GitHub:

- GitHub will automatically render this `README.md` on the repository’s main page.
- You can add screenshots, badges, or links below this section as you enhance the project.

Example commands to publish:

```bash
git init
git add .
git commit -m "Initial commit: multimodal AI VQA demo"
git branch -M main
git remote add origin https://github.com/<your-username>/multimodal-ai.git
git push -u origin main
```

Replace `<your-username>` with your actual GitHub username before running the commands.

---

### License

Add your preferred license here (e.g. MIT, Apache 2.0).  
If you plan to share this publicly on GitHub, it is recommended to include a `LICENSE` file.

