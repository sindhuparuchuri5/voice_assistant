import os
import logging
import pyttsx3
import speech_recognition as sr
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

# Initialize Flask app and SocketIO
app = Flask(__nam_e_)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Set the log file path within the container
log_file = "/voice_assistant/logs/interaction.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    tts_engine.say(text)
    tts_engine.runAndWait()

def get_speech_input():
    """Capture and recognize speech input."""
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        try:
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            print("Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)  # Adjust timeout and phrase time limit
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
    """Render the main interface page."""
    return render_template('index.html')

@socketio.on('ask_question')
def handle_question(data):
    """Handle question asking via SocketIO."""
    question = data['question']
    required = data['required']
    logging.info(f"Question: {question}")
    speak(question)
    response = None
    while True:
        response = get_speech_input()
        if response in ["yes", "no", "stop"]:
            break
        elif not required and response == "skip":
            break
    logging.info(f"Response: {response}")
    emit('response', {'response': response})

def ask_question(question, required=True):
    """Ask a question and get the response."""
    logging.info(f"Question: {question}")
    speak(question)

    response = None
    attempts = 0
    max_attempts = 3
    valid_responses = ["yes", "no", "stop", "skip"] if not required else ["yes", "no", "stop"]

    while attempts < max_attempts:
        response = get_speech_input()
        if response:
            if response in valid_responses:
                logging.info(f"Valid response: {response}")
                return response
            elif response == "stop":
                interaction_end_message = "Interaction ended by user."
                logging.info(interaction_end_message)
                speak(interaction_end_message)
                return "stop"
            else:
                logging.info(f"Invalid response: {response}")
                speak("Invalid response.")
        else:
            if attempts == 0:
                logging.info("No response detected")
                speak("I didn't hear your response.")

        attempts += 1

    logging.info("Too many attempts.")
    speak("Too many attempts.")
    return "invalid"

def main():
    """Main function to run the assistant."""
    greet_message = "Hello! I'm going to ask you a few questions. Please provide your answers."
    logging.info(greet_message)
    speak(greet_message)

    questions = [
        ("Is technology making humanity better?", True),
        ("Do you think artificial intelligence is dangerous?", True),
        ("Should self-driving cars be allowed on the roads?", False),
        ("Is social media having a positive impact on society?", False),
        ("Do you believe in climate change?", True)
    ]

    for index, (question, required) in enumerate(questions, start=1):
        response = ask_question(question, required)
        if response == "stop":
            break
        elif response == "skip":
            continue

    farewell_message = "Thank you for your responses. Have a great day!"
    logging.info(farewell_message)
    speak(farewell_message)

if __name__ == "__main__":
    main()
