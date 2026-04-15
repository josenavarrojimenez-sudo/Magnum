# Lecciones Aprendidas - Magnum

## 2026-04-15: Presets de Modelos - Configuración Rápida por Caso de Uso

---

### 📋 Contexto

**Objetivo:** Crear un sistema de presets de modelos IA para cambiar rápidamente la configuración según el tipo de tarea (coding, frontend, web search, razonamiento, chat, matemáticos, financieros, imágenes, videos).

**Solicitado por:** Jose Navarro  
**Fecha:** 2026-04-15

---

### 🎯 Presets Creados

| # | Preset | Primary | Fallbacks | Caso de Uso |
|---|--------|---------|-----------|-------------|
| 1 | `coding` | `openrouter/moonshotai/kimi-k2.5` | 3 modelos | Desarrollo de código |
| 2 | `frontend` | `openrouter/google/gemini-3-flash-preview` | 7 modelos | Frontend/UI/UX |
| 3 | `web-search` | `openrouter/bytedance-seed/seed-2.0-lite` | 2 modelos | Búsqueda web |
| 4 | `razonar` | `ollama/minimax-m2.5:cloud` | 3 modelos | Razonamiento lógico |
| 5 | `chat` | `ollama/qwen3.5` | 1 modelo | Conversación |
| 6 | `matematicos` | `openrouter/qwen/qwen3.6-plus` | 2 modelos | Matemáticas |
| 7 | `financieros` | `openrouter/qwen/qwen3.6-plus` | 3 modelos | Finanzas |
| 8 | `imagenes` | `openrouter/google/gemini-3.1-flash-image-preview` | 2 modelos | Visión/Imágenes |
| 9 | `videos` | `openrouter/google/veo-3.1` | 4 modelos | Video |
| 10 | `principales` | `ollama/glm-5.1:cloud` | 3 modelos | Default/General |

---

### 📁 Estructura Creada

```
/root/.openclaw/workspace-magnum/
├── presets/modelos/
│   ├── README.md              # Documentación general
│   ├── coding.md              # Preset coding
│   ├── frontend.md            # Preset frontend
│   ├── web-search.md          # Preset web search
│   ├── razonar.md             # Preset razonar
│   ├── chat.md                # Preset chat
│   ├── matematicos.md         # Preset matemáticos
│   ├── financieros.md         # Preset financieros
│   ├── imagenes.md            # Preset imágenes
│   ├── videos.md              # Preset videos
│   └── principales.md         # Preset principales
│
└── skills/apply-preset/
    ├── SKILL.md               # Documentación de la skill
    └── scripts/
        └── apply-preset.sh    # Script de aplicación
```

---

### 🔧 Cómo Usar

#### Comando Directo (Chat)
```
"Quiero los presets de coding"
"Aplica el preset de frontend"
"Cambiar a preset web-search"
```

#### Script CLI
```bash
# Listar presets
/root/.openclaw/workspace-magnum/skills/apply-preset/scripts/apply-preset.sh --list

# Ver detalles
/root/.openclaw/workspace-magnum/skills/apply-preset/scripts/apply-preset.sh --show coding

# Aplicar preset
/root/.openclaw/workspace-magnum/skills/apply-preset/scripts/apply-preset.sh coding
```

---

### ⚠️ Importante

1. **Requiere reinicio:** Después de aplicar un preset, reiniciar gateway:
   ```bash
   openclaw gateway restart
   ```

2. **Backup automático:** El script crea backup en `/root/.openclaw/backups/modelos/`

3. **GitHub sync:** Los presets deben subirse al repositorio:
   ```bash
   cd /root/.openclaw/workspace-magnum
   git add presets/modelos/
   git commit -m "Presets de modelos - 2026-04-15"
   git push
   ```

---

### 📝 Notas

- Cada preset incluye archivo `.md` con documentación y bloque JSON aplicable
- La skill `apply-preset` está documentada en `skills/apply-preset/SKILL.md`
- Los presets resuelven el problema de tener que editar `openclaw.json` manualmente
- Futura mejora: Aplicación automática con validación de modelos disponibles

---

## 2026-04-14: Mission Control + OpenClaw Gateway - Problema de Autenticación "Pairing Required"

---

### 📋 Contexto

**Objetivo:** Configurar Mission Control (dashboard multi-agente) para que se conecte al Gateway OpenClaw existente en el VPS de Hostinger.

**Arquitectura:**
- **OpenClaw Gateway:** `127.0.0.1:18789` (loopback)
- **Mission Control:** Docker en `/opt/mission-control` (puerto 3000)
- **Nginx:** Proxy inverso para ambos servicios
- **URLs públicas:**
  - `https://mission.cornelio.app` → Mission Control UI
  - `https://gateway.cornelio.app` → OpenClaw Gateway WebSocket

---

### ❌ Problemas Encontrados

#### 1. Error "pairing required" en WebSocket

**Síntoma:**
```
Gateway error: pairing required
WebSocket error occurred
Handshake failed on root path
```

**Causas raíz (múltiples, en cascada):**

| # | Causa | Descripción |
|---|-------|-------------|
| 1 | **Origin header incorrecto** | Nginx enviaba `origin: https://mission.cornelio.app` en lugar de `gateway.cornelio.app` |
| 2 | **Token incorrecto en Mission Control** | El `.env` tenía el token viejo (`10efc37770d...`) en lugar del token emparejado (`Gvu6M2Df70y...`) |
| 3 | **DeviceId cambiante** | Mission Control genera un nuevo `deviceId` cada vez que se reinicia o cambia de navegador |
| 4 | **Device no aprobado** | El dispositivo aparecía en `paired.json` pero con estado "pending" - requería aprobación manual |

---

### 🔧 Solución Aplicada (Paso a Paso)

#### Paso 1: Corregir Nginx Origin Header

**Problema:** El proxy Nginx en `mission.cornelio.app` no estaba cambiando el header `Origin`, causando que OpenClaw rechazara la conexión.

**Solución:** Agregar `proxy_set_header Origin` en la config de Nginx:

```nginx
# /etc/nginx/sites-available/mission.cornelio.app
location /gateway-ws {
    proxy_pass http://127.0.0.1:18789;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Origin https://gateway.cornelio.app;  # ← CLAVE
    proxy_read_timeout 86400;
    proxy_buffering off;
    proxy_cache off;
}
```

**Comando:**
```bash
# Recargar Nginx
/usr/sbin/nginx -s reload
```

---

#### Paso 2: Corregir Token en Mission Control

**Problema:** El token en `/opt/mission-control/.env` no coincidía con el token emparejado en OpenClaw.

**Token incorrecto:** `10efc37770d09876df18199c0dc1d34eb0a0ce33a9a5c49e`
**Token correcto:** `Gvu6M2Df70yodXcfxI5KYltbttcUx6z9goCcMaU7Ff0`

**Solución:**
```bash
# 1. Editar .env de Mission Control
# Cambiar: OPENCLAW_GATEWAY_TOKEN=10efc37770d...
# Por: OPENCLAW_GATEWAY_TOKEN=Gvu6M2Df70y...

# 2. Actualizar config.json dentro del contenedor
docker exec mission-control sh -c "
cat > /app/.data/config.json << 'EOF'
{\"gateway\": {\"host\": \"gateway.cornelio.app\", \"port\": 443, \"token\": \"Gvu6M2Df70yodXcfxI5KYltbttcUx6z9goCcMaU7Ff0\", \"mode\": \"gateway\"}}
EOF
"

# 3. Reiniciar Mission Control
docker restart mission-control
```

---

#### Paso 3: Obtener DeviceId Actual de Mission Control

**Problema:** Mission Control genera un nuevo `deviceId` basado en el navegador/sesión. Hay que obtener el deviceId ACTUAL que está usando.

**Solución:**
```bash
# Ver logs de OpenClaw para obtener el deviceId actual
tail -20 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep "deviceId" | tail -1

# Ejemplo de output:
# "deviceId":"889b37f866e09a32ffd8aad358b62cfbeebf8057b4b2233f33cd3bbf3734e0ca"
```

**Nota:** El deviceId puede cambiar si:
- Se borra el localStorage del navegador
- Se usa incógnito/privado
- Se cambia de navegador
- Se reinicia Mission Control

---

#### Paso 4: Agregar DeviceId a paired.json

**Problema:** El deviceId de Mission Control no estaba en `/root/.openclaw/devices/paired.json`.

**Solución:**
```bash
python3 << 'EOF'
import json
import time

# Leer paired.json existente
with open('/root/.openclaw/devices/paired.json', 'r') as f:
    paired = json.load(f)

# DeviceId de Mission Control (obtener del log)
device_id = "889b37f866e09a32ffd8aad358b62cfbeebf8057b4b2233f33cd3bbf3734e0ca"

# Token correcto
token = "Gvu6M2Df70yodXcfxI5KYltbttcUx6z9goCcMaU7Ff0"

# Crear entrada
new_device = {
    "deviceId": device_id,
    "publicKey": "MC-placeholder-key-for-mission-control",
    "platform": "web",
    "clientId": "mission-control",
    "clientMode": "browser",
    "displayName": "Mission Control",
    "role": "operator",
    "roles": ["operator"],
    "scopes": ["operator.admin", "operator.read", "operator.write", "operator.pairing"],
    "approvedScopes": ["operator.admin", "operator.read", "operator.write", "operator.pairing"],
    "tokens": {
        "operator": {
            "token": token,
            "role": "operator",
            "scopes": ["operator.admin", "operator.read", "operator.write", "operator.pairing"],
            "createdAtMs": int(time.time() * 1000),
            "rotatedAtMs": int(time.time() * 1000)
        }
    },
    "createdAtMs": int(time.time() * 1000),
    "approvedAtMs": int(time.time() * 1000)
}

# Agregar y guardar
paired[device_id] = new_device
with open('/root/.openclaw/devices/paired.json', 'w') as f:
    json.dump(paired, f, indent=2)

print(f"✅ Device {device_id[:16]}... agregado")
EOF
```

---

#### Paso 5: Aprobar Dispositivo Pendiente

**Problema:** El dispositivo aparecía como "Pending" en `openclaw devices list` - requería aprobación manual.

**Solución:**
```bash
# 1. Ver dispositivos pendientes
openclaw devices list

# Output ejemplo:
# Pending (1)
# ┌──────────────────────────────────────┬─────────────────┬──────────┐
# │ 307c2542-6e58-461f-84a3-a02536518452 │ Mission Control │ operator │
# └──────────────────────────────────────┴─────────────────┴──────────┘

# 2. Aprobar el dispositivo (usar el request ID)
openclaw devices approve 307c2542-6e58-461f-84a3-a02536518452

# Output:
# Approved 889b37f866e09a32... (307c2542-6e58-461f-84a3-a02536518452)

# 3. Verificar que está aprobado
openclaw devices list
# Ahora aparece en "Paired" en lugar de "Pending"
```

---

#### Paso 6: Verificar Conexión

**Comandos de verificación:**
```bash
# 1. Ver logs de OpenClaw (debería NO haber más "pairing required")
tail -20 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep -i "pairing"

# 2. Ver estado de dispositivos
openclaw devices list

# 3. Ver logs de Mission Control
docker logs mission-control --tail 30

# 4. En la UI: https://mission.cornelio.app
# - Gateway debe mostrar 🟢 verde
# - "Gateway connected" en el dashboard
```

---

### ✅ Resultado Final

| Ítem | Estado |
|------|--------|
| Gateway | ✅ Conectado |
| Autenticación | ✅ Aprobada |
| WebSocket | ✅ Funcionando (con fallback a /gateway-ws) |
| Agentes | ✅ 8 registrados |

---

### 📝 Fórmula Correcta (Resumen Ejecutivo)

Para conectar Mission Control a OpenClaw Gateway:

```bash
# 1. Nginx - Origin header correcto
# /etc/nginx/sites-available/mission.cornelio.app
location /gateway-ws {
    proxy_set_header Origin https://gateway.cornelio.app;
}

# 2. Mission Control - Token correcto
# /opt/mission-control/.env
OPENCLAW_GATEWAY_TOKEN=<token_de_paired.json>

# 3. paired.json - DeviceId + Token
# /root/.openclaw/devices/paired.json
{
  "<deviceId_de_logs>": {
    "deviceId": "<deviceId>",
    "tokens": {"operator": {"token": "<token>"}},
    "approvedScopes": ["operator.admin", "operator.read", "operator.write", "operator.pairing"]
  }
}

# 4. Aprobar dispositivo
openclaw devices approve <request_id>

# 5. Recargar Nginx + Reiniciar Mission Control
/usr/sbin/nginx -s reload
docker restart mission-control
```

---

### 🔍 Referencias GitHub Issues

Issues que confirmaron el problema y solución:

1. **Issue #39649**: "Control UI can hit device signature invalid after upgrade even with valid gateway token"
   - Confirma que el device identity puede volverse inválido después de upgrades
   - Solución: Aprobar manualmente el dispositivo

2. **Issue #46132**: "Dashboard permanently shows token mismatch / authentication lockout"
   - Confirma que el token debe coincidir exactamente entre config y paired.json

---

### ⚠️ Errores Comunes a Evitar

| Error | Síntoma | Solución |
|-------|---------|----------|
| Origin header incorrecto | `pairing required` | Agregar `proxy_set_header Origin` en Nginx |
| Token incorrecto | `pairing required` | Verificar token en `paired.json` y `.env` |
| DeviceId no emparejado | `not-paired` | Agregar deviceId a `paired.json` |
| Dispositivo pendiente | `Pending` en `openclaw devices list` | Ejecutar `openclaw devices approve <id>` |
| Browser cache viejo | `device signature invalid` | Usar incógnito o borrar localStorage |

---

### ️ Comandos Útiles (Cheat Sheet)

```bash
# Ver logs de OpenClaw en tiempo real
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log

# Ver dispositivos emparejados
openclaw devices list

# Aprobar dispositivo pendiente
openclaw devices approve <request_id>

# Ver logs de Mission Control
docker logs mission-control --tail 50 -f

# Reiniciar Mission Control
docker restart mission-control

# Recargar Nginx
/usr/sbin/nginx -s reload

# Verificar config de Nginx
nginx -t
```

---

### 📚 Archivos Modificados

| Archivo | Propósito |
|---------|-----------|
| `/etc/nginx/sites-available/mission.cornelio.app` | Proxy Nginx con Origin header |
| `/opt/mission-control/.env` | Token de Gateway |
| `/opt/mission-control/.data/config.json` | Config de Gateway (dentro del contenedor) |
| `/root/.openclaw/devices/paired.json` | Dispositivos emparejados |
| `/etc/hosts` | DNS local para `gateway.cornelio.app` |

---

**Fecha:** 2026-04-14 21:11 UTC
**Autor:** Magnum
**Estado:** ✅ Resuelto
**Tiempo de resolución:** ~2 horas
**Dificultad:** Alta (múltiples causas en cascada)
