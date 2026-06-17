# Website Migration Specification: rowanemilia.com → Self-Hosted Hugo Blog

## 1. Overview

**Source:** https://www.rowanemilia.com/ — a WordPress blog (WP 6.4.1) using the "rowan-wp" theme
**Target:** Local, self-hosted Hugo static site generator blog
**Goal:** Pixel-perfect recreation of the existing site with all content served locally. No external dependencies (except YouTube embeds which remain as embedded iframes).

---

## 2. Site Structure & Content Inventory

### 2.1 Pages (3 total)

| Page | Slug | WordPress URL | Description |
|------|------|---------------|-------------|
| Home | `/` | `/` | Blog post index (paginated) |
| About Rowan | `/about` | `/about` | Biography with a photo collage |
| Photo Gallery | `/s` | `/s` | NextGen Gallery plugin gallery |
| Random Videos | `/videos` | `/videos` | Embedded YouTube video collection |

### 2.2 Posts (93 total, spanning Oct 2008 – Aug 2021)

Posts are organized across 4 categories:

| Category | Post Count | Description |
|----------|-----------|-------------|
| Medical Updates | 20 | Health/cardiology updates |
| Photos | 53 | Photo-centric posts |
| Uncategorized | 9 | General posts |
| Videos | 14 | Embedded YouTube video posts |

Complete post list is in Appendix A.

### 2.3 Comments (154 total)

Comments are present on multiple posts. They should be preserved and displayed inline below each post.

### 2.4 Archives Index

Available monthly archives from October 2008 through August 2021. Each monthly archive page lists posts from that month.

---

## 3. Theme Design Specification

**Theme:** "rowan-wp" v2.3.1 by "page" (http://pageblogging.net)

### 3.1 Layout

- **Width:** 800px centered layout
- **Structure:** Two-column with main content area (640px, right) and sidebar (140px, left)
- **Layout direction:** Sidebar on the left, main content on the right

### 3.2 Color Palette

| Element | Color | Hex |
|---------|-------|-----|
| Page background | Cream/tan | `#F1F0DE` |
| Content background | Olive green | `#D9D8A8` |
| Text | Dark gray | `#333333` |
| Links | Blue | `#147` / `#06c` (hover) |
| Post title links | Olive-brown | `#58573F` |
| Sidebar headings | Orange | `#A4573A` |
| Sidebar links | Olive-gray | `#767555` |
| Footer text | Light gray | `#CCCCCC` |
| Header text | Light cream | `#F1E7DB` |
| Blockquote background | Darker olive | `#CBCAA1` |
| Post metadata border | Light olive | `#DCDBBF` |
| Ping/page link bg | Medium olive | `#BFBE8F` |

### 3.3 Typography

- **Font stack:** `'Lucida Grande', Verdana, Arial, Sans-Serif`
- **Base size:** 62.5% (1em = 10px reset)
- **Body text:** 1.2em (~12px)
- **Post titles (h2):** 1.5em
- **Sidebar headings (h2):** 1.1em, uppercase
- **Line height:** 1.8em in main content

### 3.4 Header

- **Height:** 100px
- **Background:** Uses `img/header.gif` as a background image (repeated no-repeat at 160px offset)
- **Title:** 2em, positioned at left: 340px, top: 15px, color `#eee`
- **Tagline (`.description`):** positioned at left: 360px
- **Header text color:** `#F1E7DB`

### 3.5 Navigation / Sidebar

- **Width:** 140px, float: left, text-align: right
- **Menu items:** Home, About Rowan, Photo Gallery, Random Videos
- **Widget sections:**
  - **Menu** — custom nav links
  - **Categories** — Medical Updates, Photos, Uncategorized, Videos
  - **Stuff** — Log in, Entries feed, Comments feed, WordPress.org
  - **Archives** — Monthly archive links (Oct 2008 – Aug 2021)

### 3.6 Footer

- **Background:** Uses `img/footer.gif` (no-repeat 160px)
- **Width:** 600px + padding
- **Height:** 30px
- **Text:** "Copyrights © RowanEmilia.com" (left), "Powered by WordPress, Designed by page" (right)
- **Text color:** `#CCC`
- **Links:** underline style

### 3.7 Content Area

- **Top corner:** Rounded top via `img/topcorner.gif`
- **Bottom corner:** Rounded bottom via `img/bottomcorner.gif`
- **Content padding:** 0 20px
- **Entry images:** max-width 590px, auto height, 3px margin
- **Image captions:** Standard WordPress caption style (border, centered, gray background)
- **Blockquotes:** 20px margin, 5px padding, `#CBCAA1` background

### 3.8 Image Lightbox

The site uses a Lightbox plugin for image viewing. Images open in a lightbox overlay when clicked. This behavior should be replicated in Hugo (e.g., using a lightweight JavaScript lightbox library or Hugo's built-in image render hooks).

### 3.9 Theme Background Images (all must be downloaded)

| Image | Path in Theme |
|-------|---------------|
| header.gif | `wp-content/themes/rowan-wp/img/header.gif` |
| contentback.gif | `wp-content/themes/rowan-wp/img/contentback.gif` |
| topcorner.gif | `wp-content/themes/rowan-wp/img/topcorner.gif` |
| bottomcorner.gif | `wp-content/themes/rowan-wp/img/bottomcorner.gif` |
| footer.gif | `wp-content/themes/rowan-wp/img/footer.gif` |
| ul.gif | `wp-content/themes/rowan-wp/img/ul.gif` |
| input.gif | `wp-content/themes/rowan-wp/img/input.gif` |
| textarea.gif | `wp-content/themes/rowan-wp/img/textarea.gif` |
| submit.gif | `wp-content/themes/rowan-wp/img/submit.gif` |

---

## 4. Media Inventory

### 4.1 WordPress Uploads (~132 files)

All files under `wp-content/uploads/` organized by year/month directories:
- 2008/11, 2008/12 — 6 files (collage, homecoming, christmas, awww, yawn)
- 2009/02, 2009/04, 2009/05, 2009/06, 2009/07, 2009/10, 2009/11 — ~30 files
- 2010/02, 2010/03, 2010/05, 2010/06, 2010/07, 2010/09, 2010/10, 2010/11, 2010/12 — ~30 files
- 2011/01, 2011/02, 2011/03, 2011/06, 2011/07 — ~18 files
- 2012/02, 2012/04, 2012/12 — ~8 files
- 2013/01, 2013/03, 2013/04, 2013/05, 2013/07 — ~10 files (including one .mov video)
- 2014/04, 2014/07 — 4 files
- 2017/07 — 4 files

### 4.2 NextGen Gallery Images

Located at `wp-content/gallery/rowan/` — ~20 photos with thumbs.

### 4.3 Embedded YouTube Videos

Multiple posts contain YouTube embeds. These remain as embedded iframes (cannot be self-hosted). The video content is irreplaceable — preserve the embed codes exactly.

| Post/Page | YouTube Video IDs |
|-----------|------------------|
| Some Dolls (2021) | `-9icrM6rLKQ` |
| Rowan's Ballet Recital (2020) | `ksDBSa17cA4` |
| Random Videos page | `LulNeXes18Y`, `gBKGMtOS39o`, `MwpEyq_ac0U`, `-kfBBPDtC4o`, `uCC3byiBqEk`, `cDaUpAtmS-w` |
| Various posts | Various IDs |

### 4.3 Note on YouTube Content

**Do NOT download YouTube videos.** Posts that embed YouTube content (e.g., `iframe` embeds from `youtube.com`) must preserve the original embed code. YouTube videos remain as embedded iframes pointing to youtube.com — they are the only allowed external dependency.

### 4.5 Self-Hosted Video

One .mov video file (the "Uh Oh!" post from 2013-07): `wp-content/uploads/2013/07/20130721-212122.mov` — must be downloaded and served locally.

---

## 5. Hugo Implementation Requirements

### 5.1 Theme

- Create a custom Hugo theme that replicates the "rowan-wp" design exactly
- All theme assets (CSS, images) must be bundled in the theme directory
- The theme CSS must reproduce the original style.css faithfully
- Theme background images must be stored as static files

### 5.2 Content Model

**Posts:**
- Each WordPress post → Hugo content file in `content/posts/YYYY/MM/`
- Front matter includes: title, date, slug, categories, draft: false
- Post content converted from HTML to Markdown where possible, raw HTML preserved where needed (e.g., YouTube embeds, image lightbox links)
- Post authors are noted per-post (Rowan, Uncle Shawn, mom) — optionally record in front matter

**Pages:**
- About Rowan → `content/about.md`
- Photo Gallery → `content/s.md` (custom layout needed for gallery grid)
- Random Videos → `content/videos.md`

**Comments:**
- Stored as data files (e.g., `data/comments/`) or embedded in post front matter
- Displayed below each post in the comment style of the original theme

**Categories:**
- Hugo taxonomies for categories
- Category listing pages at `/categories/medical-updates/`, etc.
- Category counts should be displayed in the sidebar

**Archives:**
- Monthly archive pages at `/archives/YYYY/MM/`
- Archive links in sidebar

### 5.3 Layout Templates

| Template | Purpose |
|----------|---------|
| `baseof.html` | Base layout with header, content area, sidebar, footer |
| `index.html` | Home page — paginated blog post list |
| `single.html` | Single post/page view |
| `list.html` | Category archive, monthly archive |
| `_default/section.html` | Section list pages |
| `partials/header.html` | Site header |
| `partials/sidebar.html` | Left sidebar with menu, categories, archives, meta links |
| `partials/footer.html` | Site footer |
| `partials/post-summary.html` | Post summary for index page |

### 5.4 Features to Implement

1. **Pagination** — Main page paginated (like the original WP pagination)
2. **Post metadata** — Date, author, categories, comment count shown below post titles
3. **Lightbox** — Clickable images that open in a lightbox overlay (vanilla JS or lightweight library)
4. **Image captions** — WordPress-style `.wp-caption` styling
5. **Responsive images** — Images should respect max-width (original was 590px max in content, 500px in posts)
6. **Comment display** — Threaded comment styling matching the original
7. **Category pages** — Filter posts by category
8. **Monthly archives** — Filter posts by month
9. **Feed** — RSS feed for posts (/feed equivalent)
10. **SEO** — Basic meta tags, noindex/nofollow can be removed (self-hosted)
11. **"Older Entries" / "Newer Entries"** — Pagination navigation at bottom of index

### 5.5 Non-Goals (things to exclude from WordPress)

- No WordPress admin panel or login
- No WordPress comments system (comments are static content)
- No `xmlrpc.php`, `wp-json/`, `wp-login.php` endpoints
- No emoji polyfill scripts
- No WordPress block library CSS (rely on converted Markdown/HTML)
- No "WordPress.org" link in sidebar meta section (replace with appropriate self-hosted links or omit)

---

## 5.5 Monthly Archives

Per-month archive pages are generated by `gen_archives.py`, a Python script that:

1. Scans `content/posts/` for all year/month directories
2. Generates `content/archives/YYYY/_index.md` and `content/archives/YYYY/MM/_index.md` files
3. Each month page shows full post content inline
4. Each year page lists all posts from that year

The script is run before `hugo` during builds (both local and Docker). No manual intervention is needed when adding new posts — the script detects new months automatically.

Archive URL structure:
- `/archives/` — Top-level list of all 45 months
- `/archives/2021/` — All posts from 2021
- `/archives/2021/08/` — All posts from August 2021 (with full content)

---

## 6. Content Conversion Notes

### 6.1 HTML to Markdown Rules

- **Standard paragraphs:** Convert `<p>` tags to Markdown paragraphs
- **Images:** Convert `<img>` tags with WordPress `srcset`/`sizes` attributes to standard Markdown `![alt](src)` or HTML `<img>` (keep `src` pointing to local file, remove `srcset`/`sizes`)
- **Image links (lightbox):** `<a href="fullsize.jpg" rel="lightbox[...]"><img ...></a>` → convert to linked image that opens in lightbox
- **WordPress captions:** `<div class="wp-caption">` → Markdown with custom shortcode or HTML
- **YouTube embeds:** `<figure class="wp-block-embed-youtube">` → preserve as HTML iframes
- **Video tags:** `<video>` → preserve as HTML5 `<video>` tag
- **WordPress content formatting:** Convert `&nbsp;` to spaces, decode HTML entities (e.g., `&#8217;` → `'`, `&#8220;` → `"`, `&#8230;` → `...`)
- **Gutenberg blocks:** Strip block wrapper divs, keep content
- **Alignment classes:** Convert `aligncenter`, `alignleft`, `alignright` to appropriate CSS classes

### 6.2 URL Migration

| WordPress URL | Hugo URL |
|--------------|----------|
| `/?p=123` | Not needed |
| `/2021/08/30/some-dolls` | `/posts/2021/08/some-dolls/` |
| `/category/photos` | `/categories/photos/` |
| `/about` | `/about/` |
| `/s` | `/s/` (photo gallery) |
| `/videos` | `/videos/` |
| `/page/2` | `/page/2/` |
| `/wp-content/uploads/YYYY/MM/filename` | `/images/YYYY/MM/filename` or similar |

---

## 7. Build & Deployment

### 7.1 Local Build

```bash
# 1. Generate per-month archive pages
python3 gen_archives.py

# 2. Build the static site
hugo --disableKinds=taxonomy

# 3. Serve locally for testing
hugo server --disableKinds=taxonomy
# Or serve the output directly:
python3 -m http.server 1314 --directory public
```

### 7.2 Docker Build

```bash
docker build . --no-cache --file Dockerfile --tag rowanemilia:latest
docker run -p 8080:80 rowanemilia:latest
```

The Dockerfile runs `gen_archives.py` before Hugo during the build.

### 7.3 GitHub Actions

A workflow at `.github/workflows/docker-image.yml` builds and pushes a Docker image to GitHub Container Registry on every push to `main`. It can also be triggered manually via `workflow_dispatch`.

### 7.4 Hugo Configuration (hugo.yaml)

```yaml
baseURL: "http://localhost:1313/"
locale: "en-US"
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

markup:
  goldmark:
    renderer:
      unsafe: true

ignoreLogs:
  - 'warning-goldmark-raw-html'
```

### 7.5 Verification Checklist

- [ ] Home page shows posts in reverse chronological order
- [ ] Pagination works (5 posts per page)
- [ ] Each post renders correctly with all content
- [ ] Images load from local files (check: no rowanemilia.com URLs)
- [ ] YouTube embeds display and play
- [ ] .mov video plays inline
- [ ] About page renders with text and image
- [ ] Photo Gallery page shows 20-image grid with lightbox
- [ ] Random Videos page shows all embedded videos
- [ ] Sidebar shows Menu, Categories, Archives (no Stuff section)
- [ ] Category links filter to correct posts (with counts)
- [ ] Archive sidebar links navigate to `/archives/YYYY/MM/` pages
- [ ] Per-month archive pages show full post content
- [ ] Year-level archive pages list all posts from that year
- [ ] Top-level `/archives/` lists all 45 months
- [ ] Comments display on posts that have them
- [ ] Lightbox opens on image click, X hidden until overlay active
- [ ] Header matches original (background image, title, tagline)
- [ ] Footer shows copyright only (no Hugo/designer credit)
- [ ] No broken image links
- [ ] No external requests to rowanemilia.com or WordPress domain
- [ ] No Hugo deprecation warnings on build
- [ ] Sidebar appears on the LEFT of content (flexbox layout)
- [ ] Post content uses Markdown, not raw HTML tags

---

## Appendix A: Complete Post List

### 2021
1. 2021-08-30 — Some Dolls (Videos) — YouTube embed `-9icrM6rLKQ`

### 2020
2. 2020-07-31 — Rowan's Ballet Recital (Videos) — YouTube embed `ksDBSa17cA4`

### 2017
3. 2017-07-15 — Some More Photos 2017 (Photos) — 2 photos
4. 2017-07-15 — Some Photos 2017 (Uncategorized) — 2 photos

### 2014
5. 2014-07-08 — June 2014 (Uncategorized) — 2 photos
6. 2014-04-13 — Some pictures. (Uncategorized) — 2 photos

### 2013
7. 2013-07-21 — Uh Oh! (Uncategorized) — .mov video
8. 2013-05-09 — Kid Updates! (Medical Updates, Photos) — 4 photos, long text update
9. 2013-04-13 — Big Boy! (Uncategorized)
10. 2013-03-31 — (no title) (Photos)
11. 2013-03-04 — 4 Months Old! (Uncategorized)
12. 2013-01-24 — 3 months old! (Uncategorized)
13. 2013-01-01 — Happy New Year! (Photos)

### 2012
14. 2012-12-05 — Some Pictures! (Uncategorized)
15. 2012-12-05 — Introducing Julian Alphonse Michael! (Photos)
16. 2012-09-19 — Rowan is 4! (Medical Updates, Photos)
17. 2012-04-16 — Prettiest Flower Girl Ever! (Photos)
18. 2012-04-16 — Twinkle Twinkle (Videos)
19. 2012-02-19 — We're Still Alive! (Uncategorized)

### 2011
20. 2011-11-26 — Rowan chatting about food (Videos)
21. 2011-07-10 — A bit of this and a bit of that… (Medical Updates)
22. 2011-07-01 — Rowan's happy and she knows it (Videos)
23. 2011-06-28 — Mega Smile (Photos)
24. 2011-06-05 — Rowan in Galveston (Photos)
25. 2011-04-27 — Some Good News! (Medical Updates)
26. 2011-03-21 — Talking, Talking, and Talking some more! (Medical Updates)
27. 2011-03-14 — I Love This Kid! (Photos)
28. 2011-02-25 — Bubbles! (Photos)
29. 2011-02-22 — a couple new photos (Photos)
30. 2011-01-23 — Someone refused to nap… (Photos)
31. 2011-01-11 — Photo Shoot! (Photos)

### 2010
32. 2010-12-22 — Just a photo (Photos)
33. 2010-12-07 — Fun Times in Rowan-land! (Medical Updates)
34. 2010-11-25 — Happy Rowan in Brownsville (Photos)
35. 2010-11-09 — Cardiology Update (Medical Updates)
36. 2010-10-31 — Happy Halloween! (Photos)
37. 2010-10-30 — FYI (Videos)
38. 2010-10-11 — Older photo (Photos)
39. 2010-09-21 — Happy Birthday Peanut! (Photos)
40. 2010-08-24 — For Your Viewing Pleasure (Videos)
41. 2010-08-05 — A Little More Good News (Medical Updates)
42. 2010-07-22 — She's Crazy! (Photos)
43. 2010-07-15 — See What I Can Do! (Videos)
44. 2010-07-06 — Surgery (Medical Updates)
45. 2010-06-23 — It's Out! (Medical Updates)
46. 2010-06-04 — Awww…part ∞ (Photos)
47. 2010-06-04 — Running Errands (Photos)
48. 2010-06-02 — 'nother walking video (Videos)
49. 2010-06-02 — Awww…part 3 (Photos)
50. 2010-06-02 — Smelly Plant (Photos)
51. 2010-06-02 — Awww…part 2 (Photos)
52. 2010-06-02 — Awww…part 1 (Photos)
53. 2010-05-27 — What She's Doing Now (Medical Updates)
54. 2010-05-25 — Photo Shoot (Photos)
55. 2010-05-24 — More Pics (Photos)
56. 2010-05-24 — After the Echo (Photos)
57. 2010-05-12 — Quick Update (Medical Updates)
58. 2010-03-05 — Working on a new cute trick (Videos)
59. 2010-03-03 — Almost Walking (Videos)
60. 2010-03-02 — She started growling (Photos)
61. 2010-02-28 — Visiting Houston (Photos)
62. 2010-02-15 — She's pretty awesome (Photos)
63. 2010-01-27 — More Crawling! (Videos)

### 2009
64. 2009-12-26 — "She really likes her food.." (Medical Updates)
65. 2009-12-23 — Milestone — Crawling!! (Videos)
66. 2009-11-29 — Rowan in Brownsville (Photos)
67. 2009-11-04 — Making Friends (Photos)
68. 2009-10-31 — It's Snow White! (Photos)
69. 2009-10-17 — Happy Birthday Peanut! (Medical Updates, Photos)
70. 2009-08-30 — Silly Girl (Photos)
71. 2009-07-27 — 10 months old! (Photos)
72. 2009-07-25 — Some newer pics (Photos)
73. 2009-06-24 — Favorite Video (Videos)
74. 2009-06-17 — Happy Girl (Photos)
75. 2009-06-17 — Milestone (Medical Updates)
76. 2009-05-30 — Big Girl! (Photos)
77. 2009-05-19 — She's 8 months old! (Medical Updates)
78. 2009-05-07 — They call this "therapy"? (Photos)
79. 2009-05-06 — New photos from the last visit (Photos)
80. 2009-04-04 — She's such a big girl! (Photos)
81. 2009-03-09 — Exciting day in Rowan-land! (Medical Updates)
82. 2009-02-27 — More Photos (Photos)
83. 2009-02-26 — Yes, she now has a mohawk instead of a comb over (Photos)
84. 2009-02-26 — Testing a new lense (Photos)
85. 2009-02-02 — Exciting Stuff! (Photos)
86. 2009-01 — (no posts this month)

### 2008
87. 2008-12-27 — Christmas 2008 (Photos)
88. 2008-12-15 — Good News (Medical Updates)
89. 2008-12-04 — Medical Update (Medical Updates)
90. 2008-11-30 — Talking to Lola (Photos)
91. 2008-11-28 — "I'm cute. Everyone says so." (Photos)
92. 2008-11-19 — Doctors appointments galore (Medical Updates)
93. 2008-11-16 — Yawn! (Photos)
94. 2008-10-31 — Rowan is home! (Photos)
