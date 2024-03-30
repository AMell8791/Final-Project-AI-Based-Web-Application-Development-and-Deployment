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

# Full code:

# Imports the requests module to allow Python script send http request.
# Imports json module to allow functions for coding and decoding json data.
import requests
import json

# Function analyzes text for emotions
def emotion_detector(text_to_analyse):
    URL = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = { "raw_document": { "text": text_to_analyse } }

    # Sends text for emotion analys and receives a response.
    response = requests.post(URL, headers=header, json = input_json)  
    output_response = response.text
    
    return output_response 
       
# Function takes response text from the emotion detection service by URL)
def emotion_predictor(output_response):
    
    # Formatting text into a Python dictionary using json function. 
    json_emotion = json.loads(output_response)
    emotions = json_emotion['emotionPredictions'][0]['emotion']

    # Extracting individual emotion scores
    anger_score = emotions.get('anger', 0)
    disgust_score = emotions.get('disgust', 0)
    fear_score = emotions.get('fear', 0)
    joy_score = emotions.get('joy', 0)
    sadness_score = emotions.get('sadness', 0)

    # Finding key in the emotions dictionary with maximum value, which emotion is domenanting.
    dominant_emotion = max(emotions, key=emotions.get)
    emotions["dominant_emotion"] = dominant_emotion
    # Constructing the output dictionary
    output = {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score,
            'dominant_emotion': dominant_emotion
            }

    return output
    
# Test the function with the provided text
input_json = emotion_detector("I love my life")
print(emotion_detector(input_json))

