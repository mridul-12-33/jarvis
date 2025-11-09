import speech_recognition as sr
import pyttsx3
import time
import webbrowser
from datetime import datetime

# Initialize speech engine once
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processcommand(command):
    command = command.lower().strip()
    if command.startswith("play "):
        query = command.replace("play", "").strip()
        if query:
            speak(f"Playing {query} on YouTube")
            webbrowser.open(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
        else:
            speak("Please tell me what to play.")

    elif command.startswith("search "):
        query = command.replace("search", "").strip()
        if query:
            speak(f"Searching Google for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        else:
            speak("Please tell me what to search for.")

    elif "youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")

    elif "instagram" in command:
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")

    elif "linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com")

    elif "time" in command:
        speak(f"The time is {datetime.now().strftime('%H:%M')}")

    else:
        speak(f"Searching the web for {command}")
        webbrowser.open(f"https://www.google.com/search?q={command.replace(' ', '+')}")

if __name__ == "__main__":
    speak("Initializing Optimus...")
    r = sr.Recognizer()
    active = False

    while True:
        try:
            with sr.Microphone() as source:
                if not active:
                    print("🎤 Listening for wake word...")
                else:
                    print("🎧 Listening for commands...")

                audio = r.listen(source, timeout=5, phrase_time_limit=5)

            try:
                text = r.recognize_google(audio)
                print("Heard:", text)
            except sr.UnknownValueError:
                print("Didn't catch that.")
                continue
            except sr.RequestError:
                speak("Network error. Check your connection.")
                continue

            if not active:
                if "optimus" in text.lower():
                    speak("Yes?")
                    active = True
            else:
                commands = [c.strip() for c in text.lower().replace("then", ",").replace("and", ",").split(",") if c.strip()]
                for cmd in commands:
                    processcommand(cmd)
                    time.sleep(0.3)
                active = False

        except sr.WaitTimeoutError:
            continue
        except Exception as e:
            print("Error:", e)
            continue
