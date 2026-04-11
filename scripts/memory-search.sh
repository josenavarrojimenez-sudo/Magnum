#!/bin/bash
# Script de búsqueda de memoria híbrida para Magnum
# Uso: ./memory-search.sh "query" [agente]

QMD_DIR="/root/.openclaw/memory-hybrid/qmd"
QUERY="$1"
AGENTE="${2:-all}"

cd "$QMD_DIR" || exit 1

echo "🔍 Buscando: '$QUERY' en sesiones de $AGENTE"
echo "============================================"

case "$AGENTE" in
  cornelio)
    qmd query "$QUERY" -c cornelio-sessions -n 5
    ;;
  magnum)
    qmd query "$QUERY" -c magnum-sessions -n 5
    ;;
  all|*)
    qmd query "$QUERY" -n 10
    ;;
esac
