#!/usr/bin/env python3
"""Convert WordPress content to Hugo markdown files."""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from html.parser import HTMLParser
from datetime import datetime

WP_BASE = "https://www.rowanemilia.com"
STATIC_DIR = "static/images"
CONTENT_DIR = "content/posts"
PAGES_DIR = "content"
DATA_DIR = "data"

# Category name -> slug mapping from WP REST API
CATEGORIES = {
    1: "uncategorized",
    3: "medical-updates",
    4: "photos",
    5: "videos",
}

CATEGORY_NAMES = {
    1: "Uncategorized",
    3: "Medical Updates",
    4: "Photos",
    5: "Videos",
}

def fetch_json(url):
    """Fetch JSON from a URL with retries."""
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            print(f"  Retry {attempt+1} for {url}: {e}")
            time.sleep(2)
    return None

def download_file(url, dest_path):
    """Download a file if it doesn't exist."""
    if os.path.exists(dest_path):
        return True
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
        with open(dest_path, "wb") as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"  FAILED to download {url}: {e}")
        return False

def wp_url_to_local(html):
    """Replace WordPress URLs with local paths."""
    # Replace wp-content/uploads/ with /images/
    html = re.sub(
        r'https?://www\.rowanemilia\.com/wp-content/uploads/([^"\')\s]+)',
        r'/images/\1',
        html
    )
    # Replace wp-content/gallery/ with /images/gallery/
    html = re.sub(
        r'https?://www\.rowanemilia\.com/wp-content/gallery/([^"\')\s]+)',
        r'/images/gallery/\1',
        html
    )
    # Replace internal links to the site
    html = re.sub(
        r'https?://www\.rowanemilia\.com/(\d{4}/\d{2}/\d{2}/[^"\')\s]+)',
        r'/\1',
        html
    )
    html = re.sub(
        r'https?://www\.rowanemilia\.com/category/([^"\')\s]+)',
        r'/categories/\1',
        html
    )
    return html

def decode_wp_entities(text):
    """Decode WordPress HTML entities."""
    entities = {
        "&#8217;": "'",
        "&#8216;": "'",
        "&#8220;": "\"",
        "&#8221;": "\"",
        "&#8230;": "...",
        "&#8211;": "-",
        "&#8212;": "--",
        "&#038;": "&",
        "&amp;": "&",
        "&nbsp;": " ",
        "&lt;": "<",
        "&gt;": ">",
        "&#215;": "x",
        "&#8243;": '"',
        "&#8242;": "'",
    }
    for code, char in entities.items():
        text = text.replace(code, char)
    return text

def html_to_markdown(html):
    """Convert WordPress HTML to a mix of Markdown and preserved HTML."""
    html = decode_wp_entities(html)
    html = wp_url_to_local(html)
    
    # Remove Gutenberg wrapper divs but keep content
    html = re.sub(r'<div class="wp-block-embed__wrapper">\s*', '', html)
    html = re.sub(r'\s*</div>\s*', '', html)
    html = re.sub(r'<figure[^>]*>', '', html)
    html = re.sub(r'</figure>', '', html)
    
    # Convert standalone <p> tags to blank-line separated text
    # But first handle special elements inside <p> that need to stay as HTML
    
    # Handle YouTube embeds - preserve iframes
    # (they'll be kept as raw HTML)
    
    # Handle images with lightbox links
    # <a href="..." rel="lightbox[N]"><img ...></a>
    # Convert to <a href="..." class="lightbox"><img ...></a>
    html = re.sub(r'rel="lightbox\[\d+\]"', 'class="lightbox"', html)
    
    # Remove WordPress-specific attributes from img tags
    html = re.sub(r' srcset="[^"]*"', '', html)
    html = re.sub(r' sizes="[^"]*"', '', html)
    html = re.sub(r' (class|id)="[^"]*"', '', html)
    
    # Fix <p> wrapping block-level elements (browsers auto-close <p> on block elements, breaking DOM)
    html = re.sub(r'<p>\s*<(div|figure|table|ul|ol|h[1-6]|blockquote|pre|video)', r'<\1', html)
    html = re.sub(r'</(div|figure|table|ul|ol|h[1-6]|blockquote|pre|video)>\s*</p>', r'</\1>', html)
    # Strip WordPress dimension suffixes from image src (e.g., image-456x500.jpg -> image.jpg)
    html = re.sub(r'(src="[^"]+)-(\d+x\d+)(\.[a-zA-Z]+")', r'\1\3', html)
    
    # Handle WordPress captions - extract the image/link and caption text
    def caption_replacer(m):
        inner = m.group(1)
        # Extract caption text
        cap_match = re.search(r'<p[^>]*class="wp-caption-text"[^>]*>(.*?)</p>', inner, re.DOTALL)
        caption = cap_match.group(1) if cap_match else ""
        # Extract link wrapping image (if any) then the image
        link_match = re.search(r'(<a[^>]*>.*?<img[^>]*>.*?</a>|<img[^>]*>)', inner, re.DOTALL)
        img_tag = link_match.group(1) if link_match else ""
        if caption:
            return f'<div class="wp-caption aligncenter">{img_tag}<p class="wp-caption-text">{caption}</p></div>\n'
        return img_tag + "\n"
    
    html = re.sub(
        r'<div[^>]*class="wp-caption[^"]*"[^>]*>(.*?)</div>',
        caption_replacer,
        html,
        flags=re.DOTALL,
    )
    
    # Remove empty paragraph tags
    html = re.sub(r'<p>\s*&nbsp;\s*</p>', '', html)
    html = re.sub(r'<p>\s*</p>', '', html)
    
    return html.strip()

def generate_front_matter(title, date, slug, categories, authors=None, wpid=None):
    """Generate Hugo front matter."""
    fm = ["---"]
    # Escape double quotes in title for YAML
    escaped_title = title.replace('"', '\\"')
    fm.append(f'title: "{escaped_title}"')
    fm.append(f'date: {date}')
    fm.append(f'slug: "{slug}"')
    if categories:
        cats = [CATEGORIES.get(c, "uncategorized") for c in categories]
        fm.append(f'categories:')
        for c in cats:
            fm.append(f'  - {c}')
    if wpid:
        fm.append(f'wpid: {wpid}')
    if authors:
        fm.append(f'authors:')
        for a in authors:
            fm.append(f'  - "{a}"')
    fm.append("draft: false")
    fm.append("---")
    return "\n".join(fm)

def process_post(post):
    """Convert a WP post to Hugo markdown."""
    post_id = post["id"]
    title = decode_wp_entities(post["title"]["rendered"]).strip()
    if not title:
        # Use date-based title for untitled posts
        date_str = post["date"][:10]
        title = f"Post from {date_str}"
    
    date_str = post["date"]
    slug = post["slug"]
    if not slug or slug == post_id:
        slug = f"post-{post_id}"
    
    categories = post.get("categories", [])
    
    # Get author info if available
    authors = []
    if "_embedded" in post and "author" in post["_embedded"]:
        for author in post["_embedded"]["author"]:
            authors.append(author.get("name", ""))
    
    # Convert content
    content_html = post["content"]["rendered"]
    content = html_to_markdown(content_html)
    
    # Generate front matter
    fm = generate_front_matter(title, date_str, slug, categories, authors if authors else None, wpid=post_id)
    
    # Parse date for directory structure
    dt = datetime.fromisoformat(date_str)
    year = dt.strftime("%Y")
    month = dt.strftime("%m")
    day = dt.strftime("%d")
    
    # Create post directory
    post_dir = os.path.join(CONTENT_DIR, year, month)
    os.makedirs(post_dir, exist_ok=True)
    
    # Write file
    filename = f"{dt.strftime('%Y-%m-%d')}-{slug}.md"
    filepath = os.path.join(post_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(fm + "\n\n" + content + "\n")
    
    return filepath

def process_page(page):
    """Convert a WP page to Hugo markdown."""
    title = decode_wp_entities(page["title"]["rendered"])
    slug = page["slug"]
    
    content_html = page["content"]["rendered"]
    content = html_to_markdown(content_html)
    
    fm_parts = ["---"]
    fm_parts.append(f'title: "{title}"')
    fm_parts.append(f'slug: "{slug}"')
    fm_parts.append("draft: false")
    fm_parts.append("---")
    fm = "\n".join(fm_parts)
    
    content = html_to_markdown(content_html)
    
    filepath = os.path.join(PAGES_DIR, f"{slug}.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(fm + "\n\n" + content + "\n")
    
    return filepath

def main():
    os.makedirs(STATIC_DIR, exist_ok=True)
    os.makedirs(CONTENT_DIR, exist_ok=True)
    os.makedirs(PAGES_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(os.path.join(STATIC_DIR, "gallery", "rowan", "thumbs"), exist_ok=True)
    
    # Step 1: Download all media files
    print("=== Fetching media library ===")
    all_media = []
    page = 1
    while True:
        url = f"{WP_BASE}/wp-json/wp/v2/media?per_page=100&page={page}"
        data = fetch_json(url)
        if not data or len(data) == 0:
            break
        all_media.extend(data)
        print(f"  Fetched page {page} ({len(data)} items)")
        page += 1
        if len(data) < 100:
            break
    
    print(f"Total media items: {len(all_media)}")
    
    # Process media by year/month
    media_by_path = {}
    for m in all_media:
        source_url = m.get("guid", {}).get("rendered", "")
        if not source_url:
            continue
        # Normalize to https
        source_url = source_url.replace("http://", "https://")
        mime = m.get("mime_type", "")
        
        # Determine local path
        # wp-content/uploads/YYYY/MM/filename -> static/images/YYYY/MM/filename
        match = re.search(r'wp-content/uploads/(\d{4}/\d{2}/.+)', source_url)
        if match:
            local_rel = match.group(1)
            local_path = os.path.join(STATIC_DIR, local_rel)
            media_by_path[local_rel] = (source_url, local_path)
    
    print(f"Downloading {len(media_by_path)} media files...")
    for local_rel, (src_url, local_path) in media_by_path.items():
        if download_file(src_url, local_path):
            pass  # Success
        else:
            print(f"  Failed: {src_url}")
    
    # Step 2: Download NextGen Gallery images  
    print("\n=== Downloading NextGen Gallery images ===")
    gallery_base = f"{WP_BASE}/wp-content/gallery/rowan"
    gallery_files = [
        "securedownload.jpg", "2010.jpg", "img_0050.jpg", "img_1937.jpg",
        "img_1865.jpg", "img_1717.jpg", "img_1643.jpg", "jeans1.jpg",
        "monkey1.jpg", "michael-family-1.jpg", "20091008-img_1493.jpg",
        "judy-rowan-1.jpg", "michaels-2.jpg", "rowan-nana-2.jpg",
        "20090912-img_1461.jpg", "20090726-img_1223.jpg", "feet.jpg",
        "lounging2.jpg", "lounging.jpg", "chubbybaby.jpg",
    ]
    for fname in gallery_files:
        # Download full size
        src = f"{gallery_base}/{fname}"
        dst = os.path.join(STATIC_DIR, "gallery", "rowan", fname)
        download_file(src, dst)
        # Download thumb
        thumb_src = f"{gallery_base}/thumbs/thumbs_{fname}"
        thumb_dst = os.path.join(STATIC_DIR, "gallery", "rowan", "thumbs", f"thumbs_{fname}")
        download_file(thumb_src, thumb_dst)
    
    # Step 3: Download self-hosted video
    print("\n=== Downloading self-hosted video ===")
    video_url = f"{WP_BASE}/wp-content/uploads/2013/07/20130721-212122.mov"
    video_dst = os.path.join(STATIC_DIR, "2013/07/20130721-212122.mov")
    download_file(video_url, video_dst)
    
    # Step 4: Fetch and convert all posts
    print("\n=== Fetching all posts ===")
    all_posts = []
    page = 1
    while True:
        url = f"{WP_BASE}/wp-json/wp/v2/posts?per_page=100&page={page}&_embed=author"
        data = fetch_json(url)
        if not data or len(data) == 0:
            break
        all_posts.extend(data)
        print(f"  Fetched page {page} ({len(data)} posts)")
        page += 1
        if len(data) < 100:
            break
    
    print(f"Total posts: {len(all_posts)}")
    
    print("\n=== Converting posts to Hugo markdown ===")
    for post in all_posts:
        filepath = process_post(post)
        title = decode_wp_entities(post["title"]["rendered"]).strip() or "(no title)"
        print(f"  {filepath} - {title}")
    
    # Step 5: Fetch and convert all pages
    print("\n=== Fetching all pages ===")
    pages = fetch_json(f"{WP_BASE}/wp-json/wp/v2/pages?per_page=10")
    if pages:
        print(f"Total pages: {len(pages)}")
        print("\n=== Converting pages to Hugo markdown ===")
        for page in pages:
            filepath = process_page(page)
            title = decode_wp_entities(page["title"]["rendered"])
            print(f"  {filepath} - {title}")
    
    # Step 6: Fetch comments
    print("\n=== Fetching comments ===")
    all_comments = []
    page = 1
    while True:
        url = f"{WP_BASE}/wp-json/wp/v2/comments?per_page=100&page={page}"
        data = fetch_json(url)
        if not data or len(data) == 0:
            break
        all_comments.extend(data)
        print(f"  Fetched page {page} ({len(data)} comments)")
        page += 1
        if len(data) < 100:
            break
    
    print(f"Total comments: {len(all_comments)}")
    
    # Organize comments by post
    comments_by_post = {}
    for c in all_comments:
        post_id = c.get("post")
        if post_id not in comments_by_post:
            comments_by_post[post_id] = []
        comments_by_post[post_id].append({
            "id": c["id"],
            "author": c.get("author_name", "Anonymous"),
            "date": c.get("date", ""),
            "content": decode_wp_entities(c.get("content", {}).get("rendered", "")),
            "parent": c.get("parent", 0),
        })
    
    # Save comments as JSON
    comments_path = os.path.join(DATA_DIR, "comments.json")
    with open(comments_path, "w", encoding="utf-8") as f:
        json.dump(comments_by_post, f, indent=2)
    print(f"  Saved comments to {comments_path}")
    
    print("\n=== Done! ===")

if __name__ == "__main__":
    main()
