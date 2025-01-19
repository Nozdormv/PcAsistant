import platform
import psutil
import tkinter as tk
from tkinter import messagebox, scrolledtext, Toplevel
import pyttsx3
import requests
import time
import pyperclip
from datetime import datetime
import threading
import json
import hashlib
import secrets
import wikipedia
import subprocess
import os
import openai

# Fetch the API Key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# If the environment variable is not set, you can still use the hardcoded key as a fallback.
if not openai.api_key:
    openai.api_key = "your-api-key-here"
    
# AI Response (using OpenAI API)
def get_ai_response(user_input):
    """Get a response from OpenAI's GPT model."""
    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # You can change this to any available model
            prompt=f"User: {user_input}\nAssistant:",
            max_tokens=150,
            temperature=0.7  # You can adjust the creativity of responses here
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 180)
engine.setProperty('voice', 'english')

# Speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Paths for credentials and session data
USER_CREDENTIALS_FILE = "credentials_salted.json"
SESSION_FILE = "session.json"

# Hashing Functions with Salt
def hash_password_with_salt(password, salt=None):
    """Hash a password using SHA256 with a salt."""
    if not salt:
        salt = secrets.token_hex(16)  # Generate a new random salt
    salted_password = password + salt
    hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
    return hashed_password, salt

# User Credential Handling
def load_user_credentials():
    """Load user credentials from a JSON file."""
    if not os.path.exists(USER_CREDENTIALS_FILE):
        return {}
    with open(USER_CREDENTIALS_FILE, "r") as file:
        return json.load(file)

def save_user_credentials(credentials):
    """Save user credentials to a JSON file."""
    with open(USER_CREDENTIALS_FILE, "w") as file:
        json.dump(credentials, file)

def authenticate_user(username, password):
    """Authenticate a user with the stored credentials and salt."""
    credentials = load_user_credentials()
    if username in credentials:
        stored_hash = credentials[username]["hash"]
        stored_salt = credentials[username]["salt"]
        hashed_password, _ = hash_password_with_salt(password, stored_salt)
        if hashed_password == stored_hash:
            return True
    return False

def register_user(username, password):
    """Register a new user with a hashed and salted password."""
    credentials = load_user_credentials()
    if username in credentials:
        return False  # Username already exists
    hashed_password, salt = hash_password_with_salt(password)
    credentials[username] = {"hash": hashed_password, "salt": salt}
    save_user_credentials(credentials)
    return True

# Persistent Session Handling
def load_session():
    """Load session data from a JSON file."""
    if not os.path.exists(SESSION_FILE):
        return None
    with open(SESSION_FILE, "r") as file:
        return json.load(file).get("username")

def save_session(username):
    """Save session data to a JSON file."""
    with open(SESSION_FILE, "w") as file:
        json.dump({"username": username}, file)

def clear_session():
    """Clear the session data."""
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

# Command Execution
def execute_command(command):
    if "help" in command:
        return (
            "Available commands:\n"
            "- 'system specs': Display system specifications.\n"
            "- 'get public ip': Retrieve public IP address.\n"
            "- 'list files [path]': List files in a directory.\n"
            "- 'set reminder [time] [message]': Set a reminder.\n"
            "- 'exit': Close the application.\n"
            "- 'search [query]': Search the web for the query.\n"
            "- 'wikipedia [topic]': Get a Wikipedia summary of the topic.\n"
            "- 'run [application]': Run a local application."
        )
    elif "search" in command:
        query = command.replace("search", "").strip()
        if query:
            try:
                response = requests.get(f"https://www.google.com/search?q={query}")
                return f"Web search result for '{query}':\n{response.url}"
            except requests.exceptions.RequestException:
                return "Error while performing web search."
        return "Please provide a search query."
    elif "wikipedia" in command:
        topic = command.replace("wikipedia", "").strip()
        if topic:
            try:
                summary = wikipedia.summary(topic, sentences=3)
                return f"Wikipedia summary for '{topic}':\n{summary}"
            except wikipedia.exceptions.DisambiguationError as e:
                return f"Multiple topics found. Please be more specific. Choices: {e.options}"
            except wikipedia.exceptions.HTTPTimeoutError:
                return "Error retrieving Wikipedia summary."
        return "Please provide a topic."
    elif "run" in command:
        app_name = command.replace("run", "").strip()
        if app_name:
            try:
                subprocess.Popen(app_name)
                return f"Running {app_name}..."
            except FileNotFoundError:
                return f"Application {app_name} not found."
        return "Please provide the application name."
    return "Unknown command. Type 'help' for available commands."

# Settings: Light/Dark Mode
current_theme = "Light"

def toggle_theme(root):
    global current_theme
    if current_theme == "Light":
        root.config(bg="black")
        current_theme = "Dark"
    else:
        root.config(bg="white")
        current_theme = "Light"
    messagebox.showinfo("Theme", f"Theme changed to {current_theme} mode.")

# Settings Window
def open_settings(root):
    def save_settings():
        new_tts_speed = tts_speed_var.get()
        engine.setProperty("rate", new_tts_speed)
        messagebox.showinfo("Settings", "Settings saved successfully!")

    settings_window = Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("300x250")

    # Center the window on the screen
    window_width = 300
    window_height = 250

    screen_width = settings_window.winfo_screenwidth()
    screen_height = settings_window.winfo_screenheight()

    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)

    settings_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    tk.Label(settings_window, text="Settings", font=("Helvetica", 14)).pack(pady=10)

    # TTS Speed Adjustment
    tts_speed_var = tk.IntVar(value=180)
    tk.Label(settings_window, text="Text-to-Speech Speed:").pack()
    tk.Scale(settings_window, from_=50, to=300, variable=tts_speed_var, orient="horizontal").pack()

    # Light/Dark Mode Toggle
    tk.Button(settings_window, text="Toggle Theme", command=lambda: toggle_theme(root)).pack(pady=10)

    tk.Button(settings_window, text="Save", command=save_settings).pack(pady=10)

# Login/Registration Window
def login_window():
    session_user = load_session()
    if session_user:
        if messagebox.askyesno("Session Found", f"Welcome back, {session_user}! Would you like to continue your session?"):
            create_gui(session_user)
            return

    def attempt_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if authenticate_user(username, password):
            save_session(username)
            messagebox.showinfo("Login", "Login successful!")
            login_screen.destroy()
            create_gui(username)  # Launch the main application
        else:
            messagebox.showerror("Login", "Invalid username or password!")

    def open_registration():
        def attempt_registration():
            username = reg_username_entry.get().strip()
            password = reg_password_entry.get().strip()
            if register_user(username, password):
                messagebox.showinfo("Registration", "Registration successful!")
                registration_screen.destroy()
            else:
                messagebox.showerror("Registration", "Username already exists!")

        registration_screen = Toplevel(login_screen)
        registration_screen.title("Register")
        registration_screen.geometry("300x200")

        tk.Label(registration_screen, text="Register", font=("Helvetica", 14)).pack(pady=10)

        tk.Label(registration_screen, text="Username:").pack()
        reg_username_entry = tk.Entry(registration_screen)
        reg_username_entry.pack()

        tk.Label(registration_screen, text="Password:").pack()
        reg_password_entry = tk.Entry(registration_screen, show="*")
        reg_password_entry.pack()

        tk.Button(registration_screen, text="Register", command=attempt_registration).pack(pady=10)

    login_screen = tk.Tk()
    login_screen.title("Login")
    login_screen.geometry("300x200")

    tk.Label(login_screen, text="Login", font=("Helvetica", 14)).pack(pady=10)

    tk.Label(login_screen, text="Username:").pack()
    username_entry = tk.Entry(login_screen)
    username_entry.pack()

    tk.Label(login_screen, text="Password:").pack()
    password_entry = tk.Entry(login_screen, show="*")
    password_entry.pack()

    tk.Button(login_screen, text="Login", command=attempt_login).pack(pady=10)
    tk.Button(login_screen, text="Register", command=open_registration).pack(pady=5)

    login_screen.mainloop()

# GUI Development
def create_gui(username):
    def on_command():
        user_input = command_entry.get().strip()
        if user_input.lower() == "exit":
            clear_session()
            root.quit()
            return

        if user_input:
            response = execute_command(user_input)
            chat_display.insert(tk.END, f"{username}: {user_input}\n", "user")
            chat_display.insert(tk.END, f"MUTHUR: {response}\n\n", "muthur")
            chat_display.see(tk.END)
            command_entry.delete(0, tk.END)

    root = tk.Tk()
    root.title(f"MUTHUR 9000 - Logged in as {username}")
    root.geometry("700x500")

    # Menu Bar
    menu_bar = tk.Menu(root)

    # File Menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Logout", command=lambda: [clear_session(), root.destroy(), login_window()])
    file_menu.add_command(label="Exit", command=root.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)

    # Tools Menu
    tools_menu = tk.Menu(menu_bar, tearoff=0)
    tools_menu.add_command(label="Settings", command=lambda: open_settings(root))
    menu_bar.add_cascade(label="Tools", menu=tools_menu)

    # Help Menu
    help_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "MUTHUR 9000 v2.0\nAI Assistant by Byron-Butler & powered by OpenAI"))
    help_menu.add_command(label="Help", command=lambda: chat_display.insert(tk.END, "MUTHUR: " + execute_command("help") + "\n\n", "muthur"))
    menu_bar.add_cascade(label="Help", menu=help_menu)

    root.config(menu=menu_bar)

    # Chat Display
    chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state="normal", font=("Courier", 10))
    chat_display.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    chat_display.tag_config("user", foreground="blue")
    chat_display.tag_config("muthur", foreground="green")
    chat_display.insert(tk.END, f"MUTHUR: Welcome, {username}! Type 'help' for available commands.\n\n", "muthur")

    # Command Entry
    command_entry = tk.Entry(root, font=("Arial", 14))
    command_entry.pack(fill=tk.X, padx=10, pady=5)
    command_entry.bind("<Return>", lambda event: on_command())

    # Focus entry field
    command_entry.focus()

    root.mainloop()

# Start the application
login_window()