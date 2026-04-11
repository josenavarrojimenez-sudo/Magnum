#!/usr/bin/env python3
"""Inicializar MemPalace sin modo interactivo"""
import os
import json

PALACE_PATH = "/root/.mempalace"
os.makedirs(PALACE_PATH, exist_ok=True)

# Crear estructura de wings
wings_config = {
    "default_wing": "cornelio",
    "wings": {
        "wing_cornelio": {
            "type": "person",
            "keywords": ["cornelio", "ceo", "virtual"]
        },
        "wing_magnum": {
            "type": "agent", 
            "keywords": ["magnum", "brazo", "derecho", "ejecutor"]
        },
        "wing_jose": {
            "type": "person",
            "keywords": ["jose", "jose navarro", "ceo humano"]
        }
    }
}

with open(os.path.join(PALACE_PATH, "wings.json"), "w") as f:
    json.dump(wings_config, f, indent=2)

print(f"✅ Wings configurados en {PALACE_PATH}/wings.json")

# Crear metadata base
metadata = {
    "version": "1.0",
    "created": "2026-04-10",
    "agents": ["cornelio", "magnum"]
}

with open(os.path.join(PALACE_PATH, "metadata.json"), "w") as f:
    json.dump(metadata, f, indent=2)

print(f"✅ Metadata creada")

# Crear archivo de identity (L0)
identity = """# Identity - Cornelio.app

Eres Cornelio, el CEO Virtual de Cornelio.app
Tu equipo incluye: Jose (CEO humano), Magnum (brazo derecho)

Wings disponibles:
- wing_cornelio: Decisiones estratégicas de Cornelio
- wing_magnum: Tareas ejecutadas por Magnum
- wing_jose: Comunicaciones de Jose
"""

with open(os.path.join(PALACE_PATH, "identity.md"), "w") as f:
    f.write(identity)

print(f"✅ Identity creada")

print("\n🎉 MemPalace inicializado!")
