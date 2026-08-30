#!/usr/bin/env python3
"""Dispatch new blog posts to social media platforms."""
import json, os, sys
from pathlib import Path
from dotenv import load_dotenv
import urllib.request, urllib.error

load_dotenv()
BLOG_URL = "https://victorkipruto.com/blog.html"
POST_URL = "https://victorkipruto.com/post.html?id="

# Load posts
with open("blog/posts.json") as f:
    posts = json.load(f)

# Only dispatch first 5 (newest) posts
posts_to_dispatch = posts[:5]

results = {"telegram": [], "twitter": [], "devto": [], "failed": []}

def post_to_telegram(title, url, tags):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return False, "Not configured"
    tags_str = " ".join([f"#{t.replace('-','')}" for t in tags[:5]])
    msg = f"<b>New Blog Post</b>\n\n<b>{title}</b>\n\n{tags_str}\n\n<a href='{url}'>Read More →</a>"
    try:
        data = json.dumps({"chat_id": chat_id, "text": msg, "parse_mode": "HTML", "disable_web_page_preview": False}).encode()
        req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage", data=data, headers={"Content-Type": "application/json"})
        resp = urllib.request.urlopen(req, timeout=15)
        return True, "Posted"
    except Exception as e:
        return False, str(e)[:100]

def post_to_devto(title, content, tags):
    api_key = os.getenv("DEVTO_API_KEY")
    if not api_key:
        return False, "Not configured"
    article = {"title": title, "body_markdown": content, "tags": tags[:4], "published": True}
    try:
        data = json.dumps(article).encode()
        req = urllib.request.Request("https://dev.to/api/articles", data=data, headers={"api-key": api_key, "Content-Type": "application/json"})
        resp = urllib.request.urlopen(req, timeout=15)
        result = json.loads(resp.read())
        return True, result.get("url", "Posted")
    except Exception as e:
        return False, str(e)[:100]

def post_to_twitter(title, url):
    try:
        import tweepy
        client = tweepy.Client(
            bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
        )
        tweet = f"📝 New Blog Post: {title}\n\nRead more: {url}\n\n#DataEngineering #Blog #Python"
        if len(tweet) > 280:
            tweet = tweet[:277] + "..."
        response = client.create_tweet(text=tweet)
        return True, response.data["id"]
    except ImportError:
        return False, "tweepy not installed"
    except Exception as e:
        return False, str(e)[:100]

print(f"Dispatching {len(posts_to_dispatch)} posts to social media...\n")

for i, post in enumerate(posts_to_dispatch, 1):
    title = post["title"]
    post_id = post.get("slug", post.get("id", ""))
    url = POST_URL + post_id
    tags = post.get("tags", ["data-engineering"])
    content = post.get("content", post.get("description", ""))
    # Strip HTML for dev.to markdown
    import re
    md_content = re.sub(r'<h2>(.*?)</h2>', r'## \1', content)
    md_content = re.sub(r'<p>(.*?)</p>', r'\1\n', md_content)
    md_content = re.sub(r'<[^>]+>', '', md_content)
    
    print(f"[{i}/{len(posts_to_dispatch)}] {title[:60]}...")
    
    # Telegram
    ok, msg = post_to_telegram(title, url, tags)
    status = "✓" if ok else "✗"
    print(f"  Telegram: {status} {msg}")
    if ok: results["telegram"].append(title[:40])
    
    # Dev.to
    ok, msg = post_to_devto(title, md_content[:10000], [t.lower().replace(" ","") for t in tags])
    status = "✓" if ok else "✗"
    print(f"  Dev.to:   {status} {msg}")
    if ok: results["devto"].append(title[:40])
    
    # Twitter
    ok, msg = post_to_twitter(title, url)
    status = "✓" if ok else "✗"
    print(f"  Twitter:  {status} {msg}")
    if ok: results["twitter"].append(title[:40])

print(f"\n=== Summary ===")
print(f"Telegram: {len(results['telegram'])} posts sent")
print(f"Dev.to:   {len(results['devto'])} posts sent")
print(f"Twitter:  {len(results['twitter'])} posts sent")