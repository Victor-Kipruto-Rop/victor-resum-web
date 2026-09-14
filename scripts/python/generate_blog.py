#!/usr/bin/env python3
"""
DBOS PHASE 1: Blog Rendering Engine
Generates HTML blog pages from posts.json
"""

import html
import json
import os
from datetime import datetime
from pathlib import Path

class BlogRenderingEngine:
    """Auto-render blog pages from posts.json"""
    
    def __init__(self):
        self.blog_dir = Path('blog')
        self.posts_file = self.blog_dir / 'posts.json'
        self.output_dir = self.blog_dir / 'rendered'
        self.posts = []
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def load_posts(self):
        """Load posts from posts.json"""
        with open(self.posts_file) as f:
            self.posts = json.load(f)
        print(f"✓ Loaded {len(self.posts)} posts")
    
    def generate_blog_homepage(self):
        """Generate main blog homepage"""
        html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog | Developer Brand</title>
    <meta name="description" content="Advanced insights on Data Engineering, Analytics, and System Design">
    <link rel="stylesheet" href="/assets/css/blog.css">
</head>
<body>
    <div class="blog-container">
        <header class="blog-header">
            <h1>📝 Developer Blog</h1>
            <p>Deep dives into Data Engineering, Analytics Engineering, and System Design</p>
        </header>
        
        <div class="blog-posts">
'''
        
        # Add published posts sorted by date (newest first)
        published = [p for p in self.posts if p.get('status') == 'published']
        published.sort(key=lambda x: x.get('publishDate', ''), reverse=True)
        
        for post in published:
            date_obj = datetime.fromisoformat(post['publishDate'].replace('Z', '+00:00'))
            formatted_date = date_obj.strftime('%B %d, %Y')
            
            html += f'''            <article class="post-card">
                <div class="post-meta">
                    <span class="category">{post['category']}</span>
                    <span class="date">{formatted_date}</span>
                    <span class="read-time">📖 {post['readTime']} min read</span>
                </div>
                <h2><a href="/blog/posts/{post['slug']}">{post['title']}</a></h2>
                <p>{post['description']}</p>
                <div class="post-tags">
'''
            for tag in post.get('tags', []):
                html += f'                    <span class="tag">#{tag}</span>\n'
            
            html += f'''                </div>
                <a href="/blog/posts/{post['slug']}" class="read-more">Read Article →</a>
            </article>
'''
        
        html += '''        </div>
    </div>
    <script src="/analytics/tracker.js"></script>
</body>
</html>
'''
        
        output_file = self.output_dir / 'index.html'
        with open(output_file, 'w') as f:
            f.write(html)
        print(f"✓ Generated blog homepage: {output_file}")
    
    def generate_category_pages(self):
        """Generate category pages"""
        categories = {}
        
        # Group posts by category
        for post in self.posts:
            if post.get('status') == 'published':
                cat = post.get('category', 'Uncategorized')
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(post)
        
        # Create category directory
        cat_dir = self.output_dir / 'categories'
        cat_dir.mkdir(parents=True, exist_ok=True)
        
        for category, posts in categories.items():
            cat_slug = category.lower().replace(' ', '-')
            html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{category} | Blog</title>
    <link rel="stylesheet" href="/assets/css/blog.css">
</head>
<body>
    <div class="blog-container">
        <header class="blog-header">
            <h1>📂 {category}</h1>
            <p>{len(posts)} article(s) in this category</p>
        </header>
        
        <div class="blog-posts">
'''
            
            # Add posts sorted by date
            posts.sort(key=lambda x: x.get('publishDate', ''), reverse=True)
            for post in posts:
                date_obj = datetime.fromisoformat(post['publishDate'].replace('Z', '+00:00'))
                formatted_date = date_obj.strftime('%B %d, %Y')
                
                html += f'''            <article class="post-card">
                <div class="post-meta">
                    <span class="date">{formatted_date}</span>
                    <span class="read-time">📖 {post['readTime']} min</span>
                </div>
                <h2><a href="/blog/posts/{post['slug']}">{post['title']}</a></h2>
                <p>{post['description']}</p>
                <a href="/blog/posts/{post['slug']}" class="read-more">Read →</a>
            </article>
'''
            
            html += '''        </div>
        <p style="margin-top: 40px; text-align: center;"><a href="/blog">← Back to Blog</a></p>
    </div>
</body>
</html>
'''
            
            output_file = cat_dir / f'{cat_slug}.html'
            with open(output_file, 'w') as f:
                f.write(html)
        
        print(f"✓ Generated {len(categories)} category pages")
    
    def generate_tag_pages(self):
        """Generate tag pages"""
        tags = {}
        
        # Group posts by tags
        for post in self.posts:
            if post.get('status') == 'published':
                for tag in post.get('tags', []):
                    if tag not in tags:
                        tags[tag] = []
                    tags[tag].append(post)
        
        # Create tags directory
        tag_dir = self.output_dir / 'tags'
        tag_dir.mkdir(parents=True, exist_ok=True)
        
        for tag, posts in tags.items():
            tag_slug = tag.lower().replace(' ', '-')
            html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>#{tag} | Blog</title>
    <link rel="stylesheet" href="/assets/css/blog.css">
</head>
<body>
    <div class="blog-container">
        <header class="blog-header">
            <h1>🏷️ #{tag}</h1>
            <p>{len(posts)} article(s) with this tag</p>
        </header>
        
        <div class="blog-posts">
'''
            
            # Add posts sorted by date
            posts.sort(key=lambda x: x.get('publishDate', ''), reverse=True)
            for post in posts:
                date_obj = datetime.fromisoformat(post['publishDate'].replace('Z', '+00:00'))
                formatted_date = date_obj.strftime('%B %d, %Y')
                
                html += f'''            <article class="post-card">
                <div class="post-meta">
                    <span class="category">{post['category']}</span>
                    <span class="date">{formatted_date}</span>
                </div>
                <h2><a href="/blog/posts/{post['slug']}">{post['title']}</a></h2>
                <p>{post['description']}</p>
                <a href="/blog/posts/{post['slug']}" class="read-more">Read →</a>
            </article>
'''
            
            html += '''        </div>
        <p style="margin-top: 40px; text-align: center;"><a href="/blog">← Back to Blog</a></p>
    </div>
</body>
</html>
'''
            
            output_file = tag_dir / f'{tag_slug}.html'
            with open(output_file, 'w') as f:
                f.write(html)
        
        print(f"✓ Generated {len(tags)} tag pages")

    def generate_post_pages(self):
        """Generate an individual page for every published post.

        Without this step, every "Read Article" link on the homepage,
        category pages, and tag pages points at a URL that was never
        actually created (a 404). Posts without a full `body` field in
        posts.json get an honest placeholder instead of fabricated
        content.
        """
        posts_dir = self.output_dir.parent / 'posts'
        posts_dir.mkdir(parents=True, exist_ok=True)

        published = [p for p in self.posts if p.get('status') == 'published']
        generated = 0

        for post in published:
            date_obj = datetime.fromisoformat(post['publishDate'].replace('Z', '+00:00'))
            formatted_date = date_obj.strftime('%B %d, %Y')

            tags_html = "\n".join(
                f'                <span class="tag">#{tag}</span>'
                for tag in post.get('tags', [])
            )

            body = post.get('body')
            if body:
                body_html = body
                placeholder_html = ''
            else:
                body_html = f"<p>{html.escape(post['description'])}</p>"
                placeholder_html = f'''            <div class="placeholder-note">
                This post's full write-up is still being drafted. Here's the summary in
                the meantime: {html.escape(post['description'])}
            </div>
'''

            page = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(post['title'])} | Blog</title>
    <meta name="description" content="{html.escape(post['description'])}">
    <link rel="stylesheet" href="/assets/css/blog.css">
</head>
<body>
    <div class="blog-container">
        <article class="post-article">
            <div class="post-meta">
                <span class="category">{html.escape(post['category'])}</span>
                <span class="date">{formatted_date}</span>
                <span class="read-time">📖 {post['readTime']} min read</span>
            </div>
            <h1>{html.escape(post['title'])}</h1>
            <div class="post-tags">
{tags_html}
            </div>
            <div class="post-body">
{body_html}
            </div>
{placeholder_html}        </article>
        <a href="/blog" class="back-link">← Back to Blog</a>
    </div>
    <script src="/analytics/tracker.js"></script>
</body>
</html>
'''

            post_dir = posts_dir / post['slug']
            post_dir.mkdir(parents=True, exist_ok=True)
            with open(post_dir / 'index.html', 'w') as f:
                f.write(page)
            generated += 1

        print(f"✓ Generated {generated} post pages")

    def run(self):
        """Execute blog rendering"""
        print("\n🚀 DBOS PHASE 1: Blog Rendering Engine\n")
        self.load_posts()
        self.generate_blog_homepage()
        self.generate_category_pages()
        self.generate_tag_pages()
        self.generate_post_pages()
        print("\n✅ Blog rendering complete!\n")

if __name__ == '__main__':
    engine = BlogRenderingEngine()
    engine.run()
