from transformers import ViltProcessor, ViltForQuestionAnswering
from PIL import Image
import torch

class VQAEngine:
    def __init__(self, model_name="dandelin/vilt-b32-finetuned-vqa"):
        self.processor = ViltProcessor.from_pretrained(model_name)
        self.model = ViltForQuestionAnswering.from_pretrained(model_name)

    def predict(self, image: Image.Image, text: str) -> str:
        try:
            encoding = self.processor(image, text, return_tensors="pt")
            
            # Forward pass
            with torch.no_grad():
                outputs = self.model(**encoding)
            
            logits = outputs.logits
            idx = logits.argmax(-1).item()
            answer = self.model.config.id2label[idx]
            return answer
        except Exception as e:
            # In a real app, log error here
            print(f"Prediction Error: {e}")
            return "Error processing request."
