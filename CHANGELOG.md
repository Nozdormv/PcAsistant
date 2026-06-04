# Changelog

## v2.0.0 (2026-06-04)

### Novedades
- 🌍 **Sistema bilingüe** — Interfaz y respuestas en español (es-ES) e inglés (en-UK), seleccionable desde Configuración
- 🧠 **Clasificador de intenciones** — Sistema inteligente de patrones que entiende lenguaje natural sin APIs externas
- 👤 **Sistema de usuarios** — Login/registro con contraseñas hasheadas con sal (SHA256)
- 💾 **Persistencia de sesión** — Al cerrar y reabrir, pregunta si querés continuar
- ⏰ **Recordatorios funcionales** — "recuérdame en X minutos que [tarea]" con aviso emergente
- 🎨 **Interfaz renovada** — Tema oscuro/claro, menú de configuración
- 🔊 **Texto a voz** — Velocidad ajustable desde Configuración

### Mejoras
- 🚀 **Startup rápido** — pyttsx3 se carga solo al usar voz (lazy-load)
- 🔒 **Apps con lista blanca** — Solo se pueden abrir aplicaciones permitidas por seguridad
- 🧹 **Código limpio** — Eliminados imports muertos (`openai`, `pyperclip`, `threading`)
- 🪟 **Ventanas integradas** — Mensajes de login/registro dentro de la misma ventana, sin popups separados
- 🌙 **Tema oscuro completo** — Cambia fondo y color del chat, no solo la ventana principal

### Fixes
- Corregido error de rutas en ejecutable compilado (buscaba archivos en directorio equivocado)
- Eliminada integración con OpenAI (API deprecada y no funcional)

---

## v1.1.8 (2025)

### Novedades
- Versión CLI con interfaz de consola y colores ANSI
- Comandos básicos: abrir apps, buscar web, Wikipedia, chistes, citas, sysinfo
- Script `.bat` para ejecución rápida en Windows

---

## v0.1.7 (2025)

### Novedades
- Sistema de login/registro con persistencia de sesión
- Integración con OpenAI (text-davinci-003) — no funcional
- Tema oscuro/claro básico
- Lector de pantalla (TTS)

---

## v0.1.6 (2025)

### Novedades
- Versión inicial con interfaz Tkinter
- Comandos básicos de sistema
-README inicial
