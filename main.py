import speech_recognition as sr
import pyttsx3
import time
import webbrowser
import traceback
from datetime import datetime

#pip install pyttsx3 traceback datetime speechrecognition webbrowser

# Make a speak function
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    time.sleep(0.5)


def processcommand(command):
    command = command.lower().strip()

    # play in youtube
    if command.startswith("play "):
        query = command.replace("play", "").strip()
        if query:
            speak(f"Playing {query} on YouTube")
            webbrowser.open(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
        else:
            speak("Please tell me what to play.")

    # search in google
    elif command.startswith("search "):
        query = command.replace("search", "").strip()
        if query:
            speak(f"Searching Google for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        else:
            speak("Please tell me what to search for.")

    #Open YouTube
    elif "youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    #Open Google
    elif "google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    #Open facebook
    elif "facebook" in command:
        speak("Opening facebook")
        webbrowser.open("https://www.facebook.com")
    #Open instagram
    elif "instagram" in command:
        speak("Opening instagram")
        webbrowser.open("https://www.instagram.com")
    #Open linkedin
    elif "linkedin" in command:
        speak("Opening linkedin")
        webbrowser.open("https://www.linkedin.com")

    # Time
    elif "time" in command:
        speak(f"The time is {datetime.now().strftime('%H:%M')}")

    # ai search
    else:
        speak(f"Searching Web for {command}")
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

                # Listen for audio
                audio = r.listen(source, timeout=5, phrase_time_limit=5)

            # Recognize speech
            text = r.recognize_google(audio)
            print("Heard:", text)

            if not active:
                # Wake word detection
                if "optimus" in text.lower():
                    speak("Yes?")
                    active = True
            else:
                # Split multiple commands by "and", "then" or commas
                commands = [
                    c.strip()
                    for c in text.lower().replace("then", ",").replace("and", ",").split(",")
                    if c.strip()
                ]
                for cmd in commands:
                    processcommand(cmd)
                    time.sleep(0.3)  # small delay between commands
                active = False  # go back to wake word

        except sr.UnknownValueError:
            print("Didn't catch that.")
        except sr.WaitTimeoutError:
            print("Listening timed out.")
        except sr.RequestError as e:
            print("Network error:", e)
        except Exception as e:
            print("Error:", e)
            traceback.print_exc()