import os
import logging
import pyttsx3
import speech_recognition as sr
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Set up Flask and SocketIO
app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Set the log file path within the container
log_file = "/voice_assistant/logs/interaction.log"

# Configure logging to the log file
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def get_speech_input(prompt):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print(prompt)
    speak(prompt)

    with microphone as source:
        try:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
        except sr.WaitTimeoutError:
            logging.error("Listening timed out while waiting for phrase to start")
            return None
        except sr.UnknownValueError:
            logging.error("Listening could not understand audio")
            return None

    try:
        response = recognizer.recognize_google(audio)
        print(f"User said: {response}")
        return response.lower()
    except sr.UnknownValueError:
        logging.error("Sorry, I did not understand that.")
        return None
    except sr.RequestError as e:
        logging.error(f"Could not request results from Google Speech Recognition service; {e}")
        return None

@app.route('/')
def index():
    return app.send_static_file('index.html')

@socketio.on('ask_question')
def handle_ask_question(json):
    question = json.get('question')
    required = json.get('required', True)
    logging.info(f"Question: {question}")
    speak(question)
    print(question)

    response = get_speech_input(question)
    emit('response', {'response': response if response else 'No response detected'})

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)
