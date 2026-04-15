# Preset: Financieros

**Descripción:** Modelos para análisis financiero, proyecciones y datos económicos.

**Activar:** "Quiero los presets de financieros"

---

## Configuración

| Prioridad | Modelo | Provider |
|-----------|--------|----------|
| 1 (primary) | `qwen/qwen3.6-plus` | `openrouter` |
| 2 (fallback) | `qwen/qwen3.5-397b-a17b` | `openrouter` |
| 3 (fallback) | `kimi-k2.5:cloud` | `ollama` |
| 4 (fallback) | `minimax/minimax-m2.1` | `openrouter` |

---

## JSON para openclaw.json

```json
{
  "model": {
    "primary": "openrouter/qwen/qwen3.6-plus",
    "fallbacks": [
      "openrouter/qwen/qwen3.5-397b-a17b",
      "ollama/kimi-k2.5:cloud",
      "openrouter/minimax/minimax-m2.1"
    ]
  }
}
```

---

**Creado:** 2026-04-15  
**Autor:** Jose Navarro  
**Versión:** 1.0
