# Multimodal AI: Visual Question Answering System

[![CI](https://github.com/nikhil383/multimodal-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/nikhil383/multimodal-ai/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A production-ready Visual Question Answering (VQA) system that enables users to upload images and ask natural language questions about them.** Built with Google Gemini Vision API and LangChain, deployed via Flask with full CI/CD automation.

**Live Demo**: [https://multimodal-ai-50ad.onrender.com](https://multimodal-ai-50ad.onrender.com)

---

## What This Demonstrates

This project showcases **full-stack AI engineering skills**:

| Competency | Technologies & Practices |
| :--- | :--- |
| **AI/ML Integration** | LangChain orchestration, Google Gemini Vision API, multimodal prompt engineering |
| **Backend Development** | Flask REST API, base64 image processing, async request handling |
| **DevOps & Cloud** | Docker containerization, GitHub Actions CI/CD, Render deployment |
| **Software Engineering** | Modular architecture, unit testing with mocks, type-safe Python 3.11+ |
| **Developer Tooling** | UV package manager, Makefile automation, ruff linting, pytest |

---

##  Quick Start

```bash
git clone https://github.com/nikhil383/multimodal-ai.git
cd multimodal-ai
make install    # or: uv sync
make run        # or: uv run python -m src.app
```

Visit `http://localhost:5000` to interact with the application.

---

##  Architecture

**Three-layer design for maintainability and scalability:**

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│  Transport      │────▶│  Intelligence    │────▶│  External API       │
│  (Flask App)    │     │  (VQA Engine)    │     │  (Gemini + LangChain)│
└─────────────────┘     └──────────────────┘     └─────────────────────┘
   • HTTP handling          • Message construction    • LLM inference
   • Image validation       • Multimodal prompts      • Response parsing
   • Base64 encoding        • JSON serialization
```

### Key Design Decisions

- **Separation of concerns**: Web layer isolated from AI logic for easy testing and swapping
- **Mock-based testing**: CI runs without API costs using `unittest.mock`
- **Data URI pattern**: Images encoded as `data:image/jpeg;base64,{encoded}` for API compatibility
- **Environment-based config**: API keys managed via `.env` (python-dotenv)

---

##  Business Value

| Use Case | Impact |
| :--- | :--- |
| **Customer Support** | Automate visual troubleshooting (e.g., "What's wrong with this product?") |
| **Accessibility** | Enable visually impaired users to understand image content |
| **Content Moderation** | Detect inappropriate or policy-violating images at scale |
| **E-commerce** | Power visual search and product recommendations |
| **Healthcare** | Assist medical professionals with image-based diagnostics (research use) |

---

##  Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **AI/ML** | Google Gemini Vision API, LangChain |
| **Backend** | Flask, Python 3.11+, python-dotenv |
| **DevOps** | Docker, GitHub Actions, Render |
| **Testing** | pytest, unittest.mock |
| **Tooling** | UV (package manager), Makefile, ruff |

---

##  Project Structure

```
multimodal-ai/
├── src/
│   ├── app.py          # Flask REST API – image upload, validation, base64 encoding
│   ├── model.py        # VQA Engine – LangChain message construction – Gemini invocation
│   ├── templates/      # HTML frontend with image upload UI
│   └── static/         # CSS/JS assets
├── tests/              # Unit tests with mocked LLM (zero API cost in CI)
├── .github/            # CI/CD pipeline – auto-test on PR
├── pyproject.toml      # Dependency management (UV)
├── Makefile            # Developer workflow automation
├── Dockerfile          # Containerized deployment
└── .env.example        # Environment variable template
```

---

##  Testing & Quality

**All code is tested and linted automatically on every commit:**

```bash
make test     # Run pytest suite
make format   # Lint + format with ruff
make docker-build  # Build container
```

**CI Pipeline** (`.github/workflows/ci.yml`):
- Runs on every PR to `main`
- Installs dependencies via `uv sync`
- Executes unit tests with mocked API calls
- Enforces code quality with `ruff check`

---

##  Installation

### Prerequisites
- Python 3.11+
- [UV](https://github.com/astral-sh/uv) (recommended) or `pip`
- Google Gemini API Key ([get one free](https://aistudio.google.com/))

### Setup

```bash
git clone https://github.com/nikhil383/multimodal-ai.git
cd multimodal-ai

# Install dependencies
make install  # or: uv sync

# Configure API key
cp .env.example .env  # Edit .env and add GOOGLE_API_KEY

# Run development server
make run      # or: uv run python -m src.app
```

Access at `http://localhost:5000`

---

## Demo

**Upload an image, ask a question, get an AI-powered answer:**

<img width="1919" height="935" alt="Demo Screenshot" src="https://github.com/user-attachments/assets/b2ddab55-cd0f-497a-a162-1e44befa5238" />

<img width="1919" height="935" alt="Demo Screenshot" src="https://github.com/user-attachments/assets/2db8287d-cbd3-4dac-881b-99cdc55c37ce" />

**Try it live**: [https://multimodal-ai-50ad.onrender.com](https://multimodal-ai-50ad.onrender.com)

---

##  What's Next

Planned enhancements to demonstrate advanced capabilities:

- **Conversation history** with LangChain `ChatBufferMemory` for multi-turn VQA
- **Real-time streaming** responses for better UX
- **Video Q&A** support for temporal reasoning

---

## About the Author

**Nikhil**  
AI/ML Engineer specializing in production-ready LLM applications.

-  **GitHub**: [@nikhil383](https://github.com/nikhil383)
-  **Connect**: Available for AI engineering roles

**Open to opportunities** in AI/ML engineering, LLM application development, and full-stack AI systems.

---

*Built with modern AI engineering practices. Questions? Reach out via GitHub.*
