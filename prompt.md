# Prompt for LLM Coding Agent: WordPress → Hugo Migration

You are tasked with migrating the website **https://www.rowanemilia.com/** from WordPress to a self-hosted Hugo static site. Read `spec.md` for the complete specification. Below is your step-by-step execution plan.

## Prerequisites

You'll need:
- `hugo` installed (extended version)
- `wget` or `curl` for downloading assets
- `python3` for content processing
- `git` for version control

## Step 1: Download All Assets

Run a script that downloads every file that needs to be served locally:

### 1a. Theme images (9 files)
```
wp-content/themes/rowan-wp/img/header.gif
wp-content/themes/rowan-wp/img/contentback.gif
wp-content/themes/rowan-wp/img/topcorner.gif
wp-content/themes/rowan-wp/img/bottomcorner.gif
wp-content/themes/rowan-wp/img/footer.gif
wp-content/themes/rowan-wp/img/ul.gif
wp-content/themes/rowan-wp/img/input.gif
wp-content/themes/rowan-wp/img/textarea.gif
wp-content/themes/rowan-wp/img/submit.gif
```

### 1b. All uploaded media (~132 files)
Download every file listed in the WordPress media library at `https://www.rowanemilia.com/wp-json/wp/v2/media?per_page=200`. Save them with their original filenames organized by year/month.

### 1c. NextGen Gallery images (~20 files)
Download from `https://www.rowanemilia.com/wp-content/gallery/rowan/` (both full-size and thumbs).

### 1d. Self-hosted video
Download `https://www.rowanemilia.com/wp-content/uploads/2013/07/20130721-212122.mov`

**Important:** Do NOT download any YouTube videos. YouTube embeds (iframes pointing to youtube.com) must be preserved as-is in the converted content. They are the only allowed external dependency.

## Step 2: Initialize Hugo Site

```bash
hugo new site rowanemilia.com --force
cd rowanemilia.com
```

## Step 3: Create Custom Theme "rowan-wp"

Create `themes/rowan-wp/` with:

- `theme.yaml` — theme metadata
- `static/css/style.css` — exact reproduction of the original theme CSS (paths adjusted for Hugo)
- `static/img/` — all downloaded theme images
- `layouts/_default/baseof.html` — base template with header, content, sidebar, footer
- `layouts/_default/index.html` — paginated post list
- `layouts/_default/single.html` — single post/page
- `layouts/_default/list.html` — category/archive listing
- `layouts/partials/header.html`
- `layouts/partials/sidebar.html`
- `layouts/partials/footer.html`
- `layouts/partials/post-summary.html`

### Sidebar Implementation

The sidebar must include all widgets from the original site:
1. **Menu** — Links: Home, About Rowan, Photo Gallery, Random Videos (with current page highlighted)
2. **Categories** — List of 4 categories with post counts
3. **Stuff** — Log in (remove or point to local), Entries feed, Comments feed
4. **Archives** — Monthly dropdown/list from Oct 2008 to Aug 2021

### Header Implementation

- Background image: header.gif (no-repeat 160px offset)
- Site title: "RowanEmilia.com" linked to homepage
- Tagline: "A chronicle of Rowan"
- Colors and positioning per spec.md

### Footer Implementation

- Background image: footer.gif
- Left: "Copyrights © RowanEmilia.com"
- Right: "Powered by Hugo, Designed by page" (modified from WordPress credit)

## Step 4: Configure Hugo

Create `hugo.yaml`:

```yaml
baseURL: "http://localhost:1313/"
languageCode: "en-US"
title: "RowanEmilia.com"
theme: "rowan-wp"
paginate: 5

params:
  description: "A chronicle of Rowan"
  copyright: "Copyrights © RowanEmilia.com"

taxonomies:
  category: categories

permalinks:
  posts: "/:year/:month/:day/:slug/"
```

## Step 5: Convert WordPress Content to Hugo

For each of the 93 posts and 3 pages:

1. Create a Markdown file with front matter (title, date, slug, categories)
2. Convert the HTML content to Markdown using these rules:
   - `<p>` → paragraph breaks
   - `<img>` → Markdown `![alt](local-path)` 
   - `<a rel="lightbox">` → linked image (lightbox-compatible)
   - Youtube embeds → preserve as raw HTML iframes
   - `<video>` → preserve as raw HTML `<video>`
   - WordPress captions → preserve as HTML or shortcode
   - Decode HTML entities: `&#8217;` → `'`, `&#8220;` → `"`, etc.
   - Strip WordPress block wrapper divs
3. Download every image referenced in the post and store locally
4. Update all image `src` attributes to point to local files

### Download Each Post's Content

Use the WordPress REST API to get the raw HTML content of each post:
```
https://www.rowanemilia.com/wp-json/wp/v2/posts/784
```

Then convert the `content.rendered` field to Markdown.

## Step 6: Handle Comments

Download all 154 comments from the REST API:
```
https://www.rowanemilia.com/wp-json/wp/v2/comments?per_page=200
```

Store comments as data files (JSON or YAML in `data/comments/`) keyed by post ID.
Create a partial template that renders comments below each post, matching the original comment styling (`.comment-body`, `.comment-author`, `.comment-meta`, threaded/children indentation).

## Step 7: Add Lightbox

Implement a lightweight JavaScript lightbox for image viewing:
- Vanilla JS (no external dependencies)
- Clicking an image opens it in a centered overlay
- Close button or click-outside to close
- Keyboard navigation (Escape to close)
- Style matches the original White theme from the Lightbox 2 plugin

## Step 8: Create Special Pages

### About Page (`content/about.md`)
- Biography text about Rowan
- Birthday collage image (download from `wp-content/uploads/2008/11/rowans-birthday-collage.jpg`)

### Photo Gallery (`content/s.md`)
- Custom layout to display the NextGen Gallery images in a grid
- Thumbnails that open full-size in lightbox

### Random Videos (`content/videos.md`)
- All 6 embedded YouTube videos from the original page

## Step 9: Implement Monthly Archives

Create archive pages that list posts by month. The sidebar should link to each month that has posts (Oct 2008 through Aug 2021, ~47 months with content).

## Step 10: Testing & Verification

After implementation, run these checks:

```bash
# Build the site
cd rowanemilia.com && hugo

# Start the dev server
hugo server -D

# Verify visually:
# 1. http://localhost:1313/ — home page with posts
# 2. http://localhost:1313/about/ — about page
# 3. http://localhost:1313/s/ — photo gallery
# 4. http://localhost:1313/videos/ — random videos
# 5. http://localhost:1313/categories/photos/ — category page
# 6. Check pagination works at /page/2/
# 7. Click images — lightbox should open
# 8. Check sidebar links work
# 9. Check there are NO requests to rowanemilia.com or wordpress.org in browser dev tools
```

## Key Requirements

1. **Pixel-perfect visual match** — The Hugo site must look identical to the WordPress original
2. **No external dependencies** — All images, CSS, theme assets served locally
3. **YouTube embeds** — These are the ONLY external requests allowed (cannot self-host YouTube)
4. **All content preserved** — Every post, page, comment, image, and video
5. **Working archives** — Monthly archive links must filter correctly
6. **Working categories** — Category sidebar links must filter correctly
7. **Paginated home page** — 5 posts per page with older/newer navigation
8. **Lightbox** — Images open in overlay when clicked
9. **.mov video** — Self-hosted video must play inline

## Output Structure

```
rowanemilia.com/
├── hugo.yaml
├── content/
│   ├── posts/
│   │   ├── 2008/
│   │   ├── 2009/
│   │   └── ... (year directories)
│   ├── about.md
│   ├── s.md
│   └── videos.md
├── data/
│   └── comments.json
├── static/
│   ├── css/
│   │   └── style.css
│   ├── img/
│   │   └── (theme images)
│   └── images/
│       └── (uploaded media by year/month)
└── themes/
    └── rowan-wp/
        ├── theme.yaml
        ├── layouts/
        │   ├── _default/
        │   │   ├── baseof.html
        │   │   ├── index.html
        │   │   ├── single.html
        │   │   └── list.html
        │   └── partials/
        │       ├── header.html
        │       ├── sidebar.html
        │       ├── footer.html
        │       └── post-summary.html
        └── static/
            ├── css/
            │   └── style.css
            └── img/
                └── (theme images)
```
