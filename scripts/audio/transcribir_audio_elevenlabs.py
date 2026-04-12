#!/usr/bin/env python3
"""
Transcripción de audio con ElevenLabs Scribe V2
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

def transcribir_audio(ruta_audio, idioma="es"):
    """
    Transcribe audio usando ElevenLabs Scribe V2
    """
    if not ELEVENLABS_API_KEY:
        raise ValueError("API Key de ElevenLabs no configurada")
    
    with open(ruta_audio, "rb") as f:
        audio_data = f.read()
    
    url = "https://api.elevenlabs.io/v1/speech-to-text"
    
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    # Usar multipart/form-data para enviar el archivo
    files = {
        "file": (os.path.basename(ruta_audio), open(ruta_audio, "rb"), "audio/ogg")
    }
    
    data = {
        "model_id": "scribe_v2"
    }
    
    # Agregar idioma solo si no es auto-detección
    if idioma and idioma != "auto":
        data["language_code"] = idioma
    
    response = requests.post(url, headers=headers, files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        return result.get("text", "")
    else:
        raise Exception(f"Error en transcripción: {response.status_code} - {response.text}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python transcribir_audio_elevenlabs.py <ruta_audio> [idioma]")
        sys.exit(1)
    
    ruta = sys.argv[1]
    idioma = sys.argv[2] if len(sys.argv) > 2 else "es"
    
    try:
        texto = transcribir_audio(ruta, idioma)
        print(f"📝 Transcripción: {texto}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
