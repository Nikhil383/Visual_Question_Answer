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
        
        print(f"Initializing Gemini VQA Engine with model: {model_name}")
        self.llm = ChatGoogleGenerativeAI(model=model_name)

    def predict(self, image_b64: str, text: str) -> str:
        """
        Executes the VQA chain using the provided base64 image and question.
        
        Args:
            image_b64 (str): Base64 encoded image string.
            text (str): The question to be answered.
            
        Returns:
            str: The natural language answer from Gemini.
        """
        try:
            print(f"Executing VQA Chain for question: '{text}'")
            
            # Construct Multimodal Message for LangChain
            message = HumanMessage(
                content=[
                    {"type": "text", "text": text},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{image_b64}"
                    }
                ]
            )
            
            # Invoke the LLM (LangChain orchestration)
            response = self.llm.invoke([message])
            
            return response.content
            
        except Exception as e:
            print(f"Engine Error: {e}")
            return f"Error processing request: {str(e)}"
