#!/usr/bin/env python3
"""
Prepare distribution content from blog posts
"""

import json
from pathlib import Path

def prepare_distribution():
    """Prepare social content from latest blog post"""
    try:
        posts_file = Path('blog/posts.json')
        
        if not posts_file.exists():
            print("❌ No blog posts found")
            return False
        
        with open(posts_file, 'r') as f:
            posts_data = json.load(f)
        
        # Get latest published post
        posts = [p for p in posts_data['posts'] if p.get('status') == 'published']
        if posts:
            latest = sorted(posts, key=lambda x: x['publishDate'], reverse=True)[0]
            
            content = {
                "post_id": latest['id'],
                "title": latest['title'],
                "slug": latest['slug'],
                "description": latest['description'],
                "category": latest['category'],
                "tags": latest['tags'],
                "image": latest.get('image', ''),
                "url": f"https://victorkipruto.com/blog/posts/{latest['slug']}.html"
            }
            
            with open('distribution-content.json', 'w') as f:
                json.dump(content, f, indent=2)
            
            print(f"✓ Prepared for distribution: {content['title']}")
            return True
        else:
            print("⚠️  No published posts found")
            return False
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    prepare_distribution()
