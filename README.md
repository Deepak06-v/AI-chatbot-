# 🎙️ ALEX - Multilingual Voice Chatbot

ALEX is a **voice-enabled, multilingual AI chatbot** built using Python. It leverages the **Groq LLaMA-3.1 API** to provide conversational responses in multiple languages and includes **text-to-speech** so the bot can speak its replies.  

The chatbot supports **English, Hindi, Telugu, Tamil, and Kannada**, and features a **friendly, short, and clear response style** by default (customizable).

---

## Features

- **Multilingual Speech Recognition:** Speak in English, Hindi, Telugu, Tamil, or Kannada.  
- **Voice Responses:** Text-to-speech replies using `gTTS` and `pygame`.  
- **Customizable Personality:** Adjust the `system` message to change the bot’s behavior or tone.  
- **Thread-Safe GUI:** Prevents overlapping chats and ensures smooth user interaction.  
- **Simple GUI:** Built with Tkinter for easy use and interaction.

---

## Demo Screenshot

*(Add a screenshot here of the Tkinter GUI with language buttons and response display.)*

---

## Requirements

- Python 3.8+
- `requests`
- `speech_recognition`
- `gtts`
- `pygame`
- `tkinter` (usually included with Python)
- A valid Groq API key

Install Python dependencies:

```bash
pip install requests speechrecognition gtts pygame
