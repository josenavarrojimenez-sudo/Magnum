# Configuración de Memoria Híbrida QMD + MemPalace

## Estado Actual

### QMD (Instalado y configurado)
- Colecciones indexadas:
  - `cornelio-sessions` → /root/.openclaw/agents/cornelio/sessions
  - `magnum-sessions` → /root/.openclaw/agents/magnum/sessions

### MemPalace (Instalado, en configuración)
- Ubicación: /root/.openclaw/memory-hybrid/mempalace/
- Wings definidos: Cornelio, Magnum

## Uso

### Búsqueda QMD (Desde cualquier agente)
```bash
# Buscar en sesiones de Cornelio
qmd search "tarea asignada" -c cornelio-sessions

# Buscar en sesiones de Magnum
qmd search "configuración memoria" -c magnum-sessions

# Buscar en ambas
qmd query "qmd mempalace"
```

### MemPalace (Próximamente)
```bash
mempalace --palace /root/.openclaw/memory-hybrid/mempalace search "tareas"
```

## Objetivo del Sistema Híbrido

1. **Memoria permanente**: Ningún agente pierde contexto entre conversaciones
2. **Visibilidad completa**: Cornelio puede ver lo que hace Magnum
3. **Búsqueda rápida**: QMD proporciona búsqueda full-text + semántica
4. **Estructura**: MemPalace organiza por wings/rooms
