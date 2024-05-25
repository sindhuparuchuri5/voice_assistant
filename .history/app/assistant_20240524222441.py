import os
import logging
import pyttsx3
import speech_recognition as sr
from flask import Flask, render_template, jsonify

# Set the log file path within the container
log_file = "/voice_assistant/logs/interaction.log"

# Configure logging to the log file
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

# Initialize text-to-speech engine once
tts_engine = pyttsx3.init()

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/question', methods=['POST'])
def ask_question():
    data = request.json
    question = data['question']
    required = data.get('required', True)
    is_last_question = data.get('is_last_question', False)

    logging.info(f"Question: {question}")
    speak(question)
    print(question)

    attempts = 0
    max_attempts = 3
    valid_responses = ["yes", "no", "stop", "skip"] if not required else ["yes", "no", "stop"]
    response = None

    while attempts < max_attempts:
        response = get_speech_input("Please answer 'Yes', 'No', 'Stop', or 'Skip':" if not required else "Please answer 'Yes', 'No', or 'Stop':")
        if response:
            if response in valid_responses:
                logging.info(f"Valid response: {response.capitalize()}")
                print(f"Logged valid response: {response.capitalize()}")
                return jsonify({'response': response.lower()})
            elif response == "stop":
                interaction_end_message = "Interaction ended by user."
                logging.info(interaction_end_message)
                print(interaction_end_message)
                speak(interaction_end_message)
                return jsonify({'response': 'stop'})
            else:
                logging.info(f"Invalid response: {response.capitalize()}")
                print(f"Logged invalid response: {response.capitalize()}")
                speak("Invalid response.")
        else:
            if attempts == 0:
                logging.info("No response detected")
                print("No response detected.")
                speak("I didn't hear your response.")

        attempts += 1

    if is_last_question:
        print("Too many attempts.")
        speak("Too many attempts.")
    else:
        print("Too many attempts. Moving to the next question.")
        speak("Too many attempts. Moving to the next question.")
    return jsonify({'response': 'invalid'})

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
            recognizer.adjust_for_ambient_noise(source)  # Adjust for noise
            print("Listening...")
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)  # Reduced timeout and phrase limit
        except sr.WaitTimeoutError:
            logging.error("Listening timed out while waiting for phrase to start")
            print("Listening timed out while waiting for phrase to start")
            return None
        except sr.UnknownValueError:
            logging.error("Listening could not understand audio")
            print("Listening could not understand audio")
            return None

    try:
        response = recognizer.recognize_google(audio)
        print(f"User said: {response}")
        return response.lower()
    except sr.UnknownValueError:
        logging.error("Sorry, I did not understand that.")
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError as e:
        logging.error(f"Could not request results from Google Speech Recognition service; {e}")
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

if __name__ == "__main__":
    app.run(debug=True)
