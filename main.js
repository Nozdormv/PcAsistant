const { app, BrowserWindow, ipcMain, shell, Notification, Tray, Menu, globalShortcut, nativeImage } = require('electron');
const path = require('path');
const fs = require('fs');
const crypto = require('crypto');
const { exec } = require('child_process');
const si = require('systeminformation');

let mainWindow, tray;
const USER_DATA_PATH = path.join(app.getPath('appData'), 'Astra');
const CREDENTIALS_FILE = path.join(USER_DATA_PATH, 'credentials_salted.json');
const SESSION_FILE = path.join(USER_DATA_PATH, 'session.json');
const LOG_FILE = path.join(USER_DATA_PATH, 'astra.log');
const LANG = require('./src/i18n');
const IntentClassifier = require('./src/classifier');

const classifier = new IntentClassifier();

function log(level, msg) {
  const ts = new Date().toISOString().replace('T', ' ').slice(0, 19);
  const line = `${ts} [${level}] ${msg}\n`;
  try {
    fs.mkdirSync(USER_DATA_PATH, { recursive: true });
    fs.appendFileSync(LOG_FILE, line);
  } catch (e) {}
}

// Capture unhandled errors to log
process.on('uncaughtException', err => {
  log('ERROR', `Uncaught exception: ${err.message}\n${err.stack}`);
});
process.on('unhandledRejection', (reason) => {
  log('ERROR', `Unhandled rejection: ${reason instanceof Error ? reason.message : reason}\n${reason instanceof Error ? reason.stack : ''}`);
});
const origError = console.error;
console.error = (...args) => {
  log('ERROR', args.map(a => typeof a === 'string' ? a : JSON.stringify(a)).join(' '));
  origError.apply(console, args);
};

function _(key, ...args) {
  let text = LANG[key] || key;
  if (args.length) {
    const obj = args[0];
    for (const k of Object.keys(obj)) {
      text = text.replace(new RegExp(`\\{${k}\\}`, 'g'), obj[k]);
    }
  }
  return text;
}

function hashPassword(password, salt) {
  if (!salt) salt = crypto.randomBytes(16).toString('hex');
  const hash = crypto.createHash('sha256').update(password + salt).digest('hex');
  return { hash, salt };
}

function loadCredentials() {
  try {
    if (!fs.existsSync(CREDENTIALS_FILE)) {
      log('INFO', 'No se encontró credentials, creando usuario demo');
      const { hash, salt } = hashPassword('demo');
      const creds = { demo: { hash, salt } };
      fs.mkdirSync(USER_DATA_PATH, { recursive: true });
      fs.writeFileSync(CREDENTIALS_FILE, JSON.stringify(creds, null, 2));
      log('INFO', 'Usuario demo creado con contraseña demo');
      return creds;
    }
    return JSON.parse(fs.readFileSync(CREDENTIALS_FILE, 'utf-8'));
  } catch (e) {
    log('ERROR', `Error loading credentials: ${e.message}`);
    return {};
  }
}

function saveCredentials(creds) {
  fs.mkdirSync(USER_DATA_PATH, { recursive: true });
  fs.writeFileSync(CREDENTIALS_FILE, JSON.stringify(creds, null, 2));
}

function loadSession() {
  try {
    if (fs.existsSync(SESSION_FILE)) {
      return JSON.parse(fs.readFileSync(SESSION_FILE, 'utf-8')).username;
    }
  } catch (e) { log('ERROR', `Error loading session: ${e.message}`); }
  return null;
}

function saveSession(username) {
  fs.mkdirSync(USER_DATA_PATH, { recursive: true });
  fs.writeFileSync(SESSION_FILE, JSON.stringify({ username }));
}

function clearSession() {
  try { if (fs.existsSync(SESSION_FILE)) fs.unlinkSync(SESSION_FILE); } catch (e) {}
}

function createTray() {
  const iconStr = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAAbwAAAG8B8aLcQwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAEoSURBVDiNpZMxTsNAEEX/rNeOAwUlHVdA4gJcAokLUNDRcAQkLkCBaOgouQIVHZyAgoKSK0QiJI5jr3cohuxarJOU/NJo5s+b2dEuqcpJUZR3AL4BzNXsJ4BhGJ4B2AO4BfAqIhcicl5V1V4URbdDQJNScgXgFsCbqt6JyGfTNLcAnojInYh8ich5XdePx+PxJYDTkr0SkRMS8Q3Aq6q+J+ebqvYAnIjIG4DvX0RE5F5Ecp/P52Fd1491Xb81TfMJYJefBEEQbp1zm5xzBkCq2gbwHobh4263OwPgRUTm/X5/i8SvbZqmBQARWQCYADgQkdcgCBa9Xm+BJFmWZQCAJEkWInII4ENEtlX1W1W/fv8FAwCq2l5eXq4B3IrImYhMAVz+PxAR+QbwCeALwGsYhv8L/gJTYWnDMQC3WQAAAABJRU5ErkJggg==';
  const icon = nativeImage.createFromDataURL(iconStr);
  tray = new Tray(icon);
  tray.setToolTip('Astra - Asistente Personal');

  const contextMenu = Menu.buildFromTemplate([
    { label: 'Mostrar Astra', click: () => { if (mainWindow) { mainWindow.show(); mainWindow.focus(); } } },
    { type: 'separator' },
    { label: 'Salir', click: () => { app.isQuitting = true; app.quit(); } }
  ]);
  tray.setContextMenu(contextMenu);

  tray.on('click', () => {
    if (mainWindow) {
      if (mainWindow.isVisible()) { mainWindow.hide(); }
      else { mainWindow.show(); mainWindow.focus(); }
    }
  });
}

// IPC Handlers
ipcMain.handle('auth:login', (_, username, password) => {
  const creds = loadCredentials();
  if (creds[username]) {
    const { hash, salt } = creds[username];
    const { hash: computed } = hashPassword(password, salt);
    if (computed === hash) {
      log('INFO', `Login exitoso: ${username}`);
      saveSession(username);
      return { ok: true };
    }
    log('ERROR', `Contraseña incorrecta: ${username}`);
    return { ok: false, error: _('login_fail') };
  }
  log('ERROR', `Usuario no encontrado: ${username}`);
  return { ok: false, error: _('login_fail') };
});

ipcMain.handle('auth:register', (_, username, password) => {
  const creds = loadCredentials();
  if (creds[username]) return { ok: false, error: _('register_fail') };
  const { hash, salt } = hashPassword(password);
  creds[username] = { hash, salt };
  saveCredentials(creds);
  log('INFO', `Usuario registrado: ${username}`);
  return { ok: true };
});

ipcMain.handle('auth:session', () => loadSession());
ipcMain.handle('auth:logout', () => { clearSession(); });

ipcMain.handle('system:info', async () => {
  const [osInfo, cpu, cpuUsage, mem, timeData] = await Promise.all([
    si.osInfo(), si.cpu(), si.currentLoad(), si.mem(), si.time()
  ]);
  const boot = new Date(timeData.uptime * 1000);
  const diff = Date.now() - boot.getTime();
  const days = Math.floor(diff / 86400000);
  const hours = Math.floor((diff % 86400000) / 3600000);
  const mins = Math.floor((diff % 3600000) / 60000);
  return {
    os: `${osInfo.platform} ${osInfo.release}`,
    processor: `${cpu.manufacturer} ${cpu.brand}`,
    physicalCores: cpu.physicalCores,
    logicalCores: cpu.cores,
    cpuPercent: cpuUsage.currentLoad.toFixed(1),
    ramUsed: (mem.used / 1024 / 1024 / 1024).toFixed(1),
    ramTotal: (mem.total / 1024 / 1024 / 1024).toFixed(1),
    ramPercent: mem.usedPercent.toFixed(1),
    uptime: `${days}d ${hours}h ${mins}m`
  };
});

ipcMain.handle('system:cpu', async () => {
  const [cpu, load] = await Promise.all([si.cpu(), si.currentLoad()]);
  return { percent: load.currentLoad.toFixed(1), physical: cpu.physicalCores, logical: cpu.cores };
});

ipcMain.handle('system:memory', async () => {
  const mem = await si.mem();
  return { used: (mem.used / 1024 / 1024 / 1024).toFixed(1), total: (mem.total / 1024 / 1024 / 1024).toFixed(1), percent: mem.usedPercent.toFixed(1) };
});

ipcMain.handle('system:uptime', async () => {
  const timeData = await si.time();
  const boot = new Date(timeData.uptime * 1000);
  const diff = Date.now() - boot.getTime();
  const days = Math.floor(diff / 86400000);
  const hours = Math.floor((diff % 86400000) / 3600000);
  const mins = Math.floor((diff % 3600000) / 60000);
  return {
    uptime: `${days}d ${hours}h ${mins}m`,
    since: boot.toLocaleDateString('es-ES', { weekday: 'long', day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit' })
  };
});

ipcMain.handle('search:web', (_, query) => {
  shell.openExternal(`https://www.google.com/search?q=${encodeURIComponent(query)}`);
});

ipcMain.handle('search:wikipedia', async (_, topic) => {
  try {
    const resp = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(topic)}`);
    if (!resp.ok) throw new Error('Not found');
    const data = await resp.json();
    return { ok: true, summary: data.extract.split('\n').slice(0, 5).join('\n') };
  } catch (e) {
    return { ok: false, error: _('wiki_notfound', { topic }) };
  }
});

const ALLOWED_APPS = {
  notepad: 'notepad.exe', calculator: 'calc.exe', paint: 'mspaint.exe',
  cmd: 'cmd.exe', 'command prompt': 'cmd.exe', explorer: 'explorer.exe',
  'file explorer': 'explorer.exe', chrome: 'chrome.exe', firefox: 'firefox.exe',
  edge: 'msedge.exe', discord: 'Discord.exe', spotify: 'Spotify.exe',
  'task manager': 'taskmgr.exe', 'control panel': 'control.exe',
  calculadora: 'calc.exe', 'bloc de notas': 'notepad.exe',
  'símbolo del sistema': 'cmd.exe', explorador: 'explorer.exe',
  'administrador de tareas': 'taskmgr.exe', 'panel de control': 'control.exe',
};

ipcMain.handle('app:open', (_, appName) => {
  const lower = appName.toLowerCase();
  if (ALLOWED_APPS[lower]) {
    exec(ALLOWED_APPS[lower], (err) => { if (err) log('ERROR', `Error abriendo ${appName}: ${err.message}`); });
    return { ok: true, app: appName };
  }
  return { ok: false, app: appName };
});

ipcMain.handle('process:chat', (_, input) => classifier.process(input));

ipcMain.handle('reminder:set', (_, { seconds, message }) => {
  setTimeout(() => {
    if (mainWindow) {
      mainWindow.webContents.send('reminder:fire', message);
      if (!mainWindow.isVisible()) {
        new Notification({ title: 'Astra - Recordatorio', body: message }).show();
      }
    }
  }, seconds * 1000);
});

ipcMain.handle('settings:save', (_, { ttsSpeed }) => {
  log('INFO', `Config guardada: ttsSpeed=${ttsSpeed}`);
});

// Window controls
ipcMain.handle('window:minimize', () => { if (mainWindow) mainWindow.minimize(); });
ipcMain.handle('window:maximize', () => {
  if (mainWindow) mainWindow.isMaximized() ? mainWindow.unmaximize() : mainWindow.maximize();
});
ipcMain.handle('window:close', () => { if (mainWindow) mainWindow.hide(); });

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 900,
    height: 620,
    minWidth: 720,
    minHeight: 480,
    frame: false,
    title: 'Astra',
    backgroundColor: '#f3f3f3',
    show: false,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false
    }
  });

  mainWindow.loadFile(path.join(__dirname, 'src', 'index.html'));

  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  mainWindow.on('close', (e) => {
    if (!app.isQuitting) {
      e.preventDefault();
      mainWindow.hide();
    }
  });

  mainWindow.on('maximize', () => {
    mainWindow.webContents.send('window:maximized');
  });
  mainWindow.on('unmaximize', () => {
    mainWindow.webContents.send('window:unmaximized');
  });
}

app.whenReady().then(() => {
  log('INFO', '=== Astra iniciado ===');
  createWindow();
  createTray();

  globalShortcut.register('Shift+CommandOrControl+A', () => {
    if (mainWindow) {
      if (mainWindow.isVisible()) { mainWindow.hide(); }
      else { mainWindow.show(); mainWindow.focus(); }
    }
  });

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
    else if (mainWindow) { mainWindow.show(); mainWindow.focus(); }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

app.on('before-quit', () => {
  app.isQuitting = true;
  globalShortcut.unregisterAll();
});
