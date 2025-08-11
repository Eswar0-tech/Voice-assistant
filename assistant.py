import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import datetime
import subprocess
import psutil  # For closing applications

# ------------------- Text-to-Speech Init -------------------
tts_engine = pyttsx3.init()

# Set female voice (Windows usually has index 1 as female)
voices = tts_engine.getProperty('voices')
if len(voices) > 1:
    tts_engine.setProperty('voice', voices[1].id)  # Female voice
else:
    tts_engine.setProperty('voice', voices[0].id)  # Default

# Optionally adjust speech rate (default ~200)
tts_engine.setProperty('rate', 180)

ASSISTANT_NAME = "Zoya"

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# ------------------- Listen from Microphone -------------------
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"{ASSISTANT_NAME} is listening...")
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return "Speech service unavailable"

# ------------------- OPEN / OTHER FUNCTIONS -------------------

# Chrome (only open now)
def open_chrome():
    webbrowser.open('http://www.google.com')

# Notepad
def open_notepad():
    os.system('notepad')

def close_notepad():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and "notepad" in proc.info['name'].lower():
            proc.kill()

# Music Folder
def play_music():
    music_path = r"C:\Users\Public\Music"
    os.startfile(music_path)

# Time
def get_time():
    now = datetime.datetime.now()
    return now.strftime("%H:%M:%S")

# YouTube (only open)
def open_youtube():
    webbrowser.open('https://www.youtube.com')

# WhatsApp (only open)
def open_whatsapp():
    webbrowser.open('https://web.whatsapp.com')

# VS Code
def open_vscode():
    subprocess.Popen(["code"])

def close_vscode():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and "code" in proc.info['name'].lower():
            proc.kill()

# File Explorer
def open_folders():
    subprocess.Popen("explorer")

def close_folders():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and "explorer" in proc.info['name'].lower():
            proc.kill()

# Gemini AI (only open)
def open_gemini():
    webbrowser.open('https://gemini.google.com')

# Google Search
def google_search(query):
    search_url = "https://www.google.com/search?q=" + '+'.join(query.split())
    webbrowser.open(search_url)
    speak(f"Searching Google for {query}")

# ------------------- NLP Intent Parsing -------------------
def nlp_parse(text):
    text = text.lower()

    # Google Search
    if text.startswith("search "):
        search_phrase = text[len("search "):].strip()
        return ("google_search", search_phrase)
    elif text.startswith("google "):
        search_phrase = text[len("google "):].strip()
        return ("google_search", search_phrase)

    # Open commands
    if "open chrome" in text: return ("open chrome", None)
    elif "open notepad" in text: return ("open notepad", None)
    elif "play music" in text: return ("play music", None)
    elif "what is the time" in text: return ("time", None)
    elif "open youtube" in text: return ("open youtube", None)
    elif "open whatsapp" in text: return ("open whatsapp", None)
    elif "open vscode" in text or "open vs code" in text: return ("open vscode", None)
    elif "open folders" in text or "open folder" in text: return ("open folders", None)
    elif "open gemini" in text or "open gemini ai" in text: return ("open gemini", None)

    # Close commands
    elif "close notepad" in text: return ("close notepad", None)
    elif "close vscode" in text or "close vs code" in text: return ("close vscode", None)
    elif "close folders" in text or "close folder" in text: return ("close folders", None)

    # Greetings / Exit
    elif "hello" in text or "hi" in text: return ("greet", None)
    elif "exit" in text or "quit" in text: return ("exit", None)
    else: return ("unknown", None)

# ------------------- Execute Task -------------------
def execute_task(intent_tuple):
    intent, param = intent_tuple

    if intent == "greet":
        return f"Hello! I am {ASSISTANT_NAME}, your voice assistant. How can I help you?"

    elif intent == "google_search":
        google_search(param)
        return None

    elif intent == "open chrome": open_chrome(); return "Opening Chrome"
    elif intent == "open notepad": open_notepad(); return "Opening Notepad"
    elif intent == "close notepad": close_notepad(); return "Closing Notepad"
    elif intent == "play music": play_music(); return "Opening Music Folder"
    elif intent == "time": return f"The current time is {get_time()}."
    elif intent == "open youtube": open_youtube(); return "Opening YouTube"
    elif intent == "open whatsapp": open_whatsapp(); return "Opening WhatsApp"
    elif intent == "open vscode": open_vscode(); return "Opening VS Code"
    elif intent == "close vscode": close_vscode(); return "Closing VS Code"
    elif intent == "open folders": open_folders(); return "Opening Folders"
    elif intent == "close folders": close_folders(); return "Closing Folders"
    elif intent == "open gemini": open_gemini(); return "Opening Gemini AI"

    elif intent == "exit":
        return f"Goodbye! {ASSISTANT_NAME} signing off."
    else:
        return "Sorry, I didn't understand that."

# ------------------- Main Loop -------------------
def main():
    speak(f"Hello! I am {ASSISTANT_NAME}. How can I assist you today?")
    print(f"{ASSISTANT_NAME} started. Say 'exit' to stop.")
    while True:
        user_text = listen()
        if not user_text:
            speak("I didn't catch that. Please say again.")
            continue
        print(f"You said: {user_text}")
        intent_tuple = nlp_parse(user_text)
        response = execute_task(intent_tuple)
        if response:
            speak(response)
        if intent_tuple[0] == "exit":
            break

if __name__ == "__main__":
    main()
