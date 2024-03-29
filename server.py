# Task 6. Web deployment of the application using Flask

from flask import Flask, request, jsonify
from final_project.emotion_detection import emotion_detector, emotion_predictor

app = Flask(__name__)

@app.route('/emotionDetector', methods=['POST'])
def emotionDetector():
    # Extract text from request data
    text_to_analyze = request.json.get('text')

    # Analyze emotions
    result = emotion_detector(text_to_analyze)
    emotions = emotion_predictor(result)

    # Format response as requested
    response_text = f"For the given statement, the system response is "
    for emotion, score in emotions.items():
        response_text += f"'{emotion}': {score}, "
    response_text += f"and the dominant emotion is {emotions['dominant_emotion']}."
    
    return jsonify(response_text)

if __name__ == '__main__':
    app.run(debug=True)
