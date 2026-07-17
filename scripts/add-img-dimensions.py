#!/usr/bin/env python3
"""
Add explicit width and height attributes to <img> tags in HTML files.
Handles minified HTML (Hugo --minify strips attribute quotes).
Prevents Cumulative Layout Shift (CLS) by reserving image space.
"""

import os
import re
import struct
import sys

PUBLIC_DIR = sys.argv[1] if len(sys.argv) > 1 else 'public'
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(PUBLIC_DIR)), 'static')
if not os.path.exists(STATIC_DIR):
    STATIC_DIR = os.path.join(os.getcwd(), 'static')

def get_jpeg_size(filepath):
    """Read JPEG dimensions from SOF0 marker."""
    with open(filepath, 'rb') as f:
        data = f.read(1024 * 10)
    i = 0
    while i < len(data) - 1:
        if data[i] == 0xFF and data[i+1] == 0xC0:
            h = struct.unpack('>H', data[i+5:i+7])[0]
            w = struct.unpack('>H', data[i+7:i+9])[0]
            return w, h
        i += 1
    return None, None

def get_png_size(filepath):
    """Read PNG dimensions from IHDR chunk (starts at byte 16)."""
    with open(filepath, 'rb') as f:
        f.read(8)   # PNG signature
        f.read(4)   # chunk length
        f.read(4)   # chunk type "IHDR"
        data = f.read(8)  # width (4) + height (4)
        if len(data) >= 8:
            w = struct.unpack('>I', data[0:4])[0]
            h = struct.unpack('>I', data[4:8])[0]
            return w, h
    return None, None

def get_image_size(filepath):
    if not os.path.exists(filepath):
        return None, None
    ext = os.path.splitext(filepath)[1].lower()
    if ext in ('.jpg', '.jpeg'):
        return get_jpeg_size(filepath)
    elif ext == '.png':
        return get_png_size(filepath)
    return None, None

def resolve_image_path(src, html_path):
    if src.startswith('/'):
        return os.path.join(STATIC_DIR, src.lstrip('/'))
    else:
        return os.path.join(os.path.dirname(html_path), src)

def add_dimensions_to_html(html_path):
    with open(html_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    img_pat = re.compile(r'<img\s[^>]*>', re.IGNORECASE)

    def replace_img(match):
        tag = match.group(0)
        if re.search(r'\b(width|height)\s*=', tag, re.IGNORECASE):
            return tag
        m = re.search(r'\bsrc\s*=\s*["\']?([^"\'\s>]+)["\']?', tag, re.IGNORECASE)
        if not m:
            return tag
        src = m.group(1)
        img_path = resolve_image_path(src, html_path)
        w, h = get_image_size(img_path)
        if not w or not h:
            return tag
        insert = f' width="{w}" height="{h}"'
        if tag.rstrip().endswith('/>'):
            tag = tag.rstrip()[:-2] + insert + ' />'
        elif tag.rstrip().endswith('>'):
            tag = tag.rstrip()[:-1] + insert + '>'
        return tag

    new_content = img_pat.sub(replace_img, content)
    if new_content != content:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    modified = 0
    for root, dirs, files in os.walk(PUBLIC_DIR):
        for fname in files:
            if fname.endswith('.html'):
                path = os.path.join(root, fname)
                if add_dimensions_to_html(path):
                    modified += 1
                    rel = os.path.relpath(path, PUBLIC_DIR)
                    print(f'  Augmented: {rel}')
    print(f'Modified {modified} HTML files')

if __name__ == '__main__':
    main()
