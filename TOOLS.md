# TOOLS.md - Magnum

Notas locales sobre la configuración de Magnum.

---

## Model Presets

Los presets de modelos están documentados en:
- `/root/.openclaw/workspace-magnum/models-presets/README.md`

### Categorías Disponibles

| Categoría | Default | Uso |
|-----------|---------|-----|
| **Coding** | `ollama/kimi-k2.5:cloud` | Programación, debugging |
| **Frontend** | `openrouter/openai/gpt-5.4-mini` | HTML/CSS/JS, frameworks |
| **Web Search** | `openrouter/bytedance-seed/seed-2.0-lite` | Búsqueda, scraping |
| **Razonar** | `ollama/minimax-m2.5:cloud` | Lógica, problemas complejos |
| **Chat** | `ollama/qwen3.5:397b-cloud` | Conversación general |
| **Matemáticos** | `openrouter/qwen/qwen3.6-plus` | Cálculos, ecuaciones |
| **Financieros** | `openrouter/qwen/qwen3.6-plus` | Análisis económico |
| **Principales** | `ollama/glm-5.1:cloud` | Uso general por defecto |

### Uso

Para activar un preset, usar:
```
"Magnum aplica los presets de [CATEGORÍA]"
```

---

## API Keys Configuradas

| Servicio | Key | Ubicación |
|----------|-----|-----------|
| OpenRouter | `sk-or-v1-79ebc...` | `.env`, `env.sh`, auth-profiles |
| Ollama | `ollama-local` | auth-profiles |
| ElevenLabs | `aa30f405...` | `.env`, `env.sh` |

---

## Proveedores de Modelos

### Ollama (Local)
- **Endpoint:** `http://127.0.0.1:11434/v1`
- **Modelos:** 22 configurados
- **Status:** ✅ Activo

### OpenRouter (Cloud)
- **Endpoint:** `https://openrouter.ai/api/v1`
- **Modelos:** 200+ disponibles
- **Status:** ✅ Activo

---

## Canales

| Canal | Status |
|-------|--------|
| Telegram | ✅ Activo |
| WhatsApp | ⚠️ Reconexiones cada 30min (normal) |
| Discord | ⚠️ Stale socket reconexiones (normal) |

---

## Workspace

- **Ruta:** `/root/.openclaw/workspace-magnum`
- **Skills:** `/root/.openclaw/workspace-magnum/skills/`
- **Logs:** `/tmp/openclaw/openclaw-*.log`

---

*Documentación de Magnum - Brazo Derecho de Cornelio*
