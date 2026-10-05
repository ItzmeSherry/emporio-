import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import random
import pywhatkit
import pyjokes


# =========================================================
# SETTINGS
# =========================================================

MUSIC_DIR = r"D:\wyzz"

VSCODE_PATH = (
    r"C:\Users\payal\AppData\Roaming\Microsoft\Windows"
    r"\Start Menu\Programs\Visual Studio Code\Visual Studio Code.lnk"
)




ASSISTANT_NAME = "Emporio"


# =========================================================
# VOICE ENGINE
# =========================================================

engine = pyttsx3.init("sapi5")

voices = engine.getProperty("voices")

if len(voices) > 1:
    engine.setProperty("voice", voices[1].id)
else:
    engine.setProperty("voice", voices[0].id)


def speak(text):
    """Make Emporio speak."""
    print(f"Emporio: {text}")
    engine.say(text)
    engine.runAndWait()


# =========================================================
# GREETING
# =========================================================

def wishme():
    """Give a greeting depending on the current time."""

    hour = datetime.datetime.now().hour

    if hour < 12:
        speak("Good Morning!..")

    elif hour < 18:
        speak("Good Afternoon!..")

    else:
        speak("Good Evening!..")

    speak("I am Emporio Sir.. Please tell how may I help you")


# =========================================================
# VOICE INPUT
# =========================================================

def take_command():
    """Listen to the microphone and return the recognized text."""

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")

        recognizer.pause_threshold = 1

        audio = recognizer.listen(source)

    try:

        print("Recognizing...")

        query = recognizer.recognize_google(
            audio,
            language="en-in"
        )

        print(f"User said: {query}\n")

        return query.lower()

    except Exception:

        print("Say that again please....")

        return "none"


# =========================================================
# WEBSITE FUNCTIONS
# =========================================================

def open_youtube():
    speak("Opening YouTube")
    webbrowser.open("https://youtube.com")


def open_google():
    speak("Opening Google")
    webbrowser.open("https://google.com")


def open_discord():
    speak("Opening Discord")
    webbrowser.open("https://discord.com")


def open_instagram():
    speak("Opening Instagram")
    webbrowser.open("https://instagram.com")


# =========================================================
# APPLICATION FUNCTIONS
# =========================================================

def open_vscode():
    speak("Opening Visual Studio Code")

    if os.path.exists(VSCODE_PATH):
        os.startfile(VSCODE_PATH)
    else:
        speak("I could not find Visual Studio Code.")



       


# =========================================================
# MUSIC FUNCTIONS
# =========================================================

def play_local_music():
    """Play a random song from your music folder."""

    if not os.path.exists(MUSIC_DIR):
        speak("I could not find your music folder.")
        return

    songs = os.listdir(MUSIC_DIR)

    if not songs:
        speak("There are no songs in your music folder.")
        return

    song = random.choice(songs)

    print(f"Playing: {song}")

    speak(f"Playing {song}")

    os.startfile(os.path.join(MUSIC_DIR, song))


def play_youtube_song(query):
    """Play a song/video from YouTube."""

    song = query.replace("play", "", 1).strip()

    if not song:
        speak("What should I play?")
        return

    speak(f"Playing {song}")

    pywhatkit.playonyt(song)


# =========================================================
# INFORMATION FUNCTIONS
# =========================================================

def tell_time():
    """Tell the current time."""

    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    speak(f"Sir, the time is {current_time}")


def tell_date():
    """Tell the current date."""

    current_date = datetime.datetime.now().strftime("%d %B %Y")

    speak(f"Today is {current_date}")


def search_wikipedia(query):
    """Search Wikipedia and speak the result."""

    topic = query.replace("wikipedia", "", 1).strip()

    if not topic:
        speak("What should I search on Wikipedia?")
        return

    try:

        speak("Searching Wikipedia...")

        results = wikipedia.summary(
            topic,
            sentences=2
        )

        print(results)

        speak("According to Wikipedia")
        speak(results)

    except wikipedia.exceptions.DisambiguationError:

        speak("That topic has multiple results. Please be more specific.")

    except wikipedia.exceptions.PageError:

        speak("I could not find that topic on Wikipedia.")

    except Exception as e:

        print(e)
        speak("Something went wrong while searching Wikipedia.")


# =========================================================
# EMAIL
# =========================================================

def send_email(to, content):
    """Send an email using Gmail SMTP."""

    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.ehlo()

    server.starttls()

    server.login(
        "youremail@gmail.com",
        "your-password-here"
    )

    server.sendmail(
        "youremail@gmail.com",
        to,
        content
    )

    server.close()


def email_to_sherry():
    """Ask for the email content and send it."""

    try:

        speak("What should I say?")

        content = take_command()

        to = "sherryyourEmail@gmail.com"

        send_email(to, content)

        speak("Email has been sent!")

    except Exception as e:

        print(e)

        speak("Sorry my friend, I am not able to send this email.")


# =========================================================
# PERSONALITY FUNCTIONS
# =========================================================

def say_hello():
    speak("Hello, how can I help you today?")


def how_are_you():
    speak(
        "I am good sir, and may your day be as good as me."
    )


def tell_joke():
    speak(pyjokes.get_joke())


def meow():
    message = (
        "Meow mau meow meow meeoowww "
        "meoaw meao mew meow moeww"
    )

    speak(message)


def relationship_status():
    speak("NO, I am in relationship with WiFi")


def tell_capabilities():
    speak(
        "Sir, I can do various tasks like opening "
        "Google, YouTube, Instagram, Discord, games, "
        "playing music, searching Wikipedia and sending emails."
    )


def headache():
    speak("Sorry, I have a headache")


# =========================================================
# COMMAND PROCESSOR
# =========================================================

def process_command(query):
    """Figure out what Emporio should do."""

    if "wikipedia" in query:

        search_wikipedia(query)

    elif "open youtube" in query:

        open_youtube()

    elif "open google" in query:

        open_google()

    elif "open discord" in query:

        open_discord()

    elif "open insta" in query or "open instagram" in query:

        open_instagram()

    elif "play music" in query:

        play_local_music()

    elif "the time" in query or "what is the time" in query:

        tell_time()

    elif "the date" in query or "what is the date" in query:

        tell_date()

    elif "open code" in query or "open vs code" in query:

        open_vscode()

    elif "email to sherry" in query:

        email_to_sherry()

    

    elif query.startswith("play "):

        play_youtube_song(query)

    elif "hello" in query:

        say_hello()

    elif "what all can you do" in query:

        tell_capabilities()

    elif "how are you" in query:

        how_are_you()

    elif "meow" in query:

        meow()

    elif "tell a joke" in query:

        tell_joke()

    elif "date" in query:

        headache()

    elif "are you single" in query:

        relationship_status()

    elif (
        "what" in query
        or "when" in query
        or "where" in query
        or "how" in query
        or "who" in query
        or "which" in query
    ):

        speak("I heard your question, sir, but I don't know the answer yet.")

    else:

        speak("I don't know that command yet.")


# =========================================================
# MAIN PROGRAM
# =========================================================

def main():
    """Start Emporio."""

    wishme()

    while True:

        query = take_command()

        if query == "none":
            continue

        if "stop" in query or "exit" in query or "quit" in query:

            speak("Goodbye sir.")

            break

        process_command(query)


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    main()