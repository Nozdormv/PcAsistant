const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('astra', {
  auth: {
    login: (user, pass) => ipcRenderer.invoke('auth:login', user, pass),
    register: (user, pass) => ipcRenderer.invoke('auth:register', user, pass),
    session: () => ipcRenderer.invoke('auth:session'),
    logout: () => ipcRenderer.invoke('auth:logout')
  },
  system: {
    info: () => ipcRenderer.invoke('system:info'),
    cpu: () => ipcRenderer.invoke('system:cpu'),
    memory: () => ipcRenderer.invoke('system:memory'),
    uptime: () => ipcRenderer.invoke('system:uptime')
  },
  search: {
    web: (q) => ipcRenderer.invoke('search:web', q),
    wikipedia: (t) => ipcRenderer.invoke('search:wikipedia', t)
  },
  app: {
    open: (name) => ipcRenderer.invoke('app:open', name)
  },
  process: {
    chat: (input) => ipcRenderer.invoke('process:chat', input)
  },
  reminder: {
    set: (data) => ipcRenderer.invoke('reminder:set', data)
  },
  settings: {
    save: (data) => ipcRenderer.invoke('settings:save', data)
  },
  window: {
    minimize: () => ipcRenderer.invoke('window:minimize'),
    maximize: () => ipcRenderer.invoke('window:maximize'),
    close: () => ipcRenderer.invoke('window:close')
  },
  onReminder: (callback) => {
    ipcRenderer.on('reminder:fire', (_, msg) => callback(msg));
  }
});
