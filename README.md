# Emporio

> A modular personal desktop voice assistant built with Python, local AI, speech recognition, and persistent memory.

Emporio is a personal desktop voice assistant designed to combine voice interaction, AI, memory, application control, web functionality, and other utilities into one modular system.

The project is being developed around a modular architecture so that new capabilities can be added without turning the entire assistant into one large Python file.

## Architecture

```text
Emporio/
│
├── main.py
├── assistant.py
├── config.py
│
├── modules/
│   ├── __init__.py
│   ├── speech.py
│   ├── ai.py
│   ├── memory.py
│   ├── applications.py
│   ├── web_search.py
│   ├── music.py
│   ├── information.py
│   ├── email_service.py
│   └── security.py
│
├── data/
│   └── emporio.db
│
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

## Core Components

| Component | Responsibility |
|---|---|
| `main.py` | Application entry point |
| `assistant.py` | Coordinates Emporio's behavior and command processing |
| `config.py` | Central configuration and environment settings |
| `speech.py` | Speech recognition and text-to-speech |
| `ai.py` | Local AI interaction |
| `memory.py` | Persistent memory using SQLite |
| `applications.py` | Application and program control |
| `web_search.py` | Web and browser-related functionality |
| `music.py` | Music-related functionality |
| `information.py` | Information, time, date, and similar utilities |
| `email_service.py` | Email functionality |
| `security.py` | Security and protected-action functionality |

## Features

Emporio is being developed with support for:

- Voice interaction
- Speech recognition
- Text-to-speech
- Local AI through Ollama
- Persistent local memory
- Application launching
- Web/browser functionality
- Music control
- Information utilities
- Email functionality
- Security and protected actions
- Modular feature expansion

## AI

Emporio uses a locally running AI model through Ollama.

```text
assistant.py
      ↓
modules/ai.py
      ↓
Ollama
      ↓
Local AI model
```

This keeps the AI implementation separate from the rest of the assistant.

## Memory

Emporio uses SQLite for persistent local memory.

```text
assistant
    ↓
modules/memory.py
    ↓
data/emporio.db
```

The database is intended to remain local and is not committed to Git.

## Security

Security is a dedicated part of Emporio's architecture:

```text
modules/security.py
```

The security layer provides a central location for protected actions, permissions, authentication, and other security-related functionality as the project develops.

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd Emporio
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and add the required values.

**Never commit `.env` to Git.**

## Ollama

Emporio's AI functionality uses Ollama.

Install Ollama separately and make sure the required model is available locally.

Example:

```bash
ollama pull qwen3:4b
```

## Running Emporio

Start the assistant with:

```bash
python emporio_v3.py
```

## Project Philosophy

### Modular
Each major capability has its own module.

### Local-first
AI and memory can operate locally, reducing unnecessary dependence on external services.

### Extensible
New capabilities should be added as modules instead of continuously expanding a single source file.

### Maintainable
Responsibilities are separated so that individual components can be developed, tested, and replaced independently.

### Security-conscious
Credentials, databases, and sensitive configuration should remain outside the public repository.

## Development Roadmap

- [ ] Complete modular migration
- [ ] Improve voice interaction
- [ ] Expand local AI capabilities
- [ ] Improve persistent memory
- [ ] Add stronger security and permission controls
- [ ] Improve application automation
- [ ] Expand web functionality
- [ ] Improve error handling
- [ ] Add testing
- [ ] Add logging
- [ ] Improve configuration management
- [ ] Add more assistant capabilities

## Privacy

Emporio may store personal assistant memory locally using SQLite.

The following are intentionally excluded from Git:

```text
.env
data/*.db
```

Do not commit API keys, passwords, personal credentials, or private databases to the repository.

## License

Emporio is distributed under the license specified in the `LICENSE` file.

All rights are reserved unless explicitly stated otherwise.

## Status

🚧 **Active Development**

Emporio is an evolving project. The architecture and individual modules will continue to develop as new functionality is implemented.
