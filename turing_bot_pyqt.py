import sys
import threading
import speech_recognition as sr
import pyttsx3
from bardapi import Bard
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget, QLabel, QScrollArea, QHBoxLayout
)
from PyQt5.QtCore import Qt, QTimer, QMetaObject, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFont

class BardUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alan Turing Chatbot")
        self.setGeometry(100, 100, 800, 600)

        self.bard_api_key = "your_bard_api_key_here"  # Replace with your Bard API key
        self.bard = Bard(token=self.bard_api_key)
        self.engine = pyttsx3.init()

        self.WAKE_WORD = "hello there"
        self.EXIT_PHRASES = ["goodbye", "exit", "stop", "bye", "end conversation"]
        self.conversation_active = False

        self.init_ui()
        self.load_stylesheet()

    def init_ui(self):
        main_layout = QVBoxLayout()

        image_layout = QHBoxLayout()
        self.image_label = QLabel(self)
        pixmap = QPixmap("turing_image.png")  # Replace with your image path
        pixmap = pixmap.scaled(1200, 600, Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(self.image_label)
        main_layout.addLayout(image_layout)

        horizontal_layout = QHBoxLayout()

        self.conversation_display = QTextEdit(self)
        self.conversation_display.setReadOnly(True)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.conversation_display)
        horizontal_layout.addWidget(scroll_area, 1)

        self.instructions_text = QTextEdit(self)
        self.instructions_text.setReadOnly(True)
        self.instructions_text.setHtml("""
            <b>Instructions:</b><br><br>
            - Say '<b>Hello There</b>' to start.<br>
            - Use exit phrases to end the conversation.<br>
            - Type or speak your questions.
        """)
        self.instructions_text.setObjectName("instructionsText")

        #or if you are using a label
        #self.instructions_label.setFont(font)
        #self.instructions_label.setObjectName("instructionsLabel")

        horizontal_layout.addWidget(self.instructions_text, 1)

        main_layout.addLayout(horizontal_layout)

        self.status_label = QLabel("Say 'Hello There' to start...", self)
        main_layout.addWidget(self.status_label)

        input_layout = QHBoxLayout()
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Type your message here...")
        input_layout.addWidget(self.input_field)
        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        main_layout.addLayout(input_layout)

        self.listen_button = QPushButton("Start Listening", self)
        self.listen_button.clicked.connect(self.start_listening_thread)
        main_layout.addWidget(self.listen_button)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def load_stylesheet(self):
        try:
            with open("style.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Stylesheet not found.")

    def start_listening_thread(self):
        self.listen_button.setEnabled(False)
        self.status_label.setText("Listening for wake word...")
        threading.Thread(target=self.listen_for_wake_word, daemon=True).start()

    def listen_for_wake_word(self):
        while not self.conversation_active:
            user_input = self.listen_to_voice()
            if user_input and self.WAKE_WORD in user_input:
                self.conversation_active = True
                self.display_message("Bot", "Hello! I am Alan Turing. How can I assist you?")
                self.speak_response("Hello! I am Alan Turing. How can I assist you?")
                self.status_label.setText("Conversation active. Listening for your questions...")
                QTimer.singleShot(0, self.start_conversation_loop)
                break

    def start_conversation_loop(self):
        threading.Thread(target=self._conversation_loop, daemon=True).start()

    def _conversation_loop(self):
        while self.conversation_active:
            user_input = self.listen_to_voice()
            if user_input:
                if any(phrase in user_input for phrase in self.EXIT_PHRASES):
                    self.conversation_active = False
                    self.display_message("Bot", "Goodbye! It was a pleasure speaking with you.")
                    self.speak_response("Goodbye! It was a pleasure speaking with you.")
                    self.status_label.setText("Say 'Hello There' to start...")
                    QMetaObject.invokeMethod(self, "reset_and_enable_button", Qt.QueuedConnection)
                    return

                response = self.generate_response(user_input)
                self.display_message("Bot", response)
                self.speak_response(response)

    @pyqtSlot()
    def reset_and_enable_button(self):
        self.conversation_display.clear()
        self.status_label.setText("Say 'Hello There' to start...")
        self.listen_button.setEnabled(True)

    def listen_to_voice(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio).lower()
                print(f"You said: {text}")
                self.display_message("You", text)
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
                print("Listening timed out.")
                return None

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
            print(f"Bard Response: {response}")
            return response
        except Exception as e:
            error_message = f"Error generating response: {e}"
            print(error_message)
            self.display_message("Bot Status", error_message)
            self.speak_response("Sorry, I encountered an error while generating a response.")
            return "Sorry, I encountered an error while generating a response."

    def speak_response(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def display_message(self, sender, message):
        formatted_message = f"{sender}: {message}\n"
        self.conversation_display.append(formatted_message)

    def send_message(self):
        user_input = self.input_field.text()
        if user_input.strip():
            self.display_message("You", user_input)
            response = self.generate_response(user_input)
            self.display_message("Bot", response)
            self.speak_response(response)
            self.input_field.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BardUI()
    window.show()
    sys.exit(app.exec_())