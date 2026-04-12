#!/usr/bin/env python3
"""
Pipeline completo: transcripción → procesamiento → respuesta en audio
"""
import os
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.audio.transcribir_audio_elevenlabs import transcribir_audio
from scripts.audio.generar_respuesta_opus import generar_audio

def pipeline_audio(ruta_audio_entrada, ruta_audio_salida, idioma="es"):
    """
    Pipeline completo para procesar audio
    1. Transcribe el audio entrante
    2. Genera respuesta
    3. Convierte la respuesta a audio
    """
    print("🎙️ Iniciando pipeline de audio...")
    
    # 1. Transcripción
    print("1️⃣ Transcribiendo audio...")
    texto_transcrito = transcribir_audio(ruta_audio_entrada, idioma)
    print(f"📝 Transcripción: {texto_transcrito}")
    
    # 2. Procesamiento de respuesta
    respuesta = f"👋 Hola! He recibido tu mensaje: '{texto_transcrito}'"
    print(f"🤖 Respuesta generada: {respuesta}")
    
    # 3. Generación de audio
    print("2️⃣ Generando audio de respuesta...")
    generar_audio(respuesta, ruta_audio_salida)
    print(f"✅ Audio guardado: {ruta_audio_salida}")
    
    return texto_transcrito, respuesta

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python transcribir_respuesta_opus.py <audio_entrada> <audio_salida> [idioma]")
        sys.exit(1)
    
    entrada = sys.argv[1]
    salida = sys.argv[2]
    idioma = sys.argv[3] if len(sys.argv) > 3 else "es"
    
    try:
        texto, respuesta = pipeline_audio(entrada, salida, idioma)
        print(f"\n🎉 Pipeline completado!")
        print(f"   Entrada: {entrada}")
        print(f"   Salida: {salida}")
        print(f"   Respuesta: {respuesta}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
