#!/usr/bin/env python3
"""
Parse restaurant menu from JSON-LD data and generate formatted output.
Usage: python3 parse_menu.py <json_file> [--format md|json]
"""
import sys
import json
import os

def format_price(price):
    """Format price as CRC with ₡ symbol."""
    try:
        return f"₡{float(price):,.0f}"
    except:
        return str(price)

def parse_to_markdown(data):
    """Convert JSON-LD to formatted markdown."""
    output = []
    
    # Restaurant info
    output.append(f"# {data.get('name', 'Restaurant')}\n")
    addr = data.get('address', {})
    output.append(f"**Dirección:** {addr.get('streetAddress', 'N/A')}, {addr.get('addressLocality', 'N/A')}\n")
    output.append(f"**Teléfono:** {data.get('telephone', 'N/A')}\n")
    
    rating = data.get('aggregateRating', {})
    output.append(f"**Rating:** ⭐ {rating.get('ratingValue', 'N/A')}/5 ({rating.get('reviewCount', 'N/A')} reviews)\n")
    
    # Menu sections
    menu = data.get('hasMenu', {})
    total_items = 0
    
    for section in menu.get('hasMenuSection', []):
        items = section.get('hasMenuItem', [])
        total_items += len(items)
        output.append(f"\n## {section['name']} ({len(items)} items)\n")
        
        for item in items:
            name = item.get('name', 'N/A')
            desc = item.get('description', '')
            price_data = item.get('offers', {})
            price = format_price(price_data.get('price', '0'))
            
            output.append(f"### {name}\n")
            if desc:
                output.append(f"_{desc}_\n")
            output.append(f"**Precio:** {price}\n")
    
    output.append(f"\n---\n**Total: {total_items} items**\n")
    return ''.join(output)

def parse_to_json(data):
    """Convert JSON-LD to simplified JSON structure."""
    result = {
        'name': data.get('name'),
        'address': data.get('address', {}),
        'phone': data.get('telephone'),
        'rating': data.get('aggregateRating', {}),
        'menu': []
    }
    
    for section in data.get('hasMenu', {}).get('hasMenuSection', []):
        section_data = {
            'name': section['name'],
            'items': []
        }
        for item in section.get('hasMenuItem', []):
            section_data['items'].append({
                'name': item['name'],
                'description': item.get('description', ''),
                'price': item.get('offers', {}).get('price', '')
            })
        result['menu'].append(section_data)
    
    return json.dumps(result, ensure_ascii=False, indent=2)

def main():
    if len(sys.argv) < 2:
        print("Usage: parse_menu.py <json_file> [--format md|json]")
        sys.exit(1)
    
    json_file = sys.argv[1]
    format_type = 'md'
    
    if len(sys.argv) > 2 and sys.argv[2] == '--format':
        if len(sys.argv) > 3:
            format_type = sys.argv[3]
    
    with open(json_file) as f:
        data = json.load(f)
    
    if format_type == 'json':
        print(parse_to_json(data))
    else:
        print(parse_to_markdown(data))

if __name__ == '__main__':
    main()