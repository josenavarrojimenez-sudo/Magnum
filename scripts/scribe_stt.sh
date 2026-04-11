#!/bin/bash
# scribe_stt.sh - Transcribe audio usando ElevenLabs Scribe V2
# Uso: scribe_stt.sh <archivo_de_audio> [language_code]
# Salida: Texto transcrito en stdout (JSON con .text)

API_KEY="aa30f405ec0c1ce39707fbf76436b6c932474c6a5985a5693d363e87c1a899f0"
FILE="$1"
LANG_CODE="${2:-es}"

if [ -z "$FILE" ]; then
  echo '{"error": "Uso: scribe_stt.sh <archivo> [lang_code]"}'
  exit 1
fi

curl -s -X POST "https://api.elevenlabs.io/v1/speech-to-text" \
  -H "xi-api-key: $API_KEY" \
  -F "model_id=scribe_v2" \
  -F "language_code=$LANG_CODE" \
  -F "file=@$FILE"
