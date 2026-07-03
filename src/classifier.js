const LANG = require('./i18n');

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

const JOKES = [
  ["Why don't scientists trust atoms?", "Because they make up everything!"],
  ["Did you hear about the mathematician who's afraid of negative numbers?", "He'll stop at nothing to avoid them!"],
  ["Why did the scarecrow win an award?", "Because he was outstanding in his field!"],
  ["What do you call fake spaghetti?", "An impasta!"],
  ["Why did the bicycle fall over?", "Because it was two-tired!"],
  ["¿Por qué los científicos no confían en los átomos?", "¡Porque todo lo inventan!"],
  ["¿Qué hace una abeja en el gimnasio?", "Zum-ba"],
  ["¿Cómo se dice 'poco' en alemán?", "Poco no sé, pero 'mucho' es 'sehr'."],
  ["¿Qué le dice un semáforo a otro?", "No me mires, me estoy cambiando."]
];

const QUOTES = [
  ["The greatest glory in living lies not in never falling, but in rising every time we fall.", "Nelson Mandela"],
  ["The way to get started is to quit talking and begin doing.", "Walt Disney"],
  ["Life is what happens when you're busy making other plans.", "John Lennon"],
  ["The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"],
  ["In the middle of every difficulty lies opportunity.", "Albert Einstein"],
  ["No importa qué tan lento vayas, mientras no te detengas.", "Confucio"],
  ["El éxito es la suma de pequeños esfuerzos repetidos día tras día.", "Robert Collier"],
  ["Cree que puedes y ya estás a medio camino.", "Theodore Roosevelt"]
];

class IntentClassifier {
  constructor() {
    this.patterns = {
      greeting: {
        patterns: [
          /\b(hello|hi|hey|good morning|good afternoon|good evening|howdy)\b/i,
          /\b(hola|buenos días|buenas|qué tal|saludos|hey|buenas tardes|buenas noches)\b/i
        ],
        handler: () => LANG.greeting_responses[Math.floor(Math.random() * LANG.greeting_responses.length)]
      },
      time: {
        patterns: [/\b(what.*time|current time|time now|tell.*time)\b/i, /\b(qué hora|hora actual|hora es|dime.*hora|hora ahora)\b/i],
        handler: () => {
          const now = new Date();
          return _('time_response', { time: now.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' }) });
        }
      },
      date: {
        patterns: [/\b(what.*date|current date|today.*date|what day)\b/i, /\b(qué fecha|fecha actual|qué día|día es hoy|a qué día)\b/i],
        handler: () => {
          const now = new Date();
          return _('date_response', { date: now.toLocaleDateString('es-ES', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }) });
        }
      },
      system_info: {
        patterns: [/\b(system specs|system info|system information|specs|sysinfo|computer info|pc specs|hardware)\b/i, /\b(especificaciones|info del sistema|información del sistema|especs|hardware|componentes)\b/i],
        handler: 'system:full'
      },
      cpu: {
        patterns: [/\b(cpu usage|cpu|processor|how.*cpu)\b/i, /\b(cpu|procesador|uso.*cpu|uso.*procesador)\b/i],
        handler: 'system:cpu'
      },
      memory: {
        patterns: [/\b(ram|memory|how.*ram|memory usage|available memory)\b/i, /\b(ram|memoria|uso.*ram|uso.*memoria|memoria disponible)\b/i],
        handler: 'system:memory'
      },
      uptime: {
        patterns: [/\b(uptime|how long.*(on|running|up)|since.*(boot|start))\b/i, /\b(tiempo activo|encendido desde|cuánto.*(encendido|activo|prendido)|desde.*inicio)\b/i],
        handler: 'system:uptime'
      },
      search: {
        patterns: [/\b(search|search for|look up|find|google|look for)\b/i, /\b(buscar|búsca|encuentra|googlear|busca)\b/i],
        handler: 'search'
      },
      wikipedia: {
        patterns: [/\b(wikipedia|wiki|summary of|tell me about)\b/i, /\b(wikipedia|wiki|resumen de|cuéntame sobre|dime sobre|qué es)\b/i],
        handler: 'wikipedia'
      },
      open_app: {
        patterns: [/\b(open|run|launch|start)\b/i, /\b(abrir|ejecutar|lanzar|iniciar|abre|ejecuta)\b/i],
        handler: 'open_app'
      },
      reminder: {
        patterns: [/\b(remind|reminder|set reminder|remind me)\b/i, /\b(recordar|recordatorio|recuérdame|pon recordatorio|crea recordatorio)\b/i],
        handler: 'reminder'
      },
      joke: {
        patterns: [/\b(joke|funny|make me laugh|tell.*joke)\b/i, /\b(chiste|chistes|broma|hazme reír|cuenta.*chiste|dime.*chiste)\b/i],
        handler: () => {
          const j = JOKES[Math.floor(Math.random() * JOKES.length)];
          return `${j[0]}\n${j[1]}`;
        }
      },
      quote: {
        patterns: [/\b(quote|inspirational|motivation|inspire)\b/i, /\b(cita|frase|inspiración|motivación|inspira)\b/i],
        handler: () => {
          const q = QUOTES[Math.floor(Math.random() * QUOTES.length)];
          return `"${q[0]}"\n— ${q[1]}`;
        }
      },
      about: {
        patterns: [/\b(who are you|what are you|about you|your name|what can you do)\b/i, /\b(quién eres|qué eres|qué puedes hacer|cómo te llamas|tú quién eres)\b/i],
        handler: () => LANG.about_responses[Math.floor(Math.random() * LANG.about_responses.length)]
      },
      thanks: {
        patterns: [/\b(thank|thanks|thank you|appreciate|grateful)\b/i, /\b(gracias|muchas gracias|te agradezco|agradecido)\b/i],
        handler: () => LANG.thanks_responses[Math.floor(Math.random() * LANG.thanks_responses.length)]
      },
      goodbye: {
        patterns: [/\b(bye|goodbye|see you|farewell)\b/i, /\b(adiós|chao|hasta luego|nos vemos|hasta pronto)\b/i],
        handler: () => _('goodbye')
      },
      help: {
        patterns: [/\b(help|commands|what can you do|capabilities|features)\b/i, /\b(ayuda|comandos|qué puedes hacer|capacidades|funciones|qué haces)\b/i],
        handler: () => _('help_text')
      }
    };
  }

  classify(input) {
    const lower = input.toLowerCase().trim();
    for (const [intent, config] of Object.entries(this.patterns)) {
      for (const pattern of config.patterns) {
        if (pattern.test(lower)) return { intent, config };
      }
    }
    return { intent: 'unknown', config: null };
  }

  async process(input) {
    const { intent, config } = this.classify(input);
    if (!config) return this._unknown(input);
    const handler = config.handler;

    if (typeof handler === 'string') {
      if (handler === 'system:full') return this._systemInfo();
      if (handler === 'system:cpu' || handler === 'system:memory' || handler === 'system:uptime') {
        return this._systemResponse(handler);
      }
      if (handler === 'search') return this._extractQuery(input, ['search for', 'search', 'look up', 'look for', 'find', 'google', 'buscar', 'búsca', 'encuentra', 'googlea'], 'search');
      if (handler === 'wikipedia') return this._extractQuery(input, ['summary of', 'tell me about', 'wikipedia', 'wiki', 'resumen de', 'cuéntame sobre', 'dime sobre', 'qué es'], 'wikipedia');
      if (handler === 'open_app') return this._extractQuery(input, ['open', 'run', 'launch', 'start', 'abrir', 'ejecutar', 'lanzar', 'iniciar', 'abre', 'ejecuta'], 'open_app');
      if (handler === 'reminder') return this._handleReminder(input);
    }

    return handler(input);
  }

  async _systemResponse(type) {
    let data;
    if (type === 'system:cpu') data = await window.astra.system.cpu();
    else if (type === 'system:memory') data = await window.astra.system.memory();
    else if (type === 'system:uptime') data = await window.astra.system.uptime();

    if (type === 'system:cpu') return _('cpu_info', { pct: data.percent, phys: data.physical || 0, log: data.logical || 0 });
    if (type === 'system:memory') return _('ram_info', { used: data.used, total: data.total, pct: data.percent });
    if (type === 'system:uptime') return _('uptime_info', { uptime: data.uptime, since: data.since });
  }

  async _systemInfo() {
    const info = await window.astra.system.info();
    return [
      _('sysinfo_label'),
      _('os_label', { os: info.os }),
      _('processor_label', { proc: info.processor }),
      _('cores_label', { phys: info.physicalCores, log: info.logicalCores }),
      _('cpu_label', { pct: info.cpuPercent }),
      _('ram_label', { used: info.ramUsed, total: info.ramTotal, pct: info.ramPercent }),
      _('uptime_label', { uptime: info.uptime })
    ].join('\n');
  }

  _extractQuery(input, prefixes, type) {
    let query = input;
    for (const prefix of prefixes) {
      const idx = input.toLowerCase().indexOf(prefix);
      if (idx >= 0) {
        query = input.slice(idx + prefix.length).trim();
        break;
      }
    }
    if (!query || query === input) {
      if (type === 'search') return _('search_ask');
      if (type === 'wikipedia') return _('wiki_ask');
      if (type === 'open_app') return _('app_ask');
    }
    if (type === 'search') return { action: 'search', query };
    if (type === 'wikipedia') return { action: 'wikipedia', topic: query };
    if (type === 'open_app') return { action: 'open_app', app: query };
  }

  _handleReminder(input) {
    const match = input.match(/(?:in|en)\s+(\d+)\s*(seconds?|secs?|minutes?|mins?|hours?|hrs?|segundos?|minutos?|horas?)/i);
    if (match) {
      const amount = parseInt(match[1]);
      const unit = match[2].toLowerCase();
      let seconds, unitLabel;
      if (unit.startsWith('sec') || unit.startsWith('seg')) { seconds = amount; unitLabel = _('d_seconds'); }
      else if (unit.startsWith('min')) { seconds = amount * 60; unitLabel = _('d_minutes'); }
      else if (unit.startsWith('hr') || unit.startsWith('hor')) { seconds = amount * 3600; unitLabel = _('d_hours'); }
      else return _('reminder_howto');

      const after = input.slice(match.index + match[0].length).trim();
      const msgMatch = after.match(/(?:to|for|que|de|:)\s*(.+)/i);
      const message = msgMatch ? msgMatch[1] : after;
      return { action: 'reminder', seconds, message, amount, unitLabel };
    }
    return _('reminder_howto');
  }

  _unknown(input) {
    const responses = LANG.unknown_responses;
    return responses[Math.floor(Math.random() * responses.length)].replace('{input}', input);
  }
}

module.exports = IntentClassifier;
