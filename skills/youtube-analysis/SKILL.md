# YouTube Video Analysis Skill

## Descripción
Extrae transcripciones de videos de YouTube y las analiza para extraer insights, resúmenes y datos clave.

## Uso
```
Tarea: Analiza el video de YouTube https://www.youtube.com/watch?v=XXXXX sobre presupuestos inmobiliarios
```

## Capabilities
1. **Transcript Extraction** - Usa yt-dlp para extraer subtitles/transcripts
2. **Content Analysis** - Analiza el transcript con IA para:
   - Resumen ejecutivo
   - Insights clave
   - Datos numéricos relevantes
   - action items

## Requisitos
- yt-dlp instalado
- openai-whisper (opcional, para videos sin subtitles)
- Modelo de IA para análisis (OpenRouter recommended)

## Limitaciones
- Solo funciona con videos que tienen subtitles/transcripts
- Videos largos pueden requerir más tiempo de procesamiento
- Alguns videos no tienen subtitles disponibles

---

_Last updated: 2026-04-12_
