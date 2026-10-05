import os
import random
import smtplib
import sqlite3
import webbrowser
import datetime

import pyjokes
import pyttsx3
import pywhatkit
import speech_recognition as sr
import wikipedia
from ollama import chat


# =========================================================
# SETTINGS
# =========================================================

ASSISTANT_NAME = "Emporio"

# ---------------------------------------------------------
# MUSIC
# ---------------------------------------------------------

MUSIC_DIR = r"D:\wyzz"

# ---------------------------------------------------------
# APPLICATION PATHS
# ---------------------------------------------------------

VSCODE_PATH = (
    r"C:\Users\payal\AppData\Roaming\Microsoft\Windows"
    r"\Start Menu\Programs\Visual Studio Code\Visual Studio Code.lnk"
)

VALORANT_PATH = (
    r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"
    r"\Riot Games\VALORANT.lnk"
)

# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------

DATABASE_PATH = "emporio.db"

# ---------------------------------------------------------
# OLLAMA
# ---------------------------------------------------------

OLLAMA_MODEL = "qwen3:4b"

# ---------------------------------------------------------
# EMAIL
# ---------------------------------------------------------

EMAIL_ADDRESS = os.getenv("EMPORIO_EMAIL")
EMAIL_APP_PASSWORD = os.getenv("EMPORIO_APP_PASSWORD")

SHERRY_EMAIL = "sherryyourEmail@gmail.com"


# =========================================================
# VOICE ENGINE
# =========================================================

engine = pyttsx3.init("sapi5")

voices = engine.getProperty("voices")

if len(voices) > 1:
    engine.setProperty("voice", voices[1].id)
else:
    engine.setProperty("voice", voices[0].id)

engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)


def speak(text):
    """Make Emporio speak."""

    print(f"{ASSISTANT_NAME}: {text}")

    try:
        engine.stop()
        engine.say(text)
        engine.runAndWait()

    except Exception as e:
        print(f"Speech error: {e}")


# =========================================================
# LOCAL SQL MEMORY
# =========================================================

def initialize_memory():
    """Create the memory database and table if they don't exist."""

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            memory TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_memory(memory):
    """Save a memory into the local SQLite database."""

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO memories (memory) VALUES (?)",
        (memory,)
    )

    connection.commit()
    connection.close()

    speak("I'll remember that, sir.")


def get_memories():
    """Return all stored memories."""

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, memory, created_at
        FROM memories
        ORDER BY id DESC
    """)

    memories = cursor.fetchall()

    connection.close()

    return memories


def search_memory(keyword):
    """Search memories containing a keyword."""

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, memory, created_at
        FROM memories
        WHERE memory LIKE ?
        ORDER BY id DESC
    """, (f"%{keyword}%",))

    memories = cursor.fetchall()

    connection.close()

    return memories


def update_memory(old_memory, new_memory):
    """Update the most recent memory containing old_memory."""

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE memories
        SET memory = ?
        WHERE id = (
            SELECT id
            FROM memories
            WHERE memory LIKE ?
            ORDER BY id DESC
            LIMIT 1
        )
    """, (new_memory, f"%{old_memory}%"))

    updated = cursor.rowcount

    connection.commit()
    connection.close()

    return updated


def forget_memory(keyword):
    """Delete memories containing a keyword."""

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM memories
        WHERE memory LIKE ?
    """, (f"%{keyword}%",))

    deleted = cursor.rowcount

    connection.commit()
    connection.close()

    return deleted


def forget_all_memories():
    """Delete all stored memories."""

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM memories")

    connection.commit()
    connection.close()

    speak("All memories have been forgotten, sir.")


# =========================================================
# MEMORY COMMANDS
# =========================================================

def remember_something(query):
    """Extract and save the user's requested memory."""

    memory = query.replace("remember that", "", 1).strip()

    if not memory:
        speak("What should I remember, sir?")
        return

    save_memory(memory)


def tell_memories():
    """Tell the user all stored memories."""

    memories = get_memories()

    if not memories:
        speak("I don't have any memories yet, sir.")
        return

    speak(f"I have {len(memories)} memories stored.")

    for _, memory, _ in memories:
        speak(memory)


def recall_memory(query):
    """Search for a specific memory."""

    keyword = query

    keyword = keyword.replace(
        "what do you remember about",
        "",
        1
    )

    keyword = keyword.replace(
        "do you remember",
        "",
        1
    )

    keyword = keyword.replace(
        "remember anything about",
        "",
        1
    )

    keyword = keyword.strip()

    if not keyword:
        tell_memories()
        return

    memories = search_memory(keyword)

    if not memories:
        speak(f"I don't remember anything about {keyword}.")
        return

    speak(f"Here's what I remember about {keyword}.")

    for _, memory, _ in memories:
        speak(memory)


def delete_memory(query):
    """Delete memories based on a keyword."""

    keyword = query

    keyword = keyword.replace(
        "forget about",
        "",
        1
    )

    keyword = keyword.replace(
        "forget",
        "",
        1
    )

    keyword = keyword.strip()

    if not keyword:
        speak("Tell me what you want me to forget.")
        return

    deleted = forget_memory(keyword)

    if deleted > 0:
        speak(f"I forgot {deleted} matching memories.")
    else:
        speak("I couldn't find a memory matching that.")


def change_memory(query):
    """Update a stored memory."""

    command = query.replace(
        "change memory",
        "",
        1
    ).strip()

    if " to " not in command:
        speak(
            "Tell me what you want to change "
            "and what it should become."
        )
        return

    old_memory, new_memory = command.split(
        " to ",
        1
    )

    old_memory = old_memory.strip()
    new_memory = new_memory.strip()

    updated = update_memory(
        old_memory,
        new_memory
    )

    if updated > 0:
        speak("Memory updated, sir.")
    else:
        speak("I couldn't find that memory.")


# =========================================================
# GREETING
# =========================================================

def wishme():
    """Greet the user based on the current time."""

    hour = datetime.datetime.now().hour

    if hour < 12:
        greeting = "Good Morning!.."

    elif hour < 18:
        greeting = "Good Afternoon!.."

    else:
        greeting = "Good Evening!.."

    speak(
        f"{greeting} "
        "I am Emporio Sir.. "
        "Please tell how may I help you"
    )


# =========================================================
# VOICE INPUT
# =========================================================

def take_command():
    """Listen to the microphone and convert speech to text."""

    recognizer = sr.Recognizer()

    recognizer.pause_threshold = 1

    try:

        with sr.Microphone() as source:

            print("Listening...")

            audio = recognizer.listen(source)

        print("Recognizing...")

        query = recognizer.recognize_google(
            audio,
            language="en-in"
        )

        print(f"User said: {query}\n")

        return query.lower().strip()

    except sr.UnknownValueError:

        print("Say that again please....")
        return "none"

    except sr.RequestError:

        print(
            "Speech recognition service is unavailable."
        )
        return "none"

    except OSError:

        print(
            "Microphone could not be accessed."
        )
        return "none"


# =========================================================
# OLLAMA / LOCAL AI
# =========================================================

def ask_ai(query):
    """
    Ask the local Qwen3 model a question through Ollama.

    This is currently used only for questions/requests
    that don't match one of Emporio's existing commands.
    """

    try:

        response = chat(
            model=OLLAMA_MODEL,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Emporio, a personal desktop "
                        "voice assistant. "
                        "Answer naturally and concisely. "
                        "You understand English, Hindi and Hinglish. "
                        "Do not explain internal reasoning. "
                        "Do not claim to perform actions that you "
                        "cannot actually perform."
                    )
                },

                {
                    "role": "user",
                    "content": query
                }
            ],

            # Disable Qwen3 thinking output
            think=False,

            # Keep model loaded briefly for faster follow-up requests
            keep_alive="2m"
        )

        answer = response.message.content.strip()

        if not answer:
            return (
                "I received an empty response "
                "from my local AI system."
            )

        return answer

    except Exception as e:

        print(f"Ollama error: {e}")

        return (
            "I am unable to access my local AI system "
            "right now."
        )


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

    if not os.path.exists(VSCODE_PATH):

        speak("I could not find Visual Studio Code.")

        print(
            f"Path not found: {VSCODE_PATH}"
        )

        return

    try:

        os.startfile(VSCODE_PATH)

    except OSError as e:

        print(e)

        speak(
            "I could not open Visual Studio Code."
        )


def open_valorant():

    speak("Opening Valorant")

    if not os.path.exists(VALORANT_PATH):

        speak("I could not find Valorant.")

        print(
            f"Path not found: {VALORANT_PATH}"
        )

        return

    try:

        os.startfile(VALORANT_PATH)

    except OSError as e:

        print(e)

        speak(
            "I could not open Valorant."
        )


# =========================================================
# MUSIC FUNCTIONS
# =========================================================

def play_local_music():
    """Play a random local song."""

    if not os.path.isdir(MUSIC_DIR):

        speak(
            "I could not find your music folder."
        )

        print(
            f"Music folder not found: {MUSIC_DIR}"
        )

        return

    songs = [
        song
        for song in os.listdir(MUSIC_DIR)
        if song.lower().endswith(
            (
                ".mp3",
                ".wav",
                ".flac",
                ".m4a",
                ".ogg"
            )
        )
    ]

    if not songs:

        speak(
            "There are no supported songs "
            "in your music folder."
        )

        return

    song = random.choice(songs)

    print(f"Playing: {song}")

    speak(
        f"Playing "
        f"{os.path.splitext(song)[0]}"
    )

    try:

        os.startfile(
            os.path.join(
                MUSIC_DIR,
                song
            )
        )

    except OSError as e:

        print(e)

        speak(
            "I could not play that song."
        )


def play_youtube_song(query):
    """Play a requested song/video through YouTube."""

    song = query.replace(
        "play",
        "",
        1
    ).strip()

    if not song:

        speak(
            "What should I play?"
        )

        return

    speak(
        f"Playing {song}"
    )

    try:

        pywhatkit.playonyt(song)

    except Exception as e:

        print(e)

        speak(
            "I could not play that right now."
        )


# =========================================================
# INFORMATION FUNCTIONS
# =========================================================

def tell_time():

    current_time = datetime.datetime.now().strftime(
        "%I:%M %p"
    )

    speak(
        f"Sir, the time is {current_time}"
    )


def tell_date():

    current_date = datetime.datetime.now().strftime(
        "%d %B %Y"
    )

    speak(
        f"Today is {current_date}"
    )


def search_wikipedia(query):
    """Search Wikipedia and speak a short result."""

    topic = query.replace(
        "wikipedia",
        "",
        1
    ).strip()

    if not topic:

        speak(
            "What should I search on Wikipedia?"
        )

        return

    try:

        speak(
            "Searching Wikipedia..."
        )

        results = wikipedia.summary(
            topic,
            sentences=2
        )

        print("\nWikipedia:")
        print(results)
        print()

        speak(
            "According to Wikipedia."
        )

        speak(results)

    except wikipedia.exceptions.DisambiguationError:

        speak(
            "That topic has multiple results. "
            "Please be more specific."
        )

    except wikipedia.exceptions.PageError:

        speak(
            "I could not find that topic on Wikipedia."
        )

    except Exception as e:

        print(e)

        speak(
            "Something went wrong while searching Wikipedia."
        )


# =========================================================
# EMAIL
# =========================================================

def send_email(to, content):
    """Send an email through Gmail SMTP."""

    if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD:

        speak(
            "Email is not configured yet."
        )

        print(
            "Set EMPORIO_EMAIL and "
            "EMPORIO_APP_PASSWORD first."
        )

        return

    try:

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.ehlo()
        server.starttls()

        server.login(
            EMAIL_ADDRESS,
            EMAIL_APP_PASSWORD
        )

        server.sendmail(
            EMAIL_ADDRESS,
            to,
            content
        )

        server.quit()

        speak(
            "Email has been sent!"
        )

    except smtplib.SMTPAuthenticationError:

        speak(
            "Email authentication failed. "
            "Check your Gmail app password."
        )

    except Exception as e:

        print(e)

        speak(
            "Sorry my friend, "
            "I am not able to send this email."
        )


def email_to_sherry():

    speak(
        "What should I say?"
    )

    content = take_command()

    if content == "none":

        speak(
            "I didn't hear the email message."
        )

        return

    send_email(
        SHERRY_EMAIL,
        content
    )


# =========================================================
# PERSONALITY FUNCTIONS
# =========================================================

def say_hello():

    speak(
        "Hello, how can I help you today?"
    )


def how_are_you():

    speak(
        "I am good sir, "
        "and may your day be as good as me."
    )


def tell_joke():

    speak(
        pyjokes.get_joke()
    )


def meow():

    speak(
        "Meow mau meow meow meeoowww "
        "meoaw meao mew meow moeww"
    )


def relationship_status():

    speak(
        "NO, I am in relationship with WiFi"
    )


def tell_capabilities():

    speak(
        "Sir, I can open Google, YouTube, "
        "Instagram, Discord, Visual Studio Code, "
        "Valorant, play music, search Wikipedia, "
        "send emails, remember things, "
        "and answer questions using my local AI."
    )


# =========================================================
# COMMAND PROCESSOR
# =========================================================

def process_command(query):
    """Determine which Emporio function should run."""

    # -----------------------------------------------------
    # MEMORY
    # -----------------------------------------------------

    if "forget everything" in query:

        forget_all_memories()

    elif "remember that" in query:

        remember_something(query)

    elif "what do you remember about" in query:

        recall_memory(query)

    elif "do you remember" in query:

        recall_memory(query)

    elif query == "what do you remember":

        tell_memories()

    elif query.startswith("forget "):

        delete_memory(query)

    elif query.startswith("change memory"):

        change_memory(query)

    # -----------------------------------------------------
    # WIKIPEDIA
    # -----------------------------------------------------

    elif "wikipedia" in query:

        search_wikipedia(query)

    # -----------------------------------------------------
    # WEBSITES
    # -----------------------------------------------------

    elif "open youtube" in query:

        open_youtube()

    elif "open google" in query:

        open_google()

    elif "open discord" in query:

        open_discord()

    elif (
        "open insta" in query
        or "open instagram" in query
    ):

        open_instagram()

    # -----------------------------------------------------
    # APPLICATIONS
    # -----------------------------------------------------

    elif (
        "open code" in query
        or "open vs code" in query
        or "open visual studio code" in query
    ):

        open_vscode()

    elif "open valorant" in query:

        open_valorant()

    # -----------------------------------------------------
    # MUSIC
    # -----------------------------------------------------

    elif query == "play music":

        play_local_music()

    elif query.startswith("play "):

        play_youtube_song(query)

    # -----------------------------------------------------
    # TIME / DATE
    # -----------------------------------------------------

    elif (
        "what time" in query
        or "the time" in query
    ):

        tell_time()

    elif (
        "what is the date" in query
        or "what's the date" in query
        or query == "date"
    ):

        tell_date()

    # -----------------------------------------------------
    # EMAIL
    # -----------------------------------------------------

    elif "email to sherry" in query:

        email_to_sherry()

    # -----------------------------------------------------
    # PERSONALITY
    # -----------------------------------------------------

    elif "hello" in query:

        say_hello()

    elif "how are you" in query:

        how_are_you()

    elif "what all can you do" in query:

        tell_capabilities()

    elif "are you single" in query:

        relationship_status()

    elif "meow" in query:

        meow()

    elif "tell a joke" in query:

        tell_joke()

    # -----------------------------------------------------
    # AI FALLBACK
    # -----------------------------------------------------

    else:

        answer = ask_ai(query)

        speak(answer)


# =========================================================
# MAIN
# =========================================================

def main():

    # Initialize local database
    initialize_memory()

    # Greeting
    wishme()

    # Main assistant loop
    while True:

        query = take_command()

        if query == "none":
            continue

        # Exit commands
        if (
            query == "stop"
            or query == "exit"
            or query == "quit"
            or "goodbye" in query
        ):

            speak("Goodbye sir.")

            break

        process_command(query)


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    main()