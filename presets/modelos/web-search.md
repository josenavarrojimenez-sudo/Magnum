# Preset: Web Search

**Descripción:** Modelos optimizados para búsqueda web, investigación y extracción de información.

**Activar:** "Quiero los presets de web search"

---

## Configuración

| Prioridad | Modelo | Provider |
|-----------|--------|----------|
| 1 (primary) | `bytedance-seed/seed-2.0-lite` | `openrouter` |
| 2 (fallback) | `kimi-k2.5:cloud` | `ollama` |
| 3 (fallback) | `minimax-m2.5:cloud` | `ollama` |

---

## JSON para openclaw.json

```json
{
  "model": {
    "primary": "openrouter/bytedance-seed/seed-2.0-lite",
    "fallbacks": [
      "ollama/kimi-k2.5:cloud",
      "ollama/minimax-m2.5:cloud"
    ]
  }
}
```

---

**Creado:** 2026-04-15
**Actualizado:** 2026-04-15
**Autor:** Jose Navarro
**Versión:** 1.1