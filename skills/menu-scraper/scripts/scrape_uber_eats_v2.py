#!/usr/bin/env python3
"""
Scrape Uber Eats menu with Playwright - Version 2
Uses mobile viewport and more waiting time to bypass anti-bot
"""
import sys
import os
import json
import time
import asyncio

async def scrape_menu():
    from playwright.async_api import async_playwright
    
    url = "https://www.ubereats.com/cr/store/woods-pizza-a-la-lena-cartago/Pa5077jjWT-XgqODtJOO8Q"
    output_dir = "/root/.openclaw/workspace-magnum/memory/woods_pizza_full"
    
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(f"{output_dir}/images", exist_ok=True)
    
    print(f"Starting scrape of: {url}")
    
    async with async_playwright() as p:
        # Try with slower network simulation to avoid bot detection
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox'
            ]
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
            viewport={"width": 390, "height": 844},
            locale="es-CR",
            extra_http_headers={
                "Accept-Language": "es-419,es;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
            }
        )
        
        page = await context.new_page()
        
        # Set extra HTTP headers
        await context.set_extra_http_headers({
            "Accept-Language": "es-CR,es;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        })
        
        print("Loading page with mobile viewport...")
        
        try:
            response = await page.goto(url, wait_until="domcontentloaded", timeout=45000)
            print(f"Page status: {response.status if response else 'no response'}")
        except Exception as e:
            print(f"Navigation error: {e}")
        
        # Wait for content to load
        print("Waiting for content...")
        await page.wait_for_timeout(5000)
        
        # Check what's on the page
        page_content = await page.content()
        print(f"Page HTML length: {len(page_content)} chars")
        
        # Check for any visible text
        body_text = await page.evaluate("document.body.innerText")
        print(f"Body text length: {len(body_text)} chars")
        print(f"Body snippet: {body_text[:500]}...")
        
        # Take a screenshot to see what's rendered
        await page.screenshot(path=f"{output_dir}/debug_screenshot.png", full_page=False)
        print("📸 Took debug screenshot")
        
        # Try to find menu items with various selectors
        menu_selectors = [
            "[data-testid='store-menu-item']",
            ".store-menu-item",
            "[class*='menu-item']",
            "article",
            "[class*='SectionHeader']",
            "h2"
        ]
        
        for selector in menu_selectors:
            count = await page.locator(selector).count()
            if count > 0:
                print(f"Found {count} items with selector: {selector}")
        
        # Try executing JavaScript to get all images
        images = await page.evaluate("""
            () => {
                const imgs = Array.from(document.querySelectorAll('img'));
                return imgs.map(img => ({
                    src: img.src,
                    loaded: img.complete && img.naturalWidth > 0
                })).filter(img => img.src.includes('uber') || img.src.includes('cdn'));
            }
        """)
        print(f"Found {len(images)} images via JS")
        
        # Get all sections
        sections = await page.evaluate("""
            () => {
                const headers = Array.from(document.querySelectorAll('h1, h2, h3'));
                return headers.map(h => h.textContent.trim()).filter(t => t.length > 0 && t.length < 100);
            }
        """)
        print(f"Sections found: {sections}")
        
        await browser.close()
        
        # Save data
        with open(f"{output_dir}/debug_data.json", 'w') as f:
            json.dump({
                'body_text': body_text[:2000],
                'images': images,
                'sections': sections
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Debug complete!")
        print(f"📁 Output: {output_dir}")

if __name__ == '__main__':
    asyncio.run(scrape_menu())