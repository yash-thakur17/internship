import speech_recognition as sr
import pyttsx3
import requests
import datetime
import time
import webbrowser
import pyautogui
import os
import pywhatkit as kit

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

CONTACTS = {
    "mom": "+917383995350",
    "dad": "+919824407041",
    "pandu": "+917779040777",
}

# =========================
# API KEYS
# =========================
OPENWEATHER_API_KEY = "0cc3d7a4b7b3d7be241e63df12c9f9ba"
NEWS_API_KEY = "0d16b03598ee4463824c6c1b9dc5acf5"

# =========================
# TEXT TO SPEECH
# =========================
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# =========================
# SPEECH TO TEXT
# =========================
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        print("You:", command)
        return command.lower()
    except:
        return ""

# =========================
# WAKE WORD
# =========================
def wait_for_wake_word():
    speak("Jarvis sleeping. Say hello jarvis.")
    while True:
        command = take_command()
        if "hello jarvis" in command:
            speak("I am awake.")
            return

# =========================
# WEATHER
# =========================
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    data = requests.get(url).json()

    if str(data.get("cod")) != "200":
        speak("City not found")
        return

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    speak(f"{city} temperature is {temp} degree Celsius with {desc}")

# =========================
# NEWS
# =========================
def read_news():
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    data = requests.get(url).json()

    if data["status"] != "ok":
        speak("News not available")
        return

    speak("Top headlines")
    for article in data["articles"][:5]:
        speak(article["title"])

# =========================
# TIME & DATE
# =========================
def tell_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"Time is {now}")

def tell_date():
    today = datetime.datetime.now().strftime("%B %d %Y")
    speak(f"Today is {today}")

# =========================
# REMINDER
# =========================
def set_reminder(reminder_time):
    speak(f"Reminder set for {reminder_time}")
    while True:
        if datetime.datetime.now().strftime("%H:%M") == reminder_time:
            speak("Reminder time")
            break
        time.sleep(20)

# =========================
# VOLUME CONTROL
# =========================
def volume_control(level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(level, None)

def volume_up():
    volume_control(0.8)
    speak("Volume up")

def volume_down():
    volume_control(0.3)
    speak("Volume down")

def mute_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMute(1, None)
    speak("Volume muted")

# =========================
# OPEN APPS & WEBSITES
# =========================
def open_youtube():
    speak("Opening YouTube")
    webbrowser.open("https://www.youtube.com")

def open_google():
    speak("Opening Google")
    webbrowser.open("https://www.google.com")

def open_notepad():
    speak("Opening Notepad")
    os.system("notepad")

def open_whatsapp():
    speak("Opening WhatsApp")
    os.startfile("whatsapp:")


# =========================
# SEARCH FUNCTIONS
# =========================
def search_google(query):
    speak(f"Searching Google for {query}")
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)

def search_youtube(query):
    speak(f"Searching YouTube for {query}")
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(url)

def play_youtube_video(query):
    speak(f"Playing {query} on YouTube")
    kit.playonyt(query)

# def send_whatsapp_message(name, message):
#     name = name.lower()

#     if name not in CONTACTS:
#         speak(f"Contact {name} not found")
#         return  
    
#     number = CONTACTS[name]
#     speak(f"Sending WhatsApp message to {name}")
#     kit.sendwhatmsg_instantly(f"+{number}", message, wait_time=10)
#     speak("Message sent")

def handle_whatsapp_command(command):
    command = command.lower()

    if "send message to" not in command or "whatsapp" not in command:
        return
    
    try: 
        message_part = command.split("send message to")[1]
        message_part = message_part.split("whatsapp")[0].strip()

        name_part = command.split("to")[1]
        name = name_part.replace("on whatsapp", "").strip()
        name = name.repalce()

        if name not in CONTACTS:
            speak(f"Contact {name} not found")
            return
        
        number = CONTACTS[name]
        speak(f"What is the message for {name}")
        kit.sendwhatmsg_instantly(f"+{number}", message_part, wait_time=10)
        speak("Message sent")

    except Exception as e:
        speak("Failed to send WhatsApp message")
        print(e)

# =========================
# MOUSE & KEYBOARD
# =========================
def mouse_click():
    pyautogui.click()
    speak("Clicked")

def move_mouse():
    pyautogui.moveRel(100, 0, duration=0.5)
    speak("Mouse moved")

def type_text():
    speak("What should I type")
    text = take_command()
    pyautogui.write(text, interval=0.1)
    speak("Typed")

# =========================
# ASSISTANT MODE
# =========================
def assistant_mode():
    speak("Tell me command")

    while True:
        command = take_command()

        if not command:
            continue

        if "time" in command:
            tell_time()

        elif "date" in command:
            tell_date()

        elif "weather" in command:
            speak("City name")
            city = take_command()
            if city:
                get_weather(city)

        elif "news" in command:
            read_news()

        elif "open youtube" in command or command == "youtube":
            open_youtube()

        elif "open google" in command or command == "google":
            open_google()

        # 🔍 GOOGLE SEARCH
        elif "search google" in command:
            speak("What should I search on Google")
            query = take_command()
            if query:
                search_google(query)

        # 🎥 YOUTUBE SEARCH
        elif "search youtube" in command:
            speak("What should I search on YouTube")
            query = take_command()
            if query:
                search_youtube(query)

        # 🧠 SMART SEARCH (ONE LINE)
        elif "search" in command and "google" in command:
            query = command.replace("search", "").replace("google", "").strip()
            if query:
                search_google(query)

        elif "search" in command and "youtube" in command:
            query = command.replace("search", "").replace("youtube", "").strip()
            if query:
                search_youtube(query)

        elif "notepad" in command:
            open_notepad()

        elif "whatsapp" in command and "send" in command:
            handle_whatsapp_command(command)

        elif "whatsapp" in command:
            open_whatsapp()

        elif "type" in command:
            type_text()

        elif "click" in command:
            mouse_click()

        elif "move mouse" in command:
            move_mouse()

        elif "volume up" in command:
            volume_up()

        elif "volume down" in command:
            volume_down()

        elif "mute" in command:
            mute_volume()

        elif "reminder" in command:
            speak("Tell time HH colon MM")
            reminder_time = take_command()
            if reminder_time:
                set_reminder(reminder_time)

        elif "sleep" in command:
            speak("Going to sleep")
            return

        elif "exit" in command or "stop" in command:
            speak("Goodbye")
            exit()

        else:
            speak("Say again")


# =========================
# MAIN LOOP
# =========================
while True:
    wait_for_wake_word()
    assistant_mode()
