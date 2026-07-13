#!/usr/bin/env python3
"""
DBOS PHASE 4: Social Distribution Engine
Auto-formats and sends posts to multiple platforms
"""

import json
from pathlib import Path
from datetime import datetime
from config import Config

class SocialDistributionEngine:
    """Format and distribute content to social platforms"""
    
    def __init__(self):
        self.posts_file = Path('blog/assets/shared/posts.json')
        self.output_dir = Path('distribution')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.base_url = Config.BASE_URL
        self.posts = []
    
    def load_posts(self):
        """Load posts"""
        with open(self.posts_file) as f:
            self.posts = json.load(f)
        
        # Get only recently published posts
        self.posts = [p for p in self.posts if p.get('status') == 'published']
        print(f"✓ Loaded {len(self.posts)} posts")
    
    def format_twitter(self, post: dict) -> dict:
        """Format post for Twitter/X"""
        url = f"{self.base_url}/blog/posts/{post['slug']}"
        
        # Create tweet threads
        tweets = []
        
        # Tweet 1 - Hook
        hook = f"🧵 Just published: {post['title']}\n\nKey insights inside 🧵👇\n\n{url}"
        tweets.append(hook[:280])
        
        # Tweet 2 - Value prop
        desc = post['description']
        if len(desc) > 250:
            desc = desc[:247] + "..."
        tweets.append(desc)
        
        # Tweet 3 - Call to action
        tags = ' '.join([f"#{tag.replace(' ', '')}" for tag in post.get('tags', [])[:3]])
        cta = f"Read the full article, save it, and share it with your network!\n\n{tags}"
        tweets.append(cta)
        
        return {
            "platform": "twitter",
            "thread": tweets,
            "hashtags": post.get('tags', [])[:5],
            "mentions": ["@VictorKipruto"],
            "url": url,
            "postType": "thread"
        }
    
    def format_linkedin(self, post: dict) -> dict:
        """Format post for LinkedIn"""
        url = f"{self.base_url}/blog/posts/{post['slug']}"
        
        post_text = f"""📚 New Blog Post: {post['title']}

{post['description']}

Key Topics:
{chr(10).join(['• ' + tag for tag in post.get('tags', [])[:5]])}

Read the full article: {url}

#DataEngineering #Analytics #SoftwareEngineering"""
        
        return {
            "platform": "linkedin",
            "postType": "article",
            "text": post_text,
            "url": url,
            "image": post.get('image'),
            "hashtags": post.get('tags', [])[:10]
        }
    
    def format_devto(self, post: dict) -> dict:
        """Format post for Dev.to"""
        url = f"{self.base_url}/blog/posts/{post['slug']}"
        
        frontmatter = f"""---
title: {post['title']}
description: {post['description']}
tags: {','.join(post.get('tags', [])[:5])}
published: true
cover_image: {post.get('image', '')}
series: {post.get('category', '')}
---

Read the full article with code examples on my blog: {url}"""
        
        return {
            "platform": "devto",
            "postType": "crosspost",
            "frontmatter": frontmatter,
            "url": url,
            "tags": post.get('tags', [])[:5]
        }
    
    def format_email(self, post: dict) -> dict:
        """Format post for email newsletter"""
        url = f"{self.base_url}/blog/posts/{post['slug']}"
        
        email_html = f"""<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
<h2>{post['title']}</h2>
<p>{post['description']}</p>

<p>
  <strong>Category:</strong> {post.get('category', 'General')}<br>
  <strong>Read Time:</strong> {post.get('readTime', '10')} min<br>
  <strong>Published:</strong> {post['publishDate']}
</p>

<h3>Key Topics:</h3>
<ul>
  {''.join([f'<li>{tag}</li>' for tag in post.get('tags', [])])}
</ul>

<p>
  <a href="{url}" style="background: #0066cc; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; display: inline-block;">
    Read Article
  </a>
</p>

<hr>
<p style="font-size: 12px; color: #666;">
  Victor Kipruto's Data Engineering & Analytics Blog
</p>
</body>
</html>"""
        
        return {
            "platform": "email",
            "postType": "newsletter",
            "subject": f"📚 {post['title']}",
            "preview": post['description'][:50] + "...",
            "body_html": email_html,
            "url": url,
            "category": post.get('category')
        }
    
    def format_telegram(self, post: dict) -> dict:
        """Format post for Telegram channel"""
        url = f"{self.base_url}/blog/posts/{post['slug']}"
        
        message = f"""📝 <b>{post['title']}</b>

{post['description']}

🏷️ Tags: {', '.join(post.get('tags', [])[:5])}
⏱️ Read time: {post.get('readTime', '10')} min

<a href="{url}">Read Full Article</a>"""
        
        return {
            "platform": "telegram",
            "postType": "channel_message",
            "message": message,
            "url": url,
            "parse_mode": "HTML"
        }
    
    def generate_distribution_plan(self):
        """Generate distribution formats for all posts"""
        distribution = []
        
        for post in self.posts[:5]:  # Focus on 5 most recent
            dist_plan = {
                "postSlug": post['slug'],
                "title": post['title'],
                "publishDate": post['publishDate'],
                "platforms": {
                    "twitter": self.format_twitter(post),
                    "linkedin": self.format_linkedin(post),
                    "devto": self.format_devto(post),
                    "email": self.format_email(post),
                    "telegram": self.format_telegram(post)
                },
                "schedule": {
                    "twitter": f"2 hours after publish",
                    "linkedin": f"4 hours after publish",
                    "devto": f"6 hours after publish",
                    "email": f"8 hours after publish",
                    "telegram": f"1 hour after publish"
                }
            }
            
            distribution.append(dist_plan)
        
        # Save distribution plans
        with open(self.output_dir / 'distribution-plan.json', 'w') as f:
            json.dump(distribution, f, indent=2)
        
        print(f"✓ Generated distribution plans for {len(distribution)} posts")
        
        # Also save individual platform templates
        for post in self.posts[:1]:  # Example post
            platforms = {
                'twitter': self.format_twitter(post),
                'linkedin': self.format_linkedin(post),
                'devto': self.format_devto(post),
                'email': self.format_email(post),
                'telegram': self.format_telegram(post)
            }
            
            with open(self.output_dir / f"{post['slug']}-twitter.json", 'w') as f:
                json.dump(platforms['twitter'], f, indent=2)
            
            with open(self.output_dir / f"{post['slug']}-linkedin.json", 'w') as f:
                json.dump(platforms['linkedin'], f, indent=2)
            
            with open(self.output_dir / f"{post['slug']}-devto.json", 'w') as f:
                json.dump(platforms['devto'], f, indent=2)
            
            with open(self.output_dir / f"{post['slug']}-email.json", 'w') as f:
                json.dump(platforms['email'], f, indent=2)
            
            with open(self.output_dir / f"{post['slug']}-telegram.json", 'w') as f:
                json.dump(platforms['telegram'], f, indent=2)
    
    def run(self):
        """Execute distribution engine"""
        print("\n🚀 DBOS PHASE 4: Social Distribution Engine\n")
        self.load_posts()
        self.generate_distribution_plan()
        print("\n✅ Distribution plan generation complete!\n")

if __name__ == '__main__':
    engine = SocialDistributionEngine()
    engine.run()
