# Preset: Chat

**Descripción:** Modelos optimizados para conversación natural y asistencia general.

**Activar:** "Quiero los presets de chat"

---

## Configuración

| Prioridad | Modelo | Provider |
|-----------|--------|----------|
| 1 (primary) | `qwen3.5` | `ollama` |
| 2 (fallback) | `bytedance/seedance-1.5 Pro` | `openrouter` |

---

## JSON para openclaw.json

```json
{
  "model": {
    "primary": "ollama/qwen3.5",
    "fallbacks": [
      "openrouter/bytedance/seedance-1.5 Pro"
    ]
  }
}
```

---

**Creado:** 2026-04-15  
**Autor:** Jose Navarro  
**Versión:** 1.0
