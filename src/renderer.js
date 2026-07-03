const $ = (id) => document.getElementById(id);
const $$ = (sel) => document.querySelector(sel);
const $$$ = (sel) => document.querySelectorAll(sel);

let currentTheme = 'Light';
let currentUser = null;

const APPS = [
  { name: 'Notepad', icon: '📝', id: 'notepad' },
  { name: 'Calculadora', icon: '🔢', id: 'calculator' },
  { name: 'Paint', icon: '🎨', id: 'paint' },
  { name: 'Chrome', icon: '🌐', id: 'chrome' },
  { name: 'Edge', icon: '🦊', id: 'edge' },
  { name: 'Discord', icon: '💬', id: 'discord' },
  { name: 'Spotify', icon: '🎵', id: 'spotify' },
  { name: 'Explorador', icon: '📁', id: 'explorer' },
  { name: 'Terminal', icon: '⬛', id: 'cmd' },
  { name: 'Task Manager', icon: '📊', id: 'task manager' },
];

function _(key, obj) {
  if (!LANG_TEXTS[key]) return key;
  let t = LANG_TEXTS[key];
  if (obj) for (const k of Object.keys(obj)) t = t.replace(`{${k}}`, obj[k]);
  return t;
}

const LANG_TEXTS = {
  welcome_back: '¡Bienvenido de nuevo, {user}!',
  continue_session: '¿Quieres continuar tu sesión?',
  login_fail: '¡Usuario o contraseña inválidos!',
  register_success: '¡Registro exitoso! Ya puedes iniciar sesión.',
  register_fail: '¡El usuario ya existe!',
  enter_credentials: 'Por favor ingresa usuario y contraseña.',
  saved: '¡Configuración guardada!',
  reminder_popup: 'Recordatorio',
  goodbye: '¡Hasta luego! Cuídate.',
  sysinfo_label: 'Información del Sistema',
};

function switchView(viewId) {
  $$$('.view').forEach(v => v.classList.add('hidden'));
  $$$('.nav-item').forEach(n => n.classList.remove('active'));
  $(`view-${viewId}`).classList.remove('hidden');
  const navItem = $$(`.nav-item[data-view="${viewId}"]`);
  if (navItem) navItem.classList.add('active');
  if (viewId === 'chat') $('chat-input').focus();
}

function addMessage(text, sender) {
  const div = $('chat-display');
  const wrapper = document.createElement('div');
  wrapper.className = `msg-wrapper ${sender}`;
  const bubble = document.createElement('div');
  bubble.className = 'msg-bubble';
  bubble.textContent = text;
  wrapper.appendChild(bubble);
  div.appendChild(wrapper);
  div.scrollTop = div.scrollHeight;
}

function addTyping() {
  const div = $('chat-display');
  const wrapper = document.createElement('div');
  wrapper.className = 'msg-wrapper astra';
  wrapper.id = 'typing-wrapper';
  const bubble = document.createElement('div');
  bubble.className = 'msg-bubble typing-indicator';
  bubble.innerHTML = '<span></span><span></span><span></span>';
  wrapper.appendChild(bubble);
  div.appendChild(wrapper);
  div.scrollTop = div.scrollHeight;
}

function removeTyping() {
  const el = $('typing-wrapper');
  if (el) el.remove();
}

function showLogin() {
  $('main-screen').classList.add('hidden');
  $('session-dialog').classList.add('hidden');
  $('register-dialog').classList.add('hidden');
  $('login-screen').classList.remove('hidden');
  $('login-status').textContent = '';
  $('username-input').value = '';
  $('password-input').value = '';
  $('username-input').focus();
}

function showMain(user) {
  currentUser = user;
  $('login-screen').classList.add('hidden');
  $('session-dialog').classList.add('hidden');
  $('register-dialog').classList.add('hidden');
  $('main-screen').classList.remove('hidden');
  $('sidebar-user').textContent = user;
  $('toolbar-title').textContent = `Astra — ${user}`;
  $('chat-display').innerHTML = '';
  addMessage('¡Bienvenido! Soy Astra, tu asistente inteligente. Escribe "ayuda" para ver qué puedo hacer.', 'astra');
  $('chat-input').focus();
  loadSystemInfo();
  renderApps();
}

function showToast(msg) {
  $('toast-msg').textContent = msg;
  $('reminder-toast').classList.remove('hidden');
  setTimeout(() => $('reminder-toast').classList.add('hidden'), 5000);
}

async function loadSystemInfo() {
  try {
    const info = await window.astra.system.info();
    const grid = $('system-cards');
    const cards = [
      { icon: '🖥', label: 'Sistema Operativo', value: info.os, detail: '' },
      { icon: '🧠', label: 'Procesador', value: info.processor.split(' ').slice(0, 2).join(' '), detail: info.processor },
      { icon: '🔲', label: 'Núcleos', value: `${info.physicalCores} físicos / ${info.logicalCores} lógicos`, detail: '' },
      { icon: '⚡', label: 'Uso de CPU', value: `${info.cpuPercent}%`, detail: '' },
      { icon: '💾', label: 'RAM', value: `${info.ramUsed}GB / ${info.ramTotal}GB`, detail: `${info.ramPercent}% usado` },
      { icon: '⏱', label: 'Tiempo activo', value: info.uptime, detail: '' },
    ];
    grid.innerHTML = cards.map(c => `
      <div class="sys-card">
        <div class="card-icon">${c.icon}</div>
        <div class="card-value">${c.value}</div>
        <div class="card-label">${c.label}</div>
        ${c.detail ? `<div class="card-detail">${c.detail}</div>` : ''}
      </div>
    `).join('');
  } catch (e) {
    console.error('Error loading system info:', e);
  }
}

function renderApps() {
  const grid = $('apps-grid');
  grid.innerHTML = APPS.map(a => `
    <button class="app-btn" data-app="${a.id}">
      <span class="app-icon">${a.icon}</span>
      <span>${a.name}</span>
    </button>
  `).join('');
  grid.querySelectorAll('.app-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      const appName = btn.dataset.app;
      const r = await window.astra.app.open(appName);
      if (!r.ok) $('app-status').textContent = `No se pudo abrir "${appName}".`;
      else $('app-status').textContent = '';
    });
  });
}

async function processInput(input) {
  const lower = input.toLowerCase().trim();
  if (['salir', 'exit', 'quit', 'adiós', 'chao', 'hasta luego', 'nos vemos', 'bye', 'goodbye'].includes(lower)) {
    setTimeout(async () => { await window.astra.auth.logout(); showLogin(); }, 2000);
    return '¡Hasta luego! Cuídate.';
  }

  const response = await window.astra.process.chat(input);
  if (typeof response === 'object') {
    if (response.action === 'search') {
      window.astra.search.web(response.query);
      return `He abierto tu navegador para buscar "${response.query}".`;
    }
    if (response.action === 'wikipedia') {
      const r = await window.astra.search.wikipedia(response.topic);
      return r.ok ? `Según Wikipedia:\n${r.summary}` : r.error;
    }
    if (response.action === 'open_app') {
      const r = await window.astra.app.open(response.app);
      return r.ok ? `Abriendo ${r.app}...` : `No pude encontrar "${response.app}".`;
    }
    if (response.action === 'reminder') {
      window.astra.reminder.set({ seconds: response.seconds, message: response.message });
      return `¡Recordatorio creado! Te avisaré en ${response.amount} ${response.unitLabel} para "${response.message}".`;
    }
  }
  return response;
}

// === Event Handlers ===

// Login
$('login-btn').addEventListener('click', async () => {
  const u = $('username-input').value.trim();
  const p = $('password-input').value.trim();
  if (!u || !p) { $('login-status').textContent = 'Por favor ingresa usuario y contraseña.'; return; }
  const r = await window.astra.auth.login(u, p);
  if (r.ok) showMain(u);
  else $('login-status').textContent = r.error;
});

$('password-input').addEventListener('keydown', e => { if (e.key === 'Enter') $('login-btn').click(); });
$('register-btn').addEventListener('click', () => { $('register-dialog').classList.remove('hidden'); $('reg-username').focus(); });

// Register
$('register-confirm').addEventListener('click', async () => {
  const u = $('reg-username').value.trim();
  const p = $('reg-password').value.trim();
  if (!u || !p) { $('register-status').textContent = 'Por favor ingresa usuario y contraseña.'; return; }
  const r = await window.astra.auth.register(u, p);
  $('register-status').textContent = r.ok ? '¡Registro exitoso! Ya puedes iniciar sesión.' : r.error;
  $('register-status').style.color = r.ok ? 'var(--accent)' : 'var(--text-secondary)';
  if (r.ok) setTimeout(() => { $('register-dialog').classList.add('hidden'); $('register-status').textContent = ''; }, 1500);
});

$('register-cancel').addEventListener('click', () => {
  $('register-dialog').classList.add('hidden');
  $('register-status').textContent = '';
});

// Session
$('session-continue').addEventListener('click', () => showMain($('session-welcome').dataset.user));
$('session-new').addEventListener('click', async () => { await window.astra.auth.logout(); showLogin(); });

// Chat
$('chat-send').addEventListener('click', async () => {
  const input = $('chat-input').value.trim();
  if (!input) return;
  $('chat-input').value = '';
  addMessage(input, 'user');
  addTyping();
  const response = await processInput(input);
  removeTyping();
  addMessage(response, 'astra');
  $('chat-display').scrollTop = $('chat-display').scrollHeight;
});

$('chat-input').addEventListener('keydown', e => { if (e.key === 'Enter') $('chat-send').click(); });

// Sidebar navigation
$$$('.nav-item[data-view]').forEach(item => {
  item.addEventListener('click', () => switchView(item.dataset.view));
});

// Title bar buttons
$('btn-minimize').addEventListener('click', () => window.astra.window.minimize());
$('btn-maximize').addEventListener('click', () => window.astra.window.maximize());
$('btn-close').addEventListener('click', () => window.astra.window.close());
$('login-close').addEventListener('click', () => window.astra.window.close());
$('session-close').addEventListener('click', () => window.astra.window.close());
$('register-close-x').addEventListener('click', () => window.astra.window.close());

// Logout
$('btn-logout').addEventListener('click', async () => {
  await window.astra.auth.logout();
  showLogin();
});

// System refresh
$('sys-refresh').addEventListener('click', loadSystemInfo);

// Custom app
$('app-custom-btn').addEventListener('click', async () => {
  const name = $('app-custom-input').value.trim();
  if (!name) return;
  const r = await window.astra.app.open(name);
  if (!r.ok) $('app-status').textContent = `No se pudo abrir "${name}".`;
  else { $('app-status').textContent = ''; $('app-custom-input').value = ''; }
});
$('app-custom-input').addEventListener('keydown', e => { if (e.key === 'Enter') $('app-custom-btn').click(); });

// Theme
$('btn-toggle-theme').addEventListener('click', () => {
  if (currentTheme === 'Light') {
    document.body.classList.add('dark');
    currentTheme = 'Dark';
    $('btn-toggle-theme').textContent = 'Cambiar a modo claro';
  } else {
    document.body.classList.remove('dark');
    currentTheme = 'Light';
    $('btn-toggle-theme').textContent = 'Cambiar a modo oscuro';
  }
});

// Toast
$('toast-close').addEventListener('click', () => $('reminder-toast').classList.add('hidden'));

// Reminders
window.astra.onReminder((msg) => { showToast(msg); });

// Init
(async function init() {
  const sessionUser = await window.astra.auth.session();
  if (sessionUser) {
    $('session-welcome').textContent = '¡Bienvenido de nuevo!';
    $('session-welcome').dataset.user = sessionUser;
    $('session-msg').textContent = '¿Quieres continuar tu sesión?';
    $('session-dialog').classList.remove('hidden');
    $('login-screen').classList.add('hidden');
  }
})();
