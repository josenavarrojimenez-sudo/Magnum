#!/usr/bin/env python3
"""
Generación de audio TTS con ElevenLabs (formato OGG Opus)
"""
import os
import sys
import json
import requests
from pathlib import Path

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
if not ELEVENLABS_API_KEY:
    try:
        with open("/root/.openclaw/openclaw.json", "r") as f:
            config = json.load(f)
            if "skills" in config and "sag" in config["skills"]:
                ELEVENLABS_API_KEY = config["skills"]["sag"]["apiKey"]
    except:
        pass

# VOICE_ID de Magnum (aviXFY7Zd7b9DnCUwaCh)
VOICE_ID = "aviXFY7Zd7b9DnCUwaCh"
MODEL = "eleven_multilingual_v2"
FORMAT = "opus_48000_128"

def generar_audio(texto, output_path):
    """
    Genera audio TTS usando ElevenLabs
    """
    if not ELEVENLABS_API_KEY:
        raise ValueError("API Key de ElevenLabs no configurada")
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    
    data = {
        "text": texto,
        "model_id": MODEL,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        return True
    else:
        raise Exception(f"Error en TTS: {response.status_code} - {response.text}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python generar_respuesta_opus.py <texto> <ruta_salida>")
        sys.exit(1)
    
    texto = sys.argv[1]
    output_path = sys.argv[2]
    
    try:
        generar_audio(texto, output_path)
        print(f"✅ Audio generado: {output_path}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
