from unittest.mock import MagicMock, patch
from PIL import Image
from src.model import VQAEngine

# We mock the transformers components to avoid downloading the model during tests
@patch('src.model.ViltProcessor')
@patch('src.model.ViltForQuestionAnswering')
def test_predict_success(mock_model_cls, mock_processor_cls):
    # Setup mocks
    mock_processor = MagicMock()
    mock_model = MagicMock()
    mock_processor_cls.from_pretrained.return_value = mock_processor
    mock_model_cls.from_pretrained.return_value = mock_model
    
    # Mock return values
    mock_processor.return_value = {"input_ids": "fake_tensor"}
    mock_outputs = MagicMock()
    # Mock logits such that argmax gives index 0
    import torch
    mock_outputs.logits = torch.tensor([[10.0, 5.0]]) 
    mock_model.return_value = mock_outputs
    mock_model.config.id2label = {0: "yes", 1: "no"}

    # Initialize engine
    engine = VQAEngine()
    
    # Create fake image
    img = Image.new('RGB', (100, 100))
    
    # Run predict
    result = engine.predict(img, "Is this a test?")
    
    # Verify
    assert result == "yes"
    mock_processor.assert_called_once()
    mock_model.assert_called_once()

def test_predict_error():
    # Test error handling
    engine = VQAEngine()
    # Force an error by passing None for image which processor might reject, 
    # or better, mock it to raise exception
    engine.processor = MagicMock(side_effect=Exception("Processing failed"))
    
    result = engine.predict(None, "Question")
    assert result == "Error processing request."
