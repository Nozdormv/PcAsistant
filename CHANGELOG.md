# Changelog

## v2.11.30 (Beta) — 03-07-2026

### Added
- Port completo de Python (Tkinter) a Node.js + Electron
- Interfaz moderna estilo Windows 11: glass-morphism, sidebar, chat, temas claro/oscuro
- Sistema de autenticación con login, registro y sesión persistente
- Clasificador de intenciones (sistema, búsqueda web, Wikipedia, apps, recordatorios, chistes, citas)
- Bandeja de sistema (system tray) con menú contextual (Mostrar / Salir)
- Atajo global `Ctrl+Shift+A` para mostrar/ocultar la ventana
- Toast de notificaciones para recordatorios
- Panel de información del sistema (CPU, RAM, disco, red, uptime)
- Grid de lanzamiento rápido de aplicaciones
- Log de eventos en `%APPDATA%\Astra\astra.log`
- Captura automática de errores no controlados (`uncaughtException`, `unhandledRejection`, `console.error`) al archivo de log
- Usuario `demo` / `demo` creado automáticamente en primer inicio

### Changed
- Migración de `PyInstaller`/`Nuitka` a `electron-builder` para evitar bloqueos de Windows Defender
- Versión actualizada de `v2.0` a `v2.11.30 (Beta)`
- Indicador de versión visible en el pie del sidebar y en panel Acerca de
- `test.bat` ahora lanza la app sin ventana de consola mediante `launch.vbs`
- **Dependencias**: Electron actualizado de `^34.0.0` a `^43.0.0`, electron-builder de `^25.0.0` a `^26.15.3`

### Fixed
- 10 bugs corregidos en el código Python original (formato seguro con llaves, shell injection, etc.)
- Ventana de consola ya no se muestra al iniciar la app
- Vulnerabilidades de seguridad en `electron` y `tar` (10 advisories, Dependabot)

### Removed
- Dependencia de Python 3.x y librerías Tkinter/PyInstaller/Nuitka

## v0.1.7 (Beta) — 26-03-2024

- Versión inicial del asistente Astra en Python con interfaz Tkinter
- Funcionalidad básica de chat con clasificador de intenciones
- Autenticación local con credenciales saladas
- Información del sistema mediante `psutil`
