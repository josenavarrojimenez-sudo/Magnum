#!/usr/bin/env python3
"""
Magnum Direct TTS - Generación de audio nativa vía API de ElevenLabs
Permite ajustar parámetros de voz de forma independiente en el workspace de Magnum.
"""
import os
import sys
import json
import requests
from datetime import datetime

# --- CONFIGURACIÓN DE MAGNUM ---
VOICE_ID = "aviXFY7Zd7b9DnCUwaCh"  # Identidad vocal de Magnum
MODEL_ID = "eleven_multilingual_v2" # Modelo de alta calidad
OUTPUT_FORMAT = "opus_48000_128"    # Formato nativo WhatsApp/Telegram

# Parámetros de voz ajustables (Personalidad de Magnum)
VOICE_SETTINGS = {
    "stability": 0.35,          # BAJO = más expresivo/emocional
    "similarity_boost": 0.75,    # Fidelidad a la voz original
    "style": 0.5,                # Exageración del estilo/emoción
    "use_speaker_boost": True    # Refuerza la claridad
}

def obtener_api_key():
    # Intenta obtener de variable de entorno o de openclaw.json
    key = os.environ.get("ELEVENLABS_API_KEY", "")
    if not key:
        try:
            with open("/root/.openclaw/openclaw.json", "r") as f:
                config = json.load(f)
                key = config["skills"]["sag"]["apiKey"]
        except:
            pass
    return key

def generar_audio_magnum(texto, ruta_salida):
    api_key = obtener_api_key()
    if not api_key:
        raise ValueError("❌ Error: API Key de ElevenLabs no encontrada.")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/ogg"
    }
    
    payload = {
        "text": texto,
        "model_id": MODEL_ID,
        "voice_settings": VOICE_SETTINGS
    }
    
    # Parámetros de consulta para el formato de salida
    params = {"output_format": OUTPUT_FORMAT}

    print(f"🎙 Generando audio para: '{texto[:30]}...'")
    response = requests.post(url, json=payload, headers=headers, params=params)

    if response.status_code == 200:
        with open(ruta_salida, "wb") as f:
            f.write(response.content)
        
        # --- Boost de Volumen con FFmpeg ---
        ruta_boost = ruta_salida.replace(".ogg", "_boost.ogg")
        print(f"🔊 Aumentando volumen 4.0x...")
        os.system(f"ffmpeg -i {ruta_salida} -filter:a 'volume=4.0' -c:a libopus -b:a 128k {ruta_boost} -y -loglevel quiet")
        if os.path.exists(ruta_boost):
            os.rename(ruta_boost, ruta_salida)
        
        print(f"✅ Audio generado y potenciado en: {ruta_salida}")
        return True
    else:
        print(f"❌ Error de API ({response.status_code}): {response.text}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 magnum_tts_directo.py <texto> [ruta_salida]")
        sys.exit(1)
    
    texto_input = sys.argv[1]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    salida = sys.argv[2] if len(sys.argv) > 2 else f"/tmp/magnum_voce_{timestamp}.ogg"
    
    generar_audio_magnum(texto_input, salida)
