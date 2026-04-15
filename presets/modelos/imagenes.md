# Preset: Imágenes

**Descripción:** Modelos de visión para análisis, descripción y procesamiento de imágenes.

**Activar:** "Quiero los presets de imagenes"

---

## Configuración

| Prioridad | Modelo | Provider |
|-----------|--------|----------|
| 1 (primary) | `google/gemini-3.1-flash-image-preview` | `openrouter` |
| 2 (fallback) | `bytedance-seed/seedream-4.5` | `openrouter` |
| 3 (fallback) | `ourceful/riverflow-v2-pro` | `openrouter` |

---

## JSON para openclaw.json

```json
{
  "model": {
    "primary": "openrouter/google/gemini-3.1-flash-image-preview",
    "fallbacks": [
      "openrouter/bytedance-seed/seedream-4.5",
      "openrouter/ourceful/riverflow-v2-pro"
    ]
  }
}
```

---

**Creado:** 2026-04-15  
**Autor:** Jose Navarro  
**Versión:** 1.0
