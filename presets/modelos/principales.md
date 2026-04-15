# Preset: Principales

**Descripción:** Configuración principal/default de modelos para uso general.

**Activar:** "Quiero los presets principales"

---

## Configuración

| Prioridad | Modelo | Provider |
|-----------|--------|----------|
| 1 (primary) | `glm-5.1` | `ollama` |
| 2 (fallback) | `minimax-m2.7:cloud` | `ollama` |
| 3 (fallback) | `stepfun/step-3.5-flash` | `openrouter` |
| 4 (fallback) | `qwen3.5:397b` | `ollama` |

---

## JSON para openclaw.json

```json
{
  "model": {
    "primary": "ollama/glm-5.1",
    "fallbacks": [
      "ollama/minimax-m2.7:cloud",
      "openrouter/stepfun/step-3.5-flash",
      "ollama/qwen3.5:397b"
    ]
  }
}
```

---

**Creado:** 2026-04-15
**Actualizado:** 2026-04-15
**Autor:** Jose Navarro
**Versión:** 1.2