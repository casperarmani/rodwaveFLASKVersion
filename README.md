# Gemini Chatbot with Video Analysis

This project is a Flask-based web application that uses the Gemini API to create a chatbot capable of analyzing videos.

## Setup

1. Clone this repository.
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up your Gemini API key:
   - Rename the `.env.example` file to `.env`
   - Replace `your_api_key_here` with your actual Gemini API key

4. Run the Flask application:
   ```
   python app.py
   ```

5. Open your web browser and navigate to `http://127.0.0.1:5000/` to use the application.

## Usage

- Use the chat interface to interact with the chatbot.
- To analyze a video, upload a video file, enter an analysis prompt, and click "Analyze Video".

## Note

Ensure that your Gemini API key is kept secret and not shared publicly.