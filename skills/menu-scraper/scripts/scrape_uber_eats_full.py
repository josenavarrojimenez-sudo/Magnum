#!/usr/bin/env python3
"""
Scrape Uber Eats menu - Full version with section screenshots
"""
import sys
import os
import json
import asyncio

async def scrape_menu():
    from playwright.async_api import async_playwright
    import requests
    
    url = "https://www.ubereats.com/cr/store/woods-pizza-a-la-lena-cartago/Pa5077jjWT-XgqODtJOO8Q"
    output_dir = "/root/.openclaw/workspace-magnum/memory/woods_pizza_full"
    
    os.makedirs(f"{output_dir}/sections", exist_ok=True)
    os.makedirs(f"{output_dir}/images", exist_ok=True)
    
    print(f"Starting full scrape: {url}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled', '--disable-dev-shm-usage', '--no-sandbox']
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 Chrome/91.0.4472.120 Mobile Safari/537.36",
            viewport={"width": 390, "height": 844},
            locale="es-CR"
        )
        
        page = await context.new_page()
        await page.set_extra_http_headers({"Accept-Language": "es-CR"})
        
        print("Loading page...")
        await page.goto(url, wait_until="domcontentloaded", timeout=45000)
        await page.wait_for_timeout(3000)
        
        # Get all sections
        sections = await page.evaluate("""
            () => {
                const headers = Array.from(document.querySelectorAll('h2'));
                return headers.map(h => h.textContent.trim()).filter(t => t.length > 0 && t.length < 50);
            }
        """)
        
        print(f"Found {len(sections)} sections: {sections}")
        
        # Scroll and screenshot each section
        menu_items = []
        
        for i, section in enumerate(sections):
            try:
                # Find section header
                await page.evaluate(f"""
                    () => {{
                        const headers = Array.from(document.querySelectorAll('h2'));
                        const target = headers.find(h => h.textContent.includes('{section}'));
                        if (target) {{
                            target.scrollIntoView({{ block: 'center' }});
                        }}
                    }}
                """)
                await page.wait_for_timeout(2000)
                
                # Screenshot section
                filename = f"section_{i+1}_{section[:15].replace(' ', '_').replace('/', '_')}.png"
                await page.screenshot(path=f"{output_dir}/sections/{filename}", full_page=False)
                print(f"  📸 {section}: captured")
                
                # Extract items from this section
                items = await page.evaluate(f"""
                    () => {{
                        const items = [];
                        // Find section header
                        const headers = Array.from(document.querySelectorAll('h2'));
                        const targetHeader = headers.find(h => h.textContent.includes('{section}'));
                        if (!targetHeader) return items;
                        
                        // Get all sibling elements until next h2
                        let el = targetHeader.nextElementSibling;
                        let itemCount = 0;
                        
                        while (el && itemCount < 20) {{
                            if (el.tagName === 'H2') break; // Next section
                            
                            // Look for menu item data
                            const article = el.querySelector('article, [class*="Item"], [class*="Card"]');
                            if (article) {{
                                const name = article.querySelector('h3, [class*="name"], [class*="title"]');
                                const price = article.querySelector('[class*="price"], [class*="Price"]');
                                const img = article.querySelector('img');
                                const desc = article.querySelector('[class*="description"], p');
                                
                                if (name) {{
                                    items.push({{
                                        name: name.textContent.trim(),
                                        price: price ? price.textContent.trim() : 'N/A',
                                        description: desc ? desc.textContent.trim() : '',
                                        image: img ? img.src : ''
                                    }});
                                }}
                            }}
                            el = el.nextElementSibling;
                            itemCount++;
                        }}
                        return items;
                    }}
                """)
                
                if items:
                    menu_items.extend(items)
                    print(f"    → {len(items)} items extracted")
                
            except Exception as e:
                print(f"  ❌ Error in section '{section}': {e}")
        
        # Get all images
        print("\nExtracting images...")
        all_images = await page.evaluate("""
            () => {
                const imgs = Array.from(document.querySelectorAll('img'));
                return imgs
                    .map(img => img.src)
                    .filter(src => src && (src.includes('uber.com') || src.includes('tb-static')));
            }
        """)
        
        print(f"Found {len(all_images)} images")
        
        # Download images
        downloaded = 0
        for i, img_url in enumerate(all_images):
            try:
                ext = img_url.split('.')[-1].split('?')[0][:4]
                if ext not in ['jpg', 'png', 'webp']:
                    ext = 'jpg'
                filename = f"img_{i+1}.{ext}"
                
                response = requests.get(img_url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
                if response.status_code == 200 and len(response.content) > 1000:
                    with open(f"{output_dir}/images/{filename}", 'wb') as f:
                        f.write(response.content)
                    downloaded += 1
                    print(f"  ✅ {filename} ({len(response.content)//1024}KB)")
            except Exception as e:
                pass
        
        # Full page screenshot
        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        await page.screenshot(path=f"{output_dir}/full_menu.png", full_page=True)
        
        await browser.close()
        
        # Save data
        final_data = {
            'restaurant': 'Woods Pizza a la Leña Cartago',
            'url': url,
            'sections': sections,
            'menu_items': menu_items,
            'images': all_images,
            'total_items': len(menu_items),
            'total_images': len(all_images),
            'downloaded_images': downloaded
        }
        
        with open(f"{output_dir}/full_menu_data.json", 'w') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ SCRAPING COMPLETE!")
        print(f"📁 Output: {output_dir}")
        print(f"📋 Sections: {len(sections)}")
        print(f"🍕 Menu items: {len(menu_items)}")
        print(f"🖼️ Images found: {len(all_images)}")
        print(f"💾 Images downloaded: {downloaded}")
        print(f"📸 Section screenshots: {len(sections)}")

if __name__ == '__main__':
    asyncio.run(scrape_menu())