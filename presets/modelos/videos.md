# Preset: Videos

**Descripción:** Modelos para generación, análisis y procesamiento de video.

**Activar:** "Quiero los presets de videos"

---

## Configuración

| Prioridad | Modelo | Provider |
|-----------|--------|----------|
| 1 (primary) | `google/veo-3.1` | `openrouter` |
| 2 (fallback) | `openai/sora-2-pro` | `openrouter` |
| 3 (fallback) | `bytedance/seedance-2.0-fast` | `openrouter` |
| 4 (fallback) | `bytedance/seedance-1-5-pro` | `openrouter` |
| 5 (fallback) | `alibaba/wan-2.7` | `openrouter` |

---

## JSON para openclaw.json

```json
{
  "model": {
    "primary": "openrouter/google/veo-3.1",
    "fallbacks": [
      "openrouter/openai/sora-2-pro",
      "openrouter/bytedance/seedance-2.0-fast",
      "openrouter/bytedance/seedance-1-5-pro",
      "openrouter/alibaba/wan-2.7"
    ]
  }
}
```

---

**Creado:** 2026-04-15  
**Autor:** Jose Navarro  
**Versión:** 1.0
