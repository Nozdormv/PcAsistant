# Astra — Asistente Personal de Escritorio

![Python](https://img.shields.io/badge/Python-3.8+-blue) ![License](https://img.shields.io/badge/License-MIT-green)

Astra es un asistente personal de escritorio con interfaz gráfica (Tkinter). Usa un sistema inteligente de reconocimiento de intenciones por patrones que entiende lenguaje natural **sin necesidad de APIs externas ni conexión a Internet** (excepto para búsqueda web y Wikipedia).

---

## ✨ Funcionalidades

| Categoría | Descripción |
|-----------|-------------|
| **🗣️ Lenguaje natural** | Escribí en inglés o español, Astra entiende la intención |
| **💻 Info del sistema** | CPU, RAM, tiempo activo, especificaciones completas |
| **🌐 Búsqueda web** | Abre Google en tu navegador con cualquier consulta |
| **📚 Wikipedia** | Resúmenes al instante sobre cualquier tema |
| **🚀 Abrir apps** | Notepad, calculadora, Chrome, Discord, Spotify y más |
| **⏰ Recordatorios** | "recuérdame en 10 minutos que revise el horno" |
| **😂 Chistes y citas** | Colección integrada en inglés y español |
| **🔊 Voz** | Texto a voz con velocidad ajustable (pyttsx3) |
| **🌙 Tema oscuro/claro** | Alterná entre ambos desde Configuración |
| **🔐 Usuarios** | Login/registro con contraseñas hasheadas con sal |
| **💾 Sesión persistente** | Recordá tu sesión al cerrar y abrir la app |
| **🌍 Bilingüe** | Interfaz y respuestas en español e inglés |

---

## 🚀 Cómo usar

### Opción 1 — Ejecutable (Windows)
Descargá la última versión desde [Releases](https://github.com/Nozdormv/PcAsistant/releases) y ejecutá `Astra.exe`.

### Opción 2 — Desde código
```bash
pip install -r requirements.txt
python main.py
```

### Primeros pasos
Usuario por defecto: `demo` / Contraseña: `demo`

O registrá un usuario nuevo desde la pantalla de login.

### Ejemplos de comandos

| Decís | Astra responde |
|-------|----------------|
| "hola" | Saludo |
| "qué hora es" | Hora actual |
| "info del sistema" | Especificaciones de la PC |
| "buscar tutoriales de Python" | Abre Google con la búsqueda |
| "cuéntame sobre Einstein" | Resumen de Wikipedia |
| "abrir calculadora" | Abre la calculadora |
| "recuérdame en 5 minutos que tome agua" | Recordatorio con aviso |
| "cuéntame un chiste" | Chiste aleatorio |
| "dame una cita" | Cita inspiradora |
| "ayuda" | Lista de comandos |
| "adiós" | Cierra la app |

---

## 📦 Dependencias

- Python 3.8+
- `psutil` — Información del sistema
- `pyttsx3` — Texto a voz
- `wikipedia` — Resúmenes de Wikipedia
- `requests` — Requerido por wikipedia

---

## 🛠️ Desarrollo

### Compilar ejecutable
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "Astra" main.py
```

### Estructura del proyecto
```
PcAsistant/
├── main.py                # Aplicación principal
├── Astra.exe              # Ejecutable compilado
├── requirements.txt       # Dependencias
├── CHANGELOG.md           # Historial de cambios
├── LICENSE                # Licencia MIT
├── .gitignore
└── version 1/             # Versión CLI anterior (Astra v1)
```

---

## 📄 Licencia

MIT License — Copyright (c) 2025 Nozdormv
