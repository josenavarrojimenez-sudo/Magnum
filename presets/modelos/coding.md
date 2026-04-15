# Preset: Coding

**Descripción:** Modelos optimizados para generación de código, debugging y desarrollo.

**Activar:** "Quiero los presets de coding"

---

## Configuración

| Prioridad | Modelo | Provider |
|-----------|--------|----------|
| 1 (primary) | `kimi-k2.5` | `openrouter` |
| 2 (fallback) | `kimi-k2.5:cloud` | `ollama` |
| 3 (fallback) | `qwen3.5` | `ollama` |
| 4 (fallback) | `google/gemini-3-flash-preview` | `ollama` |

---

## JSON para openclaw.json

```json
{
  "model": {
    "primary": "openrouter/moonshotai/kimi-k2.5",
    "fallbacks": [
      "ollama/kimi-k2.5:cloud",
      "ollama/qwen3.5",
      "ollama/google/gemini-3-flash-preview"
    ]
  }
}
```

---

**Creado:** 2026-04-15  
**Autor:** Jose Navarro  
**Versión:** 1.0
