# Joseph Smithberger — Portfolio & Blog

A static site (no build tools) for a personal portfolio and blog. Pages are plain HTML styled with CSS and a sprinkle of vanilla JS. Blog listings are driven by a small JSON file; individual posts are standalone HTML pages.

## What’s inside

- `index.html` — Home page with About, Projects, Gallery, Blog preview, Socials, and Contact
- `styles.css` — Global styles for the whole site
- `gamejam.html` — Standalone page listing game jam entries
- `blog/`
  - `index.html` — Blog index; renders cards by fetching `blog-data.json` (now with tag filter UI)
  - `blog-styles.css` — Blog-specific styles (post layout, cards)
  - `blog-data.json` — Source of truth for blog listings and prev/next navigation
  - `assets/` — Thumbnails and images used by posts and cards
  - `posts/` — Individual post HTML files, one per post; includes `_template.html` for new posts
- `tools/new_post.py` — Script to scaffold a new post and update `blog-data.json`
- `CNAME` — Custom domain for GitHub Pages (don’t edit unless the domain changes)

## How pages and the blog work

- Global styling lives in `styles.css`. Blog pages also include `blog/blog-styles.css`.
- The home page (`index.html`) shows the latest 5 posts in the “my thoughts” section. It fetches `/blog/blog-data.json` and builds cards linking to `/blog/posts/<slug>.html`.
- The blog index (`blog/index.html`) also fetches `blog-data.json` and renders all posts (newest first). It contains code intended for tag filters; UI markup for filters isn’t present yet, so filtering is effectively disabled (see Notes section for enabling it).
- Post pages are static HTML files under `blog/posts/`. They include:
  - Normal site nav and CSS links
  - A content container with title, date, tags, and article body
  - A small script that reads `blog-data.json` to wire up Previous/Next links

Data shape in `blog/blog-data.json` (used by home, blog index, and post navigation):

```jsonc
{
  "posts": [
    {
      "id": 2,
      "slug": "second-game-jam",       // no .html
      "title": "My Second Ever Game Jam!",
      "date": "June 30, 2025",         // must be parseable by new Date()
      "thumbnail": "/blog/assets/jam_thumb.jpg",
      "excerpt": "How I made Rollbit for the Xogot game jam!",
      "tags": ["game jam", "devlog", "xogot"]
    }
  ]
}
```

- Sorting is performed via `new Date(b.date) - new Date(a.date)`, so keep dates in a format the browser can parse (e.g., “June 30, 2025” or ISO).
- Card links are generated as `/blog/posts/<slug>.html`, so `slug` must not include `.html`.

## Edit existing content

- Home content: edit `index.html` and images at the repo root. Gallery images are the `*.jpg/png` files.
- Navbar: edit the `<nav>` in each page you want to change (the nav is duplicated per page).
- Global styles: `styles.css`. Blog-specific styles: `blog/blog-styles.css`.
- Blog post body: edit the corresponding HTML file in `blog/posts/`.

## Create a new blog post (standardized)

1) Pick a slug
- Use a URL-friendly name like `my-new-post` (no spaces, no `.html`).

2) Scaffold the post (automated)
- From the repo root, run:

```bash
python3 tools/new_post.py "My Post Title" my-post-slug "August 28, 2025" "Short excerpt" tag1 tag2
```

- This will:
  - Create `blog/posts/<slug>.html` from `_template.html` with title/date/tags filled
  - Append a post entry to `blog/blog-data.json`
  - Set a thumbnail placeholder `/blog/assets/<slug>.jpg` (you can change it)

3) Edit the new post content
- Open `blog/posts/<slug>.html` and replace the placeholder content in `<article class="blog-post-content">`.
- Update the Open Graph `og:image` meta to match your thumbnail if you changed it.

3) Add a thumbnail image
- Place a 16:9 or square-ish image in `blog/assets/` (e.g., `my-new-post.jpg`).
- Use the absolute path in JSON (e.g., `/blog/assets/my-new-post.jpg`).

4) Add the thumbnail
- Place the image at `blog/assets/<slug>.jpg` or update the `thumbnail` field in `blog/blog-data.json` to the correct path.

5) Commit and deploy
- Push to `main` if you’ve set up GitHub Pages. The home page and blog index will update automatically (they both read `blog-data.json`).

## Correct styling checklist for posts

- Head includes:
  - Google Font and Font Awesome (as in the templates)
  - `<link rel="stylesheet" href="/styles.css">`
  - `<link rel="stylesheet" href="/blog/blog-styles.css">`
- Body structure:
  - Site nav copied from a working post
  - `<main class="blog-post-container">` wrapping header, article, nav
  - Article content inside `<article class="blog-post-content">`
- Images inside posts get rounded corners and frames automatically; ensure you add sensible `alt` text.

## Local development

Because the pages fetch `/blog/blog-data.json`, open them via a local web server (not `file://`). Two easy options:

- VS Code Live Server extension (right-click `index.html` → “Open with Live Server”).
- Python (macOS has Python 3):

```bash
# from the repo root
python3 -m http.server 8000
# visit http://localhost:8000/
```

## Notes and small improvements

- Tag filters on the blog index are enabled; use the chips to filter by tag. Tags come from each post’s `tags` in `blog-data.json`.
- The post navigation script now derives the current slug from the URL (no more hardcoding).
- The blog index and posts use absolute CSS paths (`/styles.css`, `/blog/blog-styles.css`) for consistency.
- Removed the old unused `blog/blog-script.js` to avoid confusion.
- The comment `<!--#include file="assets/projects-section.html" -->` in `blog/index.html` is an SSI hint; GitHub Pages won’t process it. If you want that content, paste it into the page manually.
- Dates: keep them consistent and parseable to ensure sorting works.
- CNAME: only change if you move to a different domain.

## Troubleshooting

- Blog cards don’t appear / “Could not load posts” on home: ensure you’re serving the site over HTTP locally and that `blog/blog-data.json` is valid JSON.
- Post appears on the blog index but prev/next links are missing: confirm the `slug` in `blog-data.json` matches the post filename (without `.html`).
- Thumbnails not showing: check the `thumbnail` path starts with `/blog/assets/` and the file exists.
- Sorting is odd: make sure `date` values are consistent and parseable by `new Date(...)`.

## License

No explicit license is defined in this repository. Treat the content as all-rights-reserved unless the author adds a license.
