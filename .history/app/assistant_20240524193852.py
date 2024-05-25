import os
import logging
import pyttsx3
import speech_recognition as sr

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
            print("Listening timed out while waiting for phrase to start")
            return None
        except sr.UnknownValueError:
            print("Listening could not understand audio")
            return None

    try:
        response = recognizer.recognize_google(audio)
        print(f"User said: {response}")
        return response.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def ask_question(question, required=True, is_last_question=False):
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
                return response.lower()
            elif response == "stop":
                interaction_end_message = "Interaction ended by user."
                logging.info(interaction_end_message)
                print(interaction_end_message)
                speak(interaction_end_message)
                return "stop"
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
    return "invalid"

def main():
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
        is_last_question = index == len(questions)
        response = ask_question(question, required, is_last_question)
        if response == "stop":
            interaction_end_message = "Interaction ended by user."
            logging.info(interaction_end_message)
            print(interaction_end_message)
            speak(interaction_end_message)
            break
        elif response == "skip":
            skipped_question_message = "Question skipped by user."
            logging.info(skipped_question_message)
            print(skipped_question_message)
            speak(skipped_question_message)
            continue

    if response != "stop":
        farewell_message = "Thank you for your responses. Have a great day!"
        logging.info(farewell_message)
        print(farewell_message)
        speak(farewell_message)

if __name__ == "__main__":
    main()
