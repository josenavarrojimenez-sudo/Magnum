# 🦞 Infraestructura Multi-Agente de Cornelio

**Análisis detallado de la configuración OpenClaw con workspace independiente para Magnum**

---

## 📋 RESUMEN EJECUTIVO

Cornelio configuró una infraestructura **Multi-Agent Routing** de OpenClaw con:
- **2 agentes independientes:** Cornelio (CEO) + Magnum (Brazo Derecho)
- **Workspaces separados** completamente aislados
- **Directorios de agente independientes** (auth, session store)
- **Binding por channel/account** para routing determinístico
- **Shared memory** entre agentes (cross-agent QMD search)

---

## 🏗️ ARQUITECTURA GENERAL

```
┌─────────────────────────────────────────────────────────────────────┐
│                    OpenClaw Gateway (Puerto 18789)                  │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
┌───────────────────▼─────────────┐  ┌──────────────▼──────────────────┐
│         AGENTE CORNELIO         │  │         AGENTE MAGNUM         │
│         =============           │  │         ==========            │
│                                 │  │                                 │
│  ID: "cornelio"                 │  │  ID: "magnum"                   │
│  Rol: CEO Virtual               │  │  Rol: Brazo Derecho             │
│  Default: true ⭐               │  │  Default: false               │
│                                 │  │                                 │
│  Workspace:                     │  │  Workspace:                   │
│  ~/.openclaw/workspace          │  │  ~/.openclaw/workspace-magnum   │
│                                 │  │                                 │
│  AgentDir:                      │  │  AgentDir:                    │
│  ~/.openclaw/agents/cornelio    │  │  ~/.openclaw/agents/magnum    │
│                                 │  │                                 │
│  Archivos:                      │  │  Archivos:                    │
│  ├── SOUL.md (CEO)              │  │  ├── SOUL.md (COO)            │
│  ├── AGENTS.md                  │  │  ├── AGENTS.md                │
│  └── USER.md (Jose)             │  │  ├── USER.md (Jose)           │
│                                 │  │  ├── IDENTITY.md              │
│  Auth:                          │  │  └── docs/                    │
│  └── auth-profiles.json         │  │                                 │
│                                 │  │  Auth:                       │
│  Sessions:                      │  │  └── auth-profiles.json       │
│  ~/.openclaw/agents/cornelio/   │  │                                 │
│  └── sessions/                  │  │  Sessions:                   │
│                                 │  │  ~/.openclaw/agents/magnum/   │
│  Models: Shared                 │  │  └── sessions/                │
│  Memory: Shared + Cross-agent   │  │                                 │
└─────────────────────────────────┘  │  Models: Shared               │
                                     │  Memory: Shared + Cross-agent │
                                     └─────────────────────────────────┘
```

---

## 🔧 CONFIGURACIÓN DETALLADA

### 1. Agente CORNELIO (CEO Virtual)

```json5
{
  id: "cornelio",
  name: "Cornelio - CEO Virtual",
  workspace: "/root/.openclaw/workspace",
  agentDir: "/root/.openclaw/agents/cornelio/agent",
  default: true,  // ← Agent por defecto
  sandbox: { mode: "off" },
  tools: {
    allow: [
      "read", "write", "edit", "exec",
      "sessions_list", "sessions_history", "sessions_send", "sessions_spawn", "sessions_yield",
      "subagents", "agentId",
      "web_search", "web_fetch",
      "memory_search", "memory_get",
      "tts", "image", "process"
    ]
  }
}
```

**Ubicación workspace:** `/root/.openclaw/workspace`  
**Rol:** CEO Virtual - Toma decisiones estratégicas  
**Canal:** Telegram (bot default)

---

### 2. Agente MAGNUM (Brazo Derecho)

```json5
{
  id: "magnum",
  name: "Magnum - Brazo Derecho",
  workspace: "/root/.openclaw/workspace-magnum",
  agentDir: "/root/.openclaw/agents/magnum/agent",
  default: false,
  sandbox: { mode: "off" },
  tools: {
    allow: [
      "read", "write", "edit", "exec",
      "sessions_list", "sessions_history", "sessions_send", "sessions_spawn",
      "subagents", "agentId",
      "web_search", "web_fetch",
      "memory_search", "memory_get",
      "tts", "image", "process"
    ]
    // ← Sin sessions_yield (diferencia vs Cornelio)
  }
}
```

**Ubicación workspace:** `/root/.openclaw/workspace-magnum`  
**Rol:** COO - Ejecutor operativo  
**Canal:** Telegram (bot "magnum")

---

## 🎯 ROUTING (BINDINGS)

Cornelio configuró **bindings determinísticos** por channel/account:

```json5
{
  bindings: [
    // CORNELIO → Telegram bot "default"
    {
      agentId: "cornelio",
      match: { channel: "telegram", accountId: "default" }
    },

    // MAGNUM → Telegram bot "magnum"
    {
      agentId: "magnum",
      match: { channel: "telegram", accountId: "magnum" }
    },

    // CORNELIO → WhatsApp DM específico
    {
      agentId: "cornelio",
      match: {
        channel: "whatsapp",
        peer: { kind: "direct", id: "+50672516680" }
      }
    }
  ]
}
```

**Reglas:**
1. Telegram "default" → Cornelio
2. Telegram "magnum" → Magnum
3. WhatsApp DM → Cornelio

---

## 📦 CHANNELS CONFIGURADOS

### Telegram (2 cuentas/bots)

```json5
{
  telegram: {
    enabled: true,
    dmPolicy: "pairing",
    groups: {
      "*": { requireMention: true }  // ← Siempre requiere @mention en grupos
    },
    accounts: {
      default: {
        botToken: "8579844363:AAGMeemIv7tCvqv5d11kgCUGJgPHbVlxcIE"
      },
      magnum: {
        botToken: "8562696632:AAEkhgiHhZBoOabjlh6Gw9AkbQHWtSx0mec"
      }
    }
  }
}
```

**Bots:**
- **default:** Cornelio (CEO)
- **magnum:** Magnum (COO)

### WhatsApp

```json5
{
  whatsapp: {
    enabled: true,
    dmPolicy: "pairing",
    allowFrom: ["+50672516680"],  // ← Solo Jose
    selfChatMode: false
  }
}
```

---

## 🧠 SHARED MEMORY (Cross-Agent)

Cornelio configuró **cross-agent QMD memory search** para que los agentes puedan acceder a sesiones del otro:

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        qmd: {
          extraCollections: [
            // Colección 1: Sesiones de Cornelio
            {
              path: "/root/.openclaw/agents/cornelio/sessions",
              name: "cornelio-sessions"
            },
            // Colección 2: Sesiones de Magnum
            {
              path: "/root/.openclaw/agents/magnum/sessions",
              name: "magnum-sessions"
            }
          ]
        }
      }
    }
  }
}
```

**Resultado:**
- Magnum puede buscar en las sesiones de Cornelio
- Cornelio puede buscar en las sesiones de Magnum
- Memoria compartida para contexto completo

---

## 📁 ESTRUCTURA DE ARCHIVOS

### Workspace CORNELIO

```
/root/.openclaw/workspace/
├── SOUL.md              # Identidad CEO Virtual
├── AGENTS.md            # Config de agentes
├── USER.md              # Perfil de Jose
├── MEMORY.md            # Memoria general
├── memory/              # Carpeta de memoria
└── .openclaw/           # Config local
```

### Workspace MAGNUM

```
/root/.openclaw/workspace-magnum/
├── SOUL.md              # Identidad COO
├── AGENTS.md            # Config (Brazo Derecho)
├── USER.md              # Perfil de Jose (CEO)
├── IDENTITY.md          # Identidad propia
├── TOOLS.md             # Notas de tools
├── HEARTBEAT.md         # Heartbeat config
├── .fal_credentials.env # API Keys FAL + ElevenLabs
├── memory/              # Carpeta de memoria
├── logs/                # Logs específicos
├── docs/                # Documentación integración
│   └── integration/
│       ├── README.md
│       ├── fal-elevenlabs-lipsync.md
│       └── mission-control-setup.md
├── scripts/             # Scripts específicos
│   └── avatar_video.sh  # Generador de videos
└── .openclaw/           # Config local
```

### AgentDirs

```
/root/.openclaw/agents/
├── cornelio/
│   ├── agent/
│   │   ├── auth-profiles.json
│   │   └── models.json
│   └── sessions/        # Historial de sesiones
├── magnum/
│   ├── agent/
│   │   ├── auth-profiles.json
│   │   └── models.json
│   └── sessions/        # Historial de sesiones
└── main/                # Agente default del sistema
```

---

## 🎤 CONFIGURACIÓN TTS

**Configuración compartida en Gateway:**

```json5
{
  messages: {
    tts: {
      auto: "inbound",      // ← Auto-activo en mensajes entrantes
      provider: "elevenlabs",
      providers: {
        elevenlabs: {
          apiKey: "aa30f405ec0c1ce39707fbf76436b6c932474c6a5985a5693d363e87c1a899f0",
          voiceId: "iwd8AcSi0Je5Quc56ezK",  // ← Mi voz personal
          modelId: "eleven_v3",
          languageCode: "es"
        }
      }
    }
  }
}
```

---

## 🔌 PLUGINS ACTIVADOS

```json5
{
  plugins: {
    entries: {
      openrouter: { enabled: true },
      device-pair: {
        enabled: true,
        config: { publicUrl: "https://webchat.cornelio.app" }
      },
      elevenlabs: { enabled: true },
      ollama: { enabled: true }
    }
  }
}
```

---

## 🤖 MODELOS CONFIGURADOS

### Modelos Compartidos (24 modelos)

**OpenRouter (200+ modelos)**
- Claude (Sonnet, Opus, Haiku)
- GPT-4, GPT-4o, GPT-5 series
- Grok 3/4 series
- Llama 3/4 series
- Gemini 2.5 series
- DeepSeek R1, V3 series
- Y 180+ modelos más...

**Ollama Cloud (24 modelos)**
```
- kim-k2.5:cloud          (reasoning + vision)
- qwen3.5:cloud           (reasoning + vision) ⭐ PRIMARY
- glm-5.1:cloud           (reasoning)
- minimax-m2.7:cloud      (reasoning)
- deepseek-v3.1:cloud     (reasoning)
- gemma4:cloud            (reasoning + vision)
- qwen3-coder-next:cloud  (coding)
- ministral-3:cloud       (reasoning)
- nemotron-3-super:cloud  (reasoning)
- glm-5:cloud             (reasoning)
- minimax-m2.5:cloud      (reasoning)
- gemini-3-flash-preview:cloud (reasoning + vision)
- mistral-large-3:cloud   (reasoning)
- qwen3-vl:cloud           (reasoning + vision)
- devstral-small-2:cloud  (coding)
- qwen3-next:cloud        (reasoning)
- rnj-1:cloud             (coding)
- nemotron-3-nano:cloud   (reasoning)
- devstral-2:cloud        (coding)
- cogito-2.1:cloud        (reasoning)
- glm-4.7:cloud           (reasoning)
- deepseek-v3.2:cloud     (reasoning)
- gpt-oss                 (local, 13GB)
- gpt-oss-safeguard       (local, 13GB)
```

**Configuración primary:**
```json5
{
  model: {
    primary: "ollama/qwen3.5:cloud",
    fallbacks: [
      "ollama/kimi-k2.5:cloud",
      "ollama/glm-5.1:cloud",
      "ollama/minimax-m2.7:cloud",
      // ... 200+ más
    ]
  }
}
```

---

## 🔐 GATEWAY AUTH

```json5
{
  gateway: {
    mode: "local",
    auth: {
      mode: "token",
      token: "10efc37770d09876df18199c0dc1d34eb0a0ce33a9a5c49e"
    },
    port: 18789,
    bind: "lan",  // ← Accessible en LAN
    controlUi: {
      allowInsecureAuth: false,
      allowedOrigins: [
        "http://localhost:18789",
        "http://127.0.0.1:18789",
        "https://webchat.cornelio.app"
      ]
    }
  }
}
```

---

## 🔗 INTEGRACIÓN CON MISSION CONTROL

### Workers Systemd (PAUSADOS)

Cornelio también configuró **workers autónomos** en Mission Control:

```
/opt/mission-control/workers/
├── asterix-worker.sh    # Creative Director (Video/Design)
├── cornelio-worker.sh   # CEO (Estrategia/Decisiones)
└── magnum-worker.sh     # COO (Operaciones)
```

**Services:**
- `/etc/systemd/system/asterix-worker.service`
- `/etc/systemd/system/cornelio-worker.service`
- `/etc/systemd/system/magnum-worker.service`

**Estado actual:** ⏹️ Detenidos (a pedido de Jose)

---

## 🎬 INTEGRACIÓN FAL + ELEVENLABS

### Script Principal

**Ubicación:** `/root/.openclaw/workspace-magnum/scripts/avatar_video.sh`

**Flujo:**
1. ElevenLabs TTS → audio.mp3
2. Upload a tmpfiles.org → URLs públicas
3. FAL AI Lip-sync → video.mp4
4. Download → /tmp/cornelio_video.mp4

**Tiempo:** ~30 segundos

---

## 📊 DIFERENCIAS AGENTES

| Característica | CORNELIO | MAGNUM |
|----------------|----------|--------|
| **Rol** | CEO Virtual | Brazo Derecho (COO) |
| **Default** | ✅ true | ❌ false |
| **Workspace** | `/workspace` | `/workspace-magnum` |
| **Channel** | Telegram default | Telegram "magnum" |
| **Tools** | +sessions_yield | -sessions_yield |
| **Personalidad** | Estratégico | Operativo |
| **Vibe** | Decisor | Ejecutor |
| **Voz** | - | iwd8AcSi0Je5Quc56ezK |
| **Sandbox** | off | off |
| **Reporta a** | Jose | Cornelio |

---

## 🚀 COMANDOS ÚTILES

### Ver agentes

```bash
openclaw agents list --bindings
```

### Status Gateway

```bash
openclaw status
openclaw gateway status
```

### Logs de agentes

```bash
# Logs de Magnum
ls -la /root/.openclaw/agents/magnum/sessions/

# Logs de Cornelio
ls -la /root/.openclaw/agents/cornelio/sessions/
```

### Reiniciar Gateway

```bash
openclaw gateway restart
```

### Ver workers de Mission Control

```bash
mc-status
systemctl status asterix-worker cornelio-worker magnum-worker
```

---

## 🎯 PATRÓN DE TRABAJO MULTI-AGENT

```
┌─────────────────────────────────────────────────────────┐
│                    EJEMPLO DE FLUJO                     │
└─────────────────────────────────────────────────────────┘

Jose envía mensaje → Telegram "magnum" bot
                          │
                          ▼
                    ┌─────────────┐
                    │  BINDING    │
                    │  telegram:  │
                    │  magnum     │
                    └──────┬──────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ AGENT MAGNUM │
                    │  Brazo Der.  │
                    └──────┬───────┘
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
    ┌────────────────┐          ┌────────────────┐
    │ Tarea directa  │          │ Necesita CEO   │
    │ Ejecuta        │          │ Escalar a      │
    └──────┬─────────┘          │ Cornelio       │
           │                    └───────┬────────┘
           │                            │
           ▼                            ▼
    ┌────────────────┐          ┌────────────────┐
    │ Usa tools      │          │ sessions_send  │
    │ (read/exec/)   │          │ a Cornelio     │
    └────────────────┘          └────────────────┘
```

---

## 🔮 POSIBLES MEJORAS

1. **Agent-to-agent messaging** - Activar comunicación directa
2. **Cross-spawn** - Spawnear subagentes de otro workspace
3. **Agent handoff** - Transferir sesión entre agentes
4. **Memory isolation** - Separar memoria por proyecto
5. **Agent-specific models** - Modelos diferentes por agente

---

**Última actualización:** 2026-04-11  
**Análisis por:** Magnum (auto-análisis)  
**Documentación:** OpenClaw Multi-Agent Routing  
**Fuente:** docs.openclaw.ai/concepts/multi-agent

---

**Estado:** ✅ Producción activa  
**Soporte multi-agent:** 100% funcional  
**Aislación:** Completa (workspaces independientes)  
**Cross-memory:** Configurada y operativa
