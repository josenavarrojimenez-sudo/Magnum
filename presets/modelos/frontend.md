# Preset: Frontend

**Descripción:** Modelos especializados en desarrollo frontend, UI/UX, HTML/CSS/JS.

**Activar:** "Quiero los presets de frontend"

---

## Configuración

| Prioridad | Modelo | Provider |
|-----------|--------|----------|
| 1 (primary) | `google/gemini-3-flash-preview` | `openrouter` |
| 2 (fallback) | `deepseek-v3.1:cloud` | `ollama` |
| 3 (fallback) | `qwen/qwen3-vl-235b-a22b-thinking` | `openrouter` |
| 4 (fallback) | `minimax-m2.5:cloud` | `ollama` |
| 5 (fallback) | `qwen/qwen3.6-plus` | `openrouter` |
| 6 (fallback) | `deepseek/deepseek-v3.2` | `openrouter` |

---

## JSON para openclaw.json

```json
{
  "model": {
    "primary": "openrouter/google/gemini-3-flash-preview",
    "fallbacks": [
      "ollama/deepseek-v3.1:cloud",
      "openrouter/qwen/qwen3-vl-235b-a22b-thinking",
      "ollama/minimax-m2.5:cloud",
      "openrouter/qwen/qwen3.6-plus",
      "openrouter/deepseek/deepseek-v3.2"
    ]
  }
}
```

---

**Creado:** 2026-04-15
**Actualizado:** 2026-04-15
**Autor:** Jose Navarro
**Versión:** 1.1