#!/usr/bin/env python3
"""
Blog Sitemap Generator
Automatically generates sitemap.xml from assets/shared/posts.json
"""

import json
import os
from datetime import datetime
from urllib.parse import urljoin

SITE_URL = "https://victor-kipruto-rop.github.io/victor-resum-web"
BLOG_DIR = os.path.dirname(__file__)
POSTS_FILE = os.path.join(BLOG_DIR, "assets/shared/posts.json")
SITEMAP_FILE = os.path.join(os.path.dirname(BLOG_DIR), "sitemap.xml")

def load_posts():
    """Load posts from assets/shared/posts.json"""
    with open(POSTS_FILE, 'r') as f:
        posts_data = json.load(f)
    return posts_data.get('posts', [])

def get_categories():
    """Get all categories"""
    with open(POSTS_FILE, 'r') as f:
        posts_data = json.load(f)
    return posts_data.get('categories', [])

def get_tags():
    """Get all tags"""
    with open(POSTS_FILE, 'r') as f:
        posts_data = json.load(f)
    return posts_data.get('tags', [])

def format_date(date_str):
    """Format date for sitemap"""
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime('%Y-%m-%d')
    except:
        return datetime.now().strftime('%Y-%m-%d')

def generate_sitemap():
    """Generate sitemap.xml"""
    posts = load_posts()
    categories = get_categories()
    tags = get_tags()
    
    urls = []
    
    # Homepage
    urls.append({
        'loc': SITE_URL,
        'lastmod': datetime.now().strftime('%Y-%m-%d'),
        'priority': '1.0',
        'changefreq': 'daily'
    })
    
    # Blog homepage
    urls.append({
        'loc': urljoin(SITE_URL, '/blog'),
        'lastmod': datetime.now().strftime('%Y-%m-%d'),
        'priority': '0.9',
        'changefreq': 'daily'
    })
    
    # Articles
    for post in posts:
        urls.append({
            'loc': urljoin(SITE_URL, f"/blog/posts/{post['slug']}.html"),
            'lastmod': format_date(post.get('lastUpdated', post['publishDate'])),
            'priority': '0.8',
            'changefreq': 'weekly'
        })
    
    # Categories
    for category in categories:
        urls.append({
            'loc': urljoin(SITE_URL, f"/category/{category['slug']}"),
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'priority': '0.7',
            'changefreq': 'weekly'
        })
    
    # Tags
    for tag in tags:
        urls.append({
            'loc': urljoin(SITE_URL, f"/tags/{tag['slug']}"),
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'priority': '0.6',
            'changefreq': 'weekly'
        })
    
    # Generate XML
    url_entries = []
    for url in urls:
        entry = f"""  <url>
    <loc>{url['loc']}</loc>
    <lastmod>{url['lastmod']}</lastmod>
    <changefreq>{url['changefreq']}</changefreq>
    <priority>{url['priority']}</priority>
  </url>"""
        url_entries.append(entry)
    
    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
        xmlns:mobile="http://www.google.com/schemas/sitemap-mobile/1.0">
{''.join(url_entries)}
</urlset>"""
    
    with open(SITEMAP_FILE, 'w') as f:
        f.write(sitemap_content)
    
    print(f"✓ Sitemap generated: {SITEMAP_FILE}")
    print(f"  • {len(urls)} URLs included")
    return SITEMAP_FILE

def validate_sitemap():
    """Validate sitemap structure"""
    with open(SITEMAP_FILE, 'r') as f:
        content = f.read()
    
    required_tags = ['<?xml', '<urlset', '<url>', '<loc>', '</urlset>']
    issues = []
    
    for tag in required_tags:
        if tag not in content:
            issues.append(f"Missing required tag: {tag}")
    
    if issues:
        print("⚠ Sitemap Validation Issues:")
        for issue in issues:
            print(f"  • {issue}")
    else:
        print("✓ Sitemap validation passed")
    
    return len(issues) == 0

if __name__ == "__main__":
    generate_sitemap()
    validate_sitemap()
