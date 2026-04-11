#!/bin/bash
# tts_magnum.sh - TTS independiente para Magnum
# Ubicación: /root/.openclaw/workspace-magnum/scripts/tts_magnum.sh
# Uso: ./tts_magnum.sh "Texto a convertir" [output.mp3]

set -e

# Configuración independiente de Magnum
API_KEY="aa30f405ec0c1ce39707fbf76436b6c932474c6a5985a5693d363e87c1a899f0"
VOICE_ID="Fahco4VZzobUeiPqni1S"  # Voice ID único de Magnum
MODEL_ID="eleven_v3"

# Parámetros
TEXT="$1"
OUTPUT_FILE="${2:-/tmp/magnum_tts_output.mp3}"

# Validación
if [ -z "$TEXT" ]; then
    echo "❌ Error: Debes proporcionar texto"
    echo "Uso: $0 \"Texto a convertir\" [output.mp3]"
    exit 1
fi

echo "🎤 Generando TTS con voz de Magnum..."
echo "📝 Texto: $TEXT"
echo "🔊 Voice ID: $VOICE_ID"

# Llamada directa a ElevenLabs API
curl -s -X POST "https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}" \
    -H "Accept: audio/mpeg" \
    -H "Content-Type: application/json" \
    -H "xi-api-key: ${API_KEY}" \
    -d "{
        \"text\": \"${TEXT}\",
        \"model_id\": \"${MODEL_ID}\",
        \"voice_settings\": {
            \"stability\": 0.5,
            \"similarity_boost\": 0.75,
            \"speed\": 1.0
        }
    }" \
    --output "$OUTPUT_FILE"

# Verificar resultado
if [ -f "$OUTPUT_FILE" ] && [ -s "$OUTPUT_FILE" ]; then
    FILE_SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
    echo "✅ TTS generado exitosamente"
    echo "📁 Archivo: $OUTPUT_FILE"
    echo "📊 Tamaño: $FILE_SIZE"
    echo "🔊 Voice ID usado: $VOICE_ID (Magnum)"
else
    echo "❌ Error: No se pudo generar el audio"
    exit 1
fi
