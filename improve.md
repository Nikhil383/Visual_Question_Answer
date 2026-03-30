# Improvement Roadmap

This document tracks identified issues and recommended improvements for the multimodal VQA project, categorized by priority.

## 🔴 Critical (Fix Immediately)

### 1. Test Bug - `test_predict_error` Mismatch
**File:** `tests/test_model.py`

The test expects an exception to be raised, but `VQAEngine.predict()` catches all exceptions and returns an error string.

**Current (Buggy):**
```python
@pytest.raises(Exception)  # This FAILS
def test_predict_error(mock_llm_cls):
    # ... setup ...
    engine.predict("fake_base64", "Question")  # Returns string, doesn't raise
```

**Fix Option A - Update Test (Recommended):**
```python
def test_predict_error(mock_llm_cls):
    """Test that engine returns error string on failure."""
    mock_llm = MagicMock()
    mock_llm_cls.return_value = mock_llm
    mock_llm.invoke.side_effect = Exception("API Error")

    with patch.dict("os.environ", {"GOOGLE_API_KEY": "fake_key"}):
        engine = VQAEngine()

    result = engine.predict("fake_base64", "Question")
    assert "Error" in result  # Assert returned error message
```

**Fix Option B - Remove try-catch in model:**
```python
# In src/model.py, remove try-except to let exceptions bubble up
# This changes API behavior - callers must handle exceptions
```

---

## 🟠 High Priority (Production Readiness)

### 2. Add Rate Limiting
**File:** `src/app.py`

Prevent API abuse and control costs.

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/predict", methods=["POST"])
@limiter.limit("10 per minute")  # Stricter for expensive LLM calls
def predict():
    # ... existing code ...
```

**Install:** `uv add flask-limiter`

---

### 3. Add Request Timeouts
**File:** `src/model.py`

LLM calls can hang indefinitely.

```python
from requests.exceptions import Timeout, ConnectTimeout

class VQAEngine:
    def predict(self, image_b64: str, text: str, timeout: int = 30) -> str:
        try:
            message = HumanMessage(...)
            response = self.llm.invoke([message], timeout=timeout)
            return response.content
        except Timeout:
            logger.error("LLM request timed out")
            return "Error: Request timed out. Please try again."
        except Exception as e:
            logger.exception("LLM invocation failed")
            return f"Error processing request: {str(e)}"
```

---

### 4. Replace Global State with Flask `g`
**File:** `src/app.py`

Global `_engine` limits scalability and testing.

```python
from flask import g

@app.before_request
def ensure_engine():
    if 'engine' not in g:
        g.engine = VQAEngine(model_name=os.getenv("MODEL_NAME", "gemini-2.5-flash"))

@app.route("/predict", methods=["POST"])
def predict():
    engine = g.engine
    # ... use engine ...
```

**Alternative:** Use Flask Application Factory pattern.

---

### 5. Add Health Check Endpoint
**File:** `src/app.py`

Required for load balancers and container orchestration.

```python
@app.route("/health")
def health():
    """Health check for load balancers."""
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "version": "0.1.0"
    }), 200

@app.route("/ready")
def ready():
    """Readiness check - verifies engine is loaded."""
    try:
        get_engine()
        return jsonify({"ready": True}), 200
    except Exception as e:
        return jsonify({"ready": False, "error": str(e)}), 503
```

---

## 🟡 Medium Priority (Code Quality)

### 6. Replace print() with Structured Logging
**File:** `src/model.py`

```python
import logging

logger = logging.getLogger("vqa_engine")

class VQAEngine:
    def __init__(self, model_name="gemini-2.5-flash"):
        logger.info(f"Initializing Gemini VQA Engine with model: {model_name}")
        # ...
    
    def predict(self, image_b64: str, text: str) -> str:
        logger.debug(f"Executing VQA Chain for question: '{text}'")
        try:
            # ...
        except Exception as e:
            logger.error(f"Engine Error: {e}", exc_info=True)
```

---

### 7. Add Input Validation
**File:** `src/app.py`

Validate question text length and content.

```python
import re

@app.route("/predict", methods=["POST"])
def predict():
    # ... existing validation ...
    
    text = request.form.get("question", "").strip()
    
    # Length validation
    if len(text) > 500:
        return jsonify({"error": "Question too long (max 500 chars)"}), 400
    
    # Content sanitization (basic)
    if re.search(r'[<>{}]', text):
        return jsonify({"error": "Invalid characters in question"}), 400
    
    # Profanity filter (optional)
    # blocked_words = [...]
    # if any(word in text.lower() for word in blocked_words):
    #     return jsonify({"error": "Question contains prohibited content"}), 400
    
    # ... rest of handler ...
```

---

### 8. Add Response Caching
**File:** `src/model.py` or `src/app.py`

Cache identical image+question pairs to reduce API costs.

```python
from functools import lru_cache
import hashlib

class VQAEngine:
    def _get_cache_key(self, image_b64: str, text: str) -> str:
        """Generate cache key from input."""
        combined = f"{image_b64}:{text}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def predict(self, image_b64: str, text: str) -> str:
        # Simple in-memory cache (use Redis in production)
        cache_key = self._get_cache_key(image_b64, text)
        if hasattr(self, '_cache') and cache_key in self._cache:
            return self._cache[cache_key]
        
        result = self._invoke_llm(image_b64, text)
        
        if not hasattr(self, '_cache'):
            self._cache = {}
        self._cache[cache_key] = result
        return result
```

---

## 🟢 Low Priority (Nice to Have)

### 9. Add API Documentation
**File:** New endpoint documentation

```python
from flask import render_template_string

API_DOCS = """
<h1>VQA API Documentation</h1>
<h2>POST /predict</h2>
<p>Submit image and question for visual analysis.</p>
...
"""

@app.route("/docs")
def docs():
    return render_template_string(API_DOCS)
```

**Better:** Use Flask-RESTX or Flasgger for OpenAPI/Swagger docs.

---

### 10. Add Metrics Endpoint
**File:** `src/app.py`

Expose Prometheus metrics for monitoring.

```python
from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter('vqa_requests_total', 'Total requests')
REQUEST_LATENCY = Histogram('vqa_request_duration_seconds', 'Request latency')

@app.route("/predict", methods=["POST"])
@REQUEST_LATENCY.time()
def predict():
    REQUEST_COUNT.inc()
    # ... existing code ...

@app.route("/metrics")
def metrics():
    return generate_latest()
```

---

### 11. Async Support
**File:** `src/model.py`

Support async/await for better concurrency.

```python
import asyncio
from langchain_core.messages import HumanMessage

class VQAEngine:
    async def predict_async(self, image_b64: str, text: str) -> str:
        """Async version of predict for better concurrency."""
        message = HumanMessage(...)
        # Use ainvoke if available, or run in executor
        response = await asyncio.get_event_loop().run_in_executor(
            None, self.llm.invoke, [message]
        )
        return response.content
```

---

## Summary

| Priority | Task | Effort | Impact |
|----------|------|--------|--------|
| 🔴 Critical | Fix `test_predict_error` | 5 min | Blocks CI/CD |
| 🟠 High | Add rate limiting | 15 min | Production requirement |
| 🟠 High | Add timeouts | 10 min | Reliability |
| 🟠 High | Replace global state | 20 min | Scalability |
| 🟠 High | Health endpoints | 10 min | Deployment requirement |
| 🟡 Medium | Structured logging | 15 min | Observability |
| 🟡 Medium | Input validation | 15 min | Security |
| 🟡 Medium | Response caching | 30 min | Cost optimization |
| 🟢 Low | API docs | 30 min | Developer experience |
| 🟢 Low | Metrics | 20 min | Monitoring |
| 🟢 Low | Async support | 45 min | Performance |

**Estimated Total:** ~4 hours for all improvements.

**Recommended Sprint:**
- Week 1: Critical + High priority (fix test, production readiness)
- Week 2: Medium priority (logging, validation, caching)
- Week 3: Low priority (docs, metrics, async)
