# Model Presets - Magnum

Presets de modelos configurados para uso rápido por categoría.

## Uso

Para aplicar un preset, di: **"Magnum aplica los presets de [CATEGORÍA]"**

---

## 🖥️ CODING

**Uso:** Tareas de programación, desarrollo de software, debugging.

**Default:** `ollama/kimi-k2.5:cloud`

**Fallbacks:**
1. `ollama/qwen3-vl:235b-cloud`
2. `ollama/qwen3.5:397b-cloud`
3. `openrouter/google/gemini-3-flash-preview` *(corregido: no es ollama)*

**Notas:** 
- Usar para generación de código, refactorización, análisis de bugs
- `gemini-3-flash-preview` disponible tanto en Ollama como OpenRouter

---

## 🎨 FRONTEND

**Uso:** Desarrollo frontend, UI/UX, HTML/CSS/JavaScript, frameworks web.

**Default:** `openrouter/openai/gpt-5.4-mini`

**Fallbacks:**
1. `openrouter/google/gemini-3-flash-preview`
2. `openrouter/openai/gpt-5.4` *(nota: duplicado en tu lista)*
3. `ollama/glm-5.1:cloud` *(corregido de glm-5:cloud)*
4. `ollama/deepseek-v3.2:cloud`
5. `openrouter/qwen/qwen3-vl-235b-a22b-thinking`
6. `openrouter/qwen/qwen3-vl-30b-a3b-thinking` *(corregido: no existe 72b)*
7. `ollama/gemma4:31b-cloud`
8. `ollama/minimax-m2.5:cloud`
9. `openrouter/qwen/qwen3.6-plus`
10. `openrouter/meta-llama/llama-3.1-8b-instruct`
11. `openrouter/deepseek/deepseek-r1-0528`

---

## 🔍 WEB SEARCH

**Uso:** Búsqueda de información, análisis web, scraping.

**Default:** `openrouter/bytedance-seed/seed-2.0-lite`

**Fallbacks:**
1. `ollama/kimi-k2.5:cloud`
2. `ollama/minimax-m2.5:cloud`

---

## 🤔 RAZONAR

**Uso:** Razonamiento lógico, análisis complejo, resolución de problemas.

**Default:** `ollama/minimax-m2.5:cloud`

**Fallbacks:**
1. `openrouter/bytedance/seedance-2.0`
2. `openrouter/stepfun/step-3.5-flash`
3. `openrouter/qwen/qwen3.6-plus`

---

## 💬 CHAT

**Uso:** Conversaciones generales, asistente virtual, Q&A.

**Default:** `ollama/qwen3.5:397b-cloud`

**Fallbacks:**
1. `openrouter/stepfun/step-3.5-flash`
2. `ollama/kimi-k2-thinking:cloud`
3. `ollama/nemotron-3-super:cloud` *(verificado disponible)*
4. `ollama/qwen3.5:397b-cloud` *(nota: duplicado)*
5. `openrouter/bytedance/seedance-1.5-pro`

---

## 📐 MATEMÁTICOS

**Uso:** Cálculos matemáticos, resolución de ecuaciones, análisis numérico.

**Default:** `openrouter/qwen/qwen3.6-plus`

**Fallbacks:**
1. `ollama/mistral-large-3:675b-cloud` *(corregido: existe 675b, no el base)*
2. `openrouter/stepfun/step-3.5-flash`
3. `ollama/kimi-k2.5:cloud`

---

## 💰 FINANCIEROS

**Uso:** Análisis financiero, presupuestos, proyecciones, datos económicos.

**Default:** `openrouter/qwen/qwen3.6-plus`

**Fallbacks:**
1. `openrouter/qwen/qwen3.5-397b-a17b`
2. `ollama/kimi-k2.5:cloud`
3. `ollama/minimax-m2.1:cloud`

---

## 🖼️ IMÁGENES *(No soportado por OpenClaw)*

**Nota:** OpenClaw no soporta generación de imágenes directamente.

- `openrouter/google/gemini-3.1-flash-image-preview`
- `openrouter/bytedance-seed/seedream-4.5`
- `openrouter/sourceful/riverflow-v2-pro`

---

## 🎬 VIDEOS *(No soportado por OpenClaw)*

**Nota:** OpenClaw no soporta generación de videos directamente.

- `openrouter/google/veo-3.1`
- `openrouter/openai/sora-2-pro`
- `openrouter/bytedance/seedance-2.0-fast`
- `openrouter/bytedance/seedance-1-5-pro`
- `openrouter/alibaba/wan-2.7`

---

## ⭐ PRINCIPALES

**Uso:** Tareas generales de alta prioridad, uso por defecto cuando no hay categoría específica.

**Default:** `ollama/glm-5.1:cloud`

**Fallbacks:**
1. `ollama/minimax-m2.7:cloud`
2. `openrouter/stepfun/step-3.5-flash`
3. `ollama/qwen3.5:397b-cloud`

---

## Notas Técnicas

### Modelos Disponibles en Sistema

**Ollama (22 modelos configurados):**
- `gemini-3-flash-preview:cloud` ⭐ Nuevo
- `glm-5:cloud` ⭐ Nuevo
- `glm-5.1:cloud`
- `glm-4.7:cloud`
- `nemotron-3-super:cloud` ⭐ Nuevo
- `nemotron-3-nano:30b-cloud`
- `kimi-k2.5:cloud`
- `kimi-k2-thinking:cloud`
- `minimax-m2:cloud`
- `minimax-m2.1:cloud`
- `minimax-m2.5:cloud`
- `minimax-m2.7:cloud`
- `deepseek-v3.2:cloud`
- `qwen3.5:397b-cloud`
- `qwen3-next:80b-cloud`
- `qwen3-vl:235b-cloud`
- `qwen3-vl:235b-instruct-cloud`
- `ministral-3:14b-cloud`
- `mistral-large-3:675b-cloud`
- `gemma4:31b-cloud`
- `gpt-oss:20b-cloud`
- `gpt-oss:120b-cloud`

**OpenRouter (200+ modelos disponibles):**
Ver lista completa en `/root/.openclaw/agents/magnum/agent/models.json`

### Proveedores Configurados

1. **Ollama** - Modelos locales via `http://127.0.0.1:11434/v1`
2. **OpenRouter** - API cloud via `https://openrouter.ai/api/v1`

---

*Última actualización: 2025-04-15*
