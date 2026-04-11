# 🚀 Setup de Mission Control - Guía Completa

**Instalación, configuración y deployment de Mission Control para Cornelio.app**

---

## 📋 RESUMEN EJECUTIVO

**Mission Control** es el dashboard open-source para orquestación de agentes AI.

**Características principales:**
- 28 paneles especializados (tasks, agents, logs, tokens, memory, etc.)
- Real-time updates (WebSocket + SSE)
- SQLite database (sin dependencias externas)
- Role-based access (viewer, operator, admin)
- Multi-gateway support

**Stack tecnológico:**
- Next.js 16 (App Router)
- React 19 + Tailwind CSS
- TypeScript 5.7
- SQLite (WAL mode)
- WebSocket + SSE

---

## 🏗️ ARQUITECTURA

```
┌─────────────────────────────────────────────────────────────┐
│              Mission Control (Next.js 16)                   │
│  SQLite (WAL) + WebSocket + SSE                             │
│  Puerto: 3000                                               │
└─────────────────────────────────────────────────────────────┘
         │                    │
         │ x-api-key auth     │ WebSocket (gateway)
         ▼                    ▼
┌─────────────────┐   ┌──────────────────┐
│ Workers (REST)  │   │ OpenClaw Gateway │
│ - asterix       │   │ - Agent sessions │
│ - cornelio      │   │ - Device auth    │
│ - magnum        │   │ - Port: 18789    │
└─────────────────┘   └──────────────────┘
```

---

## 📦 INSTALACIÓN

### Prerrequisitos

```bash
# Docker (requerido)
docker --version

# Node.js 18+ (opcional, para desarrollo)
node --version

# PNPM (opcional, para desarrollo)
pnpm --version
```

### Docker Compose (Producción)

**1. Clonar repositorio:**
```bash
git clone https://github.com/builderz-labs/mission-control.git
cd mission-control
```

**2. Configurar variables de entorno:**
```bash
cp .env.example .env
nano .env
```

**Variables principales:**
```bash
# Server
PORT=3000
MC_API_KEY=b481ff540de108f24868760e79a504421df0ca8c1030b80c512162db00f314e4

# Gateway (OpenClaw)
OPENCLAW_GATEWAY_HOST=host.docker.internal
OPENCLAW_GATEWAY_PORT=18789

# Allowed hosts (producción)
MC_ALLOWED_HOSTS="mission.cornelio.app,31.97.214.129"
```

**3. Iniciar servicios:**
```bash
docker compose up -d
```

**4. Verificar estado:**
```bash
docker compose ps
docker logs mission-control
```

---

## 🔧 CONFIGURACIÓN

### API Key

**Generar API key:**
```bash
# En el container
docker exec mission-control node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

**Usar API key:**
```bash
curl http://localhost:3000/api/agents \
  -H "x-api-key: b481ff540de108f24868760e79a504421df0ca8c1030b80c512162db00f314e4"
```

### Base de Datos

**Ubicación:** `/app/.data/mission-control.db`

**Backup:**
```bash
docker cp mission-control:/app/.data/mission-control.db ./backup.db
```

**Restore:**
```bash
docker cp backup.db mission-control:/app/.data/mission-control.db
docker compose restart mission-control
```

---

## 🤖 AGENTES AUTÓNOMOS

### Crear Agente

```bash
curl -X POST http://localhost:3000/api/agents \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MC_API_KEY" \
  -d '{
    "name": "asterix",
    "role": "creative_director",
    "description": "Creativo de artes, videos e imágenes",
    "status": "online",
    "config": {
      "model": "ollama/qwen3-vl:cloud",
      "tools": ["read", "write", "exec"]
    }
  }'
```

### Workers Systemd

**Ubicación:** `/opt/mission-control/workers/`

**Services:**
- `asterix-worker.service`
- `cornelio-worker.service`
- `magnum-worker.service`

**Comandos:**
```bash
# Iniciar
systemctl start asterix-worker

# Detener
systemctl stop asterix-worker

# Reiniciar
systemctl restart asterix-worker

# Ver estado
systemctl status asterix-worker

# Ver logs
journalctl -u asterix-worker -f
```

---

## 📋 GESTIÓN DE TAREAS

### Crear Tarea

```bash
curl -X POST http://localhost:3000/api/tasks \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MC_API_KEY" \
  -d '{
    "title": "Video lip-sync con ElevenLabs",
    "description": "Generar video con: imagen: /path/to.jpg, voice_id: Adam, texto: \"Hola\"",
    "priority": "high",
    "assigned_to": "asterix",
    "tags": ["fai_ai", "elevenlabs", "tts", "lip_sync"]
  }'
```

### Estados de Tareas

```
inbox → assigned → in_progress → quality_review → done
```

### Comandos Útiles

```bash
# Listar tareas
curl http://localhost:3000/api/tasks \
  -H "x-api-key: $MC_API_KEY" | jq '.tasks[] | {id, title, status}'

# Ver tarea específica
curl http://localhost:3000/api/tasks/1 \
  -H "x-api-key: $MC_API_KEY" | jq .

# Actualizar tarea
curl -X PUT http://localhost:3000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MC_API_KEY" \
  -d '{"status": "done"}'

# Eliminar tarea
curl -X DELETE http://localhost:3000/api/tasks/1 \
  -H "x-api-key: $MC_API_KEY"
```

---

## 🔍 MONITOREO

### Health Check

```bash
curl http://localhost:3000/api/health
```

### Logs

```bash
# Mission Control
docker logs mission-control --tail 50

# Workers
tail -f /opt/mission-control/logs/*.log
```

### Métricas

```bash
# Agentes activos
curl http://localhost:3000/api/agents \
  -H "x-api-key: $MC_API_KEY" | jq '.agents[] | {name, status}'

# Tareas por estado
curl http://localhost:3000/api/tasks \
  -H "x-api-key: $MC_API_KEY" | jq 'group_by(.status) | map({status: .[0].status, count: length})'
```

---

## 🛡️ SEGURIDAD

### Rate Limiting

- **Default:** 100 requests/minuto por IP
- **Headers:** `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

### CSRF Protection

- Mutating requests (`POST`, `PUT`, `DELETE`, `PATCH`) validan `Origin` header
- API key authentication bypassa CSRF

### Host Allowlist

**Producción:**
```bash
MC_ALLOWED_HOSTS="mission.cornelio.app,*.cornelio.app"
```

**Desarrollo:**
```bash
MC_ALLOW_ANY_HOST=1
```

---

## 📊 COMANDOS PERSONALIZADOS

### mc-status

**Ubicación:** `/usr/local/bin/mc-status`

**Uso:**
```bash
mc-status
```

**Output:**
```
╔════════════════════════════════════════════════════════╗
║   📊 REPORTE EJECUTIVO - MISSION CONTROL              ║
║   Cornelio.app | 2026-04-11 16:37:51 UTC              ║
╚════════════════════════════════════════════════════════╝

🤖 AGENTES ACTIVOS:
  • ASTERIX: creative_director | Estado: online
  • MAGNUM: devops | Estado: idle
  • CORNELIO: assistant | Estado: idle

  Total: 3 | Online: 3

📋 TAREAS EN CURSO:
  📥 Inbox: 0
  📤 Assigned: 0
  ⚙️  In Progress: 1
  ✅ Done: 5

🔧 SERVICIOS OPERATIVOS:
  ✅ asterix-worker: Activo
  ✅ cornelio-worker: Activo
  ✅ magnum-worker: Activo
  ✅ Mission Control: Docker corriendo
```

### asterix-task

**Ubicación:** `/usr/local/bin/asterix-task`

**Uso:**
```bash
asterix-task <imagen> <voice> "<texto>"

# Ejemplo:
asterix-task /path/to/avatar.jpg Adam "Hola, soy Cornelio"
```

---

## 🐛 TROUBLESHOOTING

### Mission Control no inicia

```bash
# Ver logs
docker logs mission-control

# Verificar puerto
netstat -tlnp | grep 3000

# Reiniciar
docker compose restart mission-control
```

### Workers no ejecutan tareas

```bash
# Verificar estado
systemctl status asterix-worker

# Ver logs
tail -50 /opt/mission-control/logs/asterix-worker.log

# Reiniciar
systemctl restart asterix-worker
```

### Error de permisos

```bash
# Fixear permisos de datos
docker exec mission-control chown -R nextjs:nodejs /app/.data
```

---

## 📁 ARCHIVOS DE CONFIGURACIÓN

| Archivo | Propósito |
|---------|-----------|
| `/opt/mission-control/docker-compose.yml` | Docker config |
| `/opt/mission-control/.env` | Variables de entorno |
| `/etc/systemd/system/asterix-worker.service` | Systemd service |
| `/opt/mission-control/workers/asterix-worker.sh` | Worker script |
| `/root/.openclaw/workspace-magnum/scripts/avatar_video.sh` | Script lip-sync |

---

## 📞 SOPORTE

**Documentación oficial:**
- Mission Control: https://mintlify.wiki/builderz-labs/mission-control
- GitHub: https://github.com/builderz-labs/mission-control

**Comunidad:**
- Discord: https://discord.gg/...

---

**Última actualización:** 2026-04-11  
**Autor:** Magnum  
**Estado:** ✅ Producción
