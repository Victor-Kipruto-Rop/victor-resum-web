#!/usr/bin/env python3
"""
Blog RSS Generator
Automatically generates RSS feed from posts.json
"""

import json
import os
from datetime import datetime
from urllib.parse import urljoin

SITE_URL = "https://victor-kipruto-rop.github.io/victor-resum-web"
BLOG_DIR = os.path.dirname(__file__)
POSTS_FILE = os.path.join(BLOG_DIR, "posts.json")
RSS_FILE = os.path.join(BLOG_DIR, "feed.xml")

def load_posts():
    """Load posts from posts.json"""
    with open(POSTS_FILE, 'r') as f:
        posts_data = json.load(f)
    return posts_data.get('posts', [])

def generate_rss():
    """Generate RSS feed XML"""
    posts = load_posts()
    posts.sort(key=lambda x: x['publishDate'], reverse=True)
    
    rss_items = []
    
    for post in posts[:10]:  # Last 10 posts
        pub_date = datetime.fromisoformat(post['publishDate']).strftime('%a, %d %b %Y %H:%M:%S GMT')
        post_url = urljoin(SITE_URL, f"/blog/posts/{post['slug']}.html")
        
        item = f"""  <item>
    <title>{escape_xml(post['title'])}</title>
    <link>{post_url}</link>
    <guid isPermaLink="true">{post_url}</guid>
    <pubDate>{pub_date}</pubDate>
    <description>{escape_xml(post['description'])}</description>
    <category>{escape_xml(post['category'])}</category>
    <author>victor@example.com (Victor Kipruto)</author>
  </item>"""
        rss_items.append(item)
    
    rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Victor Kipruto - Technical Blog</title>
    <link>{SITE_URL}/blog</link>
    <description>Data Engineering, Python, and Cloud Architecture</description>
    <language>en-us</language>
    <atom:link href="{SITE_URL}/feed.xml" rel="self" type="application/rss+xml" />
    <lastBuildDate>{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}</lastBuildDate>
    <image>
      <url>{SITE_URL}/assets/1.jpeg</url>
      <title>Victor Kipruto</title>
      <link>{SITE_URL}</link>
    </image>
{''.join(rss_items)}
  </channel>
</rss>"""
    
    with open(RSS_FILE, 'w') as f:
        f.write(rss_content)
    
    print(f"✓ RSS feed generated: {RSS_FILE}")
    return RSS_FILE

def escape_xml(text):
    """Escape special XML characters"""
    if not text:
        return ""
    text = str(text)
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    text = text.replace("'", "&apos;")
    return text

def validate_rss():
    """Validate RSS feed structure"""
    with open(RSS_FILE, 'r') as f:
        content = f.read()
    
    required_tags = ['<?xml', '<rss', '<channel>', '<title>', '<link>', '<item>']
    issues = []
    
    for tag in required_tags:
        if tag not in content:
            issues.append(f"Missing required tag: {tag}")
    
    if issues:
        print("⚠ RSS Validation Issues:")
        for issue in issues:
            print(f"  • {issue}")
    else:
        print("✓ RSS feed validation passed")
    
    return len(issues) == 0

if __name__ == "__main__":
    generate_rss()
    validate_rss()
