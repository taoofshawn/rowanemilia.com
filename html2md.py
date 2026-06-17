#!/usr/bin/env python3
"""
Convert HTML content in Hugo markdown files to proper Markdown.
Preserves front matter and raw HTML that should stay as HTML (iframes, video).
Captions in divs are extracted to Markdown-friendly format.
"""

import os
import re

# Tags to ALWAYS preserve as raw HTML (blank-line separated)
RAW_HTML_TAGS = {'iframe', 'video', 'source'}

def preserve_raw_html(html, placeholders):
    """Replace elements that must stay as raw HTML with placeholders."""
    def save_tag(m):
        idx = len(placeholders)
        placeholder = f'%%RAW_{idx}%%'
        placeholders[placeholder] = m.group(0).strip()
        return '\n\n' + placeholder + '\n\n'
    # Save iframes
    html = re.sub(r'<iframe[^>]*>.*?</iframe>', save_tag, html, flags=re.DOTALL)
    # Save video tags
    html = re.sub(r'<video[^>]*>.*?</video>', save_tag, html, flags=re.DOTALL)
    return html

def restore_raw_html(text, placeholders):
    """Restore placeholders."""
    for placeholder, original in sorted(placeholders.items(), key=lambda x: -len(x[0])):
        text = text.replace(placeholder, original)
    return text

def extract_captions(html):
    """Extract WordPress caption divs, convert to Markdown-friendly format."""
    def caption_handler(m):
        inner = m.group(0)
        # Get caption text
        cap = re.search(r'<p[^>]*class="wp-caption-text"[^>]*>(.*?)</p>', inner, re.DOTALL)
        caption = cap.group(1).strip() if cap else ''
        # Get content inside the caption div (image/link)
        # Remove the caption <p> from inner
        no_cap = re.sub(r'<p[^>]*class="wp-caption-text"[^>]*>.*?</p>', '', inner, flags=re.DOTALL)
        # Also remove style/width div wrappers
        no_cap = re.sub(r'<div[^>]*>', '', no_cap)
        no_cap = re.sub(r'</div>', '', no_cap)
        no_cap = no_cap.strip()
        
        if caption:
            return f'{no_cap}\n\n*{caption}*\n\n'
        return no_cap + '\n\n'
    
    # Match caption divs (with class wp-caption)
    html = re.sub(
        r'<div[^>]*class="[^"]*wp-caption[^"]*"[^>]*>.*?</div>',
        caption_handler, html, flags=re.DOTALL
    )
    return html

def extract_other_divs(html):
    """Remove remaining non-caption div wrappers but keep inner content."""
    # Remove opening div tags (with or without attributes)
    html = re.sub(r'<div[^>]*>', '', html)
    html = re.sub(r'</div>', '', html)
    return html

def html_to_markdown(html):
    """Convert HTML content to Markdown, preserving iframes/video as raw HTML."""
    placeholders = {}
    
    # Pre-processing: remove Gutenberg wrappers
    html = re.sub(r'<figure[^>]*>', '', html)
    html = re.sub(r'</figure>', '', html)
    html = re.sub(r'<div class="wp-block-embed__wrapper">\s*', '', html)
    
    # Strip WordPress dimension suffixes from image src
    html = re.sub(r'(src="[^"]+)-(\d+x\d+)(\.[a-zA-Z]+")', r'\1\3', html)
    # Remove srcset and sizes
    html = re.sub(r' srcset="[^"]*"', '', html)
    html = re.sub(r' sizes="[^"]*"', '', html)
    # Remove specific WordPress attributes
    html = re.sub(r' (class|id)="[^"]*"', '', html)
    html = re.sub(r' aria-describedby="[^"]*"', '', html)
    html = re.sub(r' loading="lazy"', '', html)
    html = re.sub(r' decoding="async"', '', html)
    
    # Convert lightbox rel attributes to class
    html = re.sub(r'rel="lightbox\[\d+\]"', 'class="lightbox"', html)
    
    # Fix <p> wrapping block elements before any conversion
    html = re.sub(r'<p>\s*<(div|figure|table|ul|ol|h[1-6]|blockquote|pre|video|iframe)', r'<\1', html)
    html = re.sub(r'</(div|figure|table|ul|ol|h[1-6]|blockquote|pre|video)>\s*</p>', r'</\1>', html)
    
    # Extract captions to Markdown format
    html = extract_captions(html)
    
    # Remove remaining div wrappers
    html = extract_other_divs(html)
    
    # Now preserve elements that MUST stay as raw HTML
    html = preserve_raw_html(html, placeholders)
    
    # Convert bold/italic
    html = re.sub(r'<strong>(.*?)</strong>', r'**\1**', html, flags=re.DOTALL)
    html = re.sub(r'<b>(.*?)</b>', r'**\1**', html, flags=re.DOTALL)
    html = re.sub(r'<em>(.*?)</em>', r'*\1*', html, flags=re.DOTALL)
    html = re.sub(r'<i>(.*?)</i>', r'*\1*', html, flags=re.DOTALL)
    
    # Convert headings
    html = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1', html, flags=re.DOTALL)
    html = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', html, flags=re.DOTALL)
    html = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1', html, flags=re.DOTALL)
    html = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1', html, flags=re.DOTALL)
    
    # Convert images FIRST (before links)
    def img_to_md(m):
        src = ''
        alt = ''
        s = re.search(r'src="([^"]+)"', m.group(0))
        if s: src = s.group(1)
        a = re.search(r'alt="([^"]*)"', m.group(0))
        if a: alt = a.group(1)
        return f'![{alt}]({src})'
    html = re.sub(r'<img[^>]*>', img_to_md, html)
    
    # Convert links (but not lightbox ones - they were already converted above)
    # Actually lightbox links are just <a class="lightbox" href="..."><img...></a> which
    # by now have the img converted to Markdown. So handle links.
    def link_to_md(m):
        href = ''
        h = re.search(r'href="([^"]+)"', m.group(0))
        if h: href = h.group(1)
        text = m.group(1)
        return f'[{text}]({href})'
    html = re.sub(r'<a[^>]*>(.*?)</a>', link_to_md, html, flags=re.DOTALL)
    
    # Convert lists
    def ul_to_md(m):
        items = re.findall(r'<li>(.*?)</li>', m.group(1), flags=re.DOTALL)
        return '\n' + '\n'.join(f'- {i.strip()}' for i in items) + '\n'
    def ol_to_md(m):
        items = re.findall(r'<li>(.*?)</li>', m.group(1), flags=re.DOTALL)
        return '\n' + '\n'.join(f'{n}. {i.strip()}' for n, i in enumerate(items, 1)) + '\n'
    html = re.sub(r'<ul>(.*?)</ul>', ul_to_md, html, flags=re.DOTALL)
    html = re.sub(r'<ol>(.*?)</ol>', ol_to_md, html, flags=re.DOTALL)
    
    # Convert blockquotes
    def bq_to_md(m):
        inner = m.group(1).strip()
        return '\n> ' + inner.replace('\n', '\n> ') + '\n\n'
    html = re.sub(r'<blockquote>(.*?)</blockquote>', bq_to_md, html, flags=re.DOTALL)
    
    # Convert <br> to newlines
    html = re.sub(r'<br\s*/?>', '\n', html)
    
    # Convert paragraphs - <p> -> blank line separation
    html = re.sub(r'<p>(.*?)</p>', r'\1', html, flags=re.DOTALL)
    
    # Clean up remaining HTML tags
    html = re.sub(r'</?p[^>]*>', '', html)
    html = re.sub(r'</?span[^>]*>', '', html)
    html = re.sub(r'</?a[^>]*>', '', html)  # any remaining broken links
    html = re.sub(r' mce_[a-z_]+="[^"]*"', '', html)
    
    # Collapse multiple blank lines
    html = re.sub(r'\n{4,}', '\n\n\n', html)
    
    # Restore preserved HTML
    html = restore_raw_html(html, placeholders)
    
    return html.strip()

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if not content.startswith('---'):
        return
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return
    
    front_matter = parts[1]
    body = parts[2]
    
    converted = html_to_markdown(body)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f'---{front_matter}---\n\n{converted}\n')
    
    print(f'  Converted: {os.path.basename(filepath)}')

def main():
    posts_dir = 'content/posts'
    for root, dirs, files in os.walk(posts_dir):
        for file in files:
            if file.endswith('.md'):
                process_file(os.path.join(root, file))
    
    for page in ['content/about.md', 'content/videos.md']:
        if os.path.exists(page):
            process_file(page)
    
    print('Done!')

if __name__ == '__main__':
    main()
