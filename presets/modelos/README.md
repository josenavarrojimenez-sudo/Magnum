# Presets de Modelos - Magnum

**Autor:** Jose Navarro  
**Creado:** 2026-04-15  
**Ubicación:** `/root/.openclaw/workspace-magnum/presets/modelos/`

---

## ¿Qué son los Presets?

Configuraciones predefinidas de modelos IA para diferentes casos de uso. Cada preset define:
- **Primary:** Modelo principal
- **Fallbacks:** Lista ordenada de modelos de respaldo

---

## Presets Disponibles

| Preset | Comando de Activación | Archivos |
|--------|----------------------|----------|
| **Coding** | "Quiero los presets de coding" | `coding.md` |
| **Frontend** | "Quiero los presets de frontend" | `frontend.md` |
| **Web Search** | "Quiero los presets de web search" | `web-search.md` |
| **Razonar** | "Quiero los presets de razonar" | `razonar.md` |
| **Chat** | "Quiero los presets de chat" | `chat.md` |
| **Matemáticos** | "Quiero los presets de matemáticos" | `matematicos.md` |
| **Financieros** | "Quiero los presets de financieros" | `financieros.md` |
| **Imágenes** | "Quiero los presets de imagenes" | `imagenes.md` |
| **Videos** | "Quiero los presets de videos" | `videos.md` |
| **Principales** | "Quiero los presets principales" | `principales.md` |

---

## Cómo Aplicar un Preset

### Opción 1: Comando Directo
```
"Quiero los presets de [nombre]"
```

### Opción 2: Skill
```bash
/root/.openclaw/workspace-magnum/skills/apply-preset/scripts/apply-preset.sh [nombre]
```

### Opción 3: Manual
1. Leer el archivo `.md` del preset
2. Copiar el bloque JSON
3. Actualizar `/root/.openclaw/openclaw.json`
4. Reiniciar gateway: `openclaw gateway restart`

---

## Estructura de Archivos

```
presets/modelos/
├── README.md           # Este archivo
├── coding.md           # Desarrollo de código
├── frontend.md         # Frontend/UI
├── web-search.md       # Búsqueda web
├── razonar.md          # Razonamiento lógico
├── chat.md             # Conversación
├── matematicos.md      # Matemáticas
├── financieros.md      # Finanzas
├── imagenes.md         # Visión/Imágenes
├── videos.md           # Video
└── principales.md      # Default/General
```

---

## Notas Importantes

1. **Aplicar cambios:** Después de aplicar un preset, reiniciar el gateway
2. **Backup:** El sistema debe hacer backup de la config anterior
3. **Validación:** Verificar que los modelos existen antes de aplicar
4. **Documentación:** Cada cambio de preset debe registrarse en Lecciones.md

---

## GitHub

Este directorio debe sincronizarse con:
```
https://github.com/[org]/[repo]/presets/modelos/
```

**Comando de sync:**
```bash
cd /root/.openclaw/workspace-magnum
git add presets/modelos/
git commit -m "Presets de modelos - [fecha]"
git push
```
