import os
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from chatbot import Chatbot

app = FastAPI()
chatbot = Chatbot()

# Create static directory if it doesn't exist
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("templates/index.html", "r") as f:
        return f.read()

@app.post("/send_message")
async def send_message(message: str = Form(""), video: UploadFile = File(None)):
    if video:
        # Save the uploaded file temporarily
        video_path = os.path.join('temp', video.filename)
        os.makedirs('temp', exist_ok=True)
        with open(video_path, "wb") as buffer:
            buffer.write(await video.read())
        
        # Analyze the video
        analysis_result = chatbot.analyze_video(video_path, message)
        
        # Remove the temporary file
        os.remove(video_path)
        
        return {"response": analysis_result}
    else:
        # Handle text-only message
        response = chatbot.send_message(message)
        return {"response": response}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)