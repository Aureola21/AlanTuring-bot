# AlanTuring-bot

## 📄 Project Overview
**AlanTuring-bot** is an AI-powered conversational agent designed to emulate the thought process, personality, and knowledge of Alan Turing.  
Engage in meaningful discussions on computer science, artificial intelligence, cryptography, and the groundbreaking work of Alan Turing through an interactive voice interface and graphical UI.

---

## 🚀 Features
- **Wake Word Activation**: Say **"Hello There"** to start a conversation.
- **Voice Interaction**: Full duplex communication with speech recognition and text-to-speech (TTS).
- **Alan Turing Persona**: Responses mimic Turing’s style, precision, and historical context.
- **Responsive UI**: Smooth, non-blocking interface updates via threading during speech processing.
- **Exit Commands**: Ends conversation gracefully when you say "goodbye", "stop", or "exit".

---

## 🛠 Technology Stack
- Python 3
- Unofficial Bard API for conversational AI
- SpeechRecognition (Google Speech API for voice input)
- pyttsx3 (offline text-to-speech engine)
- Tkinter for GUI
- PyQt5 for design assets
- threading for non-blocking audio processing

---

## ⚙️ How It Works
1. **Initialization:**  
   Loads Bard API with your personal token, initializes the TTS engine and speech recognizer, and opens the GUI chat window with controls.

2. **Wake Word Detection:**  
   Continuously listens for the phrase **"Hello There"** to activate the chatbot.

3. **Conversation Loop:**  
   - Converts user voice input to text via speech recognition.  
   - Sends the prompt to Bard API, enhanced with system instructions to respond as Alan Turing.  
   - Displays and reads out the chatbot’s reply in Alan Turing’s style.

4. **Exit:**  
   Ends the conversation when an exit phrase is detected.

---

## 📂 File Structure
```
/AlanTuring-bot
│
├── main.py                 # Main application script
├── gui.py                  # GUI implementation using Tkinter/PyQt5
├── speech_handler.py       # Voice input/output modules
├── bard_api_wrapper.py     # Unofficial Bard API integration
├── assets/                 # UI design assets and icons
├── README.md               # This documentation
└── requirements.txt        # Project dependencies
```

---

## ▶️ Installation & Usage

1. Clone the repository:
```bash
git clone https://github.com/Aureola21/AlanTuring-bot.git
cd AlanTuring-bot
```

2. Install dependencies:
```bash
pip install speechrecognition pyttsx3 bardapi PyQt5
```

3. Add your Bard API token in the appropriate config or environment variable.

4. Run the chatbot:
```bash
python main.py
```

5. Say **"Hello There"** to activate the chatbot and start chatting with Alan Turing’s persona.

---

## 🙋‍♂️ Contribution
Feel free to fork, raise issues, and submit pull requests!

---

## ⚠️ Disclaimer
This project uses an unofficial Bard API and third-party speech recognition libraries; ensure you comply with their terms of service.
