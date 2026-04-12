#!/usr/bin/env python3
"""
Download images from restaurant schema data.
Usage: python3 download_images.py <json_file> <output_dir>
"""
import sys
import json
import os
import requests

def download_images(json_file, output_dir):
    with open(json_file) as f:
        data = json.load(f)
    
    os.makedirs(output_dir, exist_ok=True)
    
    images = data.get('image', [])
    if isinstance(images, str):
        images = [images]
    
    for i, url in enumerate(images, 1):
        url = url.replace('\\/', '/')
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                ext = url.split('.')[-1].split('?')[0][:4]
                filename = f"img_{i}.{ext}"
                filepath = os.path.join(output_dir, filename)
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"✅ Downloaded: {filename}")
            else:
                print(f"❌ Failed ({response.status_code}): {url}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 download_images.py <json_file> <output_dir>")
        sys.exit(1)
    download_images(sys.argv[1], sys.argv[2])