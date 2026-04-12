#!/usr/bin/env python3
"""
Scrape Uber Eats full menu with Playwright - Complete version
Usage: python3 scrape_uber_eats_complete.py <store_url> <output_dir>
"""
import asyncio
from playwright.async_api import async_playwright
import json, requests, os, sys

async def scrape_store(url, output_dir):
    os.makedirs(f"{output_dir}/imagenes", exist_ok=True)
    os.makedirs(f"{output_dir}/screenshots", exist_ok=True)
    os.makedirs(f"{output_dir}/productos", exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 412, "height": 915})
        page = await context.new_page()
        
        print(f"Loading {url}...")
        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        
        # Deep scroll to load all lazy content
        print("Scrolling through menu...")
        total_height = await page.evaluate("document.body.scrollHeight")
        for i in range(20):
            for y in range(0, total_height, 300):
                await page.evaluate(f"window.scrollTo(0, {y})")
                await page.wait_for_timeout(150)
            await page.evaluate("window.scrollTo(0, 0)")
            await page.wait_for_timeout(300)
        
        # Get all images
        images = await page.evaluate("""
            () => [...new Set(Array.from(document.querySelectorAll('img'))
                .filter(img => img.src && img.naturalWidth > 0)
                .map(img => img.src))]
        """)
        
        # Get sections
        sections = await page.evaluate("""
            () => Array.from(document.querySelectorAll('h2')).map(h => h.textContent.trim())
        """)
        
        # Full page screenshot
        await page.screenshot(path=f"{output_dir}/screenshots/menu_completo.png", full_page=True)
        
        await browser.close()
        
        # Download images
        downloaded = 0
        for i, img_url in enumerate(images):
            if 'tb-static.uber.com' not in img_url:
                continue
            ext = img_url.split('.')[-1].split('?')[0][:3]
            if ext not in ['jpg', 'png']:
                ext = 'jpg'
            filename = f"{output_dir}/imagenes/img_{i+1:03d}.{ext}"
            try:
                r = requests.get(img_url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
                if r.status_code == 200 and len(r.content) > 3000:
                    with open(filename, 'wb') as f:
                        f.write(r.content)
                    downloaded += 1
            except:
                pass
        
        print(f"✅ Done! Images: {downloaded}, Sections: {len(sections)}")
        return {'images': downloaded, 'sections': sections}

if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else "https://www.ubereats.com/cr/store/woods-pizza-a-la-lena-cartago/Pa5077jjWT-XgqODtJOO8Q"
    output = sys.argv[2] if len(sys.argv) > 2 else "/root/.openclaw/workspace-magnum/woods-pizza-data"
    asyncio.run(scrape_store(url, output))
