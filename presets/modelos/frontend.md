# Preset: Frontend

**Descripción:** Modelos especializados en desarrollo frontend, UI/UX, HTML/CSS/JS.

**Activar:** "Quiero los presets de frontend"

---

## Configuración

| Prioridad | Modelo | Provider |
|-----------|--------|----------|
| 1 (primary) | `google/gemini-3-flash-preview` | `openrouter` |
| 2 (fallback) | `deepseek-v3.2:cloud` | `ollama` |
| 3 (fallback) | `qwen/qwen3-vl-235b-a22b-thinking` | `openrouter` |
| 4 (fallback) | `qwen/qwen2.5-vl-72b-instruct` | `openrouter` |
| 5 (fallback) | `minimax-m2.5:cloud` | `ollama` |
| 6 (fallback) | `qwen/qwen3.6-plus` | `openrouter` |
| 7 (fallback) | `meta-llama/llama-3.1-8b-instruct` | `openrouter` |
| 8 (fallback) | `deepseek/deepseek-r1-0528` | `openrouter` |

---

## JSON para openclaw.json

```json
{
  "model": {
    "primary": "openrouter/google/gemini-3-flash-preview",
    "fallbacks": [
      "ollama/deepseek-v3.2:cloud",
      "openrouter/qwen/qwen3-vl-235b-a22b-thinking",
      "openrouter/qwen/qwen2.5-vl-72b-instruct",
      "ollama/minimax-m2.5:cloud",
      "openrouter/qwen/qwen3.6-plus",
      "openrouter/meta-llama/llama-3.1-8b-instruct",
      "openrouter/deepseek/deepseek-r1-0528"
    ]
  }
}
```

---

**Creado:** 2026-04-15  
**Autor:** Jose Navarro  
**Versión:** 1.0
