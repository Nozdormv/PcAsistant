import platform
import psutil
import tkinter as tk
from tkinter import messagebox, scrolledtext, Toplevel
import time
from datetime import datetime
import json
import hashlib
import secrets
import wikipedia
import subprocess
import os
import re
import webbrowser
import random
import threading
import sys

_tts_engine = None

def speak(text):
    global _tts_engine
    if _tts_engine is None:
        import pyttsx3
        _tts_engine = pyttsx3.init()
        _tts_engine.setProperty('rate', 180)
        _tts_engine.setProperty('voice', 'english')
    _tts_engine.say(text)
    _tts_engine.runAndWait()

def _resource_path(filename):
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, filename)

USER_CREDENTIALS_FILE = _resource_path("credentials_salted.json")
SESSION_FILE = _resource_path("session.json")

current_lang = "es"
current_theme = "Light"

LANG = {
    "es": {
        "app_name": "Astra",
        "login_title": "Iniciar Sesión",
        "register_title": "Registrarse",
        "username": "Usuario:",
        "password": "Contraseña:",
        "login_btn": "Iniciar Sesión",
        "register_btn": "Registrarse",
        "logout": "Cerrar Sesión",
        "exit": "Salir",
        "file_menu": "Archivo",
        "tools_menu": "Herramientas",
        "help_menu": "Ayuda",
        "settings": "Configuración",
        "about": "Acerca de",
        "help": "Ayuda",
        "welcome_back": "¡Bienvenido de nuevo, {user}!",
        "continue_session": "¿Quieres continuar tu sesión?",
        "continue_btn": "Continuar",
        "new_login_btn": "Nuevo Inicio",
        "login_success": "¡Inicio de sesión exitoso!",
        "login_fail": "¡Usuario o contraseña inválidos!",
        "register_success": "¡Registro exitoso! Ya puedes iniciar sesión.",
        "register_fail": "¡El usuario ya existe!",
        "enter_credentials": "Por favor ingresa usuario y contraseña.",
        "settings_title": "Configuración",
        "tts_speed": "Velocidad de Voz:",
        "toggle_theme": "Cambiar Tema",
        "save": "Guardar",
        "saved": "¡Configuración guardada!",
        "tts_pending": "Configuración guardada (se cargará al usar voz).",
        "language": "Idioma:",
        "theme_dark": "Oscuro",
        "theme_light": "Claro",
        "about_text": "Astra v2.0\nAsistente Personal de Escritorio\nSistema inteligente de respuestas por patrones",
        "welcome_chat": "¡Bienvenido! Soy Astra, tu asistente inteligente. Escribe 'ayuda' para ver qué puedo hacer.\n\n",
        "exit_cmd": "salir",
        "help_cmd": "ayuda",
        "greeting_responses": [
            "¡Hola! ¿En qué puedo ayudarte?",
            "¡Hey! Estoy aquí para ayudar. ¿Qué necesitas?",
            "¡Buenas! ¿Qué puedo hacer por ti?"
        ],
        "about_responses": [
            "Soy Astra, tu asistente personal de escritorio. Puedo revisar las especificaciones del sistema, buscar en la web, obtener resúmenes de Wikipedia, abrir aplicaciones, poner recordatorios, contar chistes, compartir citas y más.",
            "Soy Astra, un asistente virtual diseñado para ayudarte con tareas cotidianas en tu computadora. Escribe 'ayuda' para ver qué puedo hacer."
        ],
        "thanks_responses": [
            "¡De nada! Avísame si necesitas algo más.",
            "¡Encantado de ayudar! ¿Algo más?",
            "¡Cuando quieras! Estoy aquí si me necesitas."
        ],
        "time_response": "La hora actual es {time}.",
        "date_response": "Hoy es {date}.",
        "sysinfo_label": "Información del Sistema:",
        "os_label": "  SO: {os}",
        "processor_label": "  Procesador: {proc}",
        "cores_label": "  Núcleos: {phys} físicos, {log} lógicos",
        "cpu_label": "  Uso de CPU: {pct}%",
        "ram_label": "  RAM: {used:.1f}GB / {total:.1f}GB ({pct}%)",
        "uptime_label": "  Activo: {uptime}",
        "cpu_info": "Uso de CPU: {pct}% ({phys} núcleos físicos, {log} hilos lógicos)",
        "ram_info": "RAM: {used:.1f}GB usados de {total:.1f}GB ({pct}%)",
        "uptime_info": "El sistema lleva activo {uptime} (desde {since}).",
        "search_ask": "¿Qué te gustaría buscar?",
        "search_done": "He abierto tu navegador para buscar '{query}'.",
        "search_fail": "No pude abrir el navegador. Intenta de nuevo.",
        "wiki_ask": "¿Sobre qué tema quieres buscar en Wikipedia?",
        "wiki_done": "Según Wikipedia:\n{summary}",
        "wiki_multi": "Múltiples temas encontrados para '{topic}'. Sé más específico. Opciones: {options}",
        "wiki_notfound": "No encontré una página de Wikipedia para '{topic}'.",
        "wiki_fail": "Lo siento, tuve problemas al buscar '{topic}' en Wikipedia.",
        "app_ask": "¿Qué aplicación quieres abrir?",
        "app_open": "Abriendo {app}...",
        "app_fail": "No pude abrir {app}.",
        "app_attempt": "Intentando abrir {app}...",
        "app_notfound": "No pude encontrar '{app}'. Intenta con un nombre más simple.",
        "reminder_howto": "Para poner un recordatorio, di: 'recuérdame en X minutos que tengo que hacer algo'",
        "reminder_set": "¡Recordatorio creado! Te avisaré en {amount} {unit} para '{msg}'.",
        "goodbye": "¡Hasta luego! Cuídate.",
        "help_text": (
            "Esto es lo que puedo hacer:\n\n"
            "  Saludos — Di 'hola'\n"
            "  Hora y Fecha — Pregunta la hora o fecha actual\n"
            "  Info del Sistema — Ver CPU, RAM, tiempo activo y especificaciones\n"
            "  Búsqueda Web — Di 'buscar [consulta]' para abrir Google\n"
            "  Wikipedia — Di 'cuéntame sobre [tema]' para un resumen\n"
            "  Abrir Apps — Di 'abrir [app]' (notepad, calculadora, paint, chrome, etc.)\n"
            "  Recordatorios — Di 'recuérdame en X minutos que [tarea]'\n"
            "  Chistes — Pide que te cuente un chiste\n"
            "  Citas — Pide una cita inspiradora\n"
            "  Acerca de — Pregunta quién soy\n"
            "  Salir — Di 'adiós' o 'salir' para cerrar\n\n"
            "¡Escribe naturalmente y haré mi mejor esfuerzo!"
        ),
        "unknown_responses": [
            "No estoy seguro de entender '{input}'. ¿Puedes reformularlo?",
            "Eh, no tengo respuesta para eso. Prueba 'ayuda' para ver qué puedo hacer.",
            "¡Sigo aprendiendo! Intenta preguntar de otra forma. Escribe 'ayuda' para orientación.",
            "No entendí bien. Puedes pedirme buscar en la web, revisar el sistema, contar un chiste y más."
        ],
        "reminder_popup": "Recordatorio",
        "d_hours": "h",
        "d_minutes": "min",
        "d_seconds": "seg",
        "logged_as": "Astra - Conectado como {user}",
        "session_title": "Sesión Encontrada",
    },
    "en": {
        "app_name": "Astra",
        "login_title": "Login",
        "register_title": "Register",
        "username": "Username:",
        "password": "Password:",
        "login_btn": "Login",
        "register_btn": "Register",
        "logout": "Logout",
        "exit": "Exit",
        "file_menu": "File",
        "tools_menu": "Tools",
        "help_menu": "Help",
        "settings": "Settings",
        "about": "About",
        "help": "Help",
        "welcome_back": "Welcome back, {user}!",
        "continue_session": "Would you like to continue your session?",
        "continue_btn": "Continue",
        "new_login_btn": "New Login",
        "login_success": "Login successful!",
        "login_fail": "Invalid username or password!",
        "register_success": "Registration successful! You can now login.",
        "register_fail": "Username already exists!",
        "enter_credentials": "Please enter username and password.",
        "settings_title": "Settings",
        "tts_speed": "Text-to-Speech Speed:",
        "toggle_theme": "Toggle Theme",
        "save": "Save",
        "saved": "Settings saved successfully!",
        "tts_pending": "TTS settings saved (engine will load on next use).",
        "language": "Language:",
        "theme_dark": "Dark",
        "theme_light": "Light",
        "about_text": "Astra v2.0\nPersonal Desktop Assistant\nIntelligent Pattern-Based Response System",
        "welcome_chat": "Welcome! I'm Astra, your intelligent assistant. Type 'help' to see what I can do.\n\n",
        "exit_cmd": "exit",
        "help_cmd": "help",
        "greeting_responses": [
            "Hello! How can I assist you today?",
            "Hi there! What can I do for you?",
            "Hey! I'm here to help. What do you need?"
        ],
        "about_responses": [
            "I'm Astra, your personal desktop assistant. I can check system specs, search the web, get Wikipedia summaries, open applications, set reminders, tell jokes, share quotes, and more!",
            "I'm Astra, a virtual assistant designed to help you with everyday tasks on your computer. Try 'help' to see what I can do!"
        ],
        "thanks_responses": [
            "You're welcome! Let me know if you need anything else.",
            "Happy to help! Anything else I can do?",
            "Anytime! I'm here if you need me."
        ],
        "time_response": "The current time is {time}.",
        "date_response": "Today is {date}.",
        "sysinfo_label": "System Information:",
        "os_label": "  OS: {os}",
        "processor_label": "  Processor: {proc}",
        "cores_label": "  CPU Cores: {phys} physical, {log} logical",
        "cpu_label": "  CPU Usage: {pct}%",
        "ram_label": "  RAM: {used:.1f}GB / {total:.1f}GB ({pct}%)",
        "uptime_label": "  Uptime: {uptime}",
        "cpu_info": "CPU Usage: {pct}% ({phys} physical cores, {log} logical threads)",
        "ram_info": "RAM: {used:.1f}GB used out of {total:.1f}GB ({pct}%)",
        "uptime_info": "System has been running for {uptime} (since {since}).",
        "search_ask": "What would you like me to search for?",
        "search_done": "I've opened your browser to search for '{query}'.",
        "search_fail": "I couldn't open the browser. Please try again.",
        "wiki_ask": "What topic would you like me to look up on Wikipedia?",
        "wiki_done": "According to Wikipedia:\n{summary}",
        "wiki_multi": "Multiple topics found for '{topic}'. Please be more specific. Options: {options}",
        "wiki_notfound": "I couldn't find a Wikipedia page for '{topic}'.",
        "wiki_fail": "Sorry, I had trouble fetching Wikipedia data for '{topic}'.",
        "app_ask": "What application would you like me to open?",
        "app_open": "Opening {app}...",
        "app_fail": "I couldn't open {app}.",
        "app_attempt": "Attempting to open {app}...",
        "app_notfound": "I couldn't find or open '{app}'. Try using a simpler name.",
        "reminder_howto": "To set a reminder, say: 'remind me in X minutes to do something'",
        "reminder_set": "Reminder set! I'll remind you in {amount} {unit} to '{msg}'.",
        "goodbye": "Goodbye! Take care.",
        "help_text": (
            "Here's what I can do:\n\n"
            "  Greetings — Say hello!\n"
            "  Time & Date — Ask for the current time or date\n"
            "  System Info — Check CPU, RAM, uptime, and full specs\n"
            "  Web Search — Say 'search for [query]' to open a Google search\n"
            "  Wikipedia — Ask 'tell me about [topic]' for a summary\n"
            "  Open Apps — Say 'open [app]' (notepad, calculator, paint, chrome, etc.)\n"
            "  Reminders — Say 'remind me in X minutes to [task]'\n"
            "  Jokes — Ask me to tell you a joke\n"
            "  Quotes — Ask for an inspirational quote\n"
            "  About — Ask who I am\n"
            "  Exit — Say 'exit' or 'goodbye' to close\n\n"
            "Just type naturally and I'll do my best to help!"
        ),
        "unknown_responses": [
            "I'm not sure I understand '{input}'. Could you rephrase that?",
            "Hmm, I don't have a response for that. Try 'help' to see what I can do.",
            "I'm still learning! Could you try asking differently? Type 'help' for guidance.",
            "I didn't quite catch that. You can ask me to search the web, check system info, tell a joke, and more!"
        ],
        "reminder_popup": "Reminder",
        "d_hours": "h",
        "d_minutes": "min",
        "d_seconds": "sec",
        "logged_as": "Astra - Logged in as {user}",
        "session_title": "Session Found",
    }
}

def _(key, **kwargs):
    text = LANG.get(current_lang, LANG["es"]).get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text

def hash_password_with_salt(password, salt=None):
    if not salt:
        salt = secrets.token_hex(16)
    salted_password = password + salt
    hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
    return hashed_password, salt

def load_user_credentials():
    if not os.path.exists(USER_CREDENTIALS_FILE):
        return {}
    with open(USER_CREDENTIALS_FILE, "r") as file:
        return json.load(file)

def save_user_credentials(credentials):
    with open(USER_CREDENTIALS_FILE, "w") as file:
        json.dump(credentials, file)

def authenticate_user(username, password):
    credentials = load_user_credentials()
    if username in credentials:
        stored_hash = credentials[username]["hash"]
        stored_salt = credentials[username]["salt"]
        hashed_password, _ = hash_password_with_salt(password, stored_salt)
        if hashed_password == stored_hash:
            return True
    return False

def register_user(username, password):
    credentials = load_user_credentials()
    if username in credentials:
        return False
    hashed_password, salt = hash_password_with_salt(password)
    credentials[username] = {"hash": hashed_password, "salt": salt}
    save_user_credentials(credentials)
    return True

def load_session():
    if not os.path.exists(SESSION_FILE):
        return None
    with open(SESSION_FILE, "r") as file:
        return json.load(file).get("username")

def save_session(username):
    with open(SESSION_FILE, "w") as file:
        json.dump({"username": username}, file)

def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

class IntentClassifier:
    def __init__(self):
        self.patterns = {
            "greeting": {
                "patterns": [
                    r"\b(hello|hi|hey|good morning|good afternoon|good evening|howdy)\b",
                    r"\b(hola|buenos días|buenas|qué tal|saludos|hey|buenas tardes|buenas noches)\b"
                ],
                "handler": self._greeting
            },
            "time": {
                "patterns": [
                    r"\b(what.*time|current time|time now|tell.*time)\b",
                    r"\b(qué hora|hora actual|hora es|dime.*hora|hora ahora)\b"
                ],
                "handler": self._get_time
            },
            "date": {
                "patterns": [
                    r"\b(what.*date|current date|today.*date|what day)\b",
                    r"\b(qué fecha|fecha actual|qué día|día es hoy|a qué día)\b"
                ],
                "handler": self._get_date
            },
            "system_info": {
                "patterns": [
                    r"\b(system specs|system info|system information|specs|sysinfo|computer info|pc specs|hardware)\b",
                    r"\b(especificaciones|info del sistema|información del sistema|especs|hardware|componentes)\b"
                ],
                "handler": self._get_system_info
            },
            "search": {
                "patterns": [
                    r"\b(search|search for|look up|find|google|look for)\b",
                    r"\b(buscar|búsca|encuentra|googlear|busca)\b"
                ],
                "handler": self._search_web
            },
            "wikipedia": {
                "patterns": [
                    r"\b(wikipedia|wiki|summary of|tell me about)\b",
                    r"\b(wikipedia|wiki|resumen de|cuéntame sobre|dime sobre|qué es)\b"
                ],
                "handler": self._get_wikipedia
            },
            "open_app": {
                "patterns": [
                    r"\b(open|run|launch|start)\b",
                    r"\b(abrir|ejecutar|lanzar|iniciar|abre|ejecuta)\b"
                ],
                "handler": self._open_application
            },
            "reminder": {
                "patterns": [
                    r"\b(remind|reminder|set reminder|remind me)\b",
                    r"\b(recordar|recordatorio|recuérdame|pon recordatorio|crea recordatorio)\b"
                ],
                "handler": self._set_reminder
            },
            "joke": {
                "patterns": [
                    r"\b(joke|funny|make me laugh|tell.*joke)\b",
                    r"\b(chiste|chistes|broma|hazme reír|cuenta.*chiste|dime.*chiste)\b"
                ],
                "handler": self._tell_joke
            },
            "quote": {
                "patterns": [
                    r"\b(quote|inspirational|motivation|inspire)\b",
                    r"\b(cita|frase|inspiración|motivación|inspira)\b"
                ],
                "handler": self._get_quote
            },
            "about": {
                "patterns": [
                    r"\b(who are you|what are you|about you|your name|what can you do)\b",
                    r"\b(quién eres|qué eres|qué puedes hacer|cómo te llamas|tú quién eres)\b"
                ],
                "handler": self._about
            },
            "thanks": {
                "patterns": [
                    r"\b(thank|thanks|thank you|appreciate|grateful)\b",
                    r"\b(gracias|muchas gracias|te agradezco|agradecido)\b"
                ],
                "handler": self._thanks
            },
            "goodbye": {
                "patterns": [
                    r"\b(bye|goodbye|see you|farewell)\b",
                    r"\b(adiós|chao|hasta luego|nos vemos|hasta pronto)\b"
                ],
                "handler": self._goodbye
            },
            "cpu": {
                "patterns": [
                    r"\b(cpu usage|cpu|processor|how.*cpu)\b",
                    r"\b(cpu|procesador|uso.*cpu|uso.*procesador)\b"
                ],
                "handler": self._get_cpu_info
            },
            "memory": {
                "patterns": [
                    r"\b(ram|memory|how.*ram|memory usage|available memory)\b",
                    r"\b(ram|memoria|uso.*ram|uso.*memoria|memoria disponible)\b"
                ],
                "handler": self._get_memory_info
            },
            "help": {
                "patterns": [
                    r"\b(help|commands|what can you do|capabilities|features)\b",
                    r"\b(ayuda|comandos|qué puedes hacer|capacidades|funciones|qué haces)\b"
                ],
                "handler": self._get_help
            },
            "uptime": {
                "patterns": [
                    r"\b(uptime|how long.*(on|running|up)|since.*(boot|start))\b",
                    r"\b(tiempo activo|encendido desde|cuánto.*(encendido|activo|prendido)|desde.*inicio)\b"
                ],
                "handler": self._get_uptime
            }
        }

        self.reminders = []
        self.jokes = [
            ("Why don't scientists trust atoms?", "Because they make up everything!"),
            ("Did you hear about the mathematician who's afraid of negative numbers?", "He'll stop at nothing to avoid them!"),
            ("Why did the scarecrow win an award?", "Because he was outstanding in his field!"),
            ("What do you call fake spaghetti?", "An impasta!"),
            ("Why did the bicycle fall over?", "Because it was two-tired!"),
            ("Why don't skeletons fight each other?", "They don't have the guts."),
            ("What do you call a fish with no eyes?", "A fsh."),
            ("Why did the coffee file a police report?", "It got mugged."),
            ("What's the best thing about Switzerland?", "I don't know, but the flag is a big plus."),
            ("¿Por qué los científicos no confían en los átomos?", "¡Porque todo lo inventan!"),
            ("¿Qué hace una abeja en el gimnasio?", "Zum-ba"),
            ("¿Cómo se dice 'poco' en alemán?", "Poco no sé, pero 'mucho' es 'sehr'."),
            ("¿Qué le dice un semáforo a otro?", "No me mires, me estoy cambiando.")
        ]

        self.quotes = [
            ("The greatest glory in living lies not in never falling, but in rising every time we fall.", "Nelson Mandela"),
            ("The way to get started is to quit talking and begin doing.", "Walt Disney"),
            ("Life is what happens when you're busy making other plans.", "John Lennon"),
            ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
            ("The only impossible journey is the one you never begin.", "Tony Robbins"),
            ("In the middle of every difficulty lies opportunity.", "Albert Einstein"),
            ("No importa qué tan lento vayas, mientras no te detengas.", "Confucio"),
            ("El éxito es la suma de pequeños esfuerzos repetidos día tras día.", "Robert Collier"),
            ("Cree que puedes y ya estás a medio camino.", "Theodore Roosevelt")
        ]

    def classify(self, user_input):
        user_input_lower = user_input.lower().strip()
        for intent, config in self.patterns.items():
            for pattern in config["patterns"]:
                if re.search(pattern, user_input_lower):
                    return intent, config
        return "unknown", None

    def process(self, user_input):
        intent, config = self.classify(user_input)
        if config is None:
            return self._unknown_response(user_input)
        if "handler" in config:
            return config["handler"](user_input)
        return self._unknown_response(user_input)

    def _greeting(self, user_input):
        return random.choice(_("greeting_responses"))

    def _about(self, user_input):
        return random.choice(_("about_responses"))

    def _thanks(self, user_input):
        return random.choice(_("thanks_responses"))

    def _get_time(self, user_input):
        return _("time_response", time=datetime.now().strftime('%I:%M %p'))

    def _get_date(self, user_input):
        if current_lang == "es":
            dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            now = datetime.now()
            fecha = f"{dias[now.weekday()]}, {now.day} de {meses[now.month-1]} de {now.year}"
        else:
            fecha = datetime.now().strftime('%A, %B %d, %Y')
        return _("date_response", date=fecha)

    def _format_uptime(self):
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        if current_lang == "es":
            parts = []
            if days > 0: parts.append(f"{days}d")
            if hours > 0: parts.append(f"{hours}h")
            parts.append(f"{minutes}min")
            uptime_str = " ".join(parts)
            since_str = boot_time.strftime('%A, %d de %B a las %I:%M %p')
        else:
            uptime_str = f"{days}d {hours}h {minutes}m"
            since_str = boot_time.strftime('%A, %B %d at %I:%M %p')
        return uptime_str, since_str

    def _get_system_info(self, user_input):
        uptime_str, _ = self._format_uptime()
        return (
            f"{_('sysinfo_label')}\n"
            f"{_('os_label', os=f'{platform.system()} {platform.release()}')}\n"
            f"{_('processor_label', proc=platform.processor())}\n"
            f"{_('cores_label', phys=psutil.cpu_count(logical=False), log=psutil.cpu_count(logical=True))}\n"
            f"{_('cpu_label', pct=psutil.cpu_percent())}\n"
            f"{_('ram_label', used=psutil.virtual_memory().used / (1024**3), total=psutil.virtual_memory().total / (1024**3), pct=psutil.virtual_memory().percent)}\n"
            f"{_('uptime_label', uptime=uptime_str)}"
        )

    def _get_cpu_info(self, user_input):
        return _("cpu_info", pct=psutil.cpu_percent(), phys=psutil.cpu_count(logical=False), log=psutil.cpu_count(logical=True))

    def _get_memory_info(self, user_input):
        mem = psutil.virtual_memory()
        return _("ram_info", used=mem.used / (1024**3), total=mem.total / (1024**3), pct=mem.percent)

    def _get_uptime(self, user_input):
        uptime_str, since_str = self._format_uptime()
        return _("uptime_info", uptime=uptime_str, since=since_str)

    def _search_web(self, user_input):
        query = user_input
        for prefixes in [["search for", "search", "look up", "look for", "find", "google"],
                         ["buscar", "búsca", "encuentra", "googlea"]]:
            for prefix in prefixes:
                if prefix in user_input.lower():
                    idx = user_input.lower().find(prefix) + len(prefix)
                    query = user_input[idx:].strip().lstrip(" '\"")
                    break
            if query != user_input:
                break
        if not query or query == user_input:
            return _("search_ask")
        try:
            webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")
            return _("search_done", query=query)
        except Exception:
            return _("search_fail")

    def _get_wikipedia(self, user_input):
        topic = user_input
        for prefixes in [["summary of", "tell me about", "wikipedia", "wiki"],
                         ["resumen de", "cuéntame sobre", "dime sobre", "wikipedia", "wiki", "qué es"]]:
            for prefix in prefixes:
                if prefix in user_input.lower():
                    idx = user_input.lower().find(prefix) + len(prefix)
                    topic = user_input[idx:].strip().lstrip(" '\"")
                    break
            if topic != user_input:
                break
        if not topic or topic == user_input:
            return _("wiki_ask")
        try:
            summary = wikipedia.summary(topic, sentences=3)
            return _("wiki_done", summary=summary)
        except wikipedia.exceptions.DisambiguationError as e:
            return _("wiki_multi", topic=topic, options=', '.join(e.options[:5]))
        except wikipedia.exceptions.PageError:
            return _("wiki_notfound", topic=topic)
        except Exception:
            return _("wiki_fail", topic=topic)

    def _open_application(self, user_input):
        app_name = user_input
        for prefixes in [["open", "run", "launch", "start"],
                         ["abrir", "ejecutar", "lanzar", "iniciar", "abre", "ejecuta"]]:
            for prefix in prefixes:
                if user_input.lower().startswith(prefix):
                    app_name = user_input[len(prefix):].strip().lstrip(" '\"")
                    break
            if app_name != user_input:
                break
        if not app_name:
            return _("app_ask")

        allowed_apps = {
            "notepad": "notepad.exe", "calculator": "calc.exe", "paint": "mspaint.exe",
            "cmd": "cmd.exe", "command prompt": "cmd.exe", "explorer": "explorer.exe",
            "file explorer": "explorer.exe", "chrome": "chrome.exe", "firefox": "firefox.exe",
            "edge": "msedge.exe", "discord": "Discord.exe", "spotify": "Spotify.exe",
            "task manager": "taskmgr.exe", "control panel": "control.exe", "settings": "ms-settings:",
            "calculadora": "calc.exe", "bloc de notas": "notepad.exe", "paint": "mspaint.exe",
            "símbolo del sistema": "cmd.exe", "explorador": "explorer.exe",
            "administrador de tareas": "taskmgr.exe", "panel de control": "control.exe",
        }

        app_lower = app_name.lower()
        if app_lower in allowed_apps:
            try:
                subprocess.Popen(allowed_apps[app_lower], shell=True)
                return _("app_open", app=app_name)
            except Exception:
                return _("app_fail", app=app_name)
        try:
            subprocess.Popen(app_name, shell=True)
            return _("app_attempt", app=app_name)
        except Exception:
            return _("app_notfound", app=app_name)

    def _set_reminder(self, user_input):
        time_match = re.search(r"(?:in|en)\s+(\d+)\s*(seconds?|secs?|minutes?|mins?|hours?|hrs?|segundos?|minutos?|horas?)", user_input, re.IGNORECASE)
        if time_match:
            amount = int(time_match.group(1))
            unit = time_match.group(2).lower()
            if unit.startswith("sec") or unit.startswith("seg"):
                seconds = amount
                unit_label = _("d_seconds") if amount != 1 else _("d_seconds")
            elif unit.startswith("min"):
                seconds = amount * 60
                unit_label = _("d_minutes")
            elif unit.startswith("hr") or unit.startswith("hor"):
                seconds = amount * 3600
                unit_label = _("d_hours")
            else:
                return _("reminder_howto")
            after_time = user_input[time_match.end():].strip()
            message_match = re.search(r"(?:to|for|que|de|:)\s*(.+)", after_time, re.IGNORECASE)
            message = message_match.group(1) if message_match else after_time
            if not message:
                message = "Recordatorio" if current_lang == "es" else "Reminder"
            self.reminders.append({"time": time.time() + seconds, "message": message})
            def reminder_thread():
                time.sleep(seconds)
                messagebox.showinfo(_("reminder_popup"), f"{_('reminder_popup')}: {message}")
            threading.Thread(target=reminder_thread, daemon=True).start()
            return _("reminder_set", amount=amount, unit=unit_label, msg=message)
        return _("reminder_howto")

    def _tell_joke(self, user_input):
        setup, punchline = random.choice(self.jokes)
        return f"{setup}\n{punchline}"

    def _get_quote(self, user_input):
        quote, author = random.choice(self.quotes)
        return f'"{quote}"\n— {author}'

    def _goodbye(self, user_input):
        return _("goodbye")

    def _get_help(self, user_input):
        return _("help_text")

    def _unknown_response(self, user_input):
        responses = _("unknown_responses")
        return random.choice(responses).format(input=user_input)

classifier = IntentClassifier()

def execute_command(command):
    return classifier.process(command)

def toggle_theme(root, chat_display):
    global current_theme
    if current_theme == "Light":
        root.config(bg="#1e1e1e")
        chat_display.config(bg="#2d2d2d", fg="#ffffff", insertbackground="white")
        current_theme = "Dark"
    else:
        root.config(bg="#f0f0f0")
        chat_display.config(bg="#ffffff", fg="#000000", insertbackground="black")
        current_theme = "Light"

def open_settings(root, chat_display):
    def save_settings():
        global current_lang
        new_lang = lang_var.get()
        new_tts_speed = tts_speed_var.get()
        current_lang = new_lang
        try:
            global _tts_engine
            if _tts_engine is None:
                import pyttsx3
                _tts_engine = pyttsx3.init()
            _tts_engine.setProperty("rate", new_tts_speed)
        except Exception:
            pass
        messagebox.showinfo(_("settings_title"), _("saved"))

    settings_window = Toplevel(root)
    settings_window.title(_("settings_title"))
    settings_window.geometry("300x330")
    window_width = 300
    window_height = 330
    screen_width = settings_window.winfo_screenwidth()
    screen_height = settings_window.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    settings_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    tk.Label(settings_window, text=_("settings_title"), font=("Helvetica", 14)).pack(pady=10)

    tk.Label(settings_window, text=_("language")).pack()
    lang_var = tk.StringVar(value=current_lang)
    lang_frame = tk.Frame(settings_window)
    lang_frame.pack()
    tk.Radiobutton(lang_frame, text="Español", variable=lang_var, value="es").pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(lang_frame, text="English", variable=lang_var, value="en").pack(side=tk.LEFT, padx=5)

    tk.Label(settings_window, text=_("tts_speed")).pack(pady=(10, 0))
    tts_speed_var = tk.IntVar(value=180)
    tk.Scale(settings_window, from_=50, to=300, variable=tts_speed_var, orient="horizontal").pack()

    tk.Button(settings_window, text=_("toggle_theme"), command=lambda: toggle_theme(root, chat_display)).pack(pady=5)
    tk.Button(settings_window, text=_("save"), command=save_settings).pack(pady=10)

def login_window():
    session_user = load_session()
    if session_user:
        session_root = tk.Tk()
        session_root.title(_("session_title"))
        session_root.geometry("350x150")
        screen_w = session_root.winfo_screenwidth()
        screen_h = session_root.winfo_screenheight()
        session_root.geometry(f'+{screen_w//2-175}+{screen_h//2-75}')
        tk.Label(session_root, text=_("welcome_back", user=session_user), font=("Helvetica", 12)).pack(pady=15)
        tk.Label(session_root, text=_("continue_session")).pack()
        btn_frame = tk.Frame(session_root)
        btn_frame.pack(pady=15)
        def continue_session():
            session_root.destroy()
            create_gui(session_user)
        def new_login():
            session_root.destroy()
            clear_session()
            show_login_form()
        tk.Button(btn_frame, text=_("continue_btn"), command=continue_session, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text=_("new_login_btn"), command=new_login, width=15).pack(side=tk.LEFT, padx=5)
        session_root.mainloop()
        return
    show_login_form()

def show_login_form():
    def attempt_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if not username or not password:
            status_label.config(text=_("enter_credentials"), fg="red")
            return
        if authenticate_user(username, password):
            save_session(username)
            status_label.config(text=_("login_success"), fg="green")
            login_screen.after(600, lambda: [login_screen.destroy(), create_gui(username)])
        else:
            status_label.config(text=_("login_fail"), fg="red")

    def open_registration():
        def attempt_registration():
            username = reg_username_entry.get().strip()
            password = reg_password_entry.get().strip()
            if not username or not password:
                reg_status.config(text=_("enter_credentials"), fg="red")
                return
            if register_user(username, password):
                reg_status.config(text=_("register_success"), fg="green")
                registration_screen.after(1000, registration_screen.destroy)
            else:
                reg_status.config(text=_("register_fail"), fg="red")

        registration_screen = Toplevel(login_screen)
        registration_screen.title(_("register_title"))
        registration_screen.geometry("300x230")
        reg_status = tk.Label(registration_screen, text="", font=("Helvetica", 9))
        reg_status.pack()
        tk.Label(registration_screen, text=_("register_title"), font=("Helvetica", 14)).pack(pady=10)
        tk.Label(registration_screen, text=_("username")).pack()
        reg_username_entry = tk.Entry(registration_screen)
        reg_username_entry.pack()
        tk.Label(registration_screen, text=_("password")).pack()
        reg_password_entry = tk.Entry(registration_screen, show="*")
        reg_password_entry.pack()
        tk.Button(registration_screen, text=_("register_btn"), command=attempt_registration).pack(pady=10)

    login_screen = tk.Tk()
    login_screen.title(f"{_('app_name')} - {_('login_title')}")
    login_screen.geometry("300x230")
    screen_w = login_screen.winfo_screenwidth()
    screen_h = login_screen.winfo_screenheight()
    login_screen.geometry(f'+{screen_w//2-150}+{screen_h//2-115}')

    status_label = tk.Label(login_screen, text="", font=("Helvetica", 9))
    status_label.pack()

    tk.Label(login_screen, text=_("app_name"), font=("Helvetica", 14, "bold")).pack(pady=10)
    tk.Label(login_screen, text=_("username")).pack()
    username_entry = tk.Entry(login_screen)
    username_entry.pack()
    tk.Label(login_screen, text=_("password")).pack()
    password_entry = tk.Entry(login_screen, show="*")
    password_entry.pack()
    tk.Button(login_screen, text=_("login_btn"), command=attempt_login).pack(pady=10)
    tk.Button(login_screen, text=_("register_btn"), command=open_registration).pack(pady=2)
    password_entry.bind("<Return>", lambda e: attempt_login())

    login_screen.mainloop()

def create_gui(username):
    def on_command():
        user_input = command_entry.get().strip()
        if user_input.lower() in [_("exit_cmd"), "exit", "quit", "salir"]:
            clear_session()
            root.quit()
            return
        if user_input.lower() in ["bye", "goodbye", "adiós", "chao", "hasta luego", "nos vemos"]:
            response = classifier.process(user_input)
            chat_display.insert(tk.END, f"{username}: {user_input}\n", "user")
            chat_display.insert(tk.END, f"Astra: {response}\n\n", "astra")
            chat_display.see(tk.END)
            command_entry.delete(0, tk.END)
            root.after(2000, lambda: [clear_session(), root.quit()])
            return
        if user_input:
            response = execute_command(user_input)
            chat_display.insert(tk.END, f"{username}: {user_input}\n", "user")
            chat_display.insert(tk.END, f"Astra: {response}\n\n", "astra")
            chat_display.see(tk.END)
            command_entry.delete(0, tk.END)

    root = tk.Tk()
    root.title(_("logged_as", user=username))
    root.geometry("700x500")
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    root.geometry(f'+{screen_w//2-350}+{screen_h//2-250}')

    menu_bar = tk.Menu(root)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label=_("logout"), command=lambda: [clear_session(), root.destroy(), login_window()])
    file_menu.add_command(label=_("exit"), command=root.quit)
    menu_bar.add_cascade(label=_("file_menu"), menu=file_menu)
    tools_menu = tk.Menu(menu_bar, tearoff=0)
    tools_menu.add_command(label=_("settings"), command=lambda: open_settings(root, chat_display))
    menu_bar.add_cascade(label=_("tools_menu"), menu=tools_menu)
    help_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label=_("about"), command=lambda: messagebox.showinfo(_("about"), _("about_text")))
    help_menu.add_command(label=_("help"), command=lambda: chat_display.insert(tk.END, f"Astra: {execute_command(_('help_cmd'))}\n\n", "astra"))
    menu_bar.add_cascade(label=_("help_menu"), menu=help_menu)
    root.config(menu=menu_bar)

    chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state="normal", font=("Courier", 10))
    chat_display.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    chat_display.tag_config("user", foreground="blue")
    chat_display.tag_config("astra", foreground="green")
    chat_display.insert(tk.END, f"Astra: {_('welcome_chat')}", "astra")

    command_entry = tk.Entry(root, font=("Arial", 14))
    command_entry.pack(fill=tk.X, padx=10, pady=5)
    command_entry.bind("<Return>", lambda event: on_command())
    command_entry.focus()
    root.mainloop()

login_window()
