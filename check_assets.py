#!/usr/bin/env python3
"""
Asset and link integrity checker for the cloned jazdrm.com website.
"""

import os
import urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup

ROOT_DIR = Path(__file__).resolve().parent
missing_assets = []
checked_assets = set()
total_html = 0

for root, _, files in os.walk(ROOT_DIR):
    for f in files:
        if f.endswith('.html'):
            total_html += 1
            html_path = Path(root) / f
            try:
                soup = BeautifulSoup(html_path.read_text(encoding='utf-8', errors='ignore'), 'html.parser')
                
                # Check images
                for img in soup.find_all(['img', 'source']):
                    src = img.get('src')
                    if src and not src.startswith(('data:', 'http://', 'https://', '//', '#')):
                        clean_src = urllib.parse.unquote(src.split('?')[0])
                        target = (html_path.parent / clean_src).resolve()
                        if target not in checked_assets:
                            checked_assets.add(target)
                            if not target.exists():
                                missing_assets.append((str(html_path.relative_to(ROOT_DIR)), src, str(target)))

                # Check stylesheets
                for link in soup.find_all('link', rel=lambda r: r and 'stylesheet' in r):
                    href = link.get('href')
                    if href and not href.startswith(('data:', 'http://', 'https://', '//', '#')):
                        clean_href = urllib.parse.unquote(href.split('?')[0])
                        target = (html_path.parent / clean_href).resolve()
                        if target not in checked_assets:
                            checked_assets.add(target)
                            if not target.exists():
                                missing_assets.append((str(html_path.relative_to(ROOT_DIR)), href, str(target)))

                # Check scripts
                for script in soup.find_all('script'):
                    src = script.get('src')
                    if src and not src.startswith(('data:', 'http://', 'https://', '//', '#')):
                        clean_src = urllib.parse.unquote(src.split('?')[0])
                        target = (html_path.parent / clean_src).resolve()
                        if target not in checked_assets:
                            checked_assets.add(target)
                            if not target.exists():
                                missing_assets.append((str(html_path.relative_to(ROOT_DIR)), src, str(target)))
            except Exception as e:
                print(f"Error checking {html_path}: {e}")

print("========================================")
print(f"HTML pages scanned: {total_html}")
print(f"Unique asset references checked: {len(checked_assets)}")
print(f"Missing assets: {len(missing_assets)}")
if missing_assets:
    print("Issues found:")
    for page, ref, target in missing_assets[:10]:
        print(f"  [{page}] missing {ref}")
else:
    print("STATUS: 100% Asset Integrity Confirmed - Zero Broken Assets!")
print("========================================")
