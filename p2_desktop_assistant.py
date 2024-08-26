import wikipedia
import webbrowser
import speech_recognition as sr
import pyttsx3
import os
import subprocess
from datetime import datetime

# state of cmd = true or false
cmd_in_prog = False

# user guide and initiation
def main():
    user_guide = """
           ===================. USER GUIDE .===================
        1) To get quick meaning or info about a famous person, say: 'search Albert Einstein'.
        2) To launch an app, say something like: 'launch Notepad'.
        3) To get current time, say: 'what is the current time'.
        4) To launch website say: 'opem google website'"""
    print(user_guide)
    
    while True:
        global cmd_in_prog
        if not cmd_in_prog:
            cmd = recognize_speech()
            if cmd:
                proc_cmd(cmd)


# speack txt
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# Function to recognize speech using microphone
def recognize_speech():
    recognizer_machine = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer_machine.listen(source)
    try:
        cmd = recognizer_machine.recognize_google(audio)
        print(f"You said: {cmd}")
        return cmd.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        print("Request failed; please check your internet connection.")
        return None


# proc user cmd
def proc_cmd(cmd):
    global cmd_in_prog
    if 'time' in cmd:
        cmd_in_prog = True
        tell_time()
        cmd_in_prog = False
    elif 'open' in cmd and 'website' in cmd:
        cmd_in_prog = True
        open_website(cmd)
        cmd_in_prog = False
    elif 'launch' in cmd:
        cmd_in_prog = True
        launch_application(cmd)
        cmd_in_prog = False
    elif 'search' in cmd:
        cmd_in_prog = True
        searchin_wiki(cmd)
        cmd_in_prog = False
    elif 'stop' in cmd:
        speak("Stopping current action.")
        cmd_in_prog = False
    else:
        speak("I'm sorry, I can't perform that action.")
        cmd_in_prog = False

# tell curr time
def tell_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    speak(f"The current time is {current_time}")

# open goog and youtube
def open_website(cmd):
    if 'google' in cmd:
        webbrowser.open('https://www.google.com')
        speak("Launching Google")
    elif 'youtube' in cmd:
        webbrowser.open('https://www.youtube.com')
        speak("Launching YouTube")
    else:
        speak("Sorry, I can't open that website.")

# launch apps
def launch_application(cmd):
    if 'notepad' in cmd:
        os.system('notepad')
        speak("Launching Notepad")
    elif 'calculator' in cmd:
        os.system('calc')
        speak("Launching Calculator")
    elif 'google' in cmd:
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        if os.path.exists(chrome_path):
            subprocess.Popen([chrome_path])
            speak("Launching Google Chrome")
        else:
            speak("Google Chrome not found.")
    else:
        speak("Sorry, I can't launch that application.")

# search in Wikipedia
def searchin_wiki(cmd):
    try:
        query = cmd.replace('search', '').strip()
        result = wikipedia.summary(query, sentences=2)
        speak(f"According to Wikipedia, {result}")
    except wikipedia.exceptions.DisambiguationError as e:
        speak(f"Multiple results found: {e.options}")
    except wikipedia.exceptions.PageError:
        speak("Sorry, I couldn't find any results for the thing use r mentioned.")

if __name__ == "__main__":
    main()
