#!/bin/bash
# apply-preset.sh - Aplica configuraciones de modelos predefinidas
# Autor: Jose Navarro
# Versión: 1.0
# Creado: 2026-04-15

set -e

PRESETS_DIR="/root/.openclaw/workspace-magnum/presets/modelos"
CONFIG_FILE="/root/.openclaw/openclaw.json"
BACKUP_DIR="/root/.openclaw/backups/modelos"

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Mostrar ayuda
show_help() {
    echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  Apply Preset - Configuración Modelos  ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
    echo ""
    echo "Uso: $0 [opciones] [nombre-preset]"
    echo ""
    echo "Opciones:"
    echo "  --list, -l     Listar presets disponibles"
    echo "  --show, -s     Mostrar detalles de un preset"
    echo "  --apply, -a    Aplicar un preset"
    echo "  --help, -h     Mostrar esta ayuda"
    echo ""
    echo "Presets disponibles:"
    ls -1 "$PRESETS_DIR"/*.md 2>/dev/null | grep -v README | xargs -I {} basename {} .md | while read preset; do
        echo "  - $preset"
    done
}

# Listar presets
list_presets() {
    echo -e "${GREEN}Presets disponibles:${NC}"
    echo ""
    for file in "$PRESETS_DIR"/*.md; do
        if [[ "$(basename "$file")" != "README.md" ]]; then
            name=$(basename "$file" .md)
            desc=$(grep -m1 "**Descripción:**" "$file" 2>/dev/null | cut -d':' -f2- | xargs || echo "Sin descripción")
            echo -e "  ${BLUE}●${NC} $name $desc"
        fi
    done
}

# Mostrar detalles de un preset
show_preset() {
    local preset=$1
    local file="$PRESETS_DIR/$preset.md"
    
    if [[ ! -f "$file" ]]; then
        echo -e "${RED}✗ Error: El preset '$preset' no existe${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${BLUE}Preset: $preset${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    cat "$file"
}

# Crear backup de configuración
create_backup() {
    mkdir -p "$BACKUP_DIR"
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_file="$BACKUP_DIR/openclaw.json.$timestamp"
    
    cp "$CONFIG_FILE" "$backup_file"
    echo -e "${GREEN}✓ Backup creado: $backup_file${NC}"
}

# Extraer JSON del preset
extract_preset_json() {
    local preset=$1
    local file="$PRESETS_DIR/$preset.md"
    
    # Extraer bloque JSON entre ```json y ```
    sed -n '/```json/,/```/p' "$file" | sed '1d;$d'
}

# Aplicar preset
apply_preset() {
    local preset=$1
    local file="$PRESETS_DIR/$preset.md"
    
    if [[ ! -f "$file" ]]; then
        echo -e "${RED}✗ Error: El preset '$preset' no existe${NC}"
        echo ""
        echo "Presets disponibles:"
        list_presets
        exit 1
    fi
    
    echo -e "${BLUE}Aplicando preset: $preset${NC}"
    echo ""
    
    # Crear backup
    create_backup
    
    # Extraer configuración del preset
    local preset_json=$(extract_preset_json "$preset")
    
    if [[ -z "$preset_json" ]]; then
        echo -e "${RED}✗ Error: No se pudo extraer configuración del preset${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}Configuración del preset:${NC}"
    echo "$preset_json" | python3 -m json.tool 2>/dev/null || echo "$preset_json"
    echo ""
    
    # Nota: Aquí iría la lógica para actualizar openclaw.json
    # Por ahora solo mostramos la información
    
    echo -e "${YELLOW}⚠️  Para aplicar los cambios, necesitas:${NC}"
    echo ""
    echo "1. Copiar el JSON anterior"
    echo "2. Actualizar /root/.openclaw/openclaw.json"
    echo "3. Reiniciar gateway: ${BLUE}openclaw gateway restart${NC}"
    echo ""
    echo -e "${GREEN}✓ Preset '$preset' listo para aplicar${NC}"
}

# Main
case "${1:-}" in
    --list|-l)
        list_presets
        ;;
    --show|-s)
        if [[ -z "${2:-}" ]]; then
            echo -e "${RED}✗ Error: Debes especificar un preset${NC}"
            show_help
            exit 1
        fi
        show_preset "$2"
        ;;
    --apply|-a|"")
        if [[ -z "${2:-}" ]]; then
            echo -e "${RED}✗ Error: Debes especificar un preset${NC}"
            show_help
            exit 1
        fi
        apply_preset "$2"
        ;;
    --help|-h)
        show_help
        ;;
    *)
        # Asumir que es un nombre de preset directo
        apply_preset "$1"
        ;;
esac
