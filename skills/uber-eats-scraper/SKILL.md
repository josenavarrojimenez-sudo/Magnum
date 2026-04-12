---
name: uber-eats-scraper
description: Skill para scraping de menús de Uber Eats usando Playwright. Captura productos, precios, categorías, imágenes y screenshots de cualquier restaurant en Uber Eats. Incluye técnicas de bypass anti-bot usando mobile viewport y deep scroll. Se activa con frases como scrapear Uber Eats, capturar menú de restaurante, extraer imágenes de delivery, hacer scraping de comida, o descargar menú completo de restaurante online.
---

# SKILL: UBER EATS SCRAPER

## Descripción

Este skill permite hacer scraping completo de menús de Uber Eats con renderizado JavaScript. Captura:
- Productos (nombre, descripción, precio)
- Categorías
- Imágenes de platos
- Screenshots del menú

## Uso

```bash
# Installation (solo una vez)
npm install -g playwright
npx playwright install chromium

# Scraping
python3 scripts/scrape_uber_eats_complete.py "URL_RESTAURANTE" "./output"
```

## Técnicas de Bypass Anti-Bot

### 1. Mobile Viewport
```python
context = await browser.new_context(
    viewport={"width": 412, "height": 915},
    user_agent="Mozilla/5.0 (Linux; Android 11; SM-G991B)..."
)
```

### 2. Deep Scroll (Bounce)
```python
for i in range(15):
    for y in range(0, total_height, 300):
        await page.evaluate(f"window.scrollTo(0, {y})")
        await page.wait_for_timeout(150)
    await page.evaluate("window.scrollTo(0, 0)")
```

### 3. Wait for JS
```python
await page.wait_for_timeout(5000)  # Esperar que cargue JS
```

## Estructura de Output

```
output/
├── productos/productos.json    # Items estructurados
├── imagenes/                    # Fotos de comida
├── screenshots/                 # Capturas de pantalla
└── data/                       # Datos crudos
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

---

_Creado: 2026-04-12_