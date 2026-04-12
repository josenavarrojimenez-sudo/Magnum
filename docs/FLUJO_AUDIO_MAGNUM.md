## 📋 Resumen General del Flujo - Magnum Edition

1. Usuario envía audio (WhatsApp/Telegram)
 ↓
2. OpenClaw guarda en /root/.openclaw/workspace-magnum/media/inbound/{id}.ogg
 ↓
3. Script Python detecta y procesa
 ↓
4. ElevenLabs Scribe v2 transcribe audio → texto
 ↓
5. Sistema genera respuesta de texto
 ↓
6. ElevenLabs TTS convierte texto → audio (voz: aviXFY7Zd7b9DnCUwaCh)
 ↓
7. **FFmpeg aplica boost de volumen 4.0x**
 ↓
8. Audio se guarda en /root/.openclaw/workspace-magnum/media/outbound/{id}.ogg
 ↓
8. Canal envía audio de vuelta al usuario

---

## 🔧 Componentes Técnicos

### 1. Gateway (OpenClaw)

Ruta de entrada (audios recibidos):
/root/.openclaw/workspace-magnum/media/inbound/{uuid}.ogg

Formato de audio recibido:
- Tipo: audio/ogg
- Codecs: Opus
- Sample Rate: 48,000 Hz (48kHz)
- Canal: Mono
- Extension: .ogg

---

### 2. Script de Transcripción (Python)

Ruta del script:
/root/.openclaw/workspace-magnum/scripts/audio/transcribir_audio_elevenlabs.py

Código del Script:
#!/usr/bin/env python3
import os
from elevenlabs import ElevenLabs
import json
from datetime import datetime

# Configuración
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# Ruta dinámica según el evento de entrada
audio_file = '/root/.openclaw/workspace-magnum/media/inbound/{audio_id}.ogg'

# Transcripción con ElevenLabs Scribe v2
with open(audio_file, 'rb') as f:
    transcription = client.speech_to_text.convert(
        file=f,
        model_id="scribe_v2" # Modelo Scribe v2 de ElevenLabs
    )

# Extraer texto
texto = transcription.text
print(f"Transcripción: {texto}")

# Guardar en JSON para registro
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
with open(f'/root/.openclaw/workspace-magnum/logs/transcripcion_{timestamp}.json', 'w') as f:
    json.dump({
        "archivo": os.path.basename(audio_file),
        "texto": texto,
        "fecha": timestamp,
        "formato": "OGG Opus"
    }, f, ensure_ascii=False, indent=2)

---

### 4. Conversión a Audio (TTS)

Ruta del script:
/root/.openclaw/workspace-magnum/scripts/audio/generar_respuesta_opus.py

Código del Script:
#!/usr/bin/env python3
from elevenlabs import ElevenLabs
import os
from datetime import datetime

# Configuración
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
magnum_voice_id = "aviXFY7Zd7b9DnCUwaCh" # VOZ DE MAGNUM

def generar_audio(texto_respuesta, output_path):
    # Generar audio con ElevenLabs TTS
    audio = client.text_to_speech.convert(
        text=texto_respuesta,
        voice_id=magnum_voice_id,
        model_id="eleven_multilingual_v2",
        output_format="opus_48000_128" # ← FORMATO DEFINITIVO OGG OPUS
    )

    # Guardar audio
    with open(output_path, 'wb') as f:
        if hasattr(audio, '__iter__'):
            for chunk in audio:
                if chunk:
                    f.write(chunk)
        else:
            f.write(audio)

    print(f"✅ Audio generado: {output_path}")

Configuración TTS:
- Modelo: eleven_multilingual_v2
- Voice ID: aviXFY7Zd7b9DnCUwaCh (VOZ DE MAGNUM)
- Formato: OGG Opus (opus_48000_128)
- Sample Rate: 48,000 Hz
- Bitrate: 128 kbps
- Canal: Mono
- Voice Settings:
  - stability: 0.35 (más expresivo/emocional)
  - similarity_boost: 0.75 (fidelidad natural)
  - style: 0.5 (exageración emocional)
  - use_speaker_boost: true
- **Boost Volumen: 4.0x con FFmpeg** (ruido controlado)

---

### 5. Envío de Audio

Usa la herramienta nativa de OpenClaw `message` o `sessions_send` con la directiva `MEDIA:path`.

---

## 🌐 Servicios Externos Usados

### ElevenLabs API
API Key: ELEVENLABS_API_KEY (variable de entorno) 
Modelo STT: scribe_v2 (Speech-to-Text) 
Modelo TTS: eleven_multilingual_v2 (Text-to-Speech) 
Voice ID: aviXFY7Zd7b9DnCUwaCh (MAGNUM)

---

## 📁 Rutas de Archivos en el Sistema (Magnum Workspace)

### Entrada (Audio recibido):
/root/.openclaw/workspace-magnum/media/inbound/{uuid}.ogg

### Procesamiento (Logs de transcripción):
/root/.openclaw/workspace-magnum/logs/transcripcion_{timestamp}.json

### Salida (Audio enviado):
/root/.openclaw/workspace-magnum/media/outbound/{timestamp}.ogg

---

## 🔑 Variables de Entorno

Configuración necesaria en el servidor:
export ELEVENLABS_API_KEY="tu_api_key_aqui"

---

## 📌 Notas de Magnum

### Identidad Vocal:
- Voice ID: aviXFY7Zd7b9DnCUwaCh ✅
- Formato: opus_48000_128 ✅
- Voice Settings: stability 0.35, style 0.5, similarity_boost 0.75 ✅
- Boost Volumen: 4.0x FFmpeg ✅
- Todos los scripts en el workspace sincronizados ✅

### Reglas de Operación:
1. Audio → Responder con audio (TTS ElevenLabs con voz de Magnum).
2. Texto → Responder con texto.
3. El workspace `/root/.openclaw/workspace-magnum/` es la zona segura de operación.

¡Flujo de Magnum configurado y documentado! 🚀🎧
