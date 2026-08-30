#!/usr/bin/env python3
"""
SEO Asset Generator
Generates OG tags, Twitter cards, structured data JSON-LD for each post
"""

import json
import os
import html
from datetime import datetime

SITE_URL = "https://victorkipruto.com"
BLOG_DIR = os.path.dirname(__file__)
POSTS_FILE = os.path.join(BLOG_DIR, "posts.json")
ASSETS_DIR = os.path.join(os.path.dirname(BLOG_DIR), "assets")
SEO_ASSETS_DIR = os.path.join(ASSETS_DIR, "seo-assets")

def ensure_directory():
    """Create SEO assets directory if it doesn't exist"""
    os.makedirs(SEO_ASSETS_DIR, exist_ok=True)

def load_posts():
    """Load posts from posts.json"""
    with open(POSTS_FILE, 'r') as f:
        posts_data = json.load(f)
    return posts_data.get('posts', [])

def generate_og_tags(post):
    """Generate OpenGraph meta tags for post"""
    post_url = f"{SITE_URL}/blog/posts/{post['slug']}.html"
    image_url = f"{SITE_URL}{post['image']}" if post.get('image') else f"{SITE_URL}/assets/1.jpeg"
    
    tags = f"""    <!-- OpenGraph Tags -->
    <meta property="og:type" content="article" />
    <meta property="og:title" content="{html.escape(post['title'])}" />
    <meta property="og:description" content="{html.escape(post['description'])}" />
    <meta property="og:url" content="{post_url}" />
    <meta property="og:image" content="{image_url}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:site_name" content="Victor Kipruto" />
    <meta property="article:published_time" content="{post['publishDate']}T00:00:00Z" />
    <meta property="article:modified_time" content="{post.get('lastUpdated', post['publishDate'])}T00:00:00Z" />
    <meta property="article:author" content="Victor Kipruto" />
    <meta property="article:section" content="{post['category']}" />
"""
    for tag in post.get('tags', []):
        tags += f'    <meta property="article:tag" content="{tag}" />\n'
    
    return tags

def generate_twitter_card(post):
    """Generate Twitter Card meta tags"""
    post_url = f"{SITE_URL}/blog/posts/{post['slug']}.html"
    image_url = f"{SITE_URL}{post['image']}" if post.get('image') else f"{SITE_URL}/assets/1.jpeg"
    
    tags = f"""    <!-- Twitter Card Tags -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{html.escape(post['title'])}" />
    <meta name="twitter:description" content="{html.escape(post['description'])}" />
    <meta name="twitter:image" content="{image_url}" />
    <meta name="twitter:url" content="{post_url}" />
    <meta name="twitter:creator" content="@victorkirpruto" />
    <meta name="twitter:site" content="@victorkirpruto" />
"""
    return tags

def generate_structured_data(post):
    """Generate JSON-LD structured data"""
    post_url = f"{SITE_URL}/blog/posts/{post['slug']}.html"
    image_url = f"{SITE_URL}{post['image']}" if post.get('image') else f"{SITE_URL}/assets/1.jpeg"
    
    structured_data = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": post_url
        },
        "headline": post['title'],
        "description": post['description'],
        "image": image_url,
        "datePublished": post['publishDate'],
        "dateModified": post.get('lastUpdated', post['publishDate']),
        "author": {
            "@type": "Person",
            "name": "Victor Kipruto",
            "url": SITE_URL
        },
        "publisher": {
            "@type": "Organization",
            "name": "Victor Kipruto",
            "logo": {
                "@type": "ImageObject",
                "url": f"{SITE_URL}/assets/1.jpeg"
            }
        },
        "articleBody": "Read more at " + post_url,
        "keywords": ", ".join(post.get('seoKeywords', [])),
        "articleSection": post['category']
    }
    
    return f"""    <!-- Structured Data (JSON-LD) -->
    <script type="application/ld+json">
{json.dumps(structured_data, indent=2).replace(json.dumps(structured_data)[0:1], '  ')}
    </script>"""

def generate_article_schema(post):
    """Generate Article schema for SEO"""
    post_url = f"{SITE_URL}/blog/posts/{post['slug']}.html"
    
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "url": post_url,
        "headline": post['title'],
        "abstract": post['description'],
        "keywords": ", ".join(post.get('seoKeywords', [])),
        "thumbnailUrl": f"{SITE_URL}{post['image']}" if post.get('image') else f"{SITE_URL}/assets/1.jpeg",
        "datePublished": post['publishDate'],
        "dateModified": post.get('lastUpdated', post['publishDate']),
        "author": {
            "@type": "Person",
            "name": "Victor Kipruto"
        },
        "publisher": {
            "@type": "Organization",
            "name": "Victor Kipruto"
        }
    }
    
    return schema

def generate_breadcrumb_schema(post):
    """Generate Breadcrumb schema for navigation"""
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": SITE_URL
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Blog",
                "item": f"{SITE_URL}/blog"
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": post['category'],
                "item": f"{SITE_URL}/category/{post['slug']}"
            },
            {
                "@type": "ListItem",
                "position": 4,
                "name": post['title'],
                "item": f"{SITE_URL}/blog/posts/{post['slug']}.html"
            }
        ]
    }
    
    return schema

def generate_seo_assets():
    """Generate all SEO assets for posts"""
    ensure_directory()
    posts = load_posts()
    
    for post in posts:
        # Create JSON file with all SEO data
        seo_data = {
            "post": post,
            "generatedAt": datetime.now().isoformat(),
            "url": f"{SITE_URL}/blog/posts/{post['slug']}.html",
            "og_tags": generate_og_tags(post),
            "twitter_card": generate_twitter_card(post),
            "structured_data": generate_structured_data(post),
            "article_schema": generate_article_schema(post),
            "breadcrumb_schema": generate_breadcrumb_schema(post),
            "canonical_url": f"{SITE_URL}/blog/posts/{post['slug']}.html"
        }
        
        seo_file = os.path.join(SEO_ASSETS_DIR, f"{post['slug']}-seo.json")
        with open(seo_file, 'w') as f:
            json.dump(seo_data, f, indent=2)
        
        print(f"✓ SEO assets generated for: {post['title']}")
    
    return SEO_ASSETS_DIR

if __name__ == "__main__":
    generate_seo_assets()
    print("✓ All SEO assets generated successfully")
