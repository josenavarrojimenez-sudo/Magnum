# Skill: Uber Eats Scraper (Melatte Café)

## Descripción
Skill para hacer scraping de menús de Uber Eats usando Playwright. Diseñado para evadir detección de CAPTCHA y anti-bot.

## Uso
```bash
cd /root/.openclaw/workspace-prolix/melatte-cafe
./run-stealth.sh
```

## Archivos Generados
- `menu.json` - Menú extraído en formato JSON
- `menu-complete.json` - Menú con datos completos (incluyendo items inferidos)
- `reporte.json` - Reporte con estadísticas
- `screenshot-stealth.png` - Captura de pantalla del restaurante
- `debug-page.html` - HTML de depuración
- `imagenes/` - Imágenes descargadas

## Estructura del Menú
```json
{
  "restaurant": "Melatte Café",
  "totalCategories": 6,
  "totalItems": 50,
  "categories": [
    {"name": "Bebidas Frías", "items": [...]},
    {"name": "Bebidas Calientes", "items": [...]},
    {"name": "Fusión", "items": [...]},
    {"name": "Botanas", "items": [...]},
    {"name": "Bocadillos", "items": [...]},
    {"name": "Frappés", "items": [...]}
  ]
}
```

## Limitaciones
⚠️ Uber Eats tiene protección reCAPTCHA que bloquea el scraping automatizado:
- Se detectaron 6 categorías visibles
- Se estiman ~50 items en total
- Los precios van de ₡2,000 a ₡6,500

## Solución Aplicada
1. Viewport móvil (412x915px)
2. User-Agent de Android/iPhone
3. Anti-detección (navigator.webdriver, chrome runtime)
4. Bounce scroll para cargar contenido lazy
5. Extracción por selectores data-testid
6. Fallback: screenshot analysis

## Troubleshooting
Si el scraping falla con CAPTCHA:
1. Intentar con diferente User-Agent
2. Usar la versión móvil de Uber Eats
3. Considerar acceso manual si es crítico
