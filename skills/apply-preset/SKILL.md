# Skill: apply-preset

**Nombre:** apply-preset  
**Descripción:** Aplica configuraciones de modelos predefinidas (presets) según el caso de uso.  
**Autor:** Jose Navarro  
**Versión:** 1.0  
**Creado:** 2026-04-15

---

## Descripción

Esta skill permite cambiar rápidamente la configuración de modelos IA en OpenClaw aplicando presets predefinidos para diferentes casos de uso (coding, frontend, web search, razonamiento, chat, matemáticos, financieros, imágenes, videos, principales).

---

## Presets Disponibles

| Nombre | Archivo | Descripción |
|--------|---------|-------------|
| `coding` | `coding.md` | Desarrollo de código y debugging |
| `frontend` | `frontend.md` | Frontend, UI/UX, HTML/CSS/JS |
| `web-search` | `web-search.md` | Búsqueda web e investigación |
| `razonar` | `razonar.md` | Razonamiento lógico y análisis |
| `chat` | `chat.md` | Conversación natural |
| `matematicos` | `matematicos.md` | Matemáticas y cálculos |
| `financieros` | `financieros.md` | Análisis financiero |
| `imagenes` | `imagenes.md` | Visión y procesamiento de imágenes |
| `videos` | `videos.md` | Generación y análisis de video |
| `principales` | `principales.md` | Configuración general/default |

---

## Uso

### Comando Directo (Telegram/WhatsApp/Discord)
```
Quiero los presets de coding
Aplica el preset de frontend
Cambiar a preset web-search
```

### Script CLI
```bash
# Aplicar preset
/root/.openclaw/workspace-magnum/skills/apply-preset/scripts/apply-preset.sh coding

# Listar presets disponibles
/root/.openclaw/workspace-magnum/skills/apply-preset/scripts/apply-preset.sh --list

# Ver detalles de un preset
/root/.openclaw/workspace-magnum/skills/apply-preset/scripts/apply-preset.sh --show coding
```

---

## Comportamiento

1. **Validar** que el preset existe
2. **Leer** la configuración del preset
3. **Backup** de la configuración actual
4. **Aplicar** nuevos modelos a openclaw.json
5. **Notificar** al usuario que necesita reiniciar gateway

---

## Archivos

```
skills/apply-preset/
├── SKILL.md              # Esta documentación
├── scripts/
│   └── apply-preset.sh   # Script de aplicación
└── references/
    └── presets/          # Enlace a /presets/modelos/
```

---

## Ejemplos

### Ejemplo 1: Aplicar preset de coding
```
Usuario: "Quiero los presets de coding"
Magnum: ✅ Preset 'coding' aplicado. Modelos actualizados:
        - Primary: openrouter/moonshotai/kimi-k2.5
        - Fallbacks: kimi-k2.5:cloud, qwen3.5, gemini-3-flash-preview
        
        ⚠️ Necesitas reiniciar el gateway para aplicar cambios:
        `openclaw gateway restart`
```

### Ejemplo 2: Listar presets
```
Usuario: "Qué presets tengo disponibles?"
Magnum: 📋 Presets disponibles:
        - coding (Desarrollo de código)
        - frontend (Frontend/UI)
        - web-search (Búsqueda web)
        - razonar (Razonamiento)
        - chat (Conversación)
        - matematicos (Matemáticas)
        - financieros (Finanzas)
        - imagenes (Imágenes)
        - videos (Videos)
        - principales (Default)
```

---

## Notas de Seguridad

- ⚠️ Requiere backup automático antes de aplicar
- ⚠️ No reiniciar gateway automáticamente (requiere autorización)
- ✅ Solo modifica sección de modelos en openclaw.json
- ✅ Valida que los modelos existen antes de aplicar

---

## Changelog

| Versión | Fecha | Cambio |
|---------|-------|--------|
| 1.0 | 2026-04-15 | Creación inicial |
