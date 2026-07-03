const LANG = {
  app_name: 'Astra',
  login_title: 'Iniciar Sesión',
  register_title: 'Registrarse',
  username: 'Usuario:',
  password: 'Contraseña:',
  login_btn: 'Iniciar Sesión',
  register_btn: 'Registrarse',
  logout: 'Cerrar Sesión',
  exit: 'Salir',
  settings: 'Configuración',
  about: 'Acerca de',
  help: 'Ayuda',
  welcome_back: '¡Bienvenido de nuevo, {user}!',
  continue_session: '¿Quieres continuar tu sesión?',
  continue_btn: 'Continuar',
  new_login_btn: 'Nuevo Inicio',
  login_success: '¡Inicio de sesión exitoso!',
  login_fail: '¡Usuario o contraseña inválidos!',
  register_success: '¡Registro exitoso! Ya puedes iniciar sesión.',
  register_fail: '¡El usuario ya existe!',
  enter_credentials: 'Por favor ingresa usuario y contraseña.',
  settings_title: 'Configuración',
  tts_speed: 'Velocidad de Voz:',
  toggle_theme: 'Cambiar Tema',
  save: 'Guardar',
  saved: '¡Configuración guardada!',
  about_text: 'Astra v2.11.30 (Beta)\nAsistente Personal de Escritorio\nSistema inteligente de respuestas por patrones',
  welcome_chat: '¡Bienvenido! Soy Astra, tu asistente inteligente. Escribe "ayuda" para ver qué puedo hacer.',
  exit_cmd: 'salir',
  help_cmd: 'ayuda',
  greeting_responses: [
    '¡Hola! ¿En qué puedo ayudarte?',
    '¡Hey! Estoy aquí para ayudar. ¿Qué necesitas?',
    '¡Buenas! ¿Qué puedo hacer por ti?'
  ],
  about_responses: [
    'Soy Astra, tu asistente personal de escritorio. Puedo revisar las especificaciones del sistema, buscar en la web, obtener resúmenes de Wikipedia, abrir aplicaciones, poner recordatorios, contar chistes, compartir citas y más.',
    'Soy Astra, un asistente virtual diseñado para ayudarte con tareas cotidianas en tu computadora. Escribe "ayuda" para ver qué puedo hacer.'
  ],
  thanks_responses: [
    '¡De nada! Avísame si necesitas algo más.',
    '¡Encantado de ayudar! ¿Algo más?',
    '¡Cuando quieras! Estoy aquí si me necesitas.'
  ],
  time_response: 'La hora actual es {time}.',
  date_response: 'Hoy es {date}.',
  cpu_info: 'Uso de CPU: {pct}% ({phys} núcleos físicos, {log} hilos lógicos)',
  ram_info: 'RAM: {used}GB usados de {total}GB ({pct}%)',
  uptime_info: 'El sistema lleva activo {uptime} (desde {since}).',
  search_ask: '¿Qué te gustaría buscar?',
  search_done: 'He abierto tu navegador para buscar "{query}".',
  search_fail: 'No pude abrir el navegador. Intenta de nuevo.',
  wiki_ask: '¿Sobre qué tema quieres buscar en Wikipedia?',
  wiki_done: 'Según Wikipedia:\n{summary}',
  wiki_notfound: 'No encontré una página de Wikipedia para "{topic}".',
  wiki_fail: 'Lo siento, tuve problemas al buscar "{topic}" en Wikipedia.',
  app_ask: '¿Qué aplicación quieres abrir?',
  app_open: 'Abriendo {app}...',
  app_fail: 'No pude abrir {app}.',
  app_notfound: 'No pude encontrar "{app}". Intenta con un nombre más simple.',
  reminder_howto: 'Para poner un recordatorio, di: "recuérdame en X minutos que tengo que hacer algo"',
  reminder_set: '¡Recordatorio creado! Te avisaré en {amount} {unit} para "{msg}".',
  goodbye: '¡Hasta luego! Cuídate.',
  help_text: `Esto es lo que puedo hacer:

  Saludos — Di "hola"
  Hora y Fecha — Pregunta la hora o fecha actual
  Info del Sistema — Ver CPU, RAM, tiempo activo y especificaciones
  Búsqueda Web — Di "buscar [consulta]" para abrir Google
  Wikipedia — Di "cuéntame sobre [tema]" para un resumen
  Abrir Apps — Di "abrir [app]" (notepad, calculadora, paint, chrome, etc.)
  Recordatorios — Di "recuérdame en X minutos que [tarea]"
  Chistes — Pide que te cuente un chiste
  Citas — Pide una cita inspiradora
  Acerca de — Pregunta quién soy
  Salir — Di "adiós" o "salir" para cerrar

¡Escribe naturalmente y haré mi mejor esfuerzo!`,
  unknown_responses: [
    'No estoy seguro de entender "{input}". ¿Puedes reformularlo?',
    'Eh, no tengo respuesta para eso. Prueba "ayuda" para ver qué puedo hacer.',
    '¡Sigo aprendiendo! Intenta preguntar de otra forma. Escribe "ayuda" para orientación.',
    'No entendí bien. Puedes pedirme buscar en la web, revisar el sistema, contar un chiste y más.'
  ],
  reminder_popup: 'Recordatorio',
  d_hours: 'h',
  d_minutes: 'min',
  d_seconds: 'seg',
  logged_as: 'Astra - Conectado como {user}',
  session_title: 'Sesión Encontrada',
  sysinfo_label: 'Información del Sistema:',
  os_label: '  SO: {os}',
  processor_label: '  Procesador: {proc}',
  cores_label: '  Núcleos: {phys} físicos, {log} lógicos',
  cpu_label: '  Uso de CPU: {pct}%',
  ram_label: '  RAM: {used}GB / {total}GB ({pct}%)',
  uptime_label: '  Activo: {uptime}'
};

module.exports = LANG;
