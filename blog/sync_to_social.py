#!/usr/bin/env python3
"""
Sync Blog Posts to Social Media
Automatically distributes new or updated blog posts to Twitter, LinkedIn, Telegram, and Dev.to
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Setup path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from config import config
    from scripts.python.notify_telegram import send_telegram_notification
    from scripts.python.distribute_twitter import post_tweet
except ImportError as e:
    print(f"⚠️  Import error: {e}")
    print("Some social media integrations may not be available")

BLOG_DIR = Path(__file__).parent
POSTS_JSON = BLOG_DIR / "posts.json"
SYNC_STATE_FILE = BLOG_DIR / ".sync_state.json"

def load_posts() -> List[Dict]:
    """Load blog posts from posts.json"""
    try:
        with open(POSTS_JSON, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ posts.json not found at {POSTS_JSON}")
        return []
    except json.JSONDecodeError:
        print(f"❌ posts.json is invalid JSON")
        return []

def load_sync_state() -> Dict:
    """Load previously synced posts"""
    try:
        if SYNC_STATE_FILE.exists():
            with open(SYNC_STATE_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {"synced_posts": {}, "last_sync": None}

def save_sync_state(state: Dict):
    """Save sync state"""
    state["last_sync"] = datetime.now().isoformat()
    with open(SYNC_STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def format_blog_title(post: Dict) -> str:
    """Format blog title for social media"""
    return post.get('title', 'New Blog Post')

def format_twitter_post(post: Dict, blog_url: str = "https://victor-kipruto-rop.github.io/victor-resum-web/blog") -> str:
    """Format post for Twitter"""
    title = post.get('title', 'New Blog Post')
    slug = post.get('slug', post.get('id', 'post'))
    
    # Twitter character limit
    hashtags = " ".join(f"#{tag}" for tag in post.get('tags', [])[:3])
    
    post_url = f"{blog_url}/{slug}.html"
    
    # Craft tweet (280 char limit)
    tweet = f"📝 {title[:60]}...\n\n{post_url}\n\n{hashtags}"
    
    if len(tweet) > 280:
        # Truncate title if needed
        tweet = f"📝 {title[:40]}...\n{post_url}\n{hashtags}"
    
    return tweet

def format_telegram_post(post: Dict, blog_url: str = "https://victor-kipruto-rop.github.io/victor-resum-web/blog") -> str:
    """Format post for Telegram"""
    title = post.get('title', 'New Blog Post')
    description = post.get('description', post.get('excerpt', ''))
    slug = post.get('slug', post.get('id', 'post'))
    read_time = post.get('readTime', 10)
    
    post_url = f"{blog_url}/{slug}.html"
    
    message = f"""📚 *New Blog Post*

*{title}*

_{description}_

⏱️ {read_time} min read
🔗 [Read More]({post_url})
"""
    return message

def sync_to_twitter(post: Dict) -> bool:
    """Sync post to Twitter"""
    try:
        tweet = format_twitter_post(post)
        post_tweet(tweet)
        print(f"✓ Twitter: {post.get('title', 'Post')[:40]}...")
        return True
    except Exception as e:
        print(f"✗ Twitter error: {e}")
        return False

def sync_to_telegram(post: Dict) -> bool:
    """Sync post to Telegram"""
    try:
        message = format_telegram_post(post)
        send_telegram_notification(message)
        print(f"✓ Telegram: {post.get('title', 'Post')[:40]}...")
        return True
    except Exception as e:
        print(f"✗ Telegram error: {e}")
        return False

def sync_to_linkedin(post: Dict) -> bool:
    """Sync post to LinkedIn (placeholder)"""
    try:
        title = post.get('title', 'New Blog Post')
        description = post.get('description', '')
        # This would require LinkedIn API integration
        print(f"⚠️  LinkedIn: Manual share needed - {title[:40]}...")
        return False
    except Exception as e:
        print(f"✗ LinkedIn error: {e}")
        return False

def sync_to_devto(post: Dict) -> bool:
    """Sync post to Dev.to (placeholder)"""
    try:
        title = post.get('title', 'New Blog Post')
        # This would require Dev.to API integration
        print(f"⚠️  Dev.to: Manual share needed - {title[:40]}...")
        return False
    except Exception as e:
        print(f"✗ Dev.to error: {e}")
        return False

def get_new_posts(posts: List[Dict], sync_state: Dict) -> List[Dict]:
    """Get posts that haven't been synced yet"""
    synced_ids = set(sync_state.get("synced_posts", {}).keys())
    new_posts = []
    
    for post in posts:
        post_id = post.get('slug', post.get('id'))
        
        # Only sync published posts
        if post.get('status') != 'published':
            continue
        
        # Check if already synced
        if post_id not in synced_ids:
            new_posts.append(post)
    
    return sorted(new_posts, key=lambda p: p.get('publishDate', ''), reverse=True)

def main():
    """Main sync function"""
    
    print("📢 Blog Social Media Sync")
    print("=" * 60)
    
    # Load data
    posts = load_posts()
    sync_state = load_sync_state()
    
    if not posts:
        print("❌ No posts to sync")
        return 1
    
    # Find new posts
    new_posts = get_new_posts(posts, sync_state)
    
    print(f"📊 Status:")
    print(f"   Total posts:    {len(posts)}")
    print(f"   Previously synced: {len(sync_state.get('synced_posts', {}))}")
    print(f"   New posts:      {len(new_posts)}")
    print("")
    
    if not new_posts:
        print("✓ No new posts to sync")
        return 0
    
    # Sync new posts
    synced_count = 0
    for post in new_posts:
        post_id = post.get('slug', post.get('id'))
        print(f"\n📤 Syncing: {post.get('title', 'Post')[:50]}...")
        
        # Determine which platforms to use
        platforms_to_sync = ['twitter', 'telegram']  # Default platforms
        
        sync_results = {
            'twitter': sync_to_twitter(post) if 'twitter' in platforms_to_sync else None,
            'telegram': sync_to_telegram(post) if 'telegram' in platforms_to_sync else None,
            'linkedin': sync_to_linkedin(post),
            'devto': sync_to_devto(post)
        }
        
        # Mark as synced if at least one platform succeeded
        if any(sync_results.values()):
            sync_state['synced_posts'][post_id] = {
                'title': post.get('title'),
                'synced_at': datetime.now().isoformat(),
                'platforms': {k: v for k, v in sync_results.items() if v is not None}
            }
            synced_count += 1
    
    # Save state
    save_sync_state(sync_state)
    
    print("\n" + "=" * 60)
    print(f"✅ Sync complete!")
    print(f"   Successfully synced: {synced_count}/{len(new_posts)} posts")
    print(f"   Next run: Schedule via GitHub Actions or cron job")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
