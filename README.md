# AlanTuring-bot
--
## 📄 Project Overview
The Alan Turing Chatbot is an AI-powered conversational agent designed to emulate the thought process, personality, and knowledge of Alan Turing.
It engages users in meaningful discussions about computer science, artificial intelligence, cryptography, and Turing’s work, with an interactive voice interface and a graphical UI.

--
The project integrates:

- Unofficial Bard API for conversational AI.
- Speech Recognition for voice input.
- Text-to-Speech (TTS) for natural spoken responses.
- PyQt/Tkinter GUI for an interactive chat window.

--
## 🚀 Features
- Wake Word Activation: Conversation starts when the user says "Hello There".
- Voice Interaction: Full duplex communication using speech recognition and TTS.
- Alan Turing Persona: Responses mimic Turing’s style, precision, and historical context.
- Responsive UI: Threaded execution ensures smooth interface updates during speech processing.
- Exit Commands: Conversation ends when phrases like "goodbye", "stop", or "exit" are detected.

--
## 🛠 Technology Stack
- Python 3
- Bard API (unofficial)
- SpeechRecognition
- pyttsx3 (offline TTS)
- tkinter (UI)
- threading (non-blocking audio processing)
- PyQt5 (design assets)

--

#📂 File Structure
--

# ⚙️ How It Works
1. Initialization:
- Loads Bard API with personal token.
- Initializes TTS engine and speech recognizer.
- Displays UI with a conversation window and control buttons.

2. Wake Word Detection:
- Listens continuously for "Hello There" to activate the chatbot.

3. Conversation Loop:
- User speaks; speech is converted to text via Google Speech Recognition.
- Prompt is sent to Bard API, augmented with system instructions to respond as Alan Turing.
- Response is displayed in the chat window and read aloud via TTS.

4. Exit:
- If user says an exit phrase, the chatbot gracefully ends the conversation.

--

## ▶️ Usage
Install dependencies:
'''
pip install speechrecognition pyttsx3 bardapi PyQt5
'''
