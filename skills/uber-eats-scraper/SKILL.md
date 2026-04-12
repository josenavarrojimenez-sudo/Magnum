---
name: uber-eats-scraper
description: Skill completo para hacer scraping de menús de Uber Eats usando Playwright. Captura productos, precios, categorías, imágenes y screenshots de cualquier restaurant en Uber Eats. Incluye técnicas de bypass anti-bot usando mobile viewport y deep scroll. Se activa con frases como scrapear Uber Eats, capturar menú de restaurante, extraer imágenes de delivery, hacer scraping de comida, o descargar menú completo de restaurante online. También para extraer datos de Schema.org (JSON-LD) de cualquier página web.
---

# UBER EATS SCRAPER

Skill para hacer scraping completo de menús de Uber Eats con renderizado JavaScript.

## Cuando Usar

- "Scrapear menú de Uber Eats"
- "Extraer todos los productos de un restaurante"
- "Descargar imágenes de un menú de delivery"
- "Capturar información de restaurante con fotos"
- "Hacer scraping de página con JavaScript dinámico"

## Dependencias

```bash
npm install -g playwright
npx playwright install chromium
pip install requests
```

## Scripts Disponibles

| Script | Uso |
|--------|-----|
| `scripts/scrape_uber_eats_complete.py` | Principal - scraping completo |
| `scripts/download_images.py` | Descargar imágenes desde JSON |
| `scripts/parse_menu.py` | Parsear JSON-LD a markdown/JSON |

## Uso Básico

```bash
# Installation (solo una vez)
npm install -g playwright
npx playwright install chromium

# Scraping
python3 scripts/scrape_uber_eats_complete.py "URL_RESTAURANTE" "./output"
```

## Técnica Anti-Bot

El script usa varias técnicas para bypass de anti-bot:

1. **Mobile Viewport** - 412x915px simula smartphone
2. **User-Agent móvil** - Chrome en Android
3. **Deep Scroll** - Bounce technique (scroll up/down repetidamente)
4. **Wait for JS** - Espera para que JavaScript cargue contenido

```python
# Mobile viewport bypasses bot detection
context = await browser.new_context(
    viewport={"width": 412, "height": 915},
    user_agent="Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 Chrome/91.0.4472.120 Mobile Safari/537.36"
)

# Deep scroll loads all lazy images
for i in range(15):
    for y in range(0, total_height, 300):
        await page.evaluate(f"window.scrollTo(0, {y})")
        await page.wait_for_timeout(150)
    await page.evaluate("window.scrollTo(0, 0)")
```

## Estructura de Output

```
output/
├── productos/
│   └── productos.json    # 86 items con nombre, precio, categoría
├── imagenes/              # Fotos de comida descargadas
├── screenshots/           # Capturas de pantalla
└── data/                  # Datos crudos
```

### Formato productos.json

```json
{
  "restaurante": "Nombre del Restaurant",
  "ubicacion": "Dirección",
  "telefono": "+506 XXXX XXXX",
  "rating": 4.6,
  "total_items": 86,
  "productos": [
    {
      "id": 1,
      "nombre": "Pizza Pepperoni",
      "descripcion": "Con pepperoni...",
      "categoria": "Pizza",
      "precio": 9790.00,
      "moneda": "CRC"
    }
  ]
}
```

## Filtrado de Imágenes

| Tamaño | Tipo |
|--------|------|
| >30KB | Foto real de comida |
| <10KB | Ícono o logo |

## Troubleshooting

| Problema | Solución |
|---------|----------|
| "0 images" | Esperar más - JS no cargó |
| "Solo texto" | Mobile viewport + wait_for_timeout |
| "Imágenes repetidas" | Deduplicar por file size |
| "Page blocked" | User-agent móvil + más waits |

## Ejemplo Completo

```bash
# 1. Instalar
npm install -g playwright && npx playwright install chromium

# 2. Scrapear restaurant
python3 scripts/scrape_uber_eats_complete.py \
  "https://www.ubereats.com/cr/store/woods-pizza/Pa5077jjWT-XgqODtJOO8Q" \
  "./woods-pizza-data"

# 3. Ver resultados
cat woods-pizza-data/productos/productos.json
ls woods-pizza-data/imagenes/
```

## API Keys

No requiere API keys. Solo usa requests para descargar imágenes del CDN público de Uber Eats.

## Nota sobre Uber Eats

- Las imágenes se cargan lazily (solo cuando están visibles)
- El deep scroll (bounce) ayuda a cargar más imágenes
- No todas las imágenes del menú están disponibles via scraping
- Para acceso completo se necesitaría la API interna

---

_Skill creado: 2026-04-12_