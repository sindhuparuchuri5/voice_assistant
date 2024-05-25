import os
import logging
import pyttsx3
import speech_recognition as sr
from flask import Flask, render_template, request

# Initialize Flask app
app = Flask(__name__)

# Set the log file path within the container
log_file = "/voice_assistant/logs/interaction.log"

# Configure logging to the log file
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

# Initialize text-to-speech engine once
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
            recognizer.adjust_for_ambient_noise(source)  # Adjust for noise
            print("Listening...")
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)  # Reduced timeout and phrase limit
        except sr.WaitTimeoutError:
            logging.error("Listening timed out while waiting for phrase to start")
            print("Listening timed out while waiting for phrase to start")
            return None
        except sr.RequestError:
            logging.error("Could not request results from Google Speech Recognition service")
            print("Could not request results from Google Speech Recognition service")
            return None
        except Exception as e:
            logging.error(f"An error occurred while listening: {str(e)}")
            print(f"An error occurred while listening: {str(e)}")
            return None

    try:
        response = recognizer.recognize_google(audio)
        print(f"User said: {response}")
        return response.lower()
    except sr.UnknownValueError:
        logging.error("Sorry, I did not understand that.")
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        logging.error("Could not request results from Google Speech Recognition service")
        print("Could not request results from Google Speech Recognition service")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/voice-assistant', methods=['POST'])
def voice_assistant():
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

    responses = {}

    for index, (question, required) in enumerate(questions, start=1):
        is_last_question = index == len(questions)
        response = ask_question(question, required, is_last_question)
        if response == "stop":
            interaction_end_message = "Interaction ended by user."
            logging.info(interaction_end_message)
            print(interaction_end_message)
            speak(interaction_end_message)
            return render_template('result.html', responses=responses, interaction_end=True)
        elif response == "skip":
            skipped_question_message = "Question skipped by user."
            logging.info(skipped_question_message)
            print(skipped_question_message)
            speak(skipped_question_message)
            responses[question] = "Skipped"
        else:
            responses[question] = response.capitalize()

    farewell_message = "Thank you for your responses. Have a great day!"
    logging.info(farewell_message)
    print(farewell_message)
    speak(farewell_message)

    return render_template('result.html', responses=responses, interaction_end=False)

if __name__ == "__main__":
    app.run(debug=True)
