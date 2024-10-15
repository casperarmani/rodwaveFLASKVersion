import os
from flask import Flask, render_template, request, jsonify
from chatbot import Chatbot

app = Flask(__name__)
chatbot = Chatbot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form.get('message', '')
    video_file = request.files.get('video')

    if video_file:
        # Save the uploaded file temporarily
        video_path = os.path.join('temp', video_file.filename)
        os.makedirs('temp', exist_ok=True)
        video_file.save(video_path)
        
        # Analyze the video
        analysis_result = chatbot.analyze_video(video_path, message)
        
        # Remove the temporary file
        os.remove(video_path)
        
        return jsonify({'response': analysis_result})
    else:
        # Handle text-only message
        response = chatbot.send_message(message)
        return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)