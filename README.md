# 🌟 Nova — AI Desktop Voice Assistant

Nova is an interactive, GUI-driven desktop AI assistant built with **Python**, **Tkinter**, **pyttsx3**, **SpeechRecognition**, and the **OpenAI API**. It features dynamic persona switching, conversation history tracking, mood adaptation, and two-way voice communication.

---

## 🚀 Features

- 🗣️ **Two-Way Voice & Text Chat**: Speak using your microphone or type queries via an intuitive desktop GUI.
- 🎭 **Dynamic Personalities**: Switch between personas on the fly:
  - `study_buddy`: Focused on academic support, conceptual breakdown, and coding guidance.
  - `bts_friend`: Playful, energetic, and engaging with light references.
  - `roaster`: Witty and playful humor while maintaining supportive boundaries.
- 🧠 **Persistent Context & Mood Awareness**: Remembers recent conversation snippets and adapts responses dynamically based on sentiment detection (e.g., comforting if sad, energetic if happy).
- 🔒 **Secure Credential Handling**: Reads keys safely via environment variables (`.env`) to prevent accidental leaks.

---

## 📋 Prerequisites

- **Python 3.10+** installed on your system.
- An **OpenAI API Key** (with active billing/credits).
- A working microphone and speaker setup.

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/harshkumarcloud/virtual-ai.git](https://github.com/harshkumarcloud/virtual-ai.git)
cd virtual-ai
```

### 2. Create and Activate a Virtual Environment (Optional but Recommended)
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

> **Windows PyAudio Note**: If `pip install pyaudio` fails, install `pipwin` and use it:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

---

## 🔑 API Key Configuration

1. Create a file named `.env` in the root project directory (same folder as `ai_desktop_assistant.py`):
   ```env
   OPENAI_API_KEY=your_actual_openai_api_key_here
   ```
2. **When your key or credits expire:**
   - Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys) to generate a new key or top up credits.
   - Simply open your local `.env` file, replace the old key with the new one, and restart the app.
   - **Never commit `.env` to GitHub**; it is kept private by `.gitignore`.

---

## ▶️ Running the Application

Launch Nova by executing:
```bash
python ai_desktop_assistant.py
```

---

## 🛠️ Troubleshooting & Common Fixes

| Issue / Error | Cause | Solution |
| :--- | :--- | :--- |
| **`AuthenticationError` (401 / Invalid API Key)** | Missing, mistyped, or expired OpenAI API key. | Open `.env` and verify `OPENAI_API_KEY=your_key`. Ensure there are no extra spaces or quotes around the key. |
| **`RateLimitError` / Quota Exceeded (429)** | Free tier expired or insufficient API credits on OpenAI account. | Check your credit balance at [platform.openai.com/usage](https://platform.openai.com/usage). Add billing credits or switch to a funded account key. |
| **`PyAudio` installation error** | Missing C++ build tools or pre-compiled binary. | On Windows: run `pip install pipwin` followed by `pipwin install pyaudio`. On Linux/Ubuntu: run `sudo apt-get install python3-pyaudio portaudio19-dev`. |
| **Microphone fails (`Could not understand audio`)** | High ambient background noise or low input level. | Check Windows Microphone privacy settings, lower ambient noise, or adjust `recognizer.adjust_for_ambient_noise(source, duration=1.0)`. |
| **pyttsx3 voice not speaking or hangs** | TTS driver initialization issue on Windows/Linux. | Ensure SAPI5 (Windows) or `espeak` (`sudo apt-get install espeak` on Linux) is installed and operational. |

---

## 📁 Project Structure

```text
virtual-ai/
├── ai_desktop_assistant.py   # Main application entry point & Tkinter GUI
├── requirements.txt          # Python dependencies
├── .env.example              # Sample environment file template
├── .gitignore                # Prevents credentials & cache from being tracked
└── README.md                 # Project documentation
```

---

## 👤 Author

- **Harsh Kumar**
- GitHub: [@harshkumarcloud](https://github.com/harshkumarcloud)
- Email: [sharshkr047@gmail.com](mailto:sharshkr047@gmail.com)