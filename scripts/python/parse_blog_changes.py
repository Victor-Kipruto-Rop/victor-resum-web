#!/usr/bin/env python3
"""
Parse Blog Changes - Detect new and updated blog posts
"""

import json
from pathlib import Path
from datetime import datetime

def parse_blog_changes():
    """Parse changes in blog/posts.json"""
    posts_file = Path('blog/posts.json')
    
    if not posts_file.exists():
        print("❌ No blog posts found")
        return []
    
    try:
        with open(posts_file, 'r') as f:
            data = json.load(f)
        
        posts = data.get('posts', [])
        
        # Get recently updated posts (last 24 hours)
        recent_posts = []
        now = datetime.now()
        
        for post in posts:
            updated = datetime.fromisoformat(post.get('publishDate', ''))
            days_old = (now - updated).days
            
            if days_old == 0:
                recent_posts.append(post)
        
        print(f"✓ Found {len(recent_posts)} recent posts")
        
        # Save for downstream jobs
        with open('notifications/recent-posts.json', 'w') as f:
            json.dump(recent_posts, f, indent=2)
        
        return recent_posts
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

if __name__ == '__main__':
    parse_blog_changes()
