# Emporio

Emporio is a Windows desktop voice assistant written in Python. The current version combines voice commands, local SQLite memory, common desktop/web controls, media playback, Wikipedia search, Gmail SMTP support, and a local Qwen3 AI fallback through Ollama.

## Features

- 🎙️ Speech recognition using `SpeechRecognition`
- 🔊 Text-to-speech using `pyttsx3` / Windows SAPI5
- 🧠 Persistent local memory using SQLite
- 🤖 Local AI responses using Ollama + Qwen3
- 🌐 Open YouTube, Google, Discord and Instagram
- 💻 Open Visual Studio Code
- 🎮 Open Valorant
- 🎵 Play local music or YouTube music
- 📚 Search Wikipedia
- 📧 Send email through Gmail SMTP using environment variables
- 😄 Personality commands, jokes and custom responses
- ⏰ Tell the current time and date

## Project structure

```text
emporio/
├── emporio.py          # Current/main version
├── emporio_v1.py       # Earlier version
├── emporio_v2.py       # Earlier version with SQLite memory
├── testing_ollama.py   # Small Ollama test script
├── requirements.txt    # Python dependencies
├── .env.example        # Environment-variable template
├── .gitignore
└── README.md
```

## Requirements

- Windows
- Python 3.10+ recommended
- A working microphone
- Ollama installed locally if you want the AI fallback
- A Qwen3 model installed in Ollama

## Installation

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install Python dependencies:

```powershell
pip install -r requirements.txt
```

### Ollama setup

Install Ollama, then pull the model used by the current Emporio version:

```powershell
ollama pull qwen3:4b
```

Make sure Ollama is running before using AI fallback commands.

## Email configuration

Emporio does not store the Gmail password in the source code. Set these environment variables in PowerShell:

```powershell
$env:EMPORIO_EMAIL="yourmail@gmail.com"
$env:EMPORIO_APP_PASSWORD="your-app-password"
```

Use a Gmail App Password rather than your normal Gmail password.

## Run

```powershell
python emporio.py
```

Emporio will initialize `emporio.db` automatically when it starts. The database is intentionally ignored by Git because it contains local memory data.

## Example commands

```text
"open youtube"
"open code"
"play music"
"play [song name]"
"what is the time"
"what is the date"
"wikipedia [topic]"
"remember that my project is in D drive"
"what do you remember"
"do you remember my project"
"forget my project"
"change memory ... to ..."
"tell a joke"
"are you single"
"stop"
```

## Notes

The application contains Windows-specific paths for local music, Visual Studio Code, and Valorant. Update those paths in `emporio.py` if they are different on your machine.

The current version is based on the third iteration of the project and adds the local AI fallback while retaining the SQLite memory and command-based assistant architecture.

## Security

Do not commit passwords, API keys, App Passwords, `.env` files, or private database contents. The repository ignores local database and environment files by default.

## Roadmap

- Improve natural-language command routing
- Add more desktop automation
- Add configurable paths instead of hard-coded Windows paths
- Improve error handling and logging
- Add tests for command processing and memory operations
- Add a cleaner configuration system
