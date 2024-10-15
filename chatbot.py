import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the generative AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class Chatbot:
    def __init__(self):
        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
        }
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=self.generation_config,
        )
        self.chat_session = self.model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": ["you are a world class video ads and creative analyzer"],
                },
                {
                    "role": "model",
                    "parts": ["I'm Your World-Class Video Ads & Creative Analyzer! I'm ready to analyze video ads and provide insights to improve their effectiveness. How can I assist you today?"],
                },
            ]
        )

    def send_message(self, message):
        response = self.chat_session.send_message(message)
        return response.text

    def analyze_video(self, video_path, prompt):
        try:
            print("Uploading video file...")
            video_file = genai.upload_file(video_path)
            
            print("Waiting for video processing...")
            while video_file.state.name == "PROCESSING":
                video_file = genai.get_file(video_file.name)
            
            if video_file.state.name != "ACTIVE":
                raise ValueError(f"Video processing failed: {video_file.state.name}")
            
            print("Making LLM inference request...")
            response = self.model.generate_content(
                contents=[prompt, video_file],
                stream=True
            )
            response.resolve()
            return response.text
        except Exception as e:
            print(f"Error analyzing video: {str(e)}")
            return None