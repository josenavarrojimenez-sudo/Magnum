# MENU-SCRAPER - Referencias

## Método JSON-LD (Más Confiable)

Muchas plataformas de delivery embeben datos estructurados en formato JSON-LD (Schema.org) directamente en el HTML. Este método funciona sin ejecutar JavaScript.

### Paso a Paso Completo

```bash
# 1. Obtener el HTML
curl -sL "URL_DEL_RESTAURANTE" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  -H "Accept-Language: es-419,es;q=0.9" \
  > page.html

# 2. Extraer JSON-LD
grep -oP 'application/ld\+json">[^<]+' page.html | head -1 | sed 's/application\/ld+json">//' > data.json

# 3. Verificar que tenemos datos válidos
python3 -c "import json; d=json.load(open('data.json')); print('Nombre:', d.get('name'))"

# 4. Parsear y guardar
python3 parse_menu.py data.json --format md > menu.md
```

## Plataformas Específicas

### Uber Eats

```bash
# URL típica: https://www.ubereats.com/country/store/ID
curl -sL "URL" | grep -oP 'application/ld\+json">[^<]+' | sed 's/application\/ld+json">//' > ubereats_data.json
```

Estructura típica:
- `name` → Nombre del restaurante
- `address` → Dirección completa
- `aggregateRating` → Rating y reviews
- `hasMenu.hasMenuSection` → Secciones del menú (Pizza, Entradas, etc.)
- `hasMenuSection[].hasMenuItem` → Items individuales
- `image` → URLs de imágenes del restaurante

### Rappi

Rappi usa Angular/React, puede que no tenga JSON-LD visible. Probar primero:

```bash
curl -sL "URL" | grep -oP 'application/ld\+json">[^<]+'
```

Si no hay resultados, la plataforma no expone datos estructurados en HTML.

## Extracción de Imágenes

```python
import re

# URLs en JSON-LD pueden tener unicode escaping
images = data.get('image', [])
clean_urls = [url.replace('\\/', '/') for url in images]

# Descargar con requests
import requests
for i, url in enumerate(clean_urls):
    r = requests.get(url)
    ext = url.split('.')[-1].split('?')[0][:3]
    with open(f'image_{i}.{ext}', 'wb') as f:
        f.write(r.content)
```

## Troubleshooting

### Problema: "Empty response"
- Verificar que la URL es correcta
- Intentar con User-Agent diferente
- Puede que la página requiere JavaScript (usar método alternativo)

### Problema: "JSON decode error"
- Los caracteres unicode pueden estar escapados (\u002F)
- Limpiar con: `sed 's/\\ / /g' data.json`

### Problema: Solo 1 imagen
- El sitio puede tener múltiples imágenes en diferentes formatos
- Revisar `image` puede ser string único o array

## Ejemplo de Output

```
# Woods Pizza a la Leña Cartago

**Dirección:** 219 Carmen, Cartago, Costa Rica
**Teléfono:** +506 8391 6946
**Rating:** ⭐ 4.6/5 (1000 reviews)

## Pizza (29 items)

### Pizza Pepperoni
_Pepperoni. Tamaño mediano de 8 porciones._
**Precio:** ₡9,790
...
```