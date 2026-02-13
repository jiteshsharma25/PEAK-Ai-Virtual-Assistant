# PEAK AI Virtual Assistant

PEAK is a desktop-style voice assistant with a web UI, built with Python and JavaScript. It uses speech recognition, text-to-speech, and an AI chatbot backend to handle natural-language commands, open apps/websites, play YouTube content, and show real-time weather information.

## Features
- Voice activation via microphone (uses `speech_recognition`)
- Text-to-speech responses (via `pyttsx3`)
- Animated web UI powered by Eel, Bootstrap, and custom JS/CSS
- "Open" commands for desktop apps and websites using a local SQLite database
- YouTube playback for commands like “play Despacito on YouTube”
- AI chatbot responses using `hugchat`
- Integrated weather widget backed by OpenWeatherMap API

## Project Structure

```text
PEAK-Ai-Virtual-Assistant/
├─ main.py                 # Entry point, starts Eel and opens web UI
├─ Peak.db                 # SQLite database for app/website command mappings
├─ jarvis.db               # (Optional) legacy/extra database used by the engine
├─ venv/                   # Local Python virtual environment (optional, not required in repo)
├─ engine/
│  ├─ __pycache__/         # Python bytecode cache (auto-generated)
│  ├─ command.py           # Voice input (microphone) and text-to-speech (pyttsx3)
│  ├─ features.py          # Core assistant logic: open apps/sites, YouTube, chatbot routing
│  ├─ weather.py           # WeatherService class (OpenWeatherMap API integration, exposed via Eel)
│  ├─ db.py                # Database helper logic for SQLite (Peak.db)
│  └─ cookies.json         # HuggingFace / HugChat cookies used by the chatbot
└─ web/
  ├─ index.html           # Main UI (mic button, Siri-wave animation, weather overlay)
  ├─ main.js              # Voice UI logic, SiriWave, weather Eel calls
  ├─ controller.js        # Extra front-end behavior and event wiring
  ├─ script.js            # Additional UI/animation logic (if used)
  ├─ style.css            # Global styling for the PEAK UI
  └─ assests/
    ├─ audio/            # Initialization sound, microphone click sounds, etc.
    ├─ images/           # Icons, logos, and background images
    └─ vendore/
      └─ texllate/      # Text animation vendor files
        ├─ animate.css
        ├─ jquery.fittext.js
        ├─ jquery.lettering.js
        └─ style.css
```

## Requirements

You will need **Python 3.9+** on Windows (the TTS engine is configured with `sapi5`).

Recommended Python packages (from the code):

```bash
pip install eel pyttsx3 SpeechRecognition playsound requests pywhatkit hugchat
```

Additional dependencies/tools:
- A modern browser (the app currently launches Microsoft Edge via `msedge.exe`).
- Microphone access for speech recognition.
- An active internet connection for chatbot, YouTube, and weather.

## Configuration

### 1. OpenWeatherMap API key
The weather service uses OpenWeatherMap. In `engine/weather.py`, set your own API key:

```python
self.api_key = "YOUR_OPENWEATHERMAP_API_KEY"
```

### 2. HuggingFace / HugChat cookies
`engine/features.py` expects a valid `cookies.json` for `hugchat`:
- Place your HuggingFace cookies in `engine/cookies.json`.
- Make sure the path in `chatBot` matches that file (already set to `engine/cookies.json`).

### 3. Application/website commands database
The assistant reads mappings from `Peak.db` (and tables like `sys_command`, `web_command`) to resolve commands such as:

> "open chrome"

Ensure that:
- `Peak.db` exists in the project root.
- Tables `sys_command` and `web_command` contain the correct `name` and `path`/`url` values.

## Running the Assistant

From the project root:

```bash
python main.py
```

What this does:
- Initializes Eel with the `web` folder.
- Plays an initialization sound from `web/assests/audio/`.
- Starts the Eel server on `http://localhost:8000/index.html`.
- Opens Microsoft Edge in app mode pointing to the UI.

If Edge is not installed or you prefer another browser, update the `os.system` call in `main.py` accordingly.

## Using the Assistant

- Click the mic button in the UI (or use the defined keyboard shortcut if enabled) to start listening.
- Speak commands such as:
  - "open chrome"
  - "open youtube"
  - "play shape of you on youtube"
  - Any general question for the chatbot (e.g., "What is machine learning?").
- Use the **Weather** link in the UI to open the weather overlay, type a city name, and view details. The front-end calls `eel.get_weather(city)` which uses your OpenWeatherMap key.

## Troubleshooting

- **No audio output / TTS errors**: Check that your Windows audio devices are configured correctly and that `pyttsx3` can access the `sapi5` engine.
- **Microphone not working**: Ensure permissions are granted and that `speech_recognition` can see your microphone.
- **Chatbot not responding**: Verify internet connectivity and that `engine/cookies.json` contains valid HuggingFace cookies.
- **Weather errors**: Confirm that your OpenWeatherMap API key is correct and active.
- **Browser does not open**: Adjust the `os.system('start msedge.exe ...')` line in `main.py` to use your installed browser.

## Notes

- This project is primarily intended as a learning/demo assistant. Be cautious about exposing your API keys and cookies.
- For production use, consider adding robust error handling, logging, and a proper configuration system (e.g., `.env` files).
