#!/usr/bin/env python3
"""Dispatch blog posts to Twitter using tweepy."""
import os, json
from dotenv import load_dotenv
import tweepy

load_dotenv()

BLOG_URL = "https://victor-kipruto-rop.github.io/victor-resum-web/blog/"
POST_URL = "https://victor-kipruto-rop.github.io/victor-resum-web/post/?id="

with open("blog/assets/shared/posts.json") as f:
    posts = json.load(f)[:5]

client = tweepy.Client(
    bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
)

me = client.get_me()
print(f"Connected as: @{me.data.username}\n")
print(f"Dispatching {len(posts)} posts to Twitter...\n")

results = []
for i, post in enumerate(posts, 1):
    title = post["title"]
    post_id = post.get("slug", post.get("id", ""))
    url = POST_URL + post_id
    tags = " ".join([f"#{t.replace(' ','').replace('-','')}" for t in post.get("tags", [])[:3]])
    
    tweet = f"📝 New Blog Post\n\n{title}\n\n{tags}\n\n{url}"
    if len(tweet) > 280:
        tweet = f"📝 {title}\n\n{url}\n\n#DataEngineering"
    
    try:
        response = client.create_tweet(text=tweet)
        tweet_id = response.data["id"]
        tweet_url = f"https://twitter.com/{me.data.username}/status/{tweet_id}"
        print(f"[{i}/{len(posts)}] ✓ Posted: {title[:50]}...")
        print(f"       URL: {tweet_url}")
        results.append({"title": title[:40], "url": tweet_url, "status": "success"})
    except Exception as e:
        print(f"[{i}/{len(posts)}] ✗ Failed: {title[:50]}...")
        print(f"       Error: {str(e)[:80]}")
        results.append({"title": title[:40], "status": "failed", "error": str(e)[:80]})

print(f"\n{'='*50}")
print(f"Results: {sum(1 for r in results if r['status']=='success')}/{len(results)} tweets posted")