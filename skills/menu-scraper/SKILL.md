# UBER EATS SCRAPER - Complete Toolkit

## Overview

Este skill permite hacer scraping completo de menús de Uber Eats usando Playwright para ejecutar JavaScript y capturar contenido dinámico.

## Herramientas Disponibles

### 1. Playwright Setup
```bash
npm install -g playwright
npx playwright install chromium
```

### 2. Scripts Disponibles

| Script | Purpose |
|--------|---------|
| `scrape_uber_eats_v2.py` | Debug - captura estructura básica |
| `scrape_uber_eats_full.py` | Full scraping con screenshots |
| `scrape_uber_eats_complete.py` | Complete con deep scroll |
| `download_images.py` | Descarga imágenes desde URLs JSON |
| `parse_menu.py` | Parsea JSON-LD a markdown/JSON |

### 3. Técnicas de Scraping

#### a) Page Load + Basic Scroll
```python
await page.goto(url, wait_until="domcontentloaded")
await page.wait_for_timeout(3000)
```

#### b) Deep Scroll (Bounce technique)
```python
for i in range(15):
    for y in range(0, total_height, 400):
        await page.evaluate(f"window.scrollTo(0, {y})")
        await page.wait_for_timeout(300)
    await page.evaluate("window.scrollTo(0, 0)")
```

#### c) Mobile Viewport (bypassa anti-bot)
```python
context = await browser.new_context(
    viewport={"width": 412, "height": 915},
    user_agent="Mozilla/5.0 (Linux; Android 11; SM-G991B)..."
)
```

#### d) Extract Images
```python
images = await page.evaluate("""
    () => [...new Set(Array.from(document.querySelectorAll('img'))
        .filter(img => img.src && img.naturalWidth > 0)
        .map(img => img.src))]
""")
```

## Workflow Completo

1. **Install Playwright** (una vez)
2. **Load page** con mobile viewport
3. **Deep scroll** para cargar imágenes lazy
4. **Extract images** y deduplicate
5. **Download** imágenes >30KB (fotos reales)
6. **Save** JSON con menú estructurado

## Estructura de Output

```
woods-pizza-data/
├── productos/productos.json   # 86 items estructurados
├── imagenes/                   # 75 fotos de comida
├── screenshots/                # menu_completo.png
└── data/                       # datos crudos
```

## Notas Técnicas

- Uber Eats usa lazy loading - imágenes solo cargan cuando están en viewport
- Mobile viewport ayuda a bypass anti-bot detection
- Deduplicación: mismo tamaño = misma imagen
- Filtrar: >30KB = foto real de comida, <10KB = ícono/logo
- Full page screenshot puede llegar a 12,000+ px de altura

## Troubleshooting

| Problema | Solución |
|----------|----------|
| 0 images | Verificar que page cargó JS (wait_for_timeout) |
| Solo secciones vacías | Usar mobile viewport |
| Imágenes repetidas | Deduplicate por tamaño |
| Page blocked | Usar user-agent mobile + wait más largo |

## Ejemplo de Uso

```bash
# Instalar
npm install -g playwright
npx playwright install chromium

# Scrapear
python3 scripts/scrape_uber_eats_complete.py "URL_UBER_EATS" ./output
```

## API Keys Necesarias

Ninguna - solo curl y requests (para descarga de imágenes).