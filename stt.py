import requests, json, time, os, threading
from apikey import api_key
import speech_recognition as s
from gtts import gTTS
import pygame
import tkinter as tk

# --- Initialize recognizer ---
sr = s.Recognizer()

# --- Languages supported ---
languages = {
    "English": ("en-IN", "en"),
    "Hindi": ("hi-IN", "hi"),
    "Telugu": ("te-IN", "te"),
    "Tamil": ("ta-IN", "ta"),
    "Kannada": ("kn-IN", "kn")
}

# --- Initialize Pygame once ---
pygame.mixer.init()

# --- Global flag to prevent overlapping chats ---
chat_in_progress = False
chat_lock = threading.Lock()

# --- Thread-safe GUI updater ---
def update_message_label_safe(text, color="black"):
    window.after(0, lambda: message_label.config(text=text, fg=color))

# --- Thread-safe Speak Function ---
def speak(text, lang):
    try:
        tts = gTTS(text=text, lang=lang)
        filename = "reply.mp3"
        tts.save(filename)
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.music.unload()
        os.remove(filename)
    except Exception as e:
        print("⚠️ TTS Error:", str(e))

# --- Backend chat logic ---
def start_chat(selected_language):
    lang_code, tts_lang = languages[selected_language]
    update_message_label_safe(f"🎙️ Listening in {selected_language}...", "green")
    print(f"\n🎙️ Selected: {selected_language}")

    try:
        with s.Microphone() as mic:
            sr.adjust_for_ambient_noise(mic, duration=2)
            try:
                audio = sr.listen(mic, timeout=10, phrase_time_limit=12)
                text = sr.recognize_google(audio, language=lang_code)
                print(f"🗣️ You said ({selected_language}): {text}")
            except s.WaitTimeoutError:
                update_message_label_safe("No speech detected. Try again.", "red")
                return
            except s.UnknownValueError:
                update_message_label_safe("Could not understand speech.", "red")
                return
            except s.RequestError as e:
                update_message_label_safe(f"Speech recognition error: {e}", "red")
                return

        if text.strip().lower() in ["exit", "quit", "stop"]:
            update_message_label_safe("Conversation ended.", "blue")
            return

        # Send message to Groq API
        headers = {"Authorization": f"Bearer {api_key}"}
        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "You are a friendly multilingual AI assistant named ALEX. Respond in the same language as the user. Keep replies short and clear."},
                {"role": "user", "content": text}
            ]
        }

        try:
            res = requests.post("https://api.groq.com/openai/v1/chat/completions",
                                headers=headers, json=data, timeout=25)
            res_json = res.json()
            if res.status_code == 200 and "choices" in res_json:
                reply = res_json["choices"][0]["message"]["content"]
                print(f"🤖 ALEX: {reply}")
                update_message_label_safe(f"ALEX: {reply}", "blue")
                speak(reply, tts_lang)
            else:
                update_message_label_safe("API Error occurred.", "red")
        except requests.exceptions.Timeout:
            update_message_label_safe("Request timed out. Try again.", "red")
        except requests.exceptions.ConnectionError:
            update_message_label_safe("Connection error. Check your internet.", "red")

    except Exception as e:
        update_message_label_safe(f"Error: {str(e)}", "red")

# --- Thread-safe wrapper to prevent overlapping chats ---
def threaded_start_chat(selected_language):
    global chat_in_progress
    with chat_lock:
        if chat_in_progress:
            update_message_label_safe("⚠️ Chat already in progress. Please wait...", "orange")
            return
        chat_in_progress = True
    try:
        start_chat(selected_language)
    finally:
        chat_in_progress = False

# --- GUI Setup ---
window = tk.Tk()
window.title("🎙️ Multilingual Voice Chatbot - ALEX")
window.geometry("420x400")
window.config(bg="#e8f0fe")

title = tk.Label(window, text="ALEX - Multilingual Voice Chatbot", font=("Arial", 14, "bold"), bg="#e8f0fe", fg="#1a73e8")
title.pack(pady=15)

subtitle = tk.Label(window, text="Choose a language to start speaking", font=("Arial", 11), bg="#e8f0fe")
subtitle.pack(pady=5)

frame = tk.Frame(window, bg="#e8f0fe")
frame.pack(pady=15)

# --- Language Buttons ---
for lang in languages.keys():
    btn = tk.Button(frame, text=lang, width=20, font=("Arial", 11, "bold"),
                    bg="#1a73e8", fg="white", activebackground="#0b57d0",
                    relief="raised", bd=3,
                    command=lambda l=lang: threading.Thread(target=threaded_start_chat, args=(l,), daemon=True).start())
    btn.pack(pady=5)

message_label = tk.Label(window, text="Click a language button to start speaking.", bg="#e8f0fe", fg="black", font=("Arial", 10))
message_label.pack(pady=20)

exit_button = tk.Button(window, text="Exit", command=window.destroy, bg="red", fg="white", font=("Arial", 11, "bold"), width=10)
exit_button.pack(pady=10)

window.mainloop()
