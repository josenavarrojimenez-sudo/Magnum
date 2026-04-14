# UBER EATS SCRAPER - Technical Reference

## Complete Playwright Setup

### Installation
```bash
npm install -g playwright
npx playwright install chromium
```

### Key Scripts

#### scrape_uber_eats_v2.py (Debug)
```python
import asyncio
from playwright.async_api import async_playwright

async def debug_scrape():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 390, "height": 844},
            user_agent="Mozilla/5.0 (Linux; Android 11; SM-G991B)..."
        )
        page = await context.new_page()
        
        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_timeout(5000)
        
        # Get body text and sections
        body_text = await page.evaluate("document.body.innerText")
        sections = await page.evaluate("""
            () => Array.from(document.querySelectorAll('h2'))
                .map(h => h.textContent.trim())
        """)
        
        # Get images
        images = await page.evaluate("""
            () => Array.from(document.querySelectorAll('img'))
                .filter(img => img.src && img.naturalWidth > 0)
                .map(img => ({src: img.src, loaded: img.complete}))
        """)
        
        await page.screenshot(path="debug.png")
        await browser.close()
```

#### Deep Scroll (Bounce Technique)
```python
async def deep_scroll(page, bounces=15):
    total_height = await page.evaluate("document.body.scrollHeight")
    
    for i in range(bounces):
        for y in range(0, total_height, 300):
            await page.evaluate(f"window.scrollTo(0, {y})")
            await page.wait_for_timeout(150)
        
        await page.evaluate("window.scrollTo(0, 0)")
        await page.wait_for_timeout(500)
```

#### Extract All Images
```python
images = await page.evaluate("""
    () => [...new Set(
        Array.from(document.querySelectorAll('img'))
        .filter(img => img.src && img.naturalWidth > 0)
        .map(img => img.src)
    )]
""")
```

#### Download with Requests
```python
import requests

for i, url in enumerate(images):
    ext = url.split('.')[-1].split('?')[0][:3]
    if ext not in ['jpg', 'png']:
        ext = 'jpg'
    
    r = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
    if r.status_code == 200 and len(r.content) > 3000:
        with open(f"output/img_{i:03d}.{ext}", 'wb') as f:
            f.write(r.content)
```

## Image Deduplication Logic

```python
# Remove duplicates by comparing file sizes
import os

files = os.listdir('images/')
size_map = {}

for f in files:
    size = os.path.getsize(f"images/{f}")
    if size not in size_map:
        size_map[size] = f
    else:
        os.remove(f"images/{f}")  # Duplicate
```

## Filter Real Food Photos

```python
# Real food photos are >30KB
# Icons/logos are <10KB

for f in files:
    size = os.path.getsize(f"images/{f}")
    if size > 30000:
        # It's a real food photo
```

## Full Page Screenshot

```python
# Full page can be 12,000+ pixels tall
await page.screenshot(path="full_menu.png", full_page=True)
```

## JSON Structure for Products

```json
{
  "restaurante": "Woods Pizza a la Leña Cartago",
  "ubicacion": "219 Carmen, Cartago",
  "telefono": "+506 8391 6946",
  "rating": 4.6,
  "productos": [
    {
      "id": 1,
      "nombre": "Pizza Pepperoni",
      "descripcion": "Pepperoni. Tamaño mediano de 8 porciones.",
      "categoria": "Pizza",
      "precio": 9790.00,
      "moneda": "CRC"
    }
  ]
}
```

## Troubleshooting Matrix

| Symptom | Cause | Fix |
|---------|-------|-----|
| Page loads but no content | JS not executed | Add wait_for_timeout(5000) |
| 0 images found | No lazy load | Use deep scroll (bounce) |
| Only section headers | Anti-bot blocking | Use mobile viewport |
| Images too small | Icons not photos | Filter by size >30KB |
| Duplicates | Same image in multiple sections | Deduplicate by file size |

## Uber Eats URL Patterns

- Store: `https://www.ubereats.com/cr/store/{slug}/{storeId}`
- Data: JSON-LD in `<script type="application/ld+json">`
- Images: `https://tb-static.uber.com/prod/image-proc/processed_images/{hash}/{filename}`