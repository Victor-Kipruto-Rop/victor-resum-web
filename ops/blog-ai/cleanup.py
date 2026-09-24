#!/usr/bin/env python3
import os
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[2]
POSTS_DIR = REPO_ROOT / "content" / "ai-generated"
POSTS_JSON = REPO_ROOT / "public" / "blog" / "posts.json"

def cleanup_old_posts():
    """Delete posts older than 48 hours"""
    logger.info("🧹 Starting cleanup of posts older than 48 hours...")
    now = datetime.now()
    threshold = timedelta(hours=48)
    
    files_to_delete = []
    for file in POSTS_DIR.glob("*"):
        if file.suffix in [".md", ".json"]:
            file_time = datetime.fromtimestamp(file.stat().st_mtime)
            if now - file_time > threshold:
                files_to_delete.append(file)
    
    if not files_to_delete:
        logger.info("✨ No old posts found.")
        return

    # Update posts.json
    if POSTS_JSON.exists():
        with open(POSTS_JSON, 'r') as f:
            try:
                posts = json.load(f)
            except json.JSONDecodeError:
                posts = []
        
        updated_posts = []
        deleted_titles = []
        for post in posts:
            post_id = post.get('id')
            if any(file.stem.startswith(post_id) for file in files_to_delete):
                deleted_titles.append(post.get('title'))
            else:
                updated_posts.append(post)
                
        with open(POSTS_JSON, 'w') as f:
            json.dump(updated_posts, f, indent=2)
        logger.info(f"📝 Removed {len(deleted_titles)} posts from posts.json: {deleted_titles}")

    # Delete files
    for file in files_to_delete:
        file.unlink()
        logger.info(f"🗑️ Deleted: {file.name}")
    
    logger.info("✅ Cleanup complete.")

if __name__ == "__main__":
    cleanup_old_posts()
