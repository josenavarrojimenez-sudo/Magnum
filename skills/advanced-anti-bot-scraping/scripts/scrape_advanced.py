#!/usr/bin/env python3
"""
Advanced Anti-Bot Scraper - Prolix Edition
Scraping con técnicas de bypass anti-bot de vanguardia
"""
import asyncio
import random
import time
import json
from datetime import datetime
from pathlib import Path
import playwright
from playwright.async_api import async_playwright

class AdvancedScraper:
    def __init__(self):
        self.profiles = []
        self.rotator = Rotator()
        
    async def scrape_uber_eats_advanced(self, url, output_dir):
        """Scraping avanzado de Uber Eats con anti-bot"""
        async with async_playwright() as p:
            # Configuración stealth avanzada
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15'
                ]
            )
            
            # Contexto mobile con fingerprints
            context = await browser.new_context(
                viewport={'width': 375, 'height': 812},
                user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
                extra_http_headers=self.rotator.get_headers()
            )
            
            # Inyectar scripts anti-detección
            await context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['es-ES', 'es', 'en'],
                });
            """)
            
            page = await context.new_page()
            
            try:
                # Navegar con comportamientos humanos
                await self.human_navigate(page, url)
                
                # Esperar a que cargue JavaScript
                await page.wait_for_timeout(3000)
                
                # Scroll humano profundo
                await self.human_scroll_deep(page)
                
                # Esperar carga dinámica
                await page.wait_for_timeout(5000)
                
                # Extraer datos
                data = await self.extract_data(page)
                
                # Guardar todo
                await self.save_data(data, output_dir)
                
                return data
                
            except Exception as e:
                print(f"Error: {e}")
                return None
            finally:
                await browser.close()
    
    async def human_navigate(self, page, url):
        """Navegación con comportamiento humano"""
        # Simular typing humano
        for char in "https://www.ubereats.com/cr/store/woods-pizza-a-la-lena-cartago/":
            await page.keyboard.type(char)
            await asyncio.sleep(random.uniform(0.05, 0.15))
        
        await page.keyboard.press('Enter')
        
        # Esperar carga con variabilidad humana
        await asyncio.sleep(random.uniform(2, 5))
    
    async def human_scroll_deep(self, page):
        """Scroll profundo con comportamiento humano"""
        total_height = await page.evaluate('document.body.scrollHeight')
        
        for i in range(0, int(total_height), 200):
            # Scroll con movimiento humano
            await page.evaluate(f'window.scrollTo(0, {i})')
            
            # Pausas variables
            await asyncio.sleep(random.uniform(0.3, 0.8))
            
            # Movimiento del mouse aleatorio
            await self.random_mouse_movement(page)
            
            # Scroll back lento (comportamiento real)
            if i > 1000:
                await page.evaluate(f'window.scrollTo(0, {i-100})')
                await asyncio.sleep(random.uniform(0.2, 0.5))
    
    async def random_mouse_movement(self, page):
        """Movimiento aleatorio del mouse"""
        viewport_size = await page.viewport_size
        x = random.randint(0, viewport_size['width'])
        y = random.randint(0, viewport_size['height'])
        
        await page.mouse.move(x, y)
        await asyncio.sleep(random.uniform(0.1, 0.3))
    
    async def extract_data(self, page):
        """Extracción de datos con múltiples estrategias"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'url': page.url,
            'products': [],
            'categories': [],
            'images': []
        }
        
        # Esperar elementos con retries
        try:
            # Productos
            products = await page.query_selector_all('[data-testid="card"], [data-testid="item"], .menuItem, .product')
            
            for product in products:
                try:
                    name = await product.query_selector('h3, .name, .title') or await product.query_selector('text')
                    price = await product.query_selector('.price, .cost') or await product.query_selector('text')
                    image = await product.query_selector('img') or await product.query_selector('.image')
                    
                    product_data = {
                        'name': await name.inner_text() if name else 'Unknown',
                        'price': await price.inner_text() if price else 'Unknown',
                        'image': await image.get_attribute('src') if image else None
                    }
                    
                    data['products'].append(product_data)
                    
                    # Descargar imágenes
                    if image and product_data['image']:
                        await self.download_image(product_data['image'], data)
                        
                except Exception as e:
                    print(f"Error extracting product: {e}")
                    continue
            
            # Categorías
            categories = await page.query_selector_all('.category, .section, .category-title')
            for category in categories:
                name = await category.query_selector('h2, h3, .title') or await category
                category_name = await name.inner_text() if name else 'Unknown'
                data['categories'].append(category_name)
                
        except Exception as e:
            print(f"Error in extraction: {e}")
        
        return data
    
    async def download_image(self, url, data):
        """Descarga de imágenes con headers rotatorios"""
        try:
            headers = self.rotator.get_headers()
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    filename = f"image_{len(data['images'])}.jpg"
                    filepath = Path(f"/tmp/{filename}")
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    data['images'].append({
                        'url': url,
                        'filename': filename,
                        'size': len(response.content)
                    })
        except Exception as e:
            print(f"Error downloading image: {e}")
    
    async def save_data(self, data, output_dir):
        """Guardar datos estructurados"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # JSON estructurado
        with open(output_path / "data.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Productos
        with open(output_path / "productos.json", 'w', encoding='utf-8') as f:
            json.dump(data['products'], f, indent=2, ensure_ascii=False)
        
        # Categorías
        with open(output_path / "categorias.json", 'w', encoding='utf-8') as f:
            json.dump(data['categories'], f, indent=2, ensure_ascii=False)
        
        # Imágenes
        images_dir = output_path / "imagenes"
        images_dir.mkdir(exist_ok=True)
        
        for image in data['images']:
            try:
                import shutil
                shutil.move(f"/tmp/{image['filename']}", images_dir / image['filename'])
            except:
                pass

class Rotator:
    """Clase para rotación de headers y user agents"""
    
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15',
            'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        ]
        
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    def get_headers(self):
        """Obtener headers rotatorios"""
        headers = self.headers.copy()
        headers['User-Agent'] = random.choice(self.user_agents)
        headers['X-Forwarded-For'] = self.random_ip()
        return headers
    
    def random_ip(self):
        """Generar IP aleatoria"""
        return f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"

async def main():
    scraper = AdvancedScraper()
    
    url = "https://www.ubereats.com/cr/store/woods-pizza-a-la-lena-cartago/"
    output_dir = "/root/.openclaw/workspace-prolix/woods-pizza-advanced"
    
    print("🔮 Iniciando scraping avanzado de Woods Pizza a la Llená...")
    print(f"🎯 URL: {url}")
    print(f"💾 Output: {output_dir}")
    
    data = await scraper.scrape_uber_eats_advanced(url, output_dir)
    
    if data:
        print(f"✅ Extracción completada!")
        print(f"📦 Productos encontrados: {len(data['products'])}")
        print(f"📂 Categorías encontradas: {len(data['categories'])}")
        print(f"🖼️ Imágenes descargadas: {len(data['images'])}")
    else:
        print("❌ Error en la extracción")

if __name__ == "__main__":
    asyncio.run(main())