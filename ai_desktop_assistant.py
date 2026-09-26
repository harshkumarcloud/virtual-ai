import tkinter as tk
from tkinter import ttk, messagebox
import speech_recognition as sr
import pyttsx3
from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()


# ------------------ OPENAI CONFIG ------------------
# will not work as i have credit to take api key from open ai 
# Reads OPENAI_API_KEY from environment variables automatically
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MEMORY_FILE = "assistant_memory.json"

# ------------------ MEMORY FUNCTIONS ------------------
def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    # default memory
    return {
        "user_name": "Harsh",
        "personality": "study_buddy",
        "mood": "neutral",
        "chat_snippets": []
    }

def save_memory(memory):
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print("Error saving memory:", e)

def update_mood_from_text(memory, text):
    t = text.lower()
    if any(w in t for w in ["sad", "down", "upset", "bad", "tired", "depressed"]):
        memory["mood"] = "sad"
    elif any(w in t for w in ["angry", "mad", "pissed", "frustrated"]):
        memory["mood"] = "angry"
    elif any(w in t for w in ["happy", "good", "great", "awesome", "excited"]):
        memory["mood"] = "happy"
    elif any(w in t for w in ["stressed", "anxious", "nervous"]):
        memory["mood"] = "stressed"
    return memory

def add_chat_snippet(memory, user_text, assistant_text):
    memory["chat_snippets"].append({
        "user": user_text[-100:],
        "assistant": assistant_text[-100:],
    })
    memory["chat_snippets"] = memory["chat_snippets"][-10:]
    return memory

# ------------------ PERSONALITY ------------------
def get_personality_prompt(key):
    if key == "study_buddy":
        return ("You are a calm, friendly study buddy assistant. "
                "Explain clearly, support exam prep and coding, and encourage the user.")
    elif key == "bts_friend":
        return ("You are a fun BTS ARMY friend assistant. "
                "You add light BTS references, stay positive and playful, but still give accurate answers.")
    elif key == "roaster":
        return ("You are a playful roaster assistant. "
                "You roast the user lightly in a funny way but never become rude or hurtful. "
                "Be supportive if the user seems sad or stressed.")
    return "You are a friendly, helpful AI assistant."

# ------------------ TTS & STT ------------------
engine = pyttsx3.init()
engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)
voices = engine.getProperty("voices")
if voices:
    engine.setProperty("voice", voices[0].id)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

recognizer = sr.Recognizer()

def listen_from_mic():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print("You (voice):", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print("Speech Recognition error:", e)
        return ""

# ------------------ ASK AI ------------------
def ask_ai(user_text, memory):
    personality_prompt = get_personality_prompt(memory["personality"])

    if memory["chat_snippets"]:
        parts = []
        for snip in memory["chat_snippets"][-5:]:
            parts.append(f"User: {snip['user']} | Assistant: {snip['assistant']}")
        history_summary = "Previous conversation snippets:\n" + "\n".join(parts)
    else:
        history_summary = "No previous conversation yet."

    system_message = (
        f"You are a real-time assistant named Nova.\n"
        f"User's name is {memory['user_name']}.\n"
        f"User's current mood: {memory['mood']}.\n"
        f"Personality description: {personality_prompt}\n\n"
        f"{history_summary}\n\n"
        f"Adapt your tone to the user's mood: be softer if sad/stressed, "
        f"more energetic if happy."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_text},
            ],
            max_tokens=220,
        )
        reply = response.choices[0].message.content.strip()
        return reply
    except Exception as e:
        print("Error calling AI:", e)
        return "Sorry, something went wrong while contacting the AI."

# ------------------ TKINTER APP ------------------
class AssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nova - AI Desktop Assistant")
        self.root.geometry("800x600")

        self.memory = load_memory()

        self.create_widgets()
        self.append_chat(f"Nova: Hi {self.memory['user_name']}! I'm ready. Choose a personality and start chatting.\n")

    def create_widgets(self):
        # Top frame: name + personality
        top_frame = ttk.Frame(self.root, padding=5)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(top_frame, text="Name:").pack(side=tk.LEFT)
        self.name_var = tk.StringVar(value=self.memory["user_name"])
        self.name_entry = ttk.Entry(top_frame, textvariable=self.name_var, width=15)
        self.name_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(top_frame, text="Personality:").pack(side=tk.LEFT, padx=(10, 0))
        self.personality_var = tk.StringVar(value=self.memory["personality"])
        self.personality_combo = ttk.Combobox(
            top_frame,
            textvariable=self.personality_var,
            values=["study_buddy", "bts_friend", "roaster"],
            width=15,
            state="readonly"
        )
        self.personality_combo.pack(side=tk.LEFT, padx=5)

        self.save_button = ttk.Button(top_frame, text="Save Settings", command=self.save_settings)
        self.save_button.pack(side=tk.LEFT, padx=10)

        # Chat display
        mid_frame = ttk.Frame(self.root, padding=5)
        mid_frame.pack(fill=tk.BOTH, expand=True)

        self.chat_text = tk.Text(mid_frame, wrap=tk.WORD, state="disabled")
        self.chat_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(mid_frame, command=self.chat_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_text["yscrollcommand"] = scrollbar.set

        # Bottom input frame
        bottom_frame = ttk.Frame(self.root, padding=5)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(bottom_frame, textvariable=self.entry_var)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.entry.bind("<Return>", self.send_text_event)

        self.send_button = ttk.Button(bottom_frame, text="Send", command=self.send_text)
        self.send_button.pack(side=tk.LEFT)

        self.voice_button = ttk.Button(bottom_frame, text="🎤 Speak", command=self.voice_input)
        self.voice_button.pack(side=tk.LEFT, padx=5)

    def append_chat(self, text):
        self.chat_text.config(state="normal")
        self.chat_text.insert(tk.END, text)
        self.chat_text.see(tk.END)
        self.chat_text.config(state="disabled")

    def save_settings(self):
        self.memory["user_name"] = self.name_var.get().strip() or "User"
        self.memory["personality"] = self.personality_var.get()
        save_memory(self.memory)
        messagebox.showinfo("Saved", "Settings saved!")
        self.append_chat(f"Nova: Settings updated. Hi {self.memory['user_name']}! I'm in {self.memory['personality']} mode.\n")

    def send_text_event(self, event):
        self.send_text()

    def send_text(self):
        user_text = self.entry_var.get().strip()
        if not user_text:
            return
        self.entry_var.set("")

        if user_text.lower() in ["exit", "quit", "bye", "stop"]:
            self.append_chat(f"You: {user_text}\n")
            farewell = f"Okay, bye {self.memory['user_name']}! See you later.\n"
            self.append_chat(f"Nova: {farewell}\n")
            speak(farewell)
            self.root.after(500, self.root.destroy)
            return

        self.append_chat(f"You: {user_text}\n")

        # update mood & ask AI
        self.memory = update_mood_from_text(self.memory, user_text)
        reply = ask_ai(user_text, self.memory)
        self.append_chat(f"Nova: {reply}\n\n")
        speak(reply)

        self.memory = add_chat_snippet(self.memory, user_text, reply)
        save_memory(self.memory)

    def voice_input(self):
        self.append_chat("Nova: Listening... please speak.\n")
        user_text = listen_from_mic()
        if not user_text:
            self.append_chat("Nova: I couldn't hear you properly.\n")
            return

        self.append_chat(f"You (voice): {user_text}\n")

        if user_text.lower() in ["exit", "quit", "bye", "stop"]:
            farewell = f"Okay, bye {self.memory['user_name']}! See you later.\n"
            self.append_chat(f"Nova: {farewell}\n")
            speak(farewell)
            self.root.after(500, self.root.destroy)
            return

        self.memory = update_mood_from_text(self.memory, user_text)
        reply = ask_ai(user_text, self.memory)
        self.append_chat(f"Nova: {reply}\n\n")
        speak(reply)

        self.memory = add_chat_snippet(self.memory, user_text, reply)
        save_memory(self.memory)

# ------------------ MAIN ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AssistantApp(root)
    root.mainloop()
