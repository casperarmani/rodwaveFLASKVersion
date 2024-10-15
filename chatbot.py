import os
import time
import logging
import google.generativeai as genai
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get the API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("No GEMINI_API_KEY found in environment variables. Please set it in your .env file.")

# Configure the generative AI
genai.configure(api_key=api_key)

class Chatbot:
    def __init__(self):
        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
        }
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-exp-0827",
            generation_config=self.generation_config,
        )
        self.chat_session = self.model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": ["You are a world-class video ads and creative analyzer"],
                },
                {
                    "role": "model",
                    "parts": ["I'm Your World-Class Video Ads & Creative Analyzer! I'm ready to analyze video ads and provide insights to improve their effectiveness. How can I assist you today?"],
                },
            ]
        )

    def send_message(self, message):
        try:
            response = self.chat_session.send_message(message)
            return response.text
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            return "I apologize, but there was an error processing your request. Please try again."

    def analyze_video(self, video_path):
        try:
            logger.info(f"Uploading video file: {video_path}")
            video_file = genai.upload_file(video_path)
            
            logger.info("Waiting for video processing...")
            while video_file.state.name == "PROCESSING":
                time.sleep(5)
                video_file = genai.get_file(video_file.name)

            if video_file.state.name == "FAILED":
                raise ValueError(f"Video processing failed: {video_file.state.name}")

            logger.info("Video processing complete. Generating analysis...")
            prompt = "Analyze this video advertisement. Provide insights on its effectiveness, target audience, key messages, and areas for improvement. Include a comprehensive analysis of audience engagement, messaging & storytelling, visual & audio elements, brand consistency, and platform optimization."
            
            response = self.model.generate_content([video_file, prompt], request_options={"timeout": 300})
            return response.text
        except Exception as e:
            logger.error(f"Error analyzing video: {str(e)}")
            return f"An error occurred during video analysis: {str(e)}"