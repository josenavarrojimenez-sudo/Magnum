#!/bin/bash
# avatar_video.sh - FAL AI Lip-sync con ElevenLabs TTS
# Flujo: Imagen + (Voice ID + Texto) → ElevenLabs → Audio → FAL → Video
# 
# Uso 1 (con TTS): ./avatar_video.sh --tts <imagen> <voice_id> "<texto>" [output]
# Uso 2 (audio):   ./avatar_video.sh <imagen> <audio> [output]

set -e

# === CONFIGURACIÓN ===
FAL_KEY="9ed6f67a-1b81-479c-ac60-bc5382b4214e:4070adfcc70064f32bcaf82ceb1275cd"
FAL_LIPSYNC_ENDPOINT="queue.fal.run/veed/fabric-1.0"
FAL_TTS_ENDPOINT="queue.fal.run/fal-ai/elevenlabs/tts/multilingual-v2"
TMP_DIR="/tmp/fal-lipsync"
WORKSPACE="/root/.openclaw/workspace-magnum"

# === PARSE ARGS ===
USE_TTS=false
INPUT_IMAGE=""
INPUT_AUDIO=""
VOICE_ID=""
TEXT=""
OUTPUT_VIDEO="/tmp/cornelio_video.mp4"

# Parsear argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        --tts)
            USE_TTS=true
            shift
            ;;
        *)
            if [[ -z "$INPUT_IMAGE" ]]; then
                INPUT_IMAGE="$1"
            elif [[ -z "$INPUT_AUDIO" && "$USE_TTS" == "false" ]]; then
                INPUT_AUDIO="$1"
            elif [[ -z "$VOICE_ID" && "$USE_TTS" == "true" ]]; then
                VOICE_ID="$1"
            elif [[ -z "$TEXT" && "$USE_TTS" == "true" ]]; then
                TEXT="$1"
            elif [[ -z "$OUTPUT_VIDEO" ]]; then
                OUTPUT_VIDEO="$1"
            fi
            shift
            ;;
    esac
done

# === VALIDAR INPUTS ===
if [[ -z "$INPUT_IMAGE" ]]; then
    echo "❌ Uso: $0 [--tts] <imagen> <audio|voice_id> [texto] [output]"
    echo ""
    echo "Opciones:"
    echo "  Modo TTS:  $0 --tts <imagen> <voice_id> \"<texto>\" [output]"
    echo "  Modo Audio: $0 <imagen> <audio> [output]"
    echo ""
    echo "Ejemplos:"
    echo "  $0 --tts avatar.jpg 21m000cmgFQq77Hf0r2 \"Hola, soy Cornelio\" /tmp/video.mp4"
    echo "  $0 avatar.jpg audio.mp3 /tmp/video.mp4"
    exit 1
fi

if [[ ! -f "$INPUT_IMAGE" ]]; then
    echo "❌ Imagen no encontrada: $INPUT_IMAGE"
    exit 1
fi

if [[ "$USE_TTS" == "true" && -z "$VOICE_ID" ]]; then
    echo "❌ Voice ID requerido en modo TTS"
    exit 1
fi

if [[ "$USE_TTS" == "true" && -z "$TEXT" ]]; then
    echo "❌ Texto requerido en modo TTS"
    exit 1
fi

if [[ "$USE_TTS" == "false" && -z "$INPUT_AUDIO" ]]; then
    echo "❌ Audio requerido en modo audio"
    exit 1
fi

# === CREAR TMP DIR ===
rm -rf "$TMP_DIR" 2>/dev/null || true
mkdir -p "$TMP_DIR" || TMP_DIR="/tmp/fal-lipsync-$$"
mkdir -p "$TMP_DIR"

# === 1. REDIMENSIONAR IMAGEN A ~1024px ===
echo "📐 Redimensionando imagen a 1024px..."
RESIZED_IMAGE="$TMP_DIR/resized_$(basename "$INPUT_IMAGE")"

ffmpeg -y -i "$INPUT_IMAGE" \
    -vf "scale='if(gt(a,1),1024,trunc(1024/a))':'if(gt(a,1),trunc(1024/a),1024)'" \
    -q:v 2 \
    "$RESIZED_IMAGE" \
    2>/dev/null

echo "✅ Imagen redimensionada: $RESIZED_IMAGE"

# === 2. GENERAR AUDIO (TTS o usar audio existente) ===
if [[ "$USE_TTS" == "true" ]]; then
    echo "🎙️ Generando audio con ElevenLabs TTS..."
    echo "   Voice ID: $VOICE_ID"
    echo "   Texto: $TEXT"
    
    TTS_AUDIO="$TMP_DIR/tts_audio.mp3"
    
    # POST a ElevenLabs TTS via FAL (async)
    TTS_RESPONSE=$(curl -s -X POST "https://$FAL_TTS_ENDPOINT" \
        -H "Authorization: Key $FAL_KEY" \
        -H "Content-Type: application/json" \
        -d "{
            \"text\": \"$TEXT\",
            \"voice\": \"$VOICE_ID\"
        }")
    
    echo "📡 Respuesta ElevenLabs: $TTS_RESPONSE"
    
    # Extraer request_id para polling
    REQUEST_ID=$(echo "$TTS_RESPONSE" | jq -r '.request_id // empty')
    
    if [[ -z "$REQUEST_ID" || "$REQUEST_ID" == "null" ]]; then
        echo "❌ Error: No se obtuvo request_id de ElevenLabs"
        echo "Respuesta: $TTS_RESPONSE"
        exit 1
    fi
    
    echo "⏳ Esperando generación de audio (request: $REQUEST_ID)..."
    
    # Polling hasta que esté completo
    max_attempts=30
    attempt=0
    
    while [[ $attempt -lt $max_attempts ]]; do
        sleep 2
        
        result_response=$(curl -sL "https://queue.fal.run/fal-ai/elevenlabs/requests/$REQUEST_ID" \
            -H "Authorization: Key $FAL_KEY")
        
        # Check if audio URL is present (indicates completion)
        TTS_AUDIO_URL=$(echo "$result_response" | jq -r '.audio.url // .data.audio.url // empty')
        
        if [[ -n "$TTS_AUDIO_URL" && "$TTS_AUDIO_URL" != "null" ]]; then
            echo "✅ Audio generado exitosamente"
            break
        fi
        
        # Also check status field for backward compatibility
        status=$(echo "$result_response" | jq -r '.status // "unknown"')
        echo "   Status: $status (attempt: $attempt/$max_attempts)"
        
        if [[ "$status" == "FAILED" ]]; then
            echo "❌ Error generando audio: $result_response"
            exit 1
        fi
        
        attempt=$((attempt + 1))
    done
    
    if [[ $attempt -eq $max_attempts ]]; then
        echo "❌ Timeout esperando audio de ElevenLabs"
        echo "Última respuesta: $result_response"
        exit 1
    fi
    
    # Si no tenemos URL aún (caso raro), intentar extraer de nuevo
    if [[ -z "$TTS_AUDIO_URL" || "$TTS_AUDIO_URL" == "null" ]]; then
        TTS_AUDIO_URL=$(echo "$result_response" | jq -r '.audio.url // .data.audio.url // empty')
    fi
    
    if [[ -z "$TTS_AUDIO_URL" || "$TTS_AUDIO_URL" == "null" ]]; then
        echo "❌ Error: No se obtuvo URL de audio de ElevenLabs"
        echo "Respuesta: $result_response"
        exit 1
    fi
    
    echo "✅ Audio TTS generado: $TTS_AUDIO_URL"
    
    # Descargar audio
    echo "⬇️ Descargando audio TTS..."
    curl -L -o "$TTS_AUDIO" "$TTS_AUDIO_URL"
    
    if [[ ! -f "$TTS_AUDIO" || ! -s "$TTS_AUDIO" ]]; then
        echo "❌ Error descargando audio TTS"
        exit 1
    fi
    
    INPUT_AUDIO="$TTS_AUDIO"
    echo "✅ Audio TTS guardado: $INPUT_AUDIO"
else
    echo "🎵 Usando audio existente: $INPUT_AUDIO"
fi

# === 3. SUBIR ARCHIVOS A TMPFILES.ORG ===
echo "☁️ Subiendo imagen a tmpfiles.org..."
IMAGE_URL=$(curl -s -F "file=@$RESIZED_IMAGE" https://tmpfiles.org/api/v1/upload | jq -r '.data.url' | sed 's|tmpfiles.org/|tmpfiles.org/dl/|')

if [[ -z "$IMAGE_URL" || "$IMAGE_URL" == "null" ]]; then
    echo "❌ Error subiendo imagen"
    exit 1
fi
echo "✅ Imagen URL: $IMAGE_URL"

echo "☁️ Subiendo audio a tmpfiles.org..."
AUDIO_URL=$(curl -s -F "file=@$INPUT_AUDIO" https://tmpfiles.org/api/v1/upload | jq -r '.data.url' | sed 's|tmpfiles.org/|tmpfiles.org/dl/|')

if [[ -z "$AUDIO_URL" || "$AUDIO_URL" == "null" ]]; then
    echo "❌ Error subiendo audio"
    exit 1
fi
echo "✅ Audio URL: $AUDIO_URL"

# === 4. POST A FAL AI LIP-SYNC ===
echo "🎬 Generando lip-sync con FAL AI..."

LIPSYNC_RESPONSE=$(curl -s -X POST "https://$FAL_LIPSYNC_ENDPOINT" \
    -H "Authorization: Key $FAL_KEY" \
    -H "Content-Type: application/json" \
    -d "{
        \"image_url\": \"$IMAGE_URL\",
        \"audio_url\": \"$AUDIO_URL\",
        \"resolution\": \"720p\"
    }")

echo "📡 Respuesta FAL Lip-sync: $LIPSYNC_RESPONSE"

# Extraer request_id para polling
LIPSYNC_REQUEST_ID=$(echo "$LIPSYNC_RESPONSE" | jq -r '.request_id // empty')

if [[ -z "$LIPSYNC_REQUEST_ID" || "$LIPSYNC_REQUEST_ID" == "null" ]]; then
    echo "❌ Error: No se obtuvo request_id de FAL Lip-sync"
    echo "Respuesta: $LIPSYNC_RESPONSE"
    exit 1
fi

echo "⏳ Esperando lip-sync (request: $LIPSYNC_REQUEST_ID)..."

# Polling hasta que el video esté listo
max_attempts=60
attempt=0

while [[ $attempt -lt $max_attempts ]]; do
    sleep 3
    
    lipsync_result=$(curl -sL "https://$FAL_LIPSYNC_ENDPOINT/requests/$LIPSYNC_REQUEST_ID" \
        -H "Authorization: Key $FAL_KEY")
    
    # Check if video URL is present (indicates completion)
    VIDEO_URL=$(echo "$lipsync_result" | jq -r '.video.url // .data.video.url // empty')
    
    if [[ -n "$VIDEO_URL" && "$VIDEO_URL" != "null" ]]; then
        echo "✅ Video lip-sync generado exitosamente"
        break
    fi
    
    # Also check status field
    status=$(echo "$lipsync_result" | jq -r '.status // "unknown"')
    echo "   Status: $status (attempt: $attempt/$max_attempts)"
    
    if [[ "$status" == "FAILED" ]]; then
        echo "❌ Error generando lip-sync: $lipsync_result"
        exit 1
    fi
    
    attempt=$((attempt + 1))
done

if [[ $attempt -eq $max_attempts ]]; then
    echo "❌ Timeout esperando lip-sync de FAL"
    echo "Última respuesta: $lipsync_result"
    exit 1
fi

# Si no tenemos URL aún, intentar extraer de nuevo
if [[ -z "$VIDEO_URL" || "$VIDEO_URL" == "null" ]]; then
    VIDEO_URL=$(echo "$lipsync_result" | jq -r '.video.url // .data.video.url // empty')
fi

if [[ -z "$VIDEO_URL" ]]; then
    echo "❌ Error: No se obtuvo URL de video de FAL"
    echo "Respuesta: $lipsync_result"
    exit 1
fi

echo "✅ Video URL generado: $VIDEO_URL"

# === 6. DESCARGAR VIDEO ===
echo "⬇️ Descargando video..."
curl -L -o "$OUTPUT_VIDEO" "$VIDEO_URL"

if [[ -f "$OUTPUT_VIDEO" && -s "$OUTPUT_VIDEO" ]]; then
    echo "✅ Video guardado: $OUTPUT_VIDEO"
    echo "📊 Tamaño: $(du -h "$OUTPUT_VIDEO" | cut -f1)"
    echo "🎬 Duración: $(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUTPUT_VIDEO" 2>/dev/null | cut -d. -f1) segundos"
else
    echo "❌ Error descargando video"
    exit 1
fi

# === LIMPIEZA ===
rm -rf "$TMP_DIR"

echo ""
echo "✨ ¡Video de lip-sync generado exitosamente!"
echo "📁 Output: $OUTPUT_VIDEO"
echo ""
