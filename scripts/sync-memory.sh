#!/bin/bash
# sync-memory.sh - Sincroniza QMD + MemPalace con sesiones recientes de OpenClaw
# Ejecutar via cron cada 5 minutos o manualmente: bash /root/.openclaw/workspace-magnum/scripts/sync-memory.sh

set -e
QMD_DIR="/root/.openclaw/memory-hybrid/qmd"
PALACE_DIR="/root/.mempalace"
LOG="/root/.openclaw/workspace-magnum/logs/sync-memory.log"

mkdir -p "$(dirname "$LOG")"

echo "[$(date -u)] Iniciando sincronización de memoria..." >> "$LOG"

# === 1. Actualizar colecciones QMD ===
echo "[$(date -u)] Actualizando QMD collections..." >> "$LOG"
cd "$QMD_DIR" || exit 1

qmd update 2>&1 >> "$LOG"

# Re-indexar si hay archivos nuevos (verificar count)
NEW_DOCS=$(qmd status 2>&1 | grep "Pending:" | grep -oP '\d+' | head -1)

if [ -n "$NEW_DOCS" ] && [ "$NEW_DOCS" -gt 0 ]; then
    echo "[$(date -u)] Embedding $NEW_DOCS documentos nuevos..." >> "$LOG"
    qmd embed -f 2>&1 >> "$LOG"
fi

# === 2. MemPalace status check ===
if [ -d "$PALACE_DIR" ]; then
    echo "[$(date -u)] Verificando MemPalace..." >> "$LOG"
    if command -v mempalace &>/dev/null; then
        echo "✅ MemPalace disponible en $(which mempalace)" >> "$LOG"
    else
        echo "⚠️ MemPalace no encontrado en PATH" >> "$LOG
    fi
fi

echo "[$(date -u)] ✅ Sincronización completada." >> "$LOG"
echo "---" >> "$LOG"
