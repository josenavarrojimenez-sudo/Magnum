# Preset: Matemáticos

**Descripción:** Modelos especializados en matemáticas, cálculos y problemas numéricos.

**Activar:** "Quiero los presets de matemáticos"

---

## Configuración

| Prioridad | Modelo | Provider |
|-----------|--------|----------|
| 1 (primary) | `qwen/qwen3.6-plus` | `openrouter` |
| 2 (fallback) | `stepfun/step-3.5-flash` | `openrouter` |
| 3 (fallback) | `kimi-k2.5:cloud` | `ollama` |

---

## JSON para openclaw.json

```json
{
  "model": {
    "primary": "openrouter/qwen/qwen3.6-plus",
    "fallbacks": [
      "openrouter/stepfun/step-3.5-flash",
      "ollama/kimi-k2.5:cloud"
    ]
  }
}
```

---

**Creado:** 2026-04-15  
**Autor:** Jose Navarro  
**Versión:** 1.0
