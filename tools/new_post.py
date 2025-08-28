#!/usr/bin/env python3
"""
Scaffold a new blog post page and update blog/blog-data.json.
Usage:
  python3 tools/new_post.py "My Post Title" my-post-slug "August 28, 2025" "Short excerpt" tag1 tag2

- Creates blog/posts/<slug>.html from the template.
- Adds an entry to blog/blog-data.json (id auto-incremented).
- Prints next steps to add thumbnail under blog/assets/.
"""
import sys
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / 'blog' / 'posts'
DATA_FILE = ROOT / 'blog' / 'blog-data.json'
TEMPLATE = POSTS_DIR / '_template.html'


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9\- ]+", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s


def main():
    if len(sys.argv) < 5:
        print(__doc__)
        sys.exit(1)

    title = sys.argv[1]
    slug = sys.argv[2]
    date = sys.argv[3]
    excerpt = sys.argv[4]
    tags = sys.argv[5:] or []

    if slug in ("", None):
        slug = slugify(title)

    # Validate paths
    if not TEMPLATE.exists():
        print(f"Template not found: {TEMPLATE}")
        sys.exit(2)
    if not DATA_FILE.exists():
        print(f"Data file not found: {DATA_FILE}")
        sys.exit(2)

    # Create post file
    post_path = POSTS_DIR / f"{slug}.html"
    if post_path.exists():
        print(f"Post already exists: {post_path}")
        sys.exit(3)

    html = TEMPLATE.read_text(encoding='utf-8')
    html = html.replace('<!-- Post Title -->', title)
    html = html.replace('<!-- Short description for SEO/social -->', excerpt)
    html = html.replace('<!-- Short description for social -->', excerpt)
    # Keep og:image placeholder; user will add thumbnail and can update later.
    html = html.replace('<!-- Month DD, YYYY -->', date)
    html = html.replace('<!-- comma, separated, tags -->', ', '.join(tags))

    post_path.write_text(html, encoding='utf-8')

    # Update blog-data.json
    data = json.loads(DATA_FILE.read_text(encoding='utf-8'))
    posts = data.get('posts', [])
    next_id = (max((p.get('id', 0) for p in posts), default=0) + 1) if posts else 1

    # Build thumbnail path placeholder; user can change later
    thumb = f"/blog/assets/{slug}.jpg"

    posts.append({
        'id': next_id,
        'slug': slug,
        'title': title,
        'date': date,
        'thumbnail': thumb,
        'excerpt': excerpt,
        'tags': tags,
    })

    data['posts'] = posts
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding='utf-8')

    print(f"Created {post_path.relative_to(ROOT)}")
    print(f"Added post to {DATA_FILE.relative_to(ROOT)}")
    print("Next steps:")
    print(f"  1) Add a thumbnail at blog/assets/{slug}.jpg (or update 'thumbnail' in blog/blog-data.json)")
    print("  2) Commit and push — homepage and blog index will update automatically.")


if __name__ == '__main__':
    main()
