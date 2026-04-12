#!/usr/bin/env python3
"""
MAGNUM AUDIO MASTER - Integración Nativa ElevenLabs (STT + TTS)
Basado en la guía oficial de ElevenLabs para Bots de Telegram.
"""
import os
import sys
import json
import requests
from datetime import datetime

# --- CONFIGURACIÓN MAGNUM ---
VOICE_ID = "aviXFY7Zd7b9DnCUwaCh"
TTS_MODEL = "eleven_multilingual_v2"
STT_MODEL = "scribe_v2"
OUTPUT_FORMAT = "opus_48000_128"

def obtener_api_key():
    key = os.environ.get("ELEVENLABS_API_KEY", "")
    if not key:
        try:
            with open("/root/.openclaw/openclaw.json", "r") as f:
                config = json.load(f)
                key = config["skills"]["sag"]["apiKey"]
        except:
            pass
    return key

API_KEY = obtener_api_key()

def transcribir_audio(ruta_audio, idioma="es"):
    """Paso 1: Transcripción nativa con Scribe V2"""
    url = "https://api.elevenlabs.io/v1/speech-to-text"
    headers = {"xi-api-key": API_KEY}
    
    files = {
        "file": (os.path.basename(ruta_audio), open(ruta_audio, "rb"), "audio/ogg")
    }
    data = {
        "model_id": STT_MODEL,
        "tag_audio_events": "true"
    }
    if idioma and idioma != "auto":
        data["language_code"] = idioma

    print(f"🎤 Transcribiendo con {STT_MODEL}...")
    response = requests.post(url, headers=headers, files=files, data=data)
    
    if response.status_code == 200:
        texto = response.json().get("text", "")
        print(f"✅ Texto detectado: {texto}")
        return texto
    else:
        print(f"❌ Error STT: {response.text}")
        return None

def generar_respuesta_audio(texto, ruta_salida):
    """Paso 2: Generación de voz nativa Magnum"""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/ogg"
    }
    payload = {
        "text": texto,
        "model_id": TTS_MODEL,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "use_speaker_boost": True
        }
    }
    params = {"output_format": OUTPUT_FORMAT}

    print(f"🎙 Generando voz de Magnum...")
    response = requests.post(url, json=payload, headers=headers, params=params)

    if response.status_code == 200:
        with open(ruta_salida, "wb") as f:
            f.write(response.content)
        print(f"✅ Audio de Magnum listo: {ruta_salida}")
        return True
    else:
        print(f"❌ Error TTS: {response.text}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 magnum_audio_master.py <audio_entrada> [audio_salida]")
        sys.exit(1)
    
    entrada = sys.argv[1]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    salida = sys.argv[2] if len(sys.argv) > 2 else f"/tmp/respuesta_magnum_{timestamp}.ogg"
    
    # FLUJO COMPLETO
    texto_usuario = transcribir_audio(entrada)
    if texto_usuario:
        # Aquí iría la lógica de IA para procesar el mensaje
        # Por ahora, Magnum confirma la recepción para la prueba
        confirmacion = f"Entendido, procesé tu mensaje que dice: {texto_usuario}. Ejecuto de inmediato."
        generar_respuesta_audio(confirmacion, salida)
