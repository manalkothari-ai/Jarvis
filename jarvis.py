import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI client
client = OpenAI(api_key=API_KEY)

# Initialize voice engine
engine = pyttsx3.init()
engine.setProperty('rate', 175)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice (0 = male)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wish_me():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning")
    elif hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    speak("I am Jarvis with ChatGPT brain. How can I help you?")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("🧠 Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print("You said:", query)
    except:
        speak("Sorry, I didn't understand. Please say again.")
        return "none"
    return query.lower()

# ✅ ChatGPT Brain Function
def chatgpt_reply(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Jarvis, a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return "Sorry, I could not connect to ChatGPT right now."

# ---------------- MAIN PROGRAM ---------------- #
wish_me()

while True:
    query = take_command()

    if query == "none":
        continue

    # ✅ Basic Commands
    if "time" in query:
        time_now = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {time_now}")

    elif "date" in query:
        date_today = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"Today's date is {date_today}")

    elif "open google" in query:
        webbrowser.open("https://www.google.com")
        speak("Opening Google")

    elif "open youtube" in query:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")

    elif "open gmail" in query:
        webbrowser.open("https://mail.google.com")
        speak("Opening Gmail")

    elif "wikipedia" in query:
        speak("Searching Wikipedia...")
        try:
            search = query.replace("wikipedia", "")
            result = wikipedia.summary(search, sentences=2)
            speak(result)
        except:
            speak("No Wikipedia results found")

    elif "play music" in query:
        music_dir = "C:\\Music"  # ✅ CHANGE THIS PATH
        try:
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))
            speak("Playing music")
        except:
            speak("Music folder not found")

    elif "exit" in query or "stop" in query or "shutdown" in query:
        speak("Goodbye. Shutting down Jarvis.")
        sys.exit()

    # ✅ ChatGPT Fallback Brain
    else:
        speak("Let me think...")
        answer = chatgpt_reply(query)
        print("Jarvis:", answer)
        speak(answer)
