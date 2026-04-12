# Configuración de Voz TTS para Magnum

**Documento para:** Magnum (Brazo Derecho de Cornelio)  
**Fecha:** 2026-04-11  
**Solicitado por:** Jose Navarro

---

## 🎤 Estado Actual

**CONFIGURACIÓN ACTUAL:**
Actualmente estás usando la configuración **GLOBAL** de OpenClaw en `/root/.openclaw/openclaw.json`:

```json
{
  "messages": {
    "tts": {
      "auto": "inbound",
      "provider": "elevenlabs",
      "providers": {
        "elevenlabs": {
          "apiKey": "aa30f405ec0c1ce39707fbf76436b6c932474c6a5985a5693d363e87c1a899f0",
          "voiceId": "aviXFY7Zd7b9DnCUwaCh",
          "modelId": "eleven_v3",
          "languageCode": "es"
        }
      }
    }
  }
}
```

**PROBLEMA:**
Compartís la **misma voz** con Cornelio porque la configuración está en el nivel global de OpenClaw, no en tu workspace independiente.

---

## 🎯 Soluciones para Tener Tu Propia Voz

### Opción 1: Configuración Local en tu Workspace (RECOMENDADA)

Esta opción te da máxima independencia y no afecta a otros agentes.

#### Paso 1: Crear archivo de configuración TTS local

**Path:** `/root/.openclaw/workspace-magnum/openclaw.json`

**Contenido:**
```json
{
  "messages": {
    "tts": {
      "auto": "inbound",
      "provider": "elevenlabs",
      "providers": {
        "elevenlabs": {
          "apiKey": "aa30f405ec0c1ce39707fbf76436b6c932474c6a5985a5693d363e87c1a899f0",
          "voiceId": "NUEVO_VOICE_ID_AQUI",
          "modelId": "eleven_v3",
          "languageCode": "es"
        }
      }
    }
  }
}
```

#### Paso 2: Obtener un nuevo Voice ID de ElevenLabs

1. Ir a https://elevenlabs.io/app/voice-lab
2. Crear una voz nueva o clonar una existente
3. Copiar el Voice ID (formato: string alfanumérico)
4. Reemplazar `NUEVO_VOICE_ID_AQUI` en el archivo

#### Paso 3: Verificar prioridad de configuración

Tu archivo local en `/root/.openclaw/workspace-magnum/openclaw.json` debería tener prioridad sobre la configuración global.

---

### Opción 2: Modificar Configuración Global

**⚠️ ADVERTENCIA:** Esto afecta a TODOS los agentes.

Modificar `/root/.openclaw/openclaw.json` para agregar providers específicos:

```json
{
  "messages": {
    "tts": {
      "providers": {
        "elevenlabs-cornelio": {
          "apiKey": "...",
          "voiceId": "aviXFY7Zd7b9DnCUwaCh",  // ← Voz de Magnum
          "modelId": "eleven_v3",
          "languageCode": "es"
        },
        "elevenlabs-magnum": {
          "apiKey": "...",
          "voiceId": "aviXFY7Zd7b9DnCUwaCh",  // Voz de Magnum
          "modelId": "eleven_v3",
          "languageCode": "es"
        }
      }
    }
  }
}
```

Luego cada agente necesitaría un binding específico para su provider.

**No recomendado** porque:
- Más complejo
- Afecta a todos los agentes
- Requiere reinicio del Gateway

---

## 🧪 Test de Verificación

Después de configurar tu propia voz, probá:

1. Enviar un mensaje de texto a tu bot de Telegram (@Magnum_XLBot)
2. Agregar audio/voz al mensaje (si el usuario envía audio)
3. Verificar que la respuesta TTS suena diferente a Cornelio

---

## 📝 Notas Importantes

### Compatibilidad de Formatos

**Configuración actual (Opus - Nativo WhatsApp):**
- Formato: `opus_48000_128`
- Compatible: 100% iOS, Android, WhatsApp
- Tamaño: óptimo

### API Key

Usamos el **mismo API key** de ElevenLabs (`aa30f405ec0c1ce39707fbf76436b6c932474c6a5985a5693d363e87c1a899f0`) para ambos agentes.

Esto es correcto porque:
- El límite de rate limit es por cuenta, no por agente
- Podemos usar múltiples voices con el mismo API key

---

## 🔧 Troubleshooting

### Problema: Sigue sonando igual que Cornelio

**Causas posibles:**
1. El archivo `openclaw.json` en tu workspace no tiene el formato correcto
2. El Gateway está usando la config global en lugar de la local
3. El Voice ID nuevo no está activo en ElevenLabs

**Solución:**
```bash
# Verificar que el archivo existe
ls -la /root/.openclaw/workspace-magnum/openclaw.json

# Verificar sintaxis JSON
cat /root/.openclaw/workspace-magnum/openclaw.json | python3 -m json.tool

# Reiniciar Gateway si es necesario
openclaw gateway restart
```

### Problema: Error de API key inválido

**Verificar:**
- Que el API key esté completo (no truncado)
- Que tenga permisos para TTS en ElevenLabs
- Que la cuenta tenga créditos disponibles

---

## 📋 Checklist de Implementación

- [ ] Crear archivo `/root/.openclaw/workspace-magnum/openclaw.json`
- [ ] Obtener Voice ID nuevo de ElevenLabs
- [ ] Configurar voiceId en el archivo
- [ ] Verificar sintaxis JSON
- [ ] Probar enviando audio desde Telegram
- [ ] Confirmar que suena diferente a Cornelio

---

## 🚀 Próximos Pasos

1. **Decidir:** ¿Opción 1 (local) u Opción 2 (global)?
2. **Si Opción 1:** Ir a ElevenLabs y crear/clonar una voz
3. **Implementar:** Crear el archivo de configuración
4. **Testear:** Enviar mensaje de audio y verificar
5. **Reportar:** Avisar a Cornelio/Jose que está listo

---

**Documento creado por:** Cornelio (CEO Virtual)  
**Para:** Magnum (Brazo Derecho)  
**Fecha:** 2026-04-11
