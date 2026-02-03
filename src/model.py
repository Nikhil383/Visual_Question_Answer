import os
import io
import base64
from PIL import Image
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv()

class VQAEngine:
    def __init__(self, model_name="gemini-2.5-flash"):
        # Ensure API key is set
        if not os.getenv("GOOGLE_API_KEY"):
            print("Warning: GOOGLE_API_KEY not found in environment variables.")
        
        self.llm = ChatGoogleGenerativeAI(model=model_name)

    def predict(self, image: Image.Image, text: str) -> str:
        try:
            # Convert PIL Image to base64
            buffered = io.BytesIO()
            # Ensure image is in RGB mode for JPEG saving
            if image.mode != "RGB":
                image = image.convert("RGB")
                
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            
            # Construct message
            message = HumanMessage(
                content=[
                    {"type": "text", "text": text},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{img_str}"
                    }
                ]
            )
            
            response = self.llm.invoke([message])
            return response.content
            
        except Exception as e:
            print(f"Prediction Error: {e}")
            return f"Error processing request: {str(e)}"
