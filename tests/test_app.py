from io import BytesIO
from unittest.mock import MagicMock, patch

import pytest
from PIL import Image


def _make_jpeg_bytes() -> bytes:
    img = Image.new("RGB", (10, 10), color=(255, 0, 0))
    buf = BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


@pytest.fixture()
def client():
    from src.app import app

    with patch("src.app.VQAEngine") as mock_engine_cls:
        mock_engine = MagicMock()
        mock_engine.predict.return_value = "ok"
        mock_engine_cls.return_value = mock_engine

        # ensure lazy engine is re-created under patch
        import src.app as app_module

        app_module._engine = None

        app.config.update(TESTING=True)
        with app.test_client() as c:
            yield c


def test_predict_success(client):
    data = {
        "question": "What is this?",
        "image": (BytesIO(_make_jpeg_bytes()), "x.jpg"),
    }
    resp = client.post("/predict", data=data, content_type="multipart/form-data")
    assert resp.status_code == 200
    assert resp.get_json()["answer"] == "ok"


def test_predict_missing_image(client):
    resp = client.post(
        "/predict", data={"question": "Hi"}, content_type="multipart/form-data"
    )
    assert resp.status_code == 400


def test_predict_missing_question(client):
    data = {"image": (BytesIO(_make_jpeg_bytes()), "x.jpg")}
    resp = client.post("/predict", data=data, content_type="multipart/form-data")
    assert resp.status_code == 400


def test_predict_unsupported_mime(client):
    data = {
        "question": "What is this?",
        "image": (BytesIO(b"not-an-image"), "x.txt"),
    }
    resp = client.post("/predict", data=data, content_type="multipart/form-data")
    assert resp.status_code in {400, 415}
