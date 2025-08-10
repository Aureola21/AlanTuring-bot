import speech_recognition as sr
import pyttsx3
from bardapi import Bard

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set your Bard API key (from Step 2)
bard_api_key = "g.a000tQiiZOK7HihD_plVR6uYCOMB9Yq7xnzeKxikAPPxfOsq-2gzAVQJ4SQQymGfehgLJGbyDAACgYKAY8SARASFQHGX2Mi7XjeHgYjm4MQA-EAfbLVaBoVAUF8yKraExzS2VZP_WdzbRJavvKz0076"  # Replace with your Bard API key
bard = Bard(token=bard_api_key)

# Define the wake word
WAKE_WORD = "hello there"

# List of phrases to end the conversation
EXIT_PHRASES = ["goodbye", "exit", "stop", "bye", "end conversation"]

def listen_to_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio).lower()  # Convert to lowercase
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            print("Sorry, there was an issue with the speech recognition service.")
            return None
        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")
            return None

def generate_response(prompt):
    try:
        # Define the system prompt
        system_prompt = (
            "You are Alan Turing, the brilliant mathematician, logician, and pioneer of computer science. "
            "Your responses should reflect your logical thinking, curiosity, and formal writing style. "
            "You are known for your work on the Turing Machine, the Enigma code-breaking, and the concept of artificial intelligence. "
            "Respond to questions as if you are Alan Turing, using precise and thoughtful language. "
            "Please keep your responses very brief and to the point. "
            "You are having a conversation with a curious student who is interested in your work."
        )

        # Combine the system prompt with the user's input
        full_prompt = f"{system_prompt}\n\nUser: {prompt}\nAlan Turing:"

        # Get a response from Google Bard
        response = bard.get_answer(full_prompt)['content']
        print(f"Bard Response: {response}")  # Debugging: Print Bard's response
        return response
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I encountered an error while generating a response."

def speak(text):
    engine.say(text)
    engine.runAndWait()

def main():
    print("Say 'Hello There' to start talking to me.")

    while True:
        user_input = listen_to_voice()
        if user_input:
            # Check if the wake word is detected
            if WAKE_WORD in user_input:
                print("Bot: Hello! I am Alan Turing. How can I assist you?")
                speak("Hello! I am Alan Turing. How can I assist you?")

                # Start conversation loop
                while True:
                    user_input = listen_to_voice()
                    if user_input:
                        # Check if the user wants to end the conversation
                        if any(phrase in user_input for phrase in EXIT_PHRASES):
                            print("Bot: Goodbye! It was a pleasure speaking with you.")
                            speak("Goodbye! It was a pleasure speaking with you.")
                            return  # End the program

                        # Generate and speak the response
                        response = generate_response(user_input)
                        print(f"Bot: {response}")
                        speak(response)
            else:
                print("Bot: I'm waiting for the wake word. Say 'Hello There' to start.")
                speak("I'm waiting for the wake word. Say 'Hello There' to start.")

if __name__ == "__main__":
    main()