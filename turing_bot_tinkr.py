import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import speech_recognition as sr
import pyttsx3
from bardapi import Bard
import os  # Import os for environment variables if needed

class BardUI:
    def __init__(self, master):
        self.master = master
        master.title("Alan Turing Chatbot")

        # Initialize Bard API and TTS engine
        self.bard_api_key = "g.a000tQiiZOK7HihD_plVR6uYCOMB9Yq7xnzeKxikAPPxfOsq-2gzAVQJ4SQQymGfehgLJGbyDAACgYKAY8SARASFQHGX2Mi7XjeHgYjm4MQA-EAfbLVaBoVAUF8yKraExzS2VZP_WdzbRJavvKz0076" # Replace with your Bard API key or use os.environ.get("BARD_API_KEY") for security
        self.bard = Bard(token=self.bard_api_key)
        self.engine = pyttsx3.init()

        # Wake word and exit phrases
        self.WAKE_WORD = "hello there"
        self.EXIT_PHRASES = ["goodbye", "exit", "stop", "bye", "end conversation"]
        self.conversation_active = False # Flag to track if conversation is active

        # UI elements
        self.conversation_display = scrolledtext.ScrolledText(master, height=20, width=70, state=tk.DISABLED)
        self.conversation_display.pack(pady=10, padx=10)

        self.status_label = ttk.Label(master, text="Say 'Hello There' to start...")
        self.status_label.pack()

        self.listen_button = ttk.Button(master, text="Start Listening", command=self.start_listening_thread)
        self.listen_button.pack(pady=10)

    def start_listening_thread(self):
        threading.Thread(target=self.listen_for_wake_word).start()
        self.status_label.config(text="Listening for wake word...")
        self.listen_button.config(state=tk.DISABLED) # Disable button while listening

    def listen_for_wake_word(self):
        while not self.conversation_active:
            user_input = self.listen_to_voice()
            if user_input:
                if self.WAKE_WORD in user_input:
                    self.conversation_active = True
                    self.display_message("Bot", "Hello! I am Alan Turing. How can I assist you?")
                    self.speak_response("Hello! I am Alan Turing. How can I assist you?")
                    self.status_label.config(text="Conversation active. Listening for your questions...")
                    self.master.after(0, self.start_conversation_loop) # Start conversation loop in main thread
                    return # Exit wake word listening loop

    def start_conversation_loop(self):
        threading.Thread(target=self._conversation_loop).start()

    def _conversation_loop(self):
        while self.conversation_active:
            user_input = self.listen_to_voice()
            if user_input:
                if any(phrase in user_input for phrase in self.EXIT_PHRASES):
                    self.conversation_active = False
                    self.display_message("Bot", "Goodbye! It was a pleasure speaking with you.")
                    self.speak_response("Goodbye! It was a pleasure speaking with you.")
                    self.status_label.config(text="Say 'Hello There' to start...")
                    self.master.after(0, lambda: self.listen_button.config(state=tk.NORMAL)) # Enable button again
                    return

                response = self.generate_response(user_input)
                self.display_message("Bot", response)
                self.speak_response(response)

    def listen_to_voice(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...") # Console print for debugging - remove later or conditionally show
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio).lower()
                print(f"You said: {text}") # Console print for debugging
                self.display_message("You", text) # Display user input in UI
                return text
            except sr.UnknownValueError:
                self.display_message("Bot Status", "Sorry, I could not understand the audio.")
                self.speak_response("Sorry, I could not understand the audio.")
                return None
            except sr.RequestError:
                self.display_message("Bot Status", "Sorry, speech recognition service is unavailable.")
                self.speak_response("Sorry, speech recognition service is unavailable.")
                return None
            except sr.WaitTimeoutError:
                print("Listening timed out.") # Console print for debugging
                return None # No need to display timeout in UI, just retry listening

    def generate_response(self, prompt):
        try:
            system_prompt = (
                "You are Alan Turing, the brilliant mathematician, logician, and pioneer of computer science. "
                "Your responses should reflect your logical thinking, curiosity, and formal writing style. "
                "You are known for your work on the Turing Machine, the Enigma code-breaking, and the concept of artificial intelligence. "
                "Respond to questions as if you are Alan Turing, using precise and thoughtful language. "
                "Please keep your responses very brief and to the point. "
                "You are having a conversation with a curious student who is interested in your work."
            )
            full_prompt = f"{system_prompt}\n\nUser: {prompt}\nAlan Turing:"
            response = self.bard.get_answer(full_prompt)['content']
            print(f"Bard Response: {response}") # Console print for debugging
            return response
        except Exception as e:
            error_message = f"Error generating response: {e}"
            print(error_message) # Console print for debugging
            self.display_message("Bot Status", error_message)
            self.speak_response("Sorry, I encountered an error while generating a response.")
            return "Sorry, I encountered an error while generating a response."

    def speak_response(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def display_message(self, sender, message):
        formatted_message = f"{sender}: {message}\n"
        self.conversation_display.config(state=tk.NORMAL) # Enable editing to insert text
        self.conversation_display.insert(tk.END, formatted_message)
        self.conversation_display.config(state=tk.DISABLED) # Disable editing again
        self.conversation_display.see(tk.END) # Scroll to the end


if __name__ == "__main__":
    root = tk.Tk()
    app = BardUI(root)
    root.mainloop()