#!/usr/bin/env python3
"""
Scrape Uber Eats menu with images using Playwright.
Usage: python3 scrape_uber_eats.py <store_url> <output_dir>
"""
import sys
import os
import json
import time

async def scrape_menu():
    from playwright.async_api import async_playwright
    
    url = sys.argv[1] if len(sys.argv) > 1 else "https://www.ubereats.com/cr/store/woods-pizza-a-la-lena-cartago/Pa5077jjWT-XgqODtJOO8Q"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "/root/.openclaw/workspace-magnum/memory/woods_pizza_full"
    
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(f"{output_dir}/images", exist_ok=True)
    
    print(f"Starting scrape of: {url}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="es-CR"
        )
        page = await context.new_page()
        
        # Block images that are not menu items to speed up
        await page.route("**/*", lambda route: route.fulfill(path="/dev/null") if route.request.resource_type == "image" and "menu" not in route.request.url else route.continue_())
        
        print("Loading page...")
        await page.goto(url, wait_until="networkidle", timeout=60000)
        
        # Wait for menu to load
        print("Waiting for menu content...")
        try:
            await page.wait_for_selector("[data-testid='section-header'], h2", timeout=10000)
        except:
            pass
        
        # Scroll to load all content
        print("Scrolling to load all content...")
        last_height = 0
        scroll_count = 0
        while scroll_count < 50:  # Max 50 scrolls
            await page.evaluate("window.scrollBy(0, 500)")
            await page.wait_for_timeout(500)
            new_height = await page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            scroll_count += 1
        
        # Get all section titles and items
        print("Extracting menu sections...")
        sections = await page.evaluate("""
            () => {
                const result = [];
                // Try multiple selectors for sections
                const sectionHeaders = document.querySelectorAll('h2, h3, [data-testid="section-header"], .section-header');
                const menuItems = document.querySelectorAll('[data-testid="store-menu-item"], .menu-item, article');
                
                // Get all text content organized
                const allText = document.body.innerText;
                
                return {
                    sections: Array.from(sectionHeaders).map(h => h.textContent.trim()).filter(t => t.length > 0 && t.length < 100),
                    menuItemsCount: menuItems.length,
                    pageTitle: document.title,
                    bodySnippet: allText.substring(0, 2000)
                };
            }
        """)
        
        print(f"Found {sections.get('menuItemsCount', 0)} menu items")
        print(f"Sections: {sections.get('sections', [])}")
        
        # Take screenshots of each section
        print("Taking screenshots of menu sections...")
        section_names = sections.get('sections', [])
        
        # Scroll back to top
        await page.evaluate("window.scrollTo(0, 0)")
        await page.wait_for_timeout(1000)
        
        # Find and screenshot each section
        for i, section in enumerate(section_names[:20]):  # Limit to 20 sections
            try:
                # Find section by text
                await page.evaluate(f"""
                    () => {{
                        const headers = Array.from(document.querySelectorAll('h2, h3'));
                        const target = headers.find(h => h.textContent.includes('{section}'));
                        if (target) {{
                            target.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                        }}
                    }}
                """)
                await page.wait_for_timeout(1500)
                
                # Screenshot
                filename = f"section_{i+1}_{section[:20].replace(' ', '_').replace('/', '_')}.png"
                await page.screenshot(path=f"{output_dir}/images/{filename}", full_page=False)
                print(f"  📸 Captured: {filename}")
            except Exception as e:
                print(f"  ❌ Error capturing {section}: {e}")
        
        # Get all images from the page
        print("Extracting all image URLs...")
        images = await page.evaluate("""
            () => {
                const imgElements = document.querySelectorAll('img');
                const images = [];
                imgElements.forEach(img => {
                    const src = img.src || img.dataset.src || img.getAttribute('data-src');
                    if (src && src.includes('uber.com') && !images.includes(src)) {
                        images.push({
                            url: src,
                            alt: img.alt || '',
                            width: img.naturalWidth || 0,
                            height: img.naturalHeight || 0
                        });
                    }
                });
                return images;
            }
        """)
        
        print(f"Found {len(images)} images")
        
        # Download all images
        print("Downloading images...")
        import requests
        for i, img_data in enumerate(images):
            try:
                url_img = img_data['url']
                ext = url_img.split('.')[-1].split('?')[0][:4]
                if ext not in ['jpg', 'png', 'web']:
                    ext = 'jpg'
                filename = f"img_{i+1}.{ext}"
                response = requests.get(url_img, timeout=10)
                if response.status_code == 200:
                    with open(f"{output_dir}/images/{filename}", 'wb') as f:
                        f.write(response.content)
                    print(f"  ✅ {filename} ({len(response.content)} bytes)")
            except Exception as e:
                print(f"  ❌ Error downloading image {i}: {e}")
        
        # Save menu data
        menu_data = {
            'url': url,
            'sections': section_names,
            'total_images': len(images),
            'images': [img['url'] for img in images]
        }
        
        with open(f"{output_dir}/menu_data.json", 'w') as f:
            json.dump(menu_data, f, ensure_ascii=False, indent=2)
        
        # Full page screenshot
        print("Taking full page screenshot...")
        await page.screenshot(path=f"{output_dir}/full_menu.png", full_page=True)
        
        await browser.close()
        
        print(f"\n✅ Scraping complete!")
        print(f"📁 Output: {output_dir}")
        print(f"📸 Sections screenshots: {len(section_names)}")
        print(f"🖼️ Individual images: {len(images)}")
        
        return output_dir

if __name__ == '__main__':
    import asyncio
    asyncio.run(scrape_menu())