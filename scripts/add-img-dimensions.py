#!/usr/bin/env python3
"""
Add width/height attributes and descriptive alt text to <img> tags in Hugo-minified HTML.
Prevents CLS (width/height) and fixes link-name accessibility (alt text).
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
    with open(filepath, 'rb') as f:
        f.read(8); f.read(4); f.read(4)
        data = f.read(8)
        if len(data) >= 8:
            return struct.unpack('>I', data[0:4])[0], struct.unpack('>I', data[4:8])[0]
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
    return os.path.join(os.path.dirname(html_path), src)


def alt_from_filename(src):
    base = os.path.splitext(os.path.basename(src))[0]
    base = re.sub(r'^\d{6,8}[-_]?', '', base)
    base = re.sub(r'^(DSC|IMG|P)\d+[-_]?', '', base, flags=re.I)
    base = re.sub(r'[-_]+', ' ', base)
    base = base.strip()
    return base[:80] if base else 'Photo'

def process_html(html_path):
    with open(html_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    img_pat = re.compile(r'<img\s[^>]*>', re.IGNORECASE)
    dirty = False

    def replace_img(match):
        nonlocal dirty
        tag = match.group(0)

        # Extract src
        m = re.search(r'\bsrc\s*=\s*["\']?([^"\'\s>]+)["\']?', tag, re.IGNORECASE)
        if not m:
            return tag
        src = m.group(1)

        # Remove bare 'alt' (boolean attribute - Hugo minifies alt="" to alt)
        tag = re.sub(r'\balt(?!\s*=)', '', tag).strip()
        
        # Fix empty or missing alt=
        alt_m = re.search(r'\balt\s*=\s*["\']?([^"\'\s>]*)', tag, re.IGNORECASE)
        if alt_m and alt_m.group(1):
            pass  # already has a non-empty alt value, keep it
        else:
            # Remove any existing empty alt= attribute
            tag = re.sub(r'\balt\s*=\s*["\']?[^"\'\s>]*', '', tag)
            gen_alt = alt_from_filename(src)
            insert = f' alt="{gen_alt}"'
            tag = tag.rstrip()
            if tag.endswith('/>'):
                tag = tag[:-2] + insert + ' />'
            elif tag.endswith('>'):
                tag = tag[:-1] + insert + '>'
            dirty = True

        # Fix missing width/height
        if not re.search(r'\b(width|height)\s*=', tag, re.IGNORECASE):
            w, h = get_image_size(resolve_image_path(src, html_path))
            if w and h:
                dims = f' width="{w}" height="{h}"'
                tag = tag.rstrip()
                if tag.endswith('/>'):
                    tag = tag[:-2] + dims + ' />'
                elif tag.endswith('>'):
                    tag = tag[:-1] + dims + '>'
                dirty = True
        return tag

    new_content = img_pat.sub(replace_img, content)
    if dirty:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    modified = 0
    for root, dirs, files in os.walk(PUBLIC_DIR):
        for fname in files:
            if fname.endswith('.html'):
                if process_html(os.path.join(root, fname)):
                    modified += 1
                    print(f'  Processed: {os.path.relpath(os.path.join(root, fname), PUBLIC_DIR)}')
    print(f'Modified {modified} HTML files')

if __name__ == '__main__':
    main()
