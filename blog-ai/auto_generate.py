#!/usr/bin/env python3
"""
Auto Blog Generator - Generates 5 detailed technical blog posts every 24 hours.
Writes to blog/posts.json which the blog page loads automatically.
Reads topics from topics.json to avoid Python syntax issues with HTML content.
"""

import json
import random
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
POSTS_JSON = PROJECT_ROOT / "blog" / "posts.json"
TOPICS_JSON = Path(__file__).parent / "topics.json"
STATE_FILE = Path(__file__).parent / ".auto_generate_state"

IMAGES = [
    "assets/images/airflow-advanced.png",
    "assets/images/airflow-pipelines.png",
    "assets/images/cloud-infrastructure.png",
    "assets/images/data-engineering-fundamentals.png",
    "assets/images/data-quality-frameworks.png",
    "assets/images/dbt-best-practices.png",
    "assets/images/dbt-fundamentals.png",
    "assets/images/docker-kubernetes.png",
    "assets/images/kafka-streaming.png",
    "assets/images/kubernetes-patterns.png",
    "assets/images/Medallion Architecture.png",
    "assets/images/microservices-guide.png",
    "assets/images/python-optimization.png",
    "assets/images/python-performance.png",
    "assets/images/real-time-analytics.png",
    "assets/images/snowflake-performance.png",
    "assets/images/sql-optimization.png",
]

def load_topics():
    with open(TOPICS_JSON) as f:
        return json.load(f)

def load_existing_posts():
    if POSTS_JSON.exists():
        with open(POSTS_JSON) as f:
            return json.load(f)
    return []

def save_posts(posts):
    POSTS_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(POSTS_JSON, 'w') as f:
        json.dump(posts, f, indent=2)

def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_generated": None, "total_generated": 0, "used_topics": []}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def generate_post_id(title):
    return title.lower().replace(' ', '-').replace(':', '').replace("'", '').replace(',', '').replace('.', '')

def generate_posts(count=5):
    topics = load_topics()
    existing = load_existing_posts()
    existing_ids = {p.get('id') or p.get('slug') for p in existing}
    state = load_state()
    used_topics = set(state.get('used_topics', []))

    available = [t for t in topics if t['title'] not in used_topics]
    if not available:
        available = topics.copy()
        used_topics.clear()

    selected = random.sample(available, min(count, len(available)))
    new_posts = []
    now = datetime.now()

    for i, topic in enumerate(selected):
        post_id = generate_post_id(topic['title'])
        if post_id in existing_ids:
            continue

        publish_time = now - timedelta(hours=i * 4)
        post = {
            "id": post_id,
            "slug": post_id,
            "title": topic['title'],
            "description": topic['content'][:200].replace('<', '').replace('>', '').strip() + "...",
            "publishDate": publish_time.isoformat() + "Z",
            "category": topic['category'],
            "tags": topic['tags'],
            "image": random.choice(IMAGES),
            "status": "published",
            "readTime": topic['readTime'],
            "featured": random.random() < 0.3,
            "trending": random.random() < 0.4,
            "views": random.randint(500, 3000),
            "likes": random.randint(30, 200),
            "shares": random.randint(10, 80),
            "comments": random.randint(3, 30),
            "content": topic['content'],
        }
        new_posts.append(post)
        existing_ids.add(post_id)
        used_topics.add(topic['title'])

    all_posts = new_posts + existing
    all_posts.sort(key=lambda p: p.get('publishDate', ''), reverse=True)
    save_posts(all_posts)

    state['last_generated'] = now.isoformat()
    state['total_generated'] = state.get('total_generated', 0) + len(new_posts)
    state['used_topics'] = list(used_topics)
    save_state(state)

    return new_posts

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Auto-generate blog posts")
    parser.add_argument("--count", type=int, default=5, help="Number of posts to generate")
    parser.add_argument("--force", action="store_true", help="Force generation even if recently generated")
    args = parser.parse_args()

    state = load_state()
    if not args.force and state.get('last_generated'):
        last = datetime.fromisoformat(state['last_generated'])
        hours_since = (datetime.now() - last).total_seconds() / 3600
        if hours_since < 20:
            print(f"Last generation was {hours_since:.1f} hours ago. Use --force to override.")
            return

    print(f"Generating {args.count} new blog posts...")
    posts = generate_posts(args.count)

    if posts:
        print(f"\nGenerated {len(posts)} new posts:")
        for p in posts:
            print(f"  - {p['title']}")
        print(f"\nPosts saved to: {POSTS_JSON}")
        print("Posts will appear on blog.html automatically")
    else:
        print("No new posts generated (all topics already used)")

if __name__ == "__main__":
    main()