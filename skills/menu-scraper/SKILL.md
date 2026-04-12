---
name: menu-scraper
description: Extrae menús de restaurantes desde plataformas como Uber Eats o Rappi usando JSON-LD embebido en el HTML. Captura menu completo con precios, descripciones, imagenes y datos de contacto. Se activa con frases como scrapear menu, extraer restaurante, capturar precios de delivery u obtener informacion de restaurante desde URL.
---

# MENU-SCRAPER

Extrae menús de restaurantes desde plataformas como Uber Eats, Rappi, etc. usando JSON-LD embebido en el HTML.

## Cuando Usar

- "Scrapear menú de Uber Eats"
- "Extraer información de restaurante de una URL"
- "Capturar menú completo de [plataforma]"
- "Obtener precios y descripciones de un restaurante online"

## Proceso

### 1. Obtener JSON-LD

```bash
curl -sL "URL" -H "User-Agent: Mozilla/5.0" | grep -oP 'application/ld\+json">[^<]+' | sed 's/application\/ld+json">//' > data.json
```

### 2. Parsear y Extraer Datos

```python
import json

with open('data.json') as f:
    d = json.load(f)

# Información del restaurante
print(f"Nombre: {d['name']}")
print(f"Dirección: {d['address']['streetAddress']}")
print(f"Rating: {d['aggregateRating']['ratingValue']}")

# Menú por secciones
for section in d.get('hasMenu', {}).get('hasMenuSection', []):
    print(f"\n## {section['name']}")
    for item in section.get('hasMenuItem', []):
        name = item['name']
        desc = item.get('description', '')
        price = item.get('offers', {}).get('price', 'N/A')
        print(f"- {name}: ₡{price} | {desc}")
```

### 3. Guardar Resultados

- `.md` → Menú formateado para humanos
- `.json` → Datos crudos para procesamiento
- `/images/` → Imágenes descargadas

## Plataformas Soportadas

| Plataforma | Funciona | Notas |
|------------|----------|-------|
| Uber Eats | ✅ | JSON-LD en Schema.org |
| Rappi | ⚠️ | Puede requerir JS render |
| PedidosYa | ⚠️ | Puede requerir JS render |
| Other | ⚠️ | Probar primero el método JSON-LD |

## Limitaciones

- Solo extrae datos disponibles en HTML (JSON-LD embebido)
- No funciona con SPAs que cargan contenido solo con JavaScript
- Precios pueden cambiar, verificar en la plataforma

## Scripts Disponibles

- `scripts/download_images.py` - Descarga imágenes del restaurante
- `scripts/parse_menu.py` - Parser reusable para diferentes formatos

Para detalles ver [references/references.md](references/references.md)