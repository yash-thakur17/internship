import speech_recognition as sr
import pyttsx3
import requests
import datetime
import time


OPENWEATHER_API_KEY = "0cc3d7a4b7b3d7be241e63df12c9f9ba"
NEWS_API_KEY = "0d16b03598ee4463824c6c1b9dc5acf5"


engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()
    time.sleep(1.2)

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        print("Recognized:", command)
        return command.lower().strip()
    except:
        return ""

def wait_for_wake_word():
    speak("Jarvis is sleeping. Say hey jarvis to wake me up.")
    while True:
        command = take_command()
        if "hey jarvis" in command:
            speak("I am awake. Hello!")
            return

def get_weather(city):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    print("Weather API response:", data) 

    if str(data.get("cod")) != "200":
        speak("I could not find the city. Please try again.")
        return

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    speak(f"The temperature in {city} is {temp} degrees Celsius with {desc}")


def read_news():
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    data = requests.get(url).json()

    if data.get("status") != "ok":
        speak("Unable to fetch news right now.")
        return

    speak("Here are the top news headlines.")
    for article in data["articles"][:5]:
        speak(article["title"])

def set_reminder(reminder_time):
    speak(f"Reminder set for {reminder_time}")
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        if now == reminder_time:
            speak("This is your reminder.")
            break
        time.sleep(20)

def tell_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {now}")

def tell_date():
    today = datetime.datetime.now().strftime("%B %d, %Y")
    speak(f"Today's date is {today}")

def assistant_mode():
    speak("Say time, date, weather, news, reminder, sleep, or exit.")

    while True:
        command = take_command()
        if not command:
            continue

        if "hello" in command or "wake up" in command:
            speak("Hello! How can I help you?")

        elif "time" in command:
            tell_time()

        elif "date" in command:
            tell_date()

        elif "weather" in command:
            speak("Tell me the city name")
            city = take_command()
            if city:
                get_weather(city)

        elif "news" in command:
            read_news()

        elif "reminder" in command:
            speak("Tell me the time in HH colon MM format")
            reminder_time = take_command()
            set_reminder(reminder_time)

        elif "sleep" in command:
            speak("Going back to sleep.")
            return

        elif "exit" in command or "stop" in command:
            speak("Goodbye!")
            exit()

        else:
            speak("Please repeat your command.")


while True:
    wait_for_wake_word()   
    assistant_mode()       
