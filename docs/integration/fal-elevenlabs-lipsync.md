# 🎬 Integración FAL AI + ElevenLabs para Lip-Sync

**Documentación completa del flujo de generación de videos con lip-sync**

---

## 📋 RESUMEN EJECUTIVO

**Objetivo:** Generar videos de avatares con lip-sync automático usando:
- **ElevenLabs TTS** → Conversión de texto a voz
- **FAL AI** → Lip-sync de imagen + audio

**Tiempo promedio:** ~30 segundos por video

---

## 🏗️ ARQUITECTURA

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUJO COMPLETO                           │
└─────────────────────────────────────────────────────────────┘

1. INPUT
   ├── Imagen: /path/to/avatar.jpg
   ├── Voice: Adam (ElevenLabs)
   └── Texto: "Hola, soy Cornelio"

2. ElevenLabs TTS (FAL AI)
   ├── POST: queue.fal.run/fal-ai/elevenlabs/tts/multilingual-v2
   ├── Request ID → Polling cada 2s
   └── Output: audio.mp3 (URL)

3. Upload a tmpfiles.org
   ├── Imagen redimensionada (1024px)
   └── Audio TTS
   └── Output: URLs públicas HTTPS

4. FAL Lip-Sync
   ├── POST: queue.fal.run/veed/fabric-1.0
   ├── Request ID → Polling cada 3s
   └── Output: video.mp4 (URL)

5. DOWNLOAD
   └── /tmp/cornelio_video.mp4
```

---

## 🔧 CONFIGURACIÓN

### API Keys

```bash
# FAL AI Key
FAL_KEY="9ed6f67a-1b81-479c-ac60-bc5382b4214e:4070adfcc70064f32bcaf82ceb1275cd"

# Endpoints
FAL_TTS_ENDPOINT="queue.fal.run/fal-ai/elevenlabs/tts/multilingual-v2"
FAL_LIPSYNC_ENDPOINT="queue.fal.run/veed/fabric-1.0"
```

### Voices Disponibles

**Masculinas:**
- `Adam` ⭐ (profesional, claro)
- `Josh` (amigable, casual)
- `Arnold` (serio, autoritario)
- `Bill` (narrativo, calmado)
- `Antoni` (versátil)

**Femeninas:**
- `Rachel` ⭐ (profesional, clara)
- `Domi` (joven, energética)
- `Bella` (suave, cálida)
- `Elli` (narración, documental)
- `Gigi` (joven, expresiva)

---

## 📜 SCRIPT PRINCIPAL

**Ubicación:** `/root/.openclaw/workspace-magnum/scripts/avatar_video.sh`

### Uso

```bash
# Modo TTS (texto a voz + lip-sync)
./avatar_video.sh --tts <imagen> <voice_name> "<texto>" [output]

# Ejemplo:
./avatar_video.sh --tts avatar.jpg Adam "Hola, soy Cornelio" /tmp/video.mp4

# Modo audio existente (solo lip-sync)
./avatar_video.sh avatar.jpg audio.mp3 /tmp/video.mp4
```

### Parámetros

| Parámetro | Requerido | Descripción |
|-----------|-----------|-------------|
| `--tts` | Opcional | Activar modo ElevenLabs TTS |
| `<imagen>` | ✅ | Path a la imagen del avatar |
| `<voice_name>` | ✅ (modo TTS) | Nombre de la voz (Adam, Rachel, etc.) |
| `<texto>` | ✅ (modo TTS) | Texto a convertir a voz |
| `<audio>` | ✅ (sin TTS) | Path al archivo de audio |
| `[output]` | Opcional | Path de salida (default: `/tmp/cornelio_video.mp4`) |

---

## 🔍 DETALLE DEL FLUJO

### Paso 1: Redimensionar Imagen

```bash
ffmpeg -y -i input.jpg \
    -vf "scale='if(gt(a,1),1024,trunc(1024/a))':'if(gt(a,1),trunc(1024/a),1024)'" \
    -q:v 2 \
    resized.jpg
```

**Objetivo:** Normalizar imagen a ~1024px para mejor procesamiento

---

### Paso 2: ElevenLabs TTS

**Request:**
```bash
curl -X POST "https://queue.fal.run/fal-ai/elevenlabs/tts/multilingual-v2" \
  -H "Authorization: Key $FAL_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hola soy Cornelio", "voice": "Adam"}'
```

**Response (async):**
```json
{
  "status": "IN_QUEUE",
  "request_id": "019d7d85-39bb-71d1-98d5-78b4dd4df784",
  "response_url": "https://queue.fal.run/..."
}
```

**Polling:**
```bash
curl -sL "https://queue.fal.run/fal-ai/elevenlabs/requests/{request_id}" \
  -H "Authorization: Key $FAL_KEY"
```

**Response (completed):**
```json
{
  "audio": {
    "url": "https://v3b.fal.media/files/.../output.mp3",
    "content_type": "audio/mpeg",
    "file_size": 36407
  }
}
```

**Tiempo:** ~4 segundos

---

### Paso 3: Upload a tmpfiles.org

```bash
# Imagen
IMAGE_URL=$(curl -s -F "file=@resized.jpg" https://tmpfiles.org/api/v1/upload \
  | jq -r '.data.url' | sed 's|tmpfiles.org/|tmpfiles.org/dl/|')

# Audio
AUDIO_URL=$(curl -s -F "file=@audio.mp3" https://tmpfiles.org/api/v1/upload \
  | jq -r '.data.url' | sed 's|tmpfiles.org/|tmpfiles.org/dl/|')
```

**Output:** URLs públicas HTTPS válidas por ~24hs

---

### Paso 4: FAL Lip-Sync

**Request:**
```bash
curl -X POST "https://queue.fal.run/veed/fabric-1.0" \
  -H "Authorization: Key $FAL_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"image_url\": \"$IMAGE_URL\",
    \"audio_url\": \"$AUDIO_URL\",
    \"resolution\": \"720p\"
  }"
```

**Response (async):**
```json
{
  "status": "IN_QUEUE",
  "request_id": "019d7d85-afde-7ed2-ab1a-d926601eed7a"
}
```

**Polling:**
```bash
curl -sL "https://queue.fal.run/veed/fabric-1.0/requests/{request_id}" \
  -H "Authorization: Key $FAL_KEY"
```

**Response (completed):**
```json
{
  "video": {
    "url": "https://v3b.fal.media/files/.../tmp_video.mp4",
    "content_type": "video/mp4",
    "file_size": 897093
  }
}
```

**Tiempo:** ~24 segundos

---

### Paso 5: Download Video

```bash
curl -L -o /tmp/cornelio_video.mp4 "$VIDEO_URL"
```

**Output final:**
- **Path:** `/tmp/cornelio_video.mp4`
- **Tamaño:** ~877KB
- **Duración:** ~2 segundos

---

## ⚙️ INTEGRACIÓN CON MISSION CONTROL

### Agente: Asterix

**Rol:** Creative Director  
**ID:** 3  
**Worker:** `/opt/mission-control/workers/asterix-worker.sh`

### Crear Tarea

```bash
# Comando rápido
asterix-task "/path/to/avatar.jpg" Adam "Tu texto aquí"

# O vía API
curl -X POST http://localhost:3000/api/tasks \
  -H "x-api-key: $MC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Video lip-sync: Tu texto...",
    "description": "Generar video con: imagen: /path/to.jpg, voice_id: Adam, texto: \"Tu texto\"",
    "priority": "high",
    "assigned_to": "asterix",
    "tags": ["fai_ai", "elevenlabs", "tts", "lip_sync", "video"]
  }'
```

### Worker de Asterix

**Polling:** Cada 30 segundos  
**Log:** `/opt/mission-control/logs/asterix-worker.log`

**Comandos útiles:**
```bash
# Ver logs en vivo
tail -f /opt/mission-control/logs/asterix-worker.log

# Reiniciar worker
systemctl restart asterix-worker

# Ver estado
systemctl status asterix-worker
```

---

## 💰 COSTOS APROXIMADOS

| Servicio | Costo por uso | Notas |
|----------|---------------|-------|
| **ElevenLabs TTS** | ~$0.10 USD | Por 1000 caracteres |
| **FAL Lip-Sync** | ~$0.50-2.00 USD | Por video |
| **tmpfiles.org** | Gratis | URLs por 24hs |
| **TOTAL** | ~$1-3 USD | Por video |

---

## 🐛 TROUBLESHOOTING

### Error: "Voice not found"

**Causa:** Usar UUID en lugar de nombre de voz

**Solución:**
```bash
# ❌ INCORRECTO (UUID)
./avatar_video.sh --tts avatar.jpg pNInz6obpgDQGcFXmaJh "texto"

# ✅ CORRECTO (nombre)
./avatar_video.sh --tts avatar.jpg Adam "texto"
```

---

### Error: "Exhausted balance"

**Causa:** Saldo agotado en FAL AI

**Solución:**
1. Ir a https://fal.ai/dashboard/billing
2. Recargar saldo ($5-10 USD mínimo)
3. Reintentar

---

### Error: "Timeout esperando audio"

**Causa:** Endpoint de polling incorrecto

**Solución:**
```bash
# ✅ Endpoint correcto (sin /status)
curl -sL "https://queue.fal.run/fal-ai/elevenlabs/requests/{request_id}" \
  -H "Authorization: Key $FAL_KEY"

# Detectar completion buscando audio.url directamente
echo "$response" | jq -r '.audio.url // empty'
```

---

### Error: Worker no ejecuta tareas

**Causa:** Script cacheado o versión vieja

**Solución:**
```bash
# Reiniciar worker
systemctl daemon-reload
systemctl restart asterix-worker

# Verificar script actual
cat /root/.openclaw/workspace-magnum/scripts/avatar_video.sh | head -20

# Ver logs
tail -50 /opt/mission-control/logs/asterix-worker.log
```

---

## 📊 MÉTRICAS

| Métrica | Valor |
|---------|-------|
| **Tiempo total** | ~30 segundos |
| **TTS ElevenLabs** | ~4 segundos |
| **Lip-Sync FAL** | ~24 segundos |
| **Upload/Download** | ~2 segundos |
| **Tamaño video** | ~877KB (2 segundos) |
| **Resolución** | 720p |
| **Formato** | MP4 (H.264) |

---

## 📁 ARCHIVOS RELACIONADOS

| Archivo | Propósito |
|---------|-----------|
| `/root/.openclaw/workspace-magnum/scripts/avatar_video.sh` | Script principal |
| `/root/.openclaw/workspace-magnum/.fal_credentials.env` | Credenciales FAL + Voices |
| `/opt/mission-control/workers/asterix-worker.sh` | Worker autónomo Asterix |
| `/opt/mission-control/logs/asterix-worker.log` | Logs de ejecución |
| `/usr/local/bin/asterix-task` | Comando rápido para crear tareas |
| `/usr/local/bin/mc-status` | Reporte ejecutivo de estado |

---

## 🚀 QUICKSTART

**1. Preparar inputs:**
```bash
# Imagen del avatar
cp /path/to/avatar.jpg /root/.openclaw/workspace-magnum/

# (Opcional) Ver voices disponibles
cat /root/.openclaw/workspace-magnum/.fal_credentials.env | grep VOICE_
```

**2. Generar video:**
```bash
/root/.openclaw/workspace-magnum/scripts/avatar_video.sh \
  --tts /root/.openclaw/workspace-magnum/avatar.jpg \
  Adam \
  "Hola, soy Cornelio, tu CEO Virtual" \
  /tmp/cornelio_video.mp4
```

**3. Ver resultado:**
```bash
ls -lh /tmp/cornelio_video.mp4
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 /tmp/cornelio_video.mp4
```

---

## 📞 SOPORTE

**Documentación oficial:**
- FAL AI: https://fal.ai/docs
- ElevenLabs: https://elevenlabs.io/docs
- Mission Control: https://mintlify.wiki/builderz-labs/mission-control

**Logs:**
```bash
tail -f /opt/mission-control/logs/asterix-worker.log
```

---

**Última actualización:** 2026-04-11  
**Autor:** Magnum (Brazo Derecho de Cornelio)  
**Estado:** ✅ Producción
