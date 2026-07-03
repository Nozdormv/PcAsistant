# Astra — Asistente Personal de Escritorio

<p align="center">
  <strong>Astra</strong> es un asistente de escritorio inteligente con interfaz moderna estilo Windows 11.
  Construido con <strong>Node.js</strong> y <strong>Electron</strong>.
</p>

## Características

- **Chat inteligente**: clasificador de intenciones con respuestas para sistema, búsqueda web, Wikipedia, chistes, citas y más
- **Información del sistema**: CPU, RAM, disco, red, tiempo de actividad
- **Lanzador de aplicaciones**: acceso rápido a aplicaciones del sistema
- **Recordatorios**: temporizador con notificaciones emergentes
- **Autenticación**: login, registro y sesión persistente
- **Temas**: modo claro y oscuro con diseño glass-morphism
- **Bandeja de sistema**: minimizar a bandeja con atajo global `Ctrl+Mayús+A`
- **Idioma**: español (fijo, sin selector de idioma)

## Requisitos

- Windows 11 64 bits
- [Node.js](https://nodejs.org/) v24.15.0 o superior
- npm 11.12.1 o superior

## Instalación

```bash
git clone <repositorio>
cd pcasistant
npm install
```

## Ejecución en desarrollo

Haz doble clic en `test.bat` o ejecuta:

```bash
npx electron .
```

La aplicación se inicia sin ventana de consola.

## Construir instalador

```bash
npm run build
```

El instalador se genera en `dist/Astra-Setup-2.11.30.exe`.

## Primer inicio

El usuario `demo` con contraseña `demo` se crea automáticamente al arrancar la aplicación por primera vez.

## Estructura del proyecto

```
pcasistant/
├── main.js            # Proceso principal de Electron
├── preload.js         # Puente de comunicación (contextBridge)
├── launch.vbs         # Lanzador sin ventana de consola
├── test.bat           # Script de inicio rápido
├── src/
│   ├── index.html     # Interfaz de usuario
│   ├── styles.css     # Estilos (tema claro/oscuro)
│   ├── renderer.js    # Lógica de la interfaz
│   ├── classifier.js  # Clasificador de intenciones
│   └── i18n.js        # Textos en español
└── package.json
```

## Datos de usuario

Los datos de usuario y sesión se almacenan en `%APPDATA%\Astra\`:

- `credentials_salted.json` — credenciales con hash
- `session.json` — sesión activa
- `astra.log` — registro de eventos y errores

## Tecnologías

- **Electron** ^34.0.0
- **Node.js** v24.15.0
- **systeminformation** ^5.25.0
- **electron-builder** ^25.0.0

## Atajos de teclado

| Atajo | Acción |
|---|---|
| `Ctrl + Mayús + A` | Mostrar / ocultar ventana |
| `Intro` | Enviar mensaje en el chat |
| `Mayús + Intro` | Nueva línea en el chat |

## Licencia

Uso interno.
