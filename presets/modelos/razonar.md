# Preset: Razonar

**Descripción:** Modelos con capacidades avanzadas de razonamiento lógico y análisis.

**Activar:** "Quiero los presets de razonar"

---

## Configuración

| Prioridad | Modelo | Provider |
|-----------|--------|----------|
| 1 (primary) | `minimax-m2.5:cloud` | `ollama` |
| 2 (fallback) | `bytedance/seedance-2.0` | `openrouter` |
| 3 (fallback) | `stepfun/step-3.5-flash` | `openrouter` |
| 4 (fallback) | `qwen/qwen3.6-plus` | `openrouter` |

---

## JSON para openclaw.json

```json
{
  "model": {
    "primary": "ollama/minimax-m2.5:cloud",
    "fallbacks": [
      "openrouter/bytedance/seedance-2.0",
      "openrouter/stepfun/step-3.5-flash",
      "openrouter/qwen/qwen3.6-plus"
    ]
  }
}
```

---

**Creado:** 2026-04-15
**Actualizado:** 2026-04-15
**Autor:** Jose Navarro
**Versión:** 1.1